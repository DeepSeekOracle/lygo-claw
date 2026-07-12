# LYGO CLAW isolated gateway launcher (space-safe paths)
$ErrorActionPreference = 'Stop'
$USB = Split-Path -Parent $MyInvocation.MyCommand.Path
$Node = Join-Path $USB 'tools\node\node.exe'
$Gateway = Join-Path $USB 'tools\lygo-gateway\dist\entry.js'
$Config = Join-Path $USB 'lygo-claw\lygo.json'
$HomeDir = Join-Path $USB 'lygo-claw'
$Data = Join-Path $USB 'lygo-data'

$env:HOME = $HomeDir
$env:USERPROFILE = $Data
$env:APPDATA = $Data
$env:LOCALAPPDATA = $Data
$env:OPENCLAW_HOME = $HomeDir
$env:OPENCLAW_STATE_DIR = $HomeDir
$env:OLLAMA_MODELS = Join-Path $USB 'models\ollama'
$env:OLLAMA_HOST = '127.0.0.1:11434'

$engineConfig = Join-Path $HomeDir 'openclaw.json'
if (-not (Test-Path $engineConfig)) {
    Copy-Item $Config $engineConfig -Force
}

Write-Host '[LYGO CLAW Gateway] Starting isolated on USB...' -ForegroundColor Cyan
Write-Host "Node: $Node"
Write-Host "Config: $Config"
Write-Host "Ollama models: $($env:OLLAMA_MODELS)"
Write-Host ''

Set-Location (Join-Path $USB 'tools\lygo-gateway')
& $Node $Gateway gateway run --port 18789 --allow-unconfigured --cli-backend-logs --force