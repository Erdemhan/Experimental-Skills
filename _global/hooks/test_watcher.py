#!/usr/bin/env python3
"""
test_watcher.py — PostToolUse Hook for Bash commands.

Bash komutu çalıştıktan sonra devreye girer. Eğer komut bir pytest
çalıştırmasıysa, sonucu parse eder ve başarısız testleri Claude'a raporlar.
"""
from __future__ import annotations

import json
import re
import sys


def parse_pytest_output(output: str) -> dict | None:
    """
    Parse pytest output and extract test results.

    Args:
        output: Raw stdout/stderr from pytest run.

    Returns:
        Dict with test counts if pytest output detected, None otherwise.
    """
    # pytest çıktısı mı kontrol et
    if "passed" not in output and "failed" not in output and "error" not in output:
        return None

    result = {
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "warnings": 0,
        "failed_tests": [],
    }

    # Özet satırını bul: "5 passed, 2 failed, 1 error in 0.12s"
    summary_pattern = re.compile(
        r"(\d+)\s+passed|(\d+)\s+failed|(\d+)\s+error|(\d+)\s+warning"
    )
    for match in summary_pattern.finditer(output):
        groups = match.groups()
        if groups[0]:
            result["passed"] = int(groups[0])
        elif groups[1]:
            result["failed"] = int(groups[1])
        elif groups[2]:
            result["errors"] = int(groups[2])
        elif groups[3]:
            result["warnings"] = int(groups[3])

    # Başarısız test isimlerini bul
    failed_pattern = re.compile(r"FAILED\s+([\w/.:]+)")
    result["failed_tests"] = failed_pattern.findall(output)

    return result


def format_report(results: dict, command: str) -> str:
    """Format test results for Claude feedback."""
    total = results["passed"] + results["failed"] + results["errors"]
    status = "✅" if results["failed"] == 0 and results["errors"] == 0 else "❌"

    lines = [
        f"\n🧪 Test Sonuçları [{status}]",
        f"   Komut: {command[:80]}",
        f"   Toplam: {total} | ✅ {results['passed']} geçti | ❌ {results['failed']} başarısız | 💥 {results['errors']} hata",
    ]

    if results["warnings"]:
        lines.append(f"   ⚠️ {results['warnings']} uyarı")

    if results["failed_tests"]:
        lines.append("   Başarısız Testler:")
        for test in results["failed_tests"][:5]:  # İlk 5'i göster
            lines.append(f"     - {test}")
        if len(results["failed_tests"]) > 5:
            lines.append(f"     ... ve {len(results['failed_tests']) - 5} tane daha")

    return "\n".join(lines)


def main() -> None:
    """Main hook entry point."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)

        data = json.loads(raw)

        # Çalıştırılan komut
        command = data.get("tool_input", {}).get("command", "")

        # Sadece pytest komutlarını izle
        if "pytest" not in command and "python -m pytest" not in command:
            sys.exit(0)

        # Tool output'u al
        tool_output = data.get("tool_response", {})
        if isinstance(tool_output, dict):
            output = tool_output.get("output", "")
        else:
            output = str(tool_output)

        results = parse_pytest_output(output)
        if results:
            report = format_report(results, command)
            print(report, file=sys.stderr)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:  # noqa: BLE001
        print(f"⚠️ test_watcher.py hatası: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
