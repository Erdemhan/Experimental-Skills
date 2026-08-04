#!/usr/bin/env python3
"""
startup_project.py — yeni bir proje kökünü ~/.claude global kurulumuna bağlar.

NEW-PROJECT.md'deki 4 elle-yapılan adımı (CLAUDE.md, .claude/context/,
FORMULATION.md, .gitignore + git hook'ları) tek komutla otomatikleştirir.

Var olan dosyaların üzerine varsayılan olarak YAZMAZ — zaten oradaysa
dokunmadan atlar. Üzerine yazmak için --force ver; bu durumda eskisi
install-global.ps1/.sh ile aynı sözleşmeyle `<dosya>.bak-<zaman damgası>`
olarak yedeklenir, sessizce kaybolmaz.

Kullanım (yeni proje kök dizininde):
    python3 ~/.claude/scripts/startup_project.py
    python3 ~/.claude/scripts/startup_project.py --name "MARL Reward Shaping"
    python3 ~/.claude/scripts/startup_project.py --with-formulation
    python3 ~/.claude/scripts/startup_project.py --antigravity
    python3 ~/.claude/scripts/startup_project.py --dry-run
    python3 ~/.claude/scripts/startup_project.py --force

Kapsam dışı (bilerek): `git init`, MCP sunucu kaydı (bunlar proje-bağımsız,
tek seferlik — bkz. `claude mcp add -s user ...`), sanal ortam kurulumu.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_NAME_PLACEHOLDER = "<Proje Adı>"


def claude_home() -> Path:
    """~/.claude konumunu döndürür; CLAUDE_HOME ile ezilebilir."""
    return Path(os.environ.get("CLAUDE_HOME", Path.home() / ".claude")).expanduser()


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def backup(path: Path) -> Path:
    dst = path.with_name(f"{path.name}.bak-{timestamp()}")
    shutil.move(str(path), str(dst))
    return dst


def install_file(src: Path, dst: Path, *, force: bool, dry_run: bool, label: str) -> None:
    """Basit kopyala: yoksa oluştur, varsa (force değilse) dokunma."""
    if not src.exists():
        print(f"  [!] Şablon bulunamadı, atlandı: {label} ({src})")
        return
    if dst.exists() and not force:
        print(f"  [VAR] {label} zaten var, dokunulmadı -> {dst}")
        return

    action = "UZERINE YAZ" if dst.exists() else "OLUSTUR"
    print(f"  [{action}] {label} -> {dst}")
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        backed_up = backup(dst)
        print(f"           (eskisi yedeklendi -> {backed_up.name})")
    shutil.copy2(src, dst)


def step_claude_md(home: Path, project_root: Path, project_name: str, *, force: bool, dry_run: bool) -> None:
    template = home / "templates" / "PROJECT_CLAUDE.md"
    dst = project_root / "CLAUDE.md"

    if not template.exists():
        print(f"  [!] Sablon bulunamadi: {template} (once install-global calistirin)")
        return
    if dst.exists() and not force:
        print(f"  [VAR] CLAUDE.md zaten var, dokunulmadi -> {dst}")
        return

    action = "UZERINE YAZ" if dst.exists() else "OLUSTUR"
    print(f"  [{action}] CLAUDE.md -> {dst}  (proje adi: {project_name})")
    if dry_run:
        return
    if dst.exists():
        backed_up = backup(dst)
        print(f"           (eskisi yedeklendi -> {backed_up.name})")
    content = template.read_text(encoding="utf-8")
    content = content.replace(PROJECT_NAME_PLACEHOLDER, project_name, 1)
    dst.write_text(content, encoding="utf-8")


def step_context_dir(home: Path, project_root: Path, *, dry_run: bool) -> None:
    context_dir = project_root / ".claude" / "context"
    if context_dir.exists():
        print("  [VAR] .claude/context/ zaten var")
    else:
        print("  [OLUSTUR] .claude/context/")
        if not dry_run:
            context_dir.mkdir(parents=True, exist_ok=True)

    context_db = home / "hooks" / "context_db.py"
    if not context_db.exists():
        print(f"  [!] context_db.py bulunamadi ({context_db}), context.db olusturulamadi")
        return
    print("  [CALISTIR] context_db.py init")
    if not dry_run:
        subprocess.run([sys.executable, str(context_db), "init"], cwd=project_root, check=False)


def step_formulation(home: Path, project_root: Path, *, force: bool, dry_run: bool) -> None:
    template = home / "templates" / "FORMULATION.md"
    dst = project_root / ".claude" / "context" / "FORMULATION.md"
    install_file(template, dst, force=force, dry_run=dry_run, label="FORMULATION.md")


def step_gitignore(home: Path, project_root: Path, *, force: bool, dry_run: bool) -> None:
    template = home / "templates" / ".gitignore"
    dst = project_root / ".gitignore"
    install_file(template, dst, force=force, dry_run=dry_run, label=".gitignore")


def step_git_hooks(home: Path, project_root: Path, *, dry_run: bool) -> None:
    if not (project_root / ".git").exists():
        print("  [ATLA] git hook'lari: bu dizin git deposu degil (once `git init` calistirin)")
        return
    installer = home / "templates" / "git-hooks" / "install_hooks.py"
    if not installer.exists():
        print(f"  [!] install_hooks.py bulunamadi ({installer})")
        return
    print("  [CALISTIR] git-hooks/install_hooks.py")
    if not dry_run:
        subprocess.run([sys.executable, str(installer)], cwd=project_root, check=False)


def step_antigravity(home: Path, project_root: Path, *, dry_run: bool) -> None:
    sync_script = home / "hooks" / "sync_agents_md.py"
    if not sync_script.exists():
        print(f"  [!] sync_agents_md.py bulunamadi ({sync_script})")
        return
    print("  [CALISTIR] sync_agents_md.py (-> .agents/AGENTS.md)")
    if not dry_run:
        subprocess.run([sys.executable, str(sync_script)], cwd=project_root, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Yeni proje kokunu ~/.claude global kurulumuna baglar "
                     "(CLAUDE.md, .claude/context/, .gitignore, git hook'lari)."
    )
    parser.add_argument("--name", default=None, help="Proje adi (varsayilan: bulundugun klasorun adi)")
    parser.add_argument("--with-formulation", action="store_true",
                         help="FORMULATION.md sablonunu da kopyala (denklem iceren projeler icin)")
    parser.add_argument("--antigravity", action="store_true",
                         help="Antigravity IDE icin .agents/AGENTS.md uret")
    parser.add_argument("--force", action="store_true",
                         help="Var olan dosyalarin uzerine yaz (eskisini .bak-<zaman> olarak yedekleyerek)")
    parser.add_argument("--dry-run", action="store_true",
                         help="Hicbir dosyaya dokunma, sadece ne yapacagini goster")
    args = parser.parse_args()

    home = claude_home()
    if not home.exists():
        print(f"[!] {home} bulunamadi. Once install-global.ps1 / install-global.sh calistirin.", file=sys.stderr)
        return 1

    project_root = Path.cwd()
    project_name = args.name or project_root.name

    print(f"Proje kok dizini : {project_root}")
    print(f"Global kaynak    : {home}")
    print(f"Proje adi        : {project_name}")
    if args.dry_run:
        print("Mod              : DRY RUN — hicbir dosya degistirilmeyecek")
    print()

    step_claude_md(home, project_root, project_name, force=args.force, dry_run=args.dry_run)
    step_context_dir(home, project_root, dry_run=args.dry_run)

    if args.with_formulation:
        step_formulation(home, project_root, force=args.force, dry_run=args.dry_run)
    else:
        print("  [ATLA] FORMULATION.md (--with-formulation verilmedi)")

    step_gitignore(home, project_root, force=args.force, dry_run=args.dry_run)
    step_git_hooks(home, project_root, dry_run=args.dry_run)

    if args.antigravity:
        step_antigravity(home, project_root, dry_run=args.dry_run)

    print()
    if args.dry_run:
        print("DryRun tamamlandi - hicbir dosya degistirilmedi.")
        return 0

    print("Kurulum tamam. Dogrulama:")
    print("  claude                  # ac")
    print("  /                       -> skiller listelenmeli")
    print("  @                       -> 9 ajan listelenmeli (@architect, @worker-coder, ...)")
    print('  rm -rf /tmp/deneme      -> security_gate.py engellemeli (Bash calistirirken)')
    print()
    print("Proje-bagimsiz, tek seferlik MCP kaydi (zaten yapildiysa atla):")
    print("  claude mcp list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
