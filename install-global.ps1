<#
    install-global.ps1 - _global/ icerigini %USERPROFILE%\.claude altina kurar.

    Kurulan her sey TUM projelerde gecerli olur; artik .claude klasorunu
    proje proje kopyalamaya gerek kalmaz.

    Kullanim:
        .\install-global.ps1              # kur (mevcut dosyalari yedekler)
        .\install-global.ps1 -DryRun      # ne yapacagini goster, dokunma
        .\install-global.ps1 -VerifyOnly  # kurma, sadece mevcut kurulumu test et

    Not: Bu dosya bilerek ASCII tutulmustur. PowerShell 5.1 BOM'suz .ps1
    dosyalarini ANSI olarak okur ve Turkce karakterler bozulur.
#>

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'

$Source = Join-Path $PSScriptRoot '_global'
$Target = Join-Path $env:USERPROFILE '.claude'
$SettingsPath = Join-Path $Target 'settings.json'
$Stamp  = Get-Date -Format 'yyyyMMdd-HHmmss'

# ---------------------------------------------------------------
# Yardimcilar
# ---------------------------------------------------------------

# Get-Command yetmez: Windows'ta python3.exe cogu zaman Microsoft Store
# stub'idir - PATH'te gorunur, calistirilinca "Python bulunamadi" der.
# Bu yuzden her adayi gercekten calistirip sys.executable'i okuyoruz.
function Resolve-Python {
    foreach ($candidate in @('python', 'python3', 'py')) {
        if (-not (Get-Command $candidate -ErrorAction SilentlyContinue)) { continue }
        try {
            $exe = & $candidate -c 'import sys; print(sys.executable)' 2>$null
            if ($LASTEXITCODE -eq 0 -and $exe -and (Test-Path $exe)) {
                return [string]$exe
            }
        }
        catch { }
    }
    return $null
}

function Invoke-Verification {
    param(
        [Parameter(Mandatory)][string]$Target,
        [Parameter(Mandatory)][string]$PythonExe,
        [Parameter(Mandatory)][string]$SettingsPath
    )

    Write-Host 'Dogrulama:' -ForegroundColor Cyan

    # Hooklar bilerek stderr'e yazar (security_gate engelleme mesaji gibi).
    # ErrorActionPreference = Stop altinda PowerShell native stderr'i hata
    # sayip scripti durdurur; dogrulama boyunca gecici olarak gevsetiyoruz.
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'

    try {
        $gate = Join-Path $Target 'hooks\security_gate.py'

        '{"tool_input":{"command":"rm -rf /"}}' | & $PythonExe $gate 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 2) {
            Write-Host '  [OK] security_gate.py yikici komutu engelledi (exit 2)' -ForegroundColor Green
        }
        else {
            Write-Host "  [!] security_gate.py beklenen exit 2 yerine $LASTEXITCODE dondurdu" -ForegroundColor Red
        }

        '{"tool_input":{"command":"pytest -q"}}' | & $PythonExe $gate 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host '  [OK] security_gate.py zararsiz komuta izin verdi (exit 0)' -ForegroundColor Green
        }
        else {
            Write-Host "  [!] security_gate.py zararsiz komutu engelledi (exit $LASTEXITCODE)" -ForegroundColor Red
        }

        # context_sync opt-in korumasi: bos dizinde hicbir dosya yaratmamali
        $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ('claude-hook-test-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
        New-Item -ItemType Directory -Path $tmp -Force | Out-Null
        Push-Location $tmp
        '{"tool_name":"Write"}' | & $PythonExe (Join-Path $Target 'hooks\context_sync.py') pre 2>&1 | Out-Null
        $leaked = @(Get-ChildItem -Path $tmp -Recurse -Force -ErrorAction SilentlyContinue)
        Pop-Location
        Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
        if ($leaked.Count -eq 0) {
            Write-Host '  [OK] context_sync.py opt-in korumasi calisiyor (dosya yaratmadi)' -ForegroundColor Green
        }
        else {
            Write-Host "  [!] context_sync.py bos dizinde $($leaked.Count) dosya yaratti" -ForegroundColor Red
        }
    }
    finally {
        $ErrorActionPreference = $prevEAP
    }

    # settings.json gecerli mi ve yorumlayici sabitlenmis mi
    try {
        $cfg = Get-Content $SettingsPath -Raw | ConvertFrom-Json
        Write-Host '  [OK] settings.json gecerli JSON' -ForegroundColor Green

        $cmds = @()
        foreach ($event in @('PreToolUse', 'PostToolUse')) {
            foreach ($m in $cfg.hooks.$event) { foreach ($h in $m.hooks) { $cmds += $h.command } }
        }
        $bare = @($cmds | Where-Object { $_ -match '^python3?\s' })
        if ($bare.Count -eq 0 -and $cmds.Count -gt 0) {
            Write-Host "  [OK] $($cmds.Count) hook komutu mutlak yorumlayici yoluna sabitlenmis" -ForegroundColor Green
        }
        else {
            Write-Host "  [!] $($bare.Count) hook komutu hala cikplak 'python3' kullaniyor" -ForegroundColor Red
        }
    }
    catch {
        Write-Host '  [!] settings.json bozuk JSON' -ForegroundColor Red
    }

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
    Write-Host '  claude mcp add -s user memory -- npx -y @modelcontextprotocol/server-memory'
    Write-Host '  claude mcp add -s user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking'
    Write-Host ''
    Write-Host '  # codebase-memory-mcp: architect / context-manager / worker-coder ajanlarinin'
    Write-Host '  # kullandigi kod grafigi sunucusu (index_repository, search_code, trace_path,'
    Write-Host '  # get_architecture, search_graph). Once binary kurulur:'
    Write-Host '  npm install -g codebase-memory-mcp        # ya da: pip install codebase-memory-mcp'
    Write-Host '  claude mcp add -s user codebase-memory-mcp -- codebase-memory-mcp'
    Write-Host ''
    Write-Host 'Ardindan: claude mcp list'
    Write-Host ''
    Write-Host 'Onerilmeyen:' -ForegroundColor DarkGray
    Write-Host '  fetch : uvx gerektirir ve Claude Code zaten yerlesik WebFetch tasir.' -ForegroundColor DarkGray
}

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

