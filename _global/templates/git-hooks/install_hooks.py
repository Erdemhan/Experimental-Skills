#!/usr/bin/env python3
"""
install_hooks.py — Git hook'larını otomatik yükler.

Kullanım (proje kök dizininde):
    python3 .claude/templates/git-hooks/install_hooks.py

Bu script .claude/templates/git-hooks/ içindeki tüm hook
dosyalarını .git/hooks/ dizinine kopyalar ve çalıştırma
iznini ayarlar.
"""
from __future__ import annotations

import shutil
import stat
from pathlib import Path

HOOKS_SRC = Path(__file__).parent
HOOKS_DST = Path(".git/hooks")

HOOK_FILES = ["commit-msg", "pre-commit", "pre-push"]


def install() -> None:
    if not HOOKS_DST.exists():
        print("❌ .git/hooks/ dizini bulunamadı. Bu scripti proje kök dizininde çalıştırın.")
        return

    for hook in HOOK_FILES:
        src = HOOKS_SRC / hook
        dst = HOOKS_DST / hook

        if not src.exists():
            print(f"⚠️  {hook} şablonu bulunamadı, atlandı.")
            continue

        if dst.exists():
            backup = HOOKS_DST / f"{hook}.backup"
            shutil.copy2(dst, backup)
            print(f"   Yedeklendi: {dst} → {backup}")

        shutil.copy2(src, dst)
        # Çalıştırma izni ver (Unix/macOS/WSL için)
        dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"✅ Yüklendi: {hook}")

    # .gitignore kontrolü ve otomatik kopyalama
    gitignore_src = Path(".claude/templates/.gitignore")
    gitignore_dst = Path(".gitignore")

    if gitignore_src.exists() and not gitignore_dst.exists():
        shutil.copy2(gitignore_src, gitignore_dst)
        print("✅ .gitignore şablondan kök dizine kopyalandı!")

    print("\n🎉 Git hook'ları ve konfigürasyonları yüklendi!")
    print("   Conventional commit formatı: <type>(<scope>): <description>")
    print("   Akademik tipler: exp, data, result")


if __name__ == "__main__":
    install()
