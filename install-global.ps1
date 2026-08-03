<#
    install-global.ps1 - _global/ icerigini %USERPROFILE%\.claude altina kurar.

    Kurulan her sey TUM projelerde gecerli olur; artik .claude klasorunu
    proje proje kopyalamaya gerek kalmaz.

    Kullanim:
        .\install-global.ps1              # kur (mevcut dosyalari yedekler)
        .\install-global.ps1 -DryRun      # ne yapacagini goster, dokunma

    Not: Bu dosya bilerek ASCII tutulmustur. PowerShell 5.1 BOM'suz .ps1
    dosyalarini ANSI olarak okur ve Turkce karakterler bozulur.
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
    throw "Kaynak bulunamadi: $Source"
}

Write-Host "Kaynak : $Source"
Write-Host "Hedef  : $Target"
Write-Host ''

function Install-Entry {
    param(
        [Parameter(Mandatory)][string]$From,
        [Parameter(Mandatory)][string]$To,
        [Parameter(Mandatory)][string]$Label
    )

    if (Test-Path $To) {
        $backup = "$To.bak-$Stamp"
        Write-Host "  [YEDEK] $To"
        Write-Host "          -> $backup"
        if (-not $DryRun) { Move-Item -LiteralPath $To -Destination $backup }
    }

    Write-Host "  [KUR]   $Label"
    if (-not $DryRun) {
        $parent = Split-Path -Parent $To
        if (-not (Test-Path $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        Copy-Item -LiteralPath $From -Destination $To -Recurse -Force
    }
}

if (-not (Test-Path $Target) -and -not $DryRun) {
    New-Item -ItemType Directory -Path $Target -Force | Out-Null
}

Install-Entry -From (Join-Path $Source 'settings.json') -To (Join-Path $Target 'settings.json') -Label 'settings.json'
Install-Entry -From (Join-Path $Source 'CLAUDE.md')     -To (Join-Path $Target 'CLAUDE.md')     -Label 'CLAUDE.md'
Install-Entry -From (Join-Path $Source 'agents')        -To (Join-Path $Target 'agents')        -Label 'agents (9 ajan)'
Install-Entry -From (Join-Path $Source 'hooks')         -To (Join-Path $Target 'hooks')         -Label 'hooks (6 script)'
Install-Entry -From (Join-Path $Source 'templates')     -To (Join-Path $Target 'templates')     -Label 'templates'

Write-Host ''

if ($DryRun) {
    Write-Host 'DryRun - hicbir dosya degistirilmedi.' -ForegroundColor Yellow
    exit 0
}

# Kaynaktan tasinmis olabilecek derleme artiklarini temizle
Get-ChildItem -Path $Target -Directory -Recurse -Filter '__pycache__' -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host 'Kurulum tamam.' -ForegroundColor Green
Write-Host ''

# ---------------------------------------------------------------
# Duman testi
# ---------------------------------------------------------------
Write-Host 'Dogrulama:' -ForegroundColor Cyan

$pythonCmd = $null
foreach ($c in @('python3', 'python', 'py')) {
    if (Get-Command $c -ErrorAction SilentlyContinue) { $pythonCmd = $c; break }
}

if (-not $pythonCmd) {
    Write-Host '  [!] Python PATH uzerinde bulunamadi - hooklar calismaz.' -ForegroundColor Red
}
else {
    Write-Host "  [i] Python yorumlayici: $pythonCmd"
    if ($pythonCmd -ne 'python3') {
        Write-Host '  [!] settings.json icinde python3 yaziyor ama sistemde o ad yok.' -ForegroundColor Yellow
        Write-Host "      settings.json icindeki python3 ifadelerini $pythonCmd ile degistirin." -ForegroundColor Yellow
    }

    $gate = Join-Path $Target 'hooks\security_gate.py'

    # yikici komut engellenmeli (exit 2)
    '{"tool_input":{"command":"rm -rf /"}}' | & $pythonCmd $gate 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 2) {
        Write-Host '  [OK] security_gate.py yikici komutu engelledi (exit 2)' -ForegroundColor Green
    }
    else {
        Write-Host "  [!] security_gate.py beklenen exit 2 yerine $LASTEXITCODE dondurdu" -ForegroundColor Red
    }

    # zararsiz komut gecmeli (exit 0)
    '{"tool_input":{"command":"pytest -q"}}' | & $pythonCmd $gate 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host '  [OK] security_gate.py zararsiz komuta izin verdi (exit 0)' -ForegroundColor Green
    }
    else {
        Write-Host "  [!] security_gate.py zararsiz komutu engelledi (exit $LASTEXITCODE)" -ForegroundColor Red
    }
}

# settings.json gecerli JSON mu
try {
    $null = Get-Content (Join-Path $Target 'settings.json') -Raw | ConvertFrom-Json
    Write-Host '  [OK] settings.json gecerli JSON' -ForegroundColor Green
}
catch {
    Write-Host '  [!] settings.json bozuk JSON' -ForegroundColor Red
}

# beklenen dosyalar yerinde mi
$expected = @(
    'settings.json', 'CLAUDE.md',
    'agents\architect.md', 'agents\worker-coder.md',
    'hooks\security_gate.py', 'hooks\context_sync.py',
    'hooks\auto_format.py', 'hooks\test_watcher.py',
    'hooks\context_db.py', 'hooks\sync_agents_md.py',
    'templates\FORMULATION.md'
)
$missing = $expected | Where-Object { -not (Test-Path (Join-Path $Target $_)) }
if ($missing) {
    Write-Host '  [!] Eksik dosyalar:' -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "      $_" -ForegroundColor Red }
}
else {
    Write-Host "  [OK] Beklenen $($expected.Count) dosyanin tamami yerinde" -ForegroundColor Green
}

Write-Host ''
Write-Host 'MCP sunuculari settings.json uzerinden YUKLENMEZ.' -ForegroundColor Yellow
Write-Host 'Bir kereye mahsus sunlari calistirin:' -ForegroundColor Yellow
Write-Host '  claude mcp add -s user codebase-memory -- npx -y @modelcontextprotocol/server-codebase-memory'
Write-Host '  claude mcp add -s user memory -- npx -y @modelcontextprotocol/server-memory'
Write-Host '  claude mcp add -s user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking'
Write-Host '  claude mcp add -s user fetch -- uvx mcp-server-fetch'
Write-Host ''
Write-Host 'Ardindan: claude mcp list'
