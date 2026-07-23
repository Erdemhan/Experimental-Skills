#!/usr/bin/env python3
"""
context_db.py — SQLite tabanlı oturumlar arası bellek sistemi.

task-queue.json'un yerini alır. SQLite tercih sebebi:
- Eş zamanlı yazma güvenli (JSON dosyası corrupt olabilir)
- SQL sorguları ile durum filtrelemesi mümkün
- ACID garantisi (yarım yazılan kayıt yok)
- Basit: sıfır bağımlılık (stdlib sqlite3)

Kullanım:
    python3 .claude/hooks/context_db.py status
    python3 .claude/hooks/context_db.py add-task <json>
    python3 .claude/hooks/context_db.py complete <task_id>
    python3 .claude/hooks/context_db.py summary
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path(".claude/context/context.db")


def get_connection() -> sqlite3.Connection:
    """Return SQLite connection with WAL mode for concurrent safety."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging — crash-safe
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize_db() -> None:
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS projects (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL UNIQUE,
                status      TEXT DEFAULT 'active',  -- active, paused, done
                created_at  TEXT DEFAULT (datetime('now')),
                updated_at  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id          TEXT PRIMARY KEY,          -- TASK-001 format
                project_id  INTEGER REFERENCES projects(id),
                type        TEXT NOT NULL,             -- architecture, function_spec, implementation, test
                target      TEXT NOT NULL,             -- module.function veya module adı
                assigned_to TEXT,                      -- architect, module-planner, worker-coder, etc.
                status      TEXT DEFAULT 'pending',    -- pending, in_progress, done, failed, escalated
                spec_path   TEXT,
                tier        INTEGER DEFAULT 1,         -- 1=Haiku, 2=Sonnet, 3=User
                retry_count INTEGER DEFAULT 0,
                error_log   TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                updated_at  TEXT DEFAULT (datetime('now')),
                completed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at  TEXT DEFAULT (datetime('now')),
                summary     TEXT
            );

            CREATE TABLE IF NOT EXISTS adr_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                adr_number  TEXT UNIQUE,
                title       TEXT NOT NULL,
                status      TEXT DEFAULT 'proposed',
                decision    TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            );
        """)


def add_task(task_data: dict) -> str:
    """Add a new task. Returns task_id."""
    initialize_db()
    task_id = task_data.get("id", f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    with get_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO tasks (id, type, target, assigned_to, spec_path, status)
            VALUES (:id, :type, :target, :assigned_to, :spec_path, 'pending')
        """, {
            "id": task_id,
            "type": task_data.get("type", "unknown"),
            "target": task_data.get("target", ""),
            "assigned_to": task_data.get("assigned_to", ""),
            "spec_path": task_data.get("spec_path", ""),
        })
    return task_id


def update_task_status(task_id: str, status: str, error: str | None = None, tier: int | None = None) -> None:
    """Update task status. Also increments retry_count if status='failed'."""
    initialize_db()
    with get_connection() as conn:
        updates = ["status = ?", "updated_at = datetime('now')"]
        params: list = [status]

        if error:
            updates.append("error_log = ?")
            params.append(error)

        if tier:
            updates.append("tier = ?")
            params.append(tier)

        if status == "failed":
            updates.append("retry_count = retry_count + 1")

        if status == "done":
            updates.append("completed_at = datetime('now')")

        params.append(task_id)
        conn.execute(
            f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
            params,
        )


def get_session_summary() -> dict:
    """Return current session state — pending, in_progress, done tasks."""
    initialize_db()
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT status, COUNT(*) as count
            FROM tasks GROUP BY status
        """).fetchall()

        counts = {r["status"]: r["count"] for r in rows}

        pending = conn.execute("""
            SELECT id, type, target, assigned_to, retry_count
            FROM tasks WHERE status = 'pending'
            ORDER BY created_at ASC LIMIT 5
        """).fetchall()

        in_progress = conn.execute("""
            SELECT id, type, target, assigned_to, tier, retry_count
            FROM tasks WHERE status = 'in_progress'
        """).fetchall()

        escalated = conn.execute("""
            SELECT id, type, target, tier, retry_count, error_log
            FROM tasks WHERE status = 'escalated'
        """).fetchall()

    return {
        "counts": counts,
        "pending": [dict(r) for r in pending],
        "in_progress": [dict(r) for r in in_progress],
        "escalated": [dict(r) for r in escalated],
    }


def print_summary() -> None:
    """Print a human-readable session summary."""
    summary = get_session_summary()
    counts = summary["counts"]

    total = sum(counts.values())
    done = counts.get("done", 0)
    pending = counts.get("pending", 0)
    in_prog = counts.get("in_progress", 0)
    failed = counts.get("failed", 0)
    escalated = counts.get("escalated", 0)

    print(f"""
