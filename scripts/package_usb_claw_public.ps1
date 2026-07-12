param(
    [string]$SourceRoot = "I:\E Drive\LYGO_BUILDER_KEY",
    [string]$OutRoot = "",
    [switch]$IncludeWeights,
    [switch]$IncludeOllamaRuntime,
    [switch]$GitOnly
)
$ErrorActionPreference = "Stop"
$Repo = Split-Path $PSScriptRoot -Parent
if (-not $OutRoot) { $OutRoot = Join-Path $Repo "usb" }

$SourceRoot = (Resolve-Path $SourceRoot).Path
$OutRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutRoot)

Write-Host "LYGO CLAW public USB package"
Write-Host "  source: $SourceRoot"
Write-Host "  out:    $OutRoot"

if ($GitOnly -and (Test-Path $OutRoot)) {
    Write-Host "GitOnly: refreshing in place (no full wipe)"
} elseif (Test-Path $OutRoot) {
    Remove-Item -Recurse -Force $OutRoot
}
New-Item -ItemType Directory -Force -Path $OutRoot | Out-Null

$include = @(
    "LYGO_CLAW_Launch.bat",
    "LYGO_Gateway.cmd",
    "LYGO_Gateway.ps1",
    "LYGO_Ollama_USB_Boot.bat",
    "LYGO_Ollama_USB_Boot.ps1",
    "dashboard",
    "lygo-claw",
    "tools\node",
    "tools\lygo-gateway\dist",
    "tools\lygo-gateway\package.json",
    "models\MODEL_MANIFEST.json",
    "models\STANDALONE_MODEL_DESIGN.md"
)
if (-not $GitOnly) {
    $include += "tools\lygo-gateway\node_modules"
}

foreach ($rel in $include) {
    $src = Join-Path $SourceRoot $rel
    if (-not (Test-Path $src)) {
        Write-Warning "Skip missing source: $rel"
        continue
    }
    $dst = Join-Path $OutRoot $rel
    $parent = Split-Path $dst -Parent
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    if ((Get-Item $src).PSIsContainer) {
        robocopy $src $dst /E /NFL /NDL /NJH /NJS /XD ".git" "logs" | Out-Null
    } else {
        Copy-Item $src $dst -Force
    }
}

if ($IncludeWeights) {
    $mSrc = Join-Path $SourceRoot "models\ollama"
    $mDst = Join-Path $OutRoot "models\ollama"
    if (Test-Path $mSrc) {
        New-Item -ItemType Directory -Force -Path (Split-Path $mDst -Parent) | Out-Null
        Write-Host ">> copying model weights (large)..."
        robocopy $mSrc $mDst /E /NFL /NDL /NJH /NJS | Out-Null
    }
}

if ($IncludeOllamaRuntime) {
    $oSrc = Join-Path $SourceRoot "product\runtime\ollama"
    $oDst = Join-Path $OutRoot "product\runtime\ollama"
    if (Test-Path $oSrc) {
        New-Item -ItemType Directory -Force -Path (Split-Path $oDst -Parent) | Out-Null
        Write-Host ">> copying portable Ollama runtime (large)..."
        robocopy $oSrc $oDst /E /NFL /NDL /NJH /NJS | Out-Null
        $bundle = Join-Path $SourceRoot "product\runtime\ollama\LYGO_BUNDLE.json"
        if (Test-Path $bundle) { Copy-Item $bundle (Join-Path $OutRoot "product\runtime\ollama\LYGO_BUNDLE.json") -Force }
    }
}

# Fresh isolated data dir (no user state from builder stick)
$data = Join-Path $OutRoot "lygo-data"
New-Item -ItemType Directory -Force -Path $data | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $data "ollama") | Out-Null

# Public docs (no secret anchor)
$publicDocs = @(
    @("usb\PUBLIC_ANCHOR.md", "PUBLIC_ANCHOR.md"),
    @("usb\README.txt", "README.txt"),
    @("usb\START_HERE_USB.txt", "START_HERE_USB.txt"),
    @("usb\scripts\hydrate_usb_models.ps1", "scripts\hydrate_usb_models.ps1")
)
foreach ($pair in $publicDocs) {
    $src = Join-Path $Repo $pair[0]
    $dst = Join-Path $OutRoot $pair[1]
    if (-not (Test-Path $src)) { continue }
    $parent = Split-Path $dst -Parent
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    Copy-Item $src $dst -Force
}

# Ensure lygo.json engine mirror
$cfg = Join-Path $OutRoot "lygo-claw\lygo.json"
$eng = Join-Path $OutRoot "lygo-claw\openclaw.json"
if ((Test-Path $cfg) -and -not (Test-Path $eng)) { Copy-Item $cfg $eng -Force }

python (Join-Path $Repo "scripts\verify_usb_claw_public.py") $OutRoot $(if ($IncludeWeights) { "--require-weights" })
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "PUBLIC USB package OK: $OutRoot"