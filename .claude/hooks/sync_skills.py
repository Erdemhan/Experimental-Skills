#!/usr/bin/env python3
"""
sync_skills.py — Synchronizes skills and agent rules between:
1. Local .claude/skills/ -> Local .agents/skills/
2. Local CLAUDE.md -> Local .agents/AGENTS.md
3. Local rules & skills -> Global Antigravity Config (C:/Users/Erdemhan/.gemini/config)
"""

import os
import shutil
from pathlib import Path

def sync():
    root_dir = Path(__file__).resolve().parent.parent.parent
    claude_skills = root_dir / ".claude" / "skills"
    agents_dir = root_dir / ".agents"
    agents_skills = agents_dir / "skills"
    
    global_config = Path("C:/Users/Erdemhan/.gemini/config")
    global_skills = global_config / "skills"
    global_agents = global_config / "AGENTS.md"

    print("[SYNC] Starting Skills & Rules Sync...")

    # 1. Sync local .claude/skills -> .agents/skills
    if claude_skills.exists():
        if agents_skills.exists():
            shutil.rmtree(agents_skills)
        shutil.copytree(claude_skills, agents_skills)
        print(f"[OK] Local sync completed: {claude_skills} -> {agents_skills}")

    # 2. Sync local CLAUDE.md -> .agents/AGENTS.md
    claude_md = root_dir / "CLAUDE.md"
    agents_md = agents_dir / "AGENTS.md"
    if claude_md.exists():
        shutil.copy2(claude_md, agents_md)
        print(f"[OK] Local AGENTS.md sync completed: {claude_md} -> {agents_md}")

    # 3. Sync to Global Antigravity Config
    if global_config.exists():
        # Copy skills
        if global_skills.exists():
            shutil.rmtree(global_skills)
        shutil.copytree(claude_skills, global_skills)
        print(f"[GLOBAL OK] Global skills sync completed -> {global_skills}")

        # Copy AGENTS.md
        if claude_md.exists():
            shutil.copy2(claude_md, global_agents)
            print(f"[GLOBAL OK] Global AGENTS.md sync completed -> {global_agents}")
    else:
        print(f"[WARN] Global Antigravity directory not found at {global_config}")

    print("[SUCCESS] Sync completed successfully!")

if __name__ == "__main__":
    sync()
