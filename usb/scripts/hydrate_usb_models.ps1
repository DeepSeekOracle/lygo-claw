param([string]$Profile = "SOVEREIGN_FAST")
$ErrorActionPreference = "Stop"
$Usb = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$ollamaExe = Join-Path $Usb "product\runtime\ollama\ollama.exe"
if (-not (Test-Path $ollamaExe)) { Write-Error "Need full release zip (portable Ollama missing)" }
$models = Join-Path $Usb "models\ollama"
New-Item -ItemType Directory -Force -Path $models | Out-Null
$env:OLLAMA_MODELS = $models
$env:OLLAMA_HOST = "127.0.0.1:11434"
$tag = if ($Profile -eq "SPEED") { "qwen2.5:1.5b" } else { "qwen2.5:3b" }
Start-Process -FilePath $ollamaExe -ArgumentList "serve" -WindowStyle Minimized | Out-Null
Start-Sleep -Seconds 6
& $ollamaExe pull $tag
Write-Host "Hydrate complete: $models"