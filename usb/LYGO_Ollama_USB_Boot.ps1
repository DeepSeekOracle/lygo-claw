# LYGO portable Ollama launcher (space-safe paths)
$USB = Split-Path -Parent $MyInvocation.MyCommand.Path
$Ollama = Join-Path $USB 'product\runtime\ollama\ollama.exe'
$Data = Join-Path $USB 'lygo-data\ollama'

if (-not (Test-Path $Data)) { New-Item -ItemType Directory -Path $Data -Force | Out-Null }

$env:OLLAMA_MODELS = Join-Path $USB 'models\ollama'
$env:OLLAMA_HOST = '127.0.0.1:11434'
$env:OLLAMA_ORIGINS = 'null,*,file:,http://127.0.0.1,http://localhost'
$env:OLLAMA_KEEP_ALIVE = '10m'
$env:OLLAMA_HOME = $Data

Write-Host '[LYGO Ollama] Isolated USB instance' -ForegroundColor Cyan
Write-Host "EXE: $Ollama"
Write-Host "Models: $($env:OLLAMA_MODELS)"
& $Ollama serve