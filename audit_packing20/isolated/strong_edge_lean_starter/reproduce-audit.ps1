param([string] $LeanBin = '')
$ErrorActionPreference = 'Stop'
if ($LeanBin) { $env:PATH = (Resolve-Path -LiteralPath $LeanBin).Path + ';' + $env:PATH }
Push-Location $PSScriptRoot
try {
    $auditLogs = Join-Path $PSScriptRoot 'independent-rerun-logs'
    New-Item -ItemType Directory -Path $auditLogs -Force | Out-Null
    function Run-AuditCommand([string] $Name, [string] $Exe, [string[]] $CommandArgs) {
        $start = (Get-Date).ToUniversalTime().ToString('o')
        & $Exe @CommandArgs 1> (Join-Path $auditLogs "$Name.stdout.log") 2> (Join-Path $auditLogs "$Name.stderr.log")
        $code = $LASTEXITCODE
        @{ command = (@($Exe) + $CommandArgs); cwd = $PSScriptRoot; start_utc = $start; end_utc = (Get-Date).ToUniversalTime().ToString('o'); exit_code = $code } |
            ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $auditLogs "$Name.json") -Encoding utf8
        if ($code -ne 0) { throw "$Name failed with exit code $code. See $auditLogs" }
        Write-Output "$Name passed"
    }
    Run-AuditCommand 'version' 'lean' @('--version')
    Run-AuditCommand 'build' 'lake' @('build')
    Run-AuditCommand 'audit' 'lake' @('env','lean','StrongEdge/Audit.lean')
    Run-AuditCommand 'tests' 'lake' @('env','lean','StrongEdge/Tests.lean')
    Run-AuditCommand 'complete' 'lake' @('env','lean','AuditComplete.lean')
    # Lean 4.35.0-rc4 on Windows compares drive-letter case in module root paths.
    $auditRoot = $PSScriptRoot.Substring(0,1).ToLowerInvariant() + $PSScriptRoot.Substring(1)
    Run-AuditCommand 'semantic' 'lake' @('env','lean','-R',$auditRoot,(Join-Path $auditRoot 'AuditSemantic.lean'),'-o','.lake/build/lib/lean/AuditSemantic.olean')
    Run-AuditCommand 'regression' 'lake' @('env','lean','AuditRegression.lean')
    Run-AuditCommand 'environment' 'lake' @('env','lean','AuditEnvironment.lean')
    Run-AuditCommand 'dependencies' 'lake' @('env','lean','AuditDependencies.lean')
} finally { Pop-Location }
