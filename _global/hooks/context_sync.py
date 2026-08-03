#!/usr/bin/env python3
"""
context_sync.py — Pre/PostToolUse Hook for context synchronization.

Aktif görev durumunu SQLite bağlam veritabanından okur ve loglar.

Kullanıcı seviyesinde (~/.claude/hooks/) kurulur, dolayısıyla her projede
tetiklenir. Yalnızca projede .claude/context/ dizini varsa çalışır;
yoksa sessizce çıkar ve hiçbir dosya oluşturmaz.

Kullanım:
    python3 <hooks>/context_sync.py pre   # PreToolUse
    python3 <hooks>/context_sync.py post  # PostToolUse
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

TASK_QUEUE_PATH = Path(".claude/context/task-queue.json")
SYNC_LOG_PATH = Path(".claude/context/sync.log")
CLAUDE_FORMULATION = Path(".claude/context/FORMULATION.md")
AGENTS_FORMULATION = Path(".agents/context/FORMULATION.md")

CONTEXT_DIR = Path(".claude/context")


def project_opted_in() -> bool:
    """
    Global hook guard.

    This hook is installed at user scope (~/.claude), so it fires in EVERY project.
    It must not create state in projects that never asked for it. A project opts in
    by having a .claude/context/ directory; `python3 <hooks>/context_db.py init`
    creates it. Without that directory the hook is a no-op.
    """
    return CONTEXT_DIR.is_dir()



def sync_formulation_file() -> None:
    """Sync FORMULATION.md across .claude/context/ and .agents/context/ for cross-platform compatibility."""
    try:
        if CLAUDE_FORMULATION.exists() and not AGENTS_FORMULATION.exists():
            AGENTS_FORMULATION.parent.mkdir(parents=True, exist_ok=True)
            AGENTS_FORMULATION.write_text(CLAUDE_FORMULATION.read_text(encoding="utf-8"), encoding="utf-8")
        elif AGENTS_FORMULATION.exists() and not CLAUDE_FORMULATION.exists():
            CLAUDE_FORMULATION.parent.mkdir(parents=True, exist_ok=True)
            CLAUDE_FORMULATION.write_text(AGENTS_FORMULATION.read_text(encoding="utf-8"), encoding="utf-8")
    except Exception:
        pass


def ensure_context_env() -> None:
    """Ensure context DB and formulation registry are auto-initialized if absent."""
    db_path = CONTEXT_DIR / "context.db"
    if not db_path.exists():
        try:
            # context_db.py bu dosyayla aynı dizinde (global hooks klasoru)
            hooks_dir = Path(__file__).resolve().parent
            if str(hooks_dir) not in sys.path:
                sys.path.insert(0, str(hooks_dir))
            import context_db
            context_db.initialize_db()
        except Exception:
            pass
    sync_formulation_file()


def read_active_task() -> str | None:
    """Check active in-progress tasks from SQLite database or fallback gracefully."""
    ensure_context_env()
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

    # Projeye özgü bağlam yoksa hiçbir şey yapma (global hook koruması)
    if not project_opted_in():
        sys.exit(0)

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
