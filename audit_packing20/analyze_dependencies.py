import collections, hashlib, json, pathlib, re
from static_audit import strip_comments
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent
P=ROOT/'isolated'/'strong_edge_lean_starter'
rows=[]
for line in (ROOT/'logs'/'dependencies-dev.stdout.log').read_text(encoding='utf-8').splitlines():
    if line.startswith('AUDIT_DEP '): rows.append(json.loads(line.removeprefix('AUDIT_DEP ')))
assert rows and rows[0]['name']=='StrongEdge.induced_matching_packing20'
by_name={r['name']:r for r in rows}
(ROOT/'proof-dependency-graph.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
modules=sorted(set(r['module'] for r in rows))
roots=[P,*list((P/'.lake'/'packages').iterdir()),BASE/'.tools'/'lean-4.35.0-rc4-windows'/'src'/'lean']
files=[]; missing=[]; findings=[]
tok=re.compile(r'\b(sorry|admit|sorryAx|axiom|constant|unsafe|native_decide|opaque|noncomputable|implemented_by|extern)\b')
for mod in modules:
    rel=pathlib.Path(*mod.split('.')).with_suffix('.lean')
    found=next((r/rel for r in roots if (r/rel).is_file()),None)
    if not found: missing.append(mod); continue
    data=found.read_bytes(); raw=data.decode('utf-8-sig'); clean=strip_comments(raw)
    files.append(dict(module=mod,path=str(found.relative_to(BASE)),sha256=hashlib.sha256(data).hexdigest()))
    for i,line in enumerate(clean.splitlines(),1):
        for m in tok.finditer(line): findings.append(dict(module=mod,line=i,token=m.group(),source=raw.splitlines()[i-1]))
(ROOT/'dependency-source-sha256.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
(ROOT/'dependency-static-findings.json').write_text(json.dumps(findings,indent=2),encoding='utf-8')
own=[r for r in rows if r['module'].startswith('StrongEdge')]
def reachable(start):
    seen=set(); todo=[start]
    while todo:
        n=todo.pop()
        if n in seen: continue
        seen.add(n); todo.extend(by_name.get(n,{}).get('dependencies',[]))
    return seen
high_names=['StrongEdge.high20_clique_card_le_nineteen','StrongEdge.high21_clique_card_le_eighteen','StrongEdge.high22_clique_card_le_seventeen','StrongEdge.high23_clique_card_le_sixteen','StrongEdge.high24_clique_card_le_thirteen']
assert all(n in by_name for n in high_names)
wrapper_names=[r['name'] for r in own if 'Packing' in r['module']]
summary=dict(declarations=len(rows),project_declarations=len(own),modules=len(modules),source_files=len(files),missing_modules=missing,axioms=[r['name'] for r in rows if r['axiom']],unsafe=[r['name'] for r in rows if r['unsafe']],dependency_static_counts=dict(collections.Counter(r['token'] for r in findings)),high_threshold_references_to_wrappers={n:sorted(reachable(n)&set(wrapper_names)) for n in high_names},legacy_threshold_record_reachable='StrongEdge.CliqueThresholds20' in by_name)
(ROOT/'dependency-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
(ROOT/'project-proof-dependencies.json').write_text(json.dumps(own,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
