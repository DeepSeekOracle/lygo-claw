param(
    [string]$ZipIn = "I:\E Drive\lygo-claw\releases\LYGO-CLAW-USB-PUBLIC-v1.0.0.zip",
    [string]$OutDir = "I:\E Drive\Excavationpro\downloads",
    [int]$PartMB = 1800
)
$ErrorActionPreference = "Stop"
$partBytes = [int64]$PartMB * 1MB
$base = [IO.Path]::GetFileNameWithoutExtension($ZipIn)
$src = [IO.File]::OpenRead($ZipIn)
$buf = New-Object byte[] (4MB)
$idx = 1
$written = 0L
$dst = $null
function Open-Part([int]$n) {
    $path = Join-Path $OutDir ("{0}.part{1:D2}" -f $base, $n)
    Write-Host "Opening $path"
    return [IO.File]::Create($path)
}
try {
    $dst = Open-Part $idx
    while (($read = $src.Read($buf, 0, $buf.Length)) -gt 0) {
        $offset = 0
        while ($offset -lt $read) {
            $take = [Math]::Min($read - $offset, [int]($partBytes - $written))
            $dst.Write($buf, $offset, $take)
            $written += $take
            $offset += $take
            if ($written -ge $partBytes -and $src.Position -lt $src.Length) {
                $dst.Close()
                $idx++
                $written = 0
                $dst = Open-Part $idx
            }
        }
    }
} finally {
    if ($dst) { $dst.Close() }
    $src.Close()
}
$manifest = @{
    base = "$base.zip"
    parts = $idx
    part_mb = $PartMB
    join_script = "https://github.com/DeepSeekOracle/lygo-claw/blob/main/scripts/join_usb_release.ps1"
} | ConvertTo-Json
Set-Content (Join-Path $OutDir "$base.manifest.json") $manifest -Encoding utf8
Write-Host "Split complete: $idx parts"