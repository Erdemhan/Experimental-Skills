#!/usr/bin/env python3
"""
context_sync.py — Pre/PostToolUse Hook for context synchronization.

Her araç çağrısından önce/sonra task-queue.json'u okur ve
bağlamı güncel tutar. Hafif bir hook — sadece durum kaydeder.

Kullanım:
    python3 .claude/hooks/context_sync.py pre   # PreToolUse
    python3 .claude/hooks/context_sync.py post  # PostToolUse
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

TASK_QUEUE_PATH = Path(".claude/context/task-queue.json")
SYNC_LOG_PATH = Path(".claude/context/sync.log")


def read_active_task() -> str | None:
    """Check active in-progress tasks from SQLite database or fallback gracefully."""
    db_path = Path(".claude/context/context.db")
    if not db_path.exists():
        return None

    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT target, assigned_to FROM tasks WHERE status = 'in_progress' LIMIT 1"
        ).fetchone()
        conn.close()
        if row:
            return f"{row['target']} ({row['assigned_to']})"
        return None
    except Exception:
        return None


def log_sync(phase: str, tool_name: str) -> None:
    """Append a sync event to the log file."""
    try:
        SYNC_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with SYNC_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(
                f"{datetime.now().isoformat()} | {phase} | {tool_name}\n"
            )
    except OSError:
        pass  # Log yazılamazsa sessizce geç


def main() -> None:
    """Main hook entry point."""
    phase = sys.argv[1] if len(sys.argv) > 1 else "pre"

    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)

        data = json.loads(raw)
        tool_name = data.get("tool_name", "unknown")

        # Sadece log — task queue durumunu kaydet
        log_sync(phase, tool_name)

        # Pre-hook: Aktif görev varsa Claude'a hatırlat
        if phase == "pre":
            active_task = read_active_task()
            if active_task and tool_name in ("Write", "Edit", "Bash"):
                print(
                    f"📌 Aktif Görev (SQLite): {active_task}",
                    file=sys.stderr,
                )

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:  # noqa: BLE001
        print(f"⚠️ context_sync.py hatası: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
