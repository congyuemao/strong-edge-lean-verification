import collections, hashlib, json, pathlib, re
from static_audit import strip_comments
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent
P=ROOT/'isolated'/'strong_edge_lean_starter'
mods=[l.removeprefix('AUDIT_IMPORT ') for l in (ROOT/'logs'/'environment.stdout.log').read_text(encoding='utf-8').splitlines() if l.startswith('AUDIT_IMPORT ')]
roots=[P,*list((P/'.lake'/'packages').iterdir()),BASE/'.tools'/'lean-4.35.0-rc4-windows'/'src'/'lean']
roots.append(BASE/'.tools'/'lean-4.35.0-rc4-windows'/'src'/'lean'/'lake')
files=[]; missing=[]; findings=[]
tok=re.compile(r'\b(sorry|admit|sorryAx|axiom|constant|unsafe|native_decide|opaque|noncomputable|implemented_by|extern)\b')
for mod in mods:
    rel=pathlib.Path(*mod.split('.')).with_suffix('.lean')
    found=next((r/rel for r in roots if (r/rel).is_file()),None)
    if not found: missing.append(mod); continue
    data=found.read_bytes(); raw=data.decode('utf-8-sig'); clean=strip_comments(raw)
    files.append(dict(module=mod,path=str(found.relative_to(BASE)),sha256=hashlib.sha256(data).hexdigest()))
    for i,line in enumerate(clean.splitlines(),1):
        for m in tok.finditer(line): findings.append(dict(module=mod,line=i,token=m.group(),source=raw.splitlines()[i-1]))
(ROOT/'import-source-sha256.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
(ROOT/'import-static-findings.json').write_text(json.dumps(findings,indent=2),encoding='utf-8')
summary=dict(imported_modules=len(mods),source_files=len(files),missing_modules=missing,token_counts=dict(collections.Counter(r['token'] for r in findings)),note='Entire imported files, including elaborator/runtime code and unrelated declarations; not the theorem axiom closure.')
(ROOT/'import-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
