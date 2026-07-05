$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
$Dest = Join-Path $Root "vendor\openclaw"
if (Test-Path (Join-Path $Dest ".git")) {
    Write-Host "Already vendored: $Dest"
    exit 0
}
git clone --depth 1 https://github.com/openclaw/openclaw.git $Dest
Write-Host "Vendored OpenClaw to $Dest — read NOTICE and upstream LICENSE"