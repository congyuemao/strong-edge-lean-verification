param([string] $LeanBin = '', [switch] $FetchCache)
$ErrorActionPreference = 'Stop'
if ($LeanBin) { $env:PATH = (Resolve-Path -LiteralPath $LeanBin).Path + ';' + $env:PATH }
Push-Location $PSScriptRoot
try {
    $proofLogs = Join-Path $PSScriptRoot 'reproduction-logs'
    New-Item -ItemType Directory -Path $proofLogs -Force | Out-Null
    $expected = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'source-manifest.json') -Raw | ConvertFrom-Json
    foreach ($item in $expected.PSObject.Properties) {
        $actual = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $item.Name) -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -ne $item.Value) { throw "Source hash mismatch: $($item.Name)" }
    }
    function Run-Check([string] $Name, [string] $Exe, [string[]] $CommandArgs) {
        $started = (Get-Date).ToUniversalTime().ToString('o')
        & $Exe @CommandArgs 1> (Join-Path $proofLogs "$Name.stdout.log") 2> (Join-Path $proofLogs "$Name.stderr.log")
        $code = $LASTEXITCODE
        @{command=(@($Exe)+$CommandArgs);exit_code=$code;start_utc=$started;end_utc=(Get-Date).ToUniversalTime().ToString('o')} |
            ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $proofLogs "$Name.json") -Encoding utf8
        if ($code -ne 0) { throw "$Name failed (exit $code). See $proofLogs" }
        Write-Output "$Name passed"
    }
    Run-Check 'version' 'lean' @('--version')
    if ($FetchCache) { Run-Check 'cache' 'lake' @('exe','cache','get') }
    Run-Check 'build' 'lake' @('build')
    $proofRoot = $PSScriptRoot.Substring(0,1).ToLowerInvariant() + $PSScriptRoot.Substring(1)

    Run-Check 'dependencies' 'lake' @('env','lean','AuditA.lean')
    Run-Check 'crosswalk' 'lake' @('env','lean','CrosswalkA.lean')
} finally { Pop-Location }
