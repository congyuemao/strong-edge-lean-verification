import hashlib, json, pathlib, zipfile, subprocess
ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT.parent
ARCHIVE = BASE / 'strong_edge_lean_high20_checkpoint.zip'
DEST = ROOT / 'isolated'
if DEST.exists():
    raise SystemExit('Refusing to overwrite an existing isolated audit. Use a fresh audit directory.')
DEST.mkdir(exist_ok=True)
with zipfile.ZipFile(ARCHIVE) as z:
    for item in z.infolist():
        target = (DEST / item.filename).resolve()
        assert target.is_relative_to(DEST.resolve()), item.filename
    z.extractall(DEST)
PROJECT = DEST / 'strong_edge_lean_starter'
assert (PROJECT / 'lake-manifest.json').is_file()
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
sources = [*PROJECT.rglob('*.lean'), *(PROJECT / f for f in ['lean-toolchain','lake-manifest.json','lakefile.toml','lean.ps1'])]
manifest = {str(p.relative_to(PROJECT)).replace('\\','/'):sha(p) for p in sorted(sources)}
(ROOT / 'source-sha256-before.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(ROOT / 'checkpoint-sha256.json').write_text(json.dumps({ARCHIVE.name:sha(ARCHIVE)},indent=2),encoding='utf-8')
packages=BASE/'strong_edge_lean_starter'/'.lake'/'packages'
pins=json.loads((PROJECT/'lake-manifest.json').read_text())['packages']
states=[]
for pin in pins:
    p=packages/pin['name']
    head=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
    status=subprocess.check_output(['git','-C',str(p),'status','--porcelain','--untracked-files=no'],text=True)
    states.append(dict(name=pin['name'],expected=pin['rev'],actual=head,tracked_status=status,path=str(p)))
    assert head==pin['rev'] and not status, states[-1]
(ROOT/'dependency-states.json').write_text(json.dumps(states,indent=2),encoding='utf-8')
print(json.dumps(dict(project=str(PROJECT),sources=len(sources),archive_sha256=sha(ARCHIVE),dependencies=len(states)),indent=2))
