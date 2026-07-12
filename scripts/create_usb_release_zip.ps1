param(
    [string]$Staging = "I:\E Drive\lygo-claw\releases\staging-full",
    [string]$ZipOut = "I:\E Drive\lygo-claw\releases\LYGO-CLAW-USB-PUBLIC-v1.0.0.zip",
    [string]$DownloadsDir = "I:\E Drive\Excavationpro\downloads"
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $Staging)) { Write-Error "Missing staging: $Staging" }

python (Join-Path (Split-Path $PSScriptRoot -Parent) "scripts\verify_usb_claw_public.py") $Staging --require-weights
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (Test-Path $ZipOut) { Remove-Item -Force $ZipOut }
Write-Host "Creating zip (~8 GB, may take 10-30 minutes)..."
$tar = Get-Command tar -ErrorAction SilentlyContinue
if ($tar) {
    Push-Location $Staging
    try {
        & tar -a -c -f $ZipOut .
        if ($LASTEXITCODE -ne 0) { throw "tar failed with exit $LASTEXITCODE" }
    } finally {
        Pop-Location
    }
} else {
    Compress-Archive -Path (Join-Path $Staging "*") -DestinationPath $ZipOut -CompressionLevel Fastest
}

New-Item -ItemType Directory -Force -Path $DownloadsDir | Out-Null
Copy-Item -Force $ZipOut (Join-Path $DownloadsDir (Split-Path $ZipOut -Leaf))
$readme = @"
LYGO CLAW USB PUBLIC v1.0.0
Download: $(Split-Path $ZipOut -Leaf)
Docs: https://github.com/DeepSeekOracle/lygo-claw/blob/main/docs/USB_PUBLIC_RELEASE.md
Boot: extract zip, run LYGO_CLAW_Launch.bat
"@
Set-Content -Path (Join-Path $DownloadsDir "LYGO-CLAW-USB-README.txt") -Value $readme -Encoding utf8
Write-Host "Release zip OK: $ZipOut"
Write-Host "Copied to: $DownloadsDir"