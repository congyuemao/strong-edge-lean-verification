param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $LakeArgs = @('build')
)

$ErrorActionPreference = 'Stop'
$localBin = Join-Path (Split-Path $PSScriptRoot -Parent) '.tools\lean-4.35.0-rc4-windows\bin'
if (Test-Path -LiteralPath (Join-Path $localBin 'lake.exe')) {
    $env:PATH = $localBin + ';' + $env:PATH
}
$env:MATHLIB_CACHE_DIR = Join-Path $PSScriptRoot '.cache'
Push-Location $PSScriptRoot
try {
    & lake @LakeArgs
    $buildExitCode = $LASTEXITCODE
} finally {
    Pop-Location
}
exit $buildExitCode
