#!/usr/bin/env python3
"""
sync_agents_md.py — CLAUDE.md -> AGENTS.md aynalama (Antigravity IDE uyumluluğu).

Eski sync_skills.py'nin yerini alir. Iki degisiklik:

1. Skill kopyalama kaldirildi. Skill'ler artik Claude hesabinda kullanici
   seviyesinde tutuluyor; proje icine kopyalanmalarina gerek yok.
2. Antigravity config yolu artik makineye sabitlenmis degil. Sirasiyla
   ANTIGRAVITY_CONFIG ortam degiskenine, sonra platforma gore varsayilan
   konuma bakar.

Kullanim:
    python3 <hooks>/sync_agents_md.py            # calisilan dizinde
    python3 <hooks>/sync_agents_md.py <proje>    # belirtilen dizinde
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def antigravity_config_dir() -> Path | None:
    """Antigravity config dizinini dinamik olarak cozumle."""
    env = os.environ.get("ANTIGRAVITY_CONFIG")
    if env:
        p = Path(env)
        return p if p.is_dir() else None

    candidates = [Path.home() / ".gemini" / "config"]
    for c in candidates:
        if c.is_dir():
            return c
    return None


def sync(project_root: Path) -> int:
    claude_md = project_root / "CLAUDE.md"
    if not claude_md.is_file():
        print(f"[SKIP] CLAUDE.md bulunamadi: {claude_md}")
        return 0

    agents_dir = project_root / ".agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    agents_md = agents_dir / "AGENTS.md"
    shutil.copy2(claude_md, agents_md)
    print(f"[OK] {claude_md.name} -> {agents_md}")

    global_config = antigravity_config_dir()
    if global_config:
        shutil.copy2(claude_md, global_config / "AGENTS.md")
        print(f"[OK] {claude_md.name} -> {global_config / 'AGENTS.md'}")
    else:
        print("[INFO] Antigravity config dizini yok — global aynalama atlandi.")
        print("       Gerekliyse ANTIGRAVITY_CONFIG ortam degiskenini ayarlayin.")

    return 0


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    raise SystemExit(sync(root))
