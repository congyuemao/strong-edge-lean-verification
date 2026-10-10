import collections, hashlib, json, pathlib, re, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent
P=ROOT/'isolated'/'strong_edge_lean_starter'
def sha(b): return hashlib.sha256(b).hexdigest()
before=json.loads((ROOT/'source-sha256-before.json').read_text())
assert all(sha((P/n).read_bytes())==h for n,h in before.items())
with zipfile.ZipFile(BASE/'strong_edge_lean_high21_checkpoint.zip') as z:
    old={n.removeprefix('strong_edge_lean_starter/'):z.read(n) for n in z.namelist() if not n.endswith('/')}
comparison=[]
for n,b in old.items():
    path=P/n
    current=path.read_bytes() if path.exists() else None
    comparison.append(dict(path=n,old_sha256=sha(b),new_sha256=sha(current) if current else None,unchanged=current==b,append_only=current.startswith(b) if current else False))
(ROOT/'high21-checkpoint-comparison.json').write_text(json.dumps(comparison,indent=2),encoding='utf-8')
tokens=re.compile(r'\b(sorry|admit|sorryAx|axiom|constant|unsafe|native_decide|opaque|noncomputable|implemented_by|extern)\b')
def strip_comments(s):
    # Preserve newlines/columns; nested Lean block comments and strings are ignored.
    out=[]; i=0; depth=0; string=False
    while i<len(s):
        if depth:
            if s[i:i+2]=='/-': depth+=1; out.extend('  '); i+=2; continue
            if s[i:i+2]=='-/': depth-=1; out.extend('  '); i+=2; continue
            out.append('\n' if s[i]=='\n' else ' '); i+=1; continue
        if string:
            if s[i]=='\\': out.extend('  '); i+=2; continue
            if s[i]=='"': string=False
            out.append('\n' if s[i]=='\n' else ' '); i+=1; continue
        if s[i:i+2]=='/-': depth=1; out.extend('  '); i+=2; continue
        if s[i:i+2]=='--':
            j=s.find('\n',i)
            if j<0: j=len(s)
            out.extend(' '*(j-i)); i=j; continue
        if s[i]=='"': string=True; out.append(' '); i+=1; continue
        out.append(s[i]); i+=1
    return ''.join(out)
own=[P/n for n in before if n.endswith('.lean')]
findings=[]
for path in own:
    raw=path.read_text(encoding='utf-8-sig'); clean=strip_comments(raw)
    for i,line in enumerate(clean.splitlines(),1):
        for m in tokens.finditer(line): findings.append(dict(file=str(path.relative_to(P)),line=i,token=m.group(),source=raw.splitlines()[i-1]))
(ROOT/'own-static-findings.json').write_text(json.dumps(findings,indent=2),encoding='utf-8')
decls=[]
for path in own:
    for m in re.finditer(r'^\s*(?:noncomputable\s+)?(?:theorem|lemma|def|structure)\s+([^\s(:{]+)',strip_comments(path.read_text(encoding='utf-8-sig')),re.M):
        decls.append(dict(file=str(path.relative_to(P)),line=path.read_text(encoding='utf-8-sig')[:m.start()].count('\n')+1,name='StrongEdge.'+m[1]))
(ROOT/'declaration-index.json').write_text(json.dumps(decls,indent=2),encoding='utf-8')
audit=(P/'StrongEdge'/'Audit.lean').read_text(encoding='utf-8-sig')
ax=re.findall(r'^#print axioms (\S+)',audit,re.M)
checks=re.findall(r'^#check (\S+)',audit,re.M)
summary=dict(source_files=len(own),axiom_commands=len(ax),unique_axiom_names=len(set(ax)),check_commands=len(checks),old_lean_unchanged=sum(x['unchanged'] and x['path'].endswith('.lean') for x in comparison),old_lean_changes=[x for x in comparison if not x['unchanged'] and x['path'].endswith('.lean')],config_unchanged=all(x['unchanged'] for x in comparison if x['path'] in ['lean-toolchain','lake-manifest.json','lakefile.toml','lean.ps1']),new_lean=[n for n in before if n.endswith('.lean') and n not in old],own_static_counts=dict(collections.Counter(x['token'] for x in findings)))
(ROOT/'static-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
