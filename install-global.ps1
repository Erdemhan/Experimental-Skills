<#
    install-global.ps1 — _global/ içeriğini %USERPROFILE%\.claude altına kurar.

    Kurulan her şey TÜM projelerde geçerli olur; artık .claude klasörünü
    proje proje kopyalamaya gerek kalmaz.

    Kullanım:
        .\install-global.ps1              # kur (mevcut dosyaları yedekler)
        .\install-global.ps1 -DryRun      # ne yapacağını göster, dokunma
#>

[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$Source = Join-Path $PSScriptRoot '_global'
$Target = Join-Path $env:USERPROFILE '.claude'
$Stamp  = Get-Date -Format 'yyyyMMdd-HHmmss'

if (-not (Test-Path $Source)) {
    throw "Kaynak bulunamadı: $Source"
}

Write-Host "Kaynak : $Source"
Write-Host "Hedef  : $Target"
Write-Host ""

function Copy-Item-Safe {
    param([string]$From, [string]$To, [string]$Label)

    if (Test-Path $To) {
        $backup = "$To.bak-$Stamp"
        Write-Host "  [YEDEK] $To -> $backup"
        if (-not $DryRun) { Move-Item -LiteralPath $To -Destination $backup }
    }

    Write-Host "  [KUR]   $Label"
    if (-not $DryRun) {
        $parent = Split-Path -Parent $To
        if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        Copy-Item -LiteralPath $From -Destination $To -Recurse -Force
    }
}

if (-not (Test-Path $Target) -and -not $DryRun) {
    New-Item -ItemType Directory -Path $Target -Force | Out-Null
}

Copy-Item-Safe -From (Join-Path $Source 'settings.json') -To (Join-Path $Target 'settings.json') -Label 'settings.json'
Copy-Item-Safe -From (Join-Path $Source 'CLAUDE.md')     -To (Join-Path $Target 'CLAUDE.md')     -Label 'CLAUDE.md'
Copy-Item-Safe -From (Join-Path $Source 'agents')        -To (Join-Path $Target 'agents')        -Label 'agents\ (9 ajan)'
Copy-Item-Safe -From (Join-Path $Source 'hooks')         -To (Join-Path $Target 'hooks')         -Label 'hooks\ (6 script)'
Copy-Item-Safe -From (Join-Path $Source 'templates')     -To (Join-Path $Target 'templates')     -Label 'templates\'

Write-Host ""
if ($DryRun) {
    Write-Host "DryRun — hiçbir dosya değiştirilmedi." -ForegroundColor Yellow
    exit 0
}

# Kaynaktan taşınmış olabilecek derleme artıklarını temizle
Get-ChildItem -Path $Target -Directory -Recurse -Filter '__pycache__' -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host "Kurulum tamam." -ForegroundColor Green
Write-Host ""
Write-Host "Doğrulama:"
Write-Host "  python3 `"$Target\hooks\security_gate.py`" < nul    # hata vermemeli"
Write-Host "  claude mcp list                                      # MCP sunucuları"
Write-Host ""
Write-Host "MCP sunucuları settings.json'dan OKUNMUYOR. Bir kereye mahsus şunları çalıştır:" -ForegroundColor Yellow
Write-Host '  claude mcp add -s user codebase-memory -- npx -y @modelcontextprotocol/server-codebase-memory'
Write-Host '  claude mcp add -s user memory -- npx -y @modelcontextprotocol/server-memory'
Write-Host '  claude mcp add -s user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking'
Write-Host '  claude mcp add -s user fetch -- uvx mcp-server-fetch'