📋 OTURUM BAĞLAMI — {datetime.now().strftime('%Y-%m-%d %H:%M')}
═══════════════════════════════════════════════════

📊 Görev Durumu:
   ✅ Tamamlandı:    {done}/{total}
   🔄 Devam Ediyor: {in_prog}
   ⏳ Bekliyor:     {pending}
   ❌ Başarısız:    {failed}
   🛑 Escalated:   {escalated}
""")

    if summary["in_progress"]:
        print("🔄 Aktif Görevler:")
        for t in summary["in_progress"]:
            tier_label = ["", "Haiku", "Sonnet", "USER"][t.get("tier", 1)]
            print(f"   [{t['id']}] {t['target']} → {t['assigned_to']} (Tier: {tier_label}, Retry: {t['retry_count']})")

    if summary["escalated"]:
        print("\n🛑 Manuel Müdahale Gereken Görevler:")
        for t in summary["escalated"]:
            print(f"   [{t['id']}] {t['target']} — 6 deneme tükendi")

    if summary["pending"]:
        print(f"\n⏳ Sonraki {len(summary['pending'])} Görev:")
        for t in summary["pending"]:
            print(f"   [{t['id']}] {t['type']}: {t['target']} → {t['assigned_to']}")


def export_to_json(output_path: Path = Path(".claude/context/context_snapshot.json")) -> None:
    """Export SQLite database state to a clean JSON file for versioning."""
    initialize_db()
    with get_connection() as conn:
        tasks = [dict(r) for r in conn.execute("SELECT * FROM tasks").fetchall()]
        projects = [dict(r) for r in conn.execute("SELECT * FROM projects").fetchall()]
        adrs = [dict(r) for r in conn.execute("SELECT * FROM adr_log").fetchall()]

    snapshot = {
        "exported_at": datetime.now().isoformat(),
        "projects": projects,
        "tasks": tasks,
        "adrs": adrs,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Context JSON olarak dışa aktarıldı: {output_path}")


def import_from_json(input_path: Path = Path(".claude/context/context_snapshot.json")) -> None:
    """Import context snapshot from JSON back into SQLite database."""
    if not input_path.exists():
        print(f"❌ Snapshot dosyası bulunamadı: {input_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    initialize_db()

    with get_connection() as conn:
        for p in data.get("projects", []):
            conn.execute(
                "INSERT OR REPLACE INTO projects (id, name, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (p["id"], p["name"], p["status"], p.get("created_at"), p.get("updated_at")),
            )
        for t in data.get("tasks", []):
            conn.execute(
                """INSERT OR REPLACE INTO tasks 
                   (id, project_id, type, target, assigned_to, status, spec_path, tier, retry_count, error_log, created_at, updated_at, completed_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    t["id"],
                    t.get("project_id"),
                    t["type"],
                    t["target"],
                    t.get("assigned_to"),
                    t.get("status"),
                    t.get("spec_path"),
                    t.get("tier", 1),
                    t.get("retry_count", 0),
                    t.get("error_log"),
                    t.get("created_at"),
                    t.get("updated_at"),
                    t.get("completed_at"),
                ),
            )
    print(f"✅ Context JSON'dan yüklendi: {input_path}")


def main() -> None:
    """CLI entry point."""
    initialize_db()

    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"

    if cmd == "summary":
        print_summary()

    elif cmd == "status":
        print_summary()

    elif cmd == "export-json":
        path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".claude/context/context_snapshot.json")
        export_to_json(path)

    elif cmd == "import-json":
        path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".claude/context/context_snapshot.json")
        import_from_json(path)

    elif cmd == "add-task":
        if len(sys.argv) < 3:
            print("Kullanım: context_db.py add-task '<json>'", file=sys.stderr)
            sys.exit(1)
        task_data = json.loads(sys.argv[2])
        task_id = add_task(task_data)
        print(f"✅ Görev eklendi: {task_id}")

    elif cmd == "complete":
        if len(sys.argv) < 3:
            print("Kullanım: context_db.py complete <task_id>", file=sys.stderr)
            sys.exit(1)
        update_task_status(sys.argv[2], "done")
        print(f"✅ Tamamlandı: {sys.argv[2]}")

    elif cmd == "fail":
        task_id = sys.argv[2] if len(sys.argv) > 2 else ""
        error = sys.argv[3] if len(sys.argv) > 3 else ""
        update_task_status(task_id, "failed", error=error)
        print(f"❌ Başarısız: {task_id}")

    elif cmd == "escalate":
        task_id = sys.argv[2] if len(sys.argv) > 2 else ""
        update_task_status(task_id, "escalated", tier=3)
        print(f"🛑 Escalated: {task_id}")

    elif cmd == "init":
        print("✅ Veritabanı başlatıldı:", DB_PATH)

    else:
        print(f"Bilinmeyen komut: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
