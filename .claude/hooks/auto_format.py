#!/usr/bin/env python3
"""
auto_format.py — PostToolUse Hook for Write/Edit operations.

Claude Code bir dosya yazdıktan veya düzenledikten sonra otomatik
olarak ilgili formatter'ı çalıştırır.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


FORMATTERS: dict[str, list[str]] = {
    ".py": ["black", "--quiet"],
    ".json": ["python3", "-m", "json.tool", "--indent", "2"],
    ".md": [],  # Markdown: format yok (içerik değişmesin)
    ".yaml": [],
    ".yml": [],
    ".toml": [],
    ".js": ["prettier", "--write"],
    ".ts": ["prettier", "--write"],
    ".jsx": ["prettier", "--write"],
    ".tsx": ["prettier", "--write"],
    ".css": ["prettier", "--write"],
    ".html": ["prettier", "--write"],
}


def is_tool_available(tool: str) -> bool:
    """Check if a command-line tool is available on PATH."""
    return subprocess.run(
        ["where" if os.name == "nt" else "which", tool],
        capture_output=True,
    ).returncode == 0


def format_file(file_path: str) -> None:
    """Format a file using the appropriate formatter."""
    path = Path(file_path)

    if not path.exists():
        return

    ext = path.suffix.lower()
    formatter_args = FORMATTERS.get(ext)

    if formatter_args is None:
        # Bilinmeyen uzantı — atla
        return

    if not formatter_args:
        # Formatter yok — atla
        return

    tool = formatter_args[0]
    if not is_tool_available(tool):
        print(f"ℹ️ auto_format: '{tool}' bulunamadı, atlanıyor.", file=sys.stderr)
        return

    cmd = formatter_args + [str(path)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(
            f"⚠️ auto_format: {tool} hatası:\n{result.stderr[:500]}",
            file=sys.stderr,
        )
    else:
        print(f"✨ auto_format: {path.name} formatlandı ({tool})", file=sys.stderr)


def main() -> None:
    """Main hook entry point."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)

        data = json.loads(raw)

        # Write tool: tool_input.file_path
        # Edit tool: tool_input.path
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path") or tool_input.get("path", "")

        if file_path:
            format_file(file_path)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:  # noqa: BLE001
        print(f"⚠️ auto_format.py hatası: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
