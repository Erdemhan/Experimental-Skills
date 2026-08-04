#!/usr/bin/env python3
"""
check_interfaces.py — FunctionSpec <-> gerçek kod imza denetimi (deterministik, sıfır LLM token).

`integration-verifier` ajanının en pahalı adımı, kodu okuyup her fonksiyonun
imzasının spec'e uyup uymadığını manuel çıkarsamasıydı — bu saf bir eşleştirme
problemi, akıl yürütme gerektirmiyor. Bu script `.claude/context/function-specs/`
altındaki her FunctionSpec JSON'u okur, `file_path`'teki gerçek Python dosyasını
`ast` ile parse eder ve imzaları (parametre adları, tip anotasyonları, dönüş tipi)
karşılaştırır. Sonuç kesin (OK / MISMATCH / MISSING) — LLM'in tekrar üretmesine
gerek yok, integration-verifier sadece bu raporu okuyup davranışsal/semantik
kısma (pytest sonuçlarının yorumlanması) odaklanır.

Kullanım (proje kök dizininde):
    python3 ~/.claude/scripts/check_interfaces.py
    python3 ~/.claude/scripts/check_interfaces.py --json
    python3 ~/.claude/scripts/check_interfaces.py --specs-dir .claude/context/function-specs

Exit code: 0 = tüm imzalar eşleşiyor, 1 = en az bir uyuşmazlık/eksik var.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclass
class ParamInfo:
    name: str
    annotation: str | None


@dataclass
class SignatureInfo:
    params: list[ParamInfo] = field(default_factory=list)
    returns: str | None = None

    def as_tuple(self) -> tuple:
        return (tuple((p.name, p.annotation) for p in self.params), self.returns)


@dataclass
class CheckResult:
    module: str
    function_name: str
    file_path: str
    status: str  # "OK" | "SIGNATURE_MISMATCH" | "MISSING_FILE" | "MISSING_FUNCTION" | "SPEC_UNPARSEABLE"
    detail: str = ""


def unparse_annotation(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def extract_signature(func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> SignatureInfo:
    params = []
    args = func_node.args
    # positional-only + regular positional-or-keyword args, in declaration order
    all_positional = list(args.posonlyargs) + list(args.args)
    for a in all_positional:
        params.append(ParamInfo(name=a.arg, annotation=unparse_annotation(a.annotation)))
    if args.vararg:
        params.append(ParamInfo(name="*" + args.vararg.arg, annotation=unparse_annotation(args.vararg.annotation)))
    for a in args.kwonlyargs:
        params.append(ParamInfo(name=a.arg, annotation=unparse_annotation(a.annotation)))
    if args.kwarg:
        params.append(ParamInfo(name="**" + args.kwarg.arg, annotation=unparse_annotation(args.kwarg.annotation)))
    returns = unparse_annotation(func_node.returns)
    return SignatureInfo(params=params, returns=returns)


def parse_signature_string(signature: str) -> SignatureInfo | None:
    """FunctionSpec'teki 'signature' alanindaki metni (orn. 'def foo(a: int) -> int')
    gercek bir AST FunctionDef'e cevirip extract_signature ile ayni yoldan gecirir -
    boylece 'beklenen' ve 'gercek' TAM AYNI normalizasyondan cikar, kirilgan string
    karsilastirmasi olmaz."""
    text = signature.strip()
    if not text.startswith("def "):
        text = "def " + text
    if not text.rstrip().endswith(":"):
        text = text.rstrip() + ":"
    text += "\n    pass"
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return extract_signature(node)
    return None


def find_function(tree: ast.AST, name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    return None


def load_function_specs(specs_dir: Path) -> list[dict]:
    specs = []
    if not specs_dir.is_dir():
        return specs
    for path in sorted(specs_dir.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        # module_spec.json'lar FunctionSpec degil (function_name/signature tasimaz) - atla
        if isinstance(data, dict) and "function_name" in data and "signature" in data:
            data["_spec_path"] = str(path)
            specs.append(data)
    return specs


def check_one(spec: dict, project_root: Path) -> CheckResult:
    module = spec.get("module", "?")
    function_name = spec.get("function_name", "?")
    file_path = spec.get("file_path", "")
    signature = spec.get("signature", "")

    expected = parse_signature_string(signature) if signature else None
    if expected is None:
        return CheckResult(module, function_name, file_path, "SPEC_UNPARSEABLE",
                            f"spec's 'signature' field could not be parsed: {signature!r}")

    target = (project_root / file_path) if file_path else None
    if not target or not target.is_file():
        return CheckResult(module, function_name, file_path, "MISSING_FILE",
                            f"source file not found: {file_path}")

    try:
        tree = ast.parse(target.read_text(encoding="utf-8"))
    except SyntaxError as e:
        return CheckResult(module, function_name, file_path, "MISSING_FUNCTION",
                            f"source file has a syntax error: {e}")

    func_node = find_function(tree, function_name)
    if func_node is None:
        return CheckResult(module, function_name, file_path, "MISSING_FUNCTION",
                            f"function '{function_name}' not defined in {file_path}")

    actual = extract_signature(func_node)
    if actual.as_tuple() != expected.as_tuple():
        exp_str = f"({', '.join(f'{p.name}: {p.annotation}' for p in expected.params)}) -> {expected.returns}"
        act_str = f"({', '.join(f'{p.name}: {p.annotation}' for p in actual.params)}) -> {actual.returns}"
        return CheckResult(module, function_name, file_path, "SIGNATURE_MISMATCH",
                            f"expected {exp_str} but found {act_str}")

    return CheckResult(module, function_name, file_path, "OK")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic FunctionSpec <-> code signature check.")
    parser.add_argument("--specs-dir", default=".claude/context/function-specs",
                         help="Directory containing FunctionSpec JSON files (default: .claude/context/function-specs)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of text")
    args = parser.parse_args()

    project_root = Path.cwd()
    specs_dir = project_root / args.specs_dir
    specs = load_function_specs(specs_dir)

    if not specs:
        msg = {"status": "NO_SPECS", "specs_dir": str(specs_dir), "count": 0}
        if args.json:
            print(json.dumps(msg, indent=2))
        else:
            print(f"[NO_SPECS] {specs_dir} altında FunctionSpec bulunamadı — kontrol atlandı.")
        return 0

    results = [check_one(spec, project_root) for spec in specs]
    ok = [r for r in results if r.status == "OK"]
    problems = [r for r in results if r.status != "OK"]

    if args.json:
        print(json.dumps({
            "status": "PASS" if not problems else "FAIL",
            "total": len(results),
            "ok": len(ok),
            "problems": [r.__dict__ for r in problems],
        }, indent=2))
    else:
        print(f"Interface check: {len(ok)}/{len(results)} OK")
        for r in problems:
            print(f"  [{r.status}] {r.module}.{r.function_name} ({r.file_path}): {r.detail}")
        if not problems:
            print("All FunctionSpec signatures match the implementation.")

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
