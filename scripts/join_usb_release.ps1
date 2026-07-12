param(
    [string]$Dir = ".",
    [string]$Base = "LYGO-CLAW-USB-PUBLIC-v1.0.0"
)
$ErrorActionPreference = "Stop"
$out = Join-Path $Dir "$Base.zip"
$parts = Get-ChildItem (Join-Path $Dir "$Base.part*") | Sort-Object Name
if (-not $parts) { Write-Error "No parts found for $Base" }
$fs = [IO.File]::Create($out)
try {
    foreach ($p in $parts) {
        Write-Host "Appending $($p.Name)..."
        $bytes = [IO.File]::ReadAllBytes($p.FullName)
        $fs.Write($bytes, 0, $bytes.Length)
    }
} finally {
    $fs.Close()
}
Write-Host "Joined: $out"