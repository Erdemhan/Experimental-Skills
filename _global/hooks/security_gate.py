#!/usr/bin/env python3
"""
security_gate.py — PreToolUse Hook for Bash commands.

Akademik araştırma ortamı için yapılandırılmıştır.
Yalnızca geri alınamaz yıkıcı komutları engeller (disk silimi, fork bomb vb.).

Kasıtlı olarak engellenmeyenler:
  - chmod 777   : Araştırma scriptleri için gerekebilir
  - Env değişkenleri: Kullanıcı verisi veya üretim sırrı yok
  - Docker komutları: Her zaman kullanılmıyor
"""
from __future__ import annotations

import json
import re
import sys

# Yalnızca geri alınamaz, yıkıcı komutlar engellenir
BLOCKED_PATTERNS: list[tuple[str, str]] = [
    (r"\brm\s+-rf\b",                "rm -rf engellendi — yıkıcı silme işlemi"),
    (r"\brm\s+--no-preserve-root\b", "rm --no-preserve-root engellendi"),
    (r"\bformat\s+[A-Z]:\b",         "Disk format komutu engellendi (Windows)"),
    (r"\bdel\s+/[Ff]\s+/[Ss]\b",     "Recursive force delete engellendi (Windows)"),
    (r":\(\)\s*\{.*:\|:.*\}",        "Fork bomb tespit edildi"),
    (r"\bdd\s+if=.*of=/dev/[hs]d",   "dd ile disk yazımı engellendi"),
    (r"\bmkfs\b",                    "Disk formatlama (mkfs) engellendi"),
    # Git koruma
    (r"git\s+push\s+.*--force(?!-with-lease).*(?:main|master)\b",
     "git push --force main/master engellendi — --force-with-lease kullanın"),
    (r"git\s+push\s+-f\s+.*(?:main|master)\b",
     "git push -f main/master engellendi — --force-with-lease kullanın"),
]


def check_command(command: str) -> tuple[bool, str]:
    """
    Check if a bash command is safe to execute.

    Args:
        command: The bash command string to check.

    Returns:
        Tuple of (is_blocked, reason). is_blocked=True means blocked.
    """
    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, reason
    return False, ""


def main() -> None:
    """Main hook entry point. Reads JSON from stdin, checks command."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)

        data = json.loads(raw)
        command = data.get("tool_input", {}).get("command", "")

        if not command:
            sys.exit(0)

        is_blocked, reason = check_command(command)

        if is_blocked:
            print(
                f"🛑 GÜVENLİK KAPISI: Komut engellendi\n"
                f"   Neden: {reason}\n"
                f"   Komut: {command[:200]}\n"
                f"   Bu komutu çalıştırmak istiyorsanız manuel onay gerekir.",
                file=sys.stderr,
            )
            sys.exit(2)  # Exit 2 = block the tool call

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:  # noqa: BLE001
        print(f"⚠️ security_gate.py hatası: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