# ---------------------------------------------------------------
# 1. Yorumlayici
# ---------------------------------------------------------------
Write-Host 'Python yorumlayicisi araniyor...' -ForegroundColor Cyan
$PythonExe = Resolve-Python

if (-not $PythonExe) {
    Write-Host '  [!] Calisan Python bulunamadi. Hooklar calismaz.' -ForegroundColor Red
    Write-Host '      Python kurun ya da conda ortaminizi aktiflestirip tekrar deneyin.' -ForegroundColor Red
    if (-not $DryRun) { throw 'Python bulunamadi - kurulum durduruldu.' }
}
else {
    Write-Host "  [OK] $PythonExe" -ForegroundColor Green
}
Write-Host ''

if ($VerifyOnly) {
    Write-Host 'VerifyOnly - kurulum atlandi, yalnizca dogrulama yapiliyor.' -ForegroundColor Yellow
    Write-Host ''
    Invoke-Verification -Target $Target -PythonExe $PythonExe -SettingsPath $SettingsPath
    exit 0
}

# ---------------------------------------------------------------
# 2. Kurulum
# ---------------------------------------------------------------
if (-not (Test-Path $Source)) {
    throw "Kaynak bulunamadi: $Source"
}

Write-Host "Kaynak : $Source"
Write-Host "Hedef  : $Target"
Write-Host ''

if (-not (Test-Path $Target) -and -not $DryRun) {
    New-Item -ItemType Directory -Path $Target -Force | Out-Null
}

Install-Entry -From (Join-Path $Source 'settings.json') -To $SettingsPath                    -Label 'settings.json'
Install-Entry -From (Join-Path $Source 'CLAUDE.md')     -To (Join-Path $Target 'CLAUDE.md')  -Label 'CLAUDE.md'
Install-Entry -From (Join-Path $Source 'agents')        -To (Join-Path $Target 'agents')     -Label 'agents (9 ajan)'
Install-Entry -From (Join-Path $Source 'hooks')         -To (Join-Path $Target 'hooks')      -Label 'hooks (6 script)'
Install-Entry -From (Join-Path $Source 'templates')     -To (Join-Path $Target 'templates')  -Label 'templates'

Write-Host ''

if ($DryRun) {
    Write-Host 'DryRun - hicbir dosya degistirilmedi.' -ForegroundColor Yellow
    exit 0
}

# ---------------------------------------------------------------
# 3. settings.json icindeki yorumlayiciyi mutlak yola sabitle
# ---------------------------------------------------------------
$settings = Get-Content $SettingsPath -Raw | ConvertFrom-Json
$pyQuoted = '"' + ($PythonExe -replace '\\', '/') + '"'
$patched = 0

foreach ($event in @('PreToolUse', 'PostToolUse')) {
    foreach ($matcher in $settings.hooks.$event) {
        foreach ($h in $matcher.hooks) {
            if ($h.command -match '^python3?\s') {
                $h.command = $h.command -replace '^python3?\s', "$pyQuoted "
                $patched++
            }
        }
    }
}

$settings | ConvertTo-Json -Depth 12 | Set-Content $SettingsPath -Encoding UTF8
Write-Host "settings.json: $patched hook komutu $pyQuoted ile guncellendi." -ForegroundColor Green

# Derleme artiklarini temizle
Get-ChildItem -Path $Target -Directory -Recurse -Filter '__pycache__' -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host 'Kurulum tamam.' -ForegroundColor Green
Write-Host ''

# ---------------------------------------------------------------
# 4. Dogrulama
# ---------------------------------------------------------------
Invoke-Verification -Target $Target -PythonExe $PythonExe -SettingsPath $SettingsPath
