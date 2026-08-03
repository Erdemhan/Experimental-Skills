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

echo
if (( DRY_RUN )); then
  echo "DryRun — hiçbir dosya değiştirilmedi."
  exit 0
fi

# Kaynaktan taşınmış olabilecek derleme artıklarını temizle
find "$DST" -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true

chmod +x "$DST"/hooks/*.py 2>/dev/null || true

echo "Kurulum tamam."
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
