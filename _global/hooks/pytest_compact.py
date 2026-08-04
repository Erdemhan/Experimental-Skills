#!/usr/bin/env python3
"""
pytest_compact.py — PreToolUse Hook for Bash commands.

Anthropic'in kendi "reduce token usage" dokümantasyonundaki önerilen desen:
gürültülü komut çıktısını Claude'un context'ine girmeden ÖNCE kısalt. pytest'in
varsayılan/verbose çıktısı (collection satırları, her PASSED testi için bir
satır, uzun traceback context'i) büyük projelerde context'i şişiriyor —
`test_watcher.py` (PostToolUse) bunun üstüne bir özet ekliyor ama ham çıktı
zaten context'e girmiş oluyor, o kısmı küçültmüyor.

Bu hook, pytest çağrılarına `-q --tb=short` ekler:
  -q          : "5 passed" gibi tek satırlık özet, testler için satır satır çıktı yok.
  --tb=short  : Kısa traceback formatı — gerçek hatayı ve son frame'i TAM gösterir,
                sadece pytest'in ürettiği fazladan kaynak-context satırlarını kırpar.

BİLEREK YAPILMAYAN: Tam sessizleştirme / grep ile FAIL satırlarına indirgeme.
_global/CLAUDE.md'deki "Spekülatif Hata Ayıklama Yasak — kök neden ampirik
olarak doğrulanmadan değişiklik yapılamaz" kuralı gereği, başarısız bir testte
teşhis için yeterli bilgi (asıl hata mesajı + son frame) hep kalmalı. --tb=short
bunu sağlıyor; --tb=line ya da bir grep filtresi çok agresif olurdu.

Kullanıcının kendi bayrakları önceliklidir: komutta zaten -v/--verbose, -q,
veya --tb= varsa hiç dokunulmaz.
"""
from __future__ import annotations

import json
import re
import sys

PYTEST_PATTERN = re.compile(r"(?:^|[;&|]\s*)(?:python3?\s+-m\s+)?pytest\b")
HAS_VERBOSITY_FLAG = re.compile(r"(?:^|\s)(-v+\b|--verbose\b|-q\b|--quiet\b|--tb=)")


def maybe_compact(command: str) -> str | None:
    """Pytest cagrisiysa ve kullanici zaten verbosity/tb bayragi vermemisse
    '-q --tb=short' ekler. Degisiklik yoksa None doner."""
    if not PYTEST_PATTERN.search(command):
        return None
    if HAS_VERBOSITY_FLAG.search(command):
        return None
    return command.rstrip() + " -q --tb=short"


def main() -> None:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            print("{}")
            return

        data = json.loads(raw)
        command = data.get("tool_input", {}).get("command", "")
        if not command:
            print("{}")
            return

        updated = maybe_compact(command)
        if updated is None:
            print("{}")
            return

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "updatedInput": {"command": updated},
            }
        }))

    except json.JSONDecodeError:
        print("{}")
    except Exception as e:  # noqa: BLE001
        # Hata durumunda komuta asla dokunma - sessizce oldugu gibi gecir.
        print(f"⚠️ pytest_compact.py hatası: {e}", file=sys.stderr)
        print("{}")


if __name__ == "__main__":
    main()
