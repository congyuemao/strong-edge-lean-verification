from pathlib import Path
import json,hashlib,shutil,re,zipfile
D=Path(__file__).resolve().parent
ROOT=D.parent
P=D/'lean'
DEST=D/'packages'
OUT=ROOT/'output/dual_proofs'
OUT.mkdir(parents=True,exist_ok=True)
baseline=json.loads((D/'original_source_hashes.json').read_text(encoding='utf-8'))
cross=json.loads((D/'proof_crosswalk.json').read_text(encoding='utf-8'))
audit=(P/'AuditRoutes.lean').read_text(encoding='utf-8')
# Name comparisons avoid resolving the other route in a standalone audit.
audit=audit.replace('root == '+chr(96)*2+'StrongEdge.induced_matching_packing20',
                    '(toString root) == "StrongEdge.induced_matching_packing20"')
audit=audit.replace('root == '+chr(96)*2+'PaperRoute.induced_matching_packing20',
                    '(toString root) == "PaperRoute.induced_matching_packing20"')

base_ps=r'''param([string] $LeanBin = '', [switch] $FetchCache)
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
__EXTRA__
    Run-Check 'dependencies' 'lake' @('env','lean','Audit__ROUTE__.lean')
    Run-Check 'crosswalk' 'lake' @('env','lean','Crosswalk__ROUTE__.lean')
} finally { Pop-Location }
'''
for route,root_name in [('A','route_a_lean'),('B','route_b_lean')]:
    dest=DEST/root_name
    dest.mkdir(parents=True,exist_ok=True)
    if route=='A':
        for src in [P/'PaperRoute.lean',*list((P/'PaperRoute').rglob('*.lean'))]:
            target=dest/src.relative_to(P);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
        for name in ['lean-toolchain','lake-manifest.json']:
            shutil.copy2(P/name,dest/name)
        config=(P/'lakefile.toml').read_text(encoding='utf-8')
        config=config.replace('defaultTargets = ["StrongEdge"]','defaultTargets = ["PaperRoute"]')
        config=config.replace('[[lean_lib]]\nname = "StrongEdge"\n\n','')
        (dest/'lakefile.toml').write_text(config,encoding='utf-8')
        srcs=[n for n in ['PaperRoute.induced_matching_packing20','PaperRoute.Sharpness.twenty_is_necessary_real',
                         'PaperRoute.private_iff_closed_intersection','PaperRoute.Semantics.endpoint_packing20']]
        imports='import PaperRoute\nimport Lean\n'
        extra=''
        endpoint='PaperRoute.induced_matching_packing20'
        origin='The local Library is a documented fork: 39 files only rename the namespace; six supporting files are refactored. The manuscript-level theorems, exact identities and unified load proof are supplied separately. This is not a claim of an unrelated mathematical strategy.'
    else:
        for rel,h in baseline.items():
            src=ROOT/'strong_edge_lean_starter'/rel
            assert hashlib.sha256(src.read_bytes()).hexdigest()==h
            target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
        for name in ['AuditSemantic.lean','AuditRegression.lean','OriginalSharpness.lean']:
            shutil.copy2(P/name,dest/name)
        srcs=['StrongEdge.induced_matching_packing20','OriginalSharpness.twenty_is_necessary_real']
        imports='import StrongEdge\nimport OriginalSharpness\nimport Lean\n'
        extra='\n'.join(
            f"    Run-Check '{stem}' 'lake' @('env','lean','-R',$proofRoot,(Join-Path $proofRoot '{name}.lean'),'-o','.lake/build/lib/lean/{name}.olean')"
            for stem,name in [('semantic','AuditSemantic'),('regression','AuditRegression'),('sharpness','OriginalSharpness')])
        endpoint='StrongEdge.induced_matching_packing20'
        origin='All 49 original Lean/source configuration files are byte-identical to the independent audit baseline. The semantic, regression, real-sharpness and audit files are supplements and do not change that proof.'
    aa=audit[audit.index('open Lean Elab Command in'):]
    start=aa.index('  let roots := [')
    end=aa.index('  for root in roots do')
    aa=aa[:start]+'  let roots := ['+',\n    '.join(chr(96)*2+n for n in srcs)+']\n'+aa[end:]
    aa=aa[:aa.index('\n#check')]+''.join('\n#check '+n+'\n#print axioms '+n+'\n' for n in srcs)
    (dest/f'Audit{route}.lean').write_text(imports+'\n'+aa,encoding='utf-8')
    shutil.copy2(P/f'Crosswalk{route}.lean',dest/f'Crosswalk{route}.lean')
    (dest/'reproduce.ps1').write_text(base_ps.replace('__EXTRA__',extra).replace('__ROUTE__',route),encoding='utf-8')
    (dest/'README.txt').write_text(f'''ROUTE {route}: complete Lean source project

Main theorem: {endpoint}
Toolchain: leanprover/lean4:v4.35.0-rc4
mathlib commit: 49fd9dee36e7bbf345fe7981d2de6aeeb591f75b

{origin}

The project includes all project-specific source dependencies, the pinned Lake
manifest, independent semantic/sharpness checks, and an executable dependency audit.
It does not include Lean binaries, mathlib source/binary caches, or .lake.
An initial reproduction therefore needs network access to fetch the pinned
dependencies (or an existing cache). No dependency on the other route is required.

WINDOWS REPRODUCTION
1. Install the exact Lean version above (for example using elan).
2. Open PowerShell in this extracted directory.
3. Run: .\\reproduce.ps1 -FetchCache
   If Lean is not on PATH: .\\reproduce.ps1 -LeanBin 'C:\\path\\to\\lean\\bin' -FetchCache
   With dependencies already available, omit -FetchCache.
The script verifies source hashes, builds the default library, checks supplemental
proofs, audits actual proof dependencies, and checks all crosswalk declarations.
It stops on any failed command and writes reproduction-logs.

The source-manifest.json hashes exclude themselves and reproduction logs.
The package contains no admitted mathematical lemma. The accepted dependency
axioms are propext, Classical.choice and Quot.sound.

See the paired English PDF, the Chinese ROUTE_COMPARISON report and
proof_crosswalk.csv in the full delivery for the mathematical correspondence.
''',encoding='utf-8')
    subset=[]
    for row in cross:
        subset.append({'paper_ref':row['paper_ref'],'claim':row['claim'],
                       'declarations':row['route_'+route.lower()],
                       'locations':row['route_'+route.lower()+'_locations'],'comparison_note':row['difference']})
    (dest/'proof-crosswalk.json').write_text(json.dumps(subset,ensure_ascii=False,indent=2),encoding='utf-8')
    # Verify every local import resolves without the other route's source.
    for src in dest.rglob('*.lean'):
        for module in re.findall(r'^(?:public )?import ([\w.]+)',src.read_text(encoding='utf-8'),re.M):
            if module.startswith(('Mathlib','Lean')):continue
            assert (dest/(module.replace('.','/')+'.lean')).exists(),(src,module)
    hashes={str(p.relative_to(dest)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(dest.rglob('*')) if p.is_file() and p.name!='source-manifest.json'}
    (dest/'source-manifest.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    with zipfile.ZipFile(OUT/(root_name+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(dest.rglob('*')):
            if p.is_file():z.write(p,root_name+'/'+str(p.relative_to(dest)).replace('\\','/'))
    print(route,len(hashes),'files plus source manifest; local import closure complete.')
