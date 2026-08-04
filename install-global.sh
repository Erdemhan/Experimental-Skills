#!/usr/bin/env bash
# install-global.sh — _global/ içeriğini ~/.claude altına kurar (Linux / macOS / cluster).
#
# Kullanım:
#     ./install-global.sh              # kur (mevcut dosyaları yedekler)
#     ./install-global.sh --dry-run    # ne yapacağını göster, dokunma

set -euo pipefail

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_global"
DST="$HOME/.claude"
STAMP="$(date +%Y%m%d-%H%M%S)"

[[ -d "$SRC" ]] || { echo "Kaynak bulunamadı: $SRC" >&2; exit 1; }

echo "Kaynak : $SRC"
echo "Hedef  : $DST"
echo

# HPC/cluster ortamlarında `python3` PATH'te olmayabilir (conda env, module
# load vb.) — Windows tarafındaki Resolve-Python ile aynı mantık: adayı
# gerçekten çalıştırıp sys.executable'ı okuyoruz, PATH'te görünmesine güvenmiyoruz.
resolve_python() {
  local candidate exe
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
      exe="$("$candidate" -c 'import sys; print(sys.executable)' 2>/dev/null || true)"
      if [[ -n "$exe" && -x "$exe" ]]; then
        echo "$exe"
        return 0
      fi
    fi
  done
  return 1
}

echo "Python yorumlayıcısı aranıyor..."
PYEXE="$(resolve_python || true)"
if [[ -z "$PYEXE" ]]; then
  echo "  [!] Çalışan Python bulunamadı. Hook'lar çalışmaz." >&2
else
  echo "  [OK] $PYEXE"
fi
echo

install_item() {
  local from="$1" to="$2" label="$3"
  if [[ -e "$to" ]]; then
    echo "  [YEDEK] $to -> $to.bak-$STAMP"
    (( DRY_RUN )) || mv "$to" "$to.bak-$STAMP"
  fi
  echo "  [KUR]   $label"
  (( DRY_RUN )) || { mkdir -p "$(dirname "$to")"; cp -r "$from" "$to"; }
}

(( DRY_RUN )) || mkdir -p "$DST"

# Linux'ta hook yolları $HOME üzerinden çözümlenir
install_item "$SRC/settings.linux.json" "$DST/settings.json" "settings.json (linux varyantı)"
install_item "$SRC/CLAUDE.md"           "$DST/CLAUDE.md"     "CLAUDE.md"
install_item "$SRC/agents"              "$DST/agents"        "agents/ (9 ajan)"
install_item "$SRC/hooks"               "$DST/hooks"         "hooks/ (6 script)"
install_item "$SRC/templates"           "$DST/templates"     "templates/"
install_item "$SRC/scripts"             "$DST/scripts"       "scripts/ (startup_project.py)"
install_item "$(dirname "$SRC")/_new-project/CLAUDE.md" "$DST/templates/PROJECT_CLAUDE.md" "templates/PROJECT_CLAUDE.md (yeni proje şablonu)"

echo
if (( DRY_RUN )); then
  echo "DryRun — hiçbir dosya değiştirilmedi."
  exit 0
fi

# Kaynaktan taşınmış olabilecek derleme artıklarını temizle
find "$DST" -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true

chmod +x "$DST"/hooks/*.py 2>/dev/null || true
chmod +x "$DST"/scripts/*.py 2>/dev/null || true

# settings.json içindeki <CLAUDE_HOME> yer tutucusunu ve çıplak 'python3'ü
# bu makinedeki gerçek değerlerle sabitle (ps1 ile aynı sözleşme).
if [[ -n "$PYEXE" ]]; then
  "$PYEXE" - "$DST/settings.json" "$DST" "$PYEXE" <<'PYEOF'
import json
import sys

path, claude_home, py_exe = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path, encoding="utf-8") as f:
    cfg = json.load(f)

patched = 0
for event in ("PreToolUse", "PostToolUse"):
    for matcher in cfg.get("hooks", {}).get(event, []):
        for h in matcher.get("hooks", []):
            original = h.get("command", "")
            cmd = original.replace("<CLAUDE_HOME>", claude_home)
            if cmd.startswith("python3 ") or cmd.startswith("python "):
                cmd = py_exe + " " + cmd.split(" ", 1)[1]
            if cmd != original:
                patched += 1
            h["command"] = cmd

with open(path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"settings.json: {patched} hook komutu guncellendi ({py_exe}).")
PYEOF
else
  echo "  [!] Python bulunamadigi icin settings.json icindeki <CLAUDE_HOME> cozumlenemedi." >&2
fi

echo "Kurulum tamam."
echo
echo "Yeni bir proje başlatırken (proje kök dizininde):"
echo "  python3 $DST/scripts/startup_project.py"
echo '  # CLAUDE.md + .claude/context/ + .gitignore + git hook'"'"'larını tek seferde kurar.'
echo '  # Seçenekler: --name "Proje Adı"  --with-formulation  --antigravity  --dry-run  --force'
echo
echo "MCP sunucuları settings.json'dan OKUNMUYOR. Bir kereye mahsus:"
echo '  claude mcp add -s user memory -- npx -y @modelcontextprotocol/server-memory'
echo '  claude mcp add -s user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking'
echo
echo '  # codebase-memory-mcp: ajanlarin kullandigi kod grafigi sunucusu'
echo '  npm install -g codebase-memory-mcp   # ya da: pip install codebase-memory-mcp'
echo '  claude mcp add -s user codebase-memory-mcp -- codebase-memory-mcp'
echo
echo 'Onerilmeyen:'
echo '  fetch : uvx gerektirir; Claude Code zaten yerlesik WebFetch tasir.'
