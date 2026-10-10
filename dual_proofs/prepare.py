from pathlib import Path
import shutil, json, hashlib

root=Path(__file__).resolve().parent.parent
dst=root/"dual_proofs/lean"
dst.mkdir(parents=True,exist_ok=True)
src=root/"strong_edge_lean_starter"
before=json.loads((root/"audit_packing20/source-sha256-before.json").read_text())
for rel,sha in before.items():
    p=src/rel
    assert hashlib.sha256(p.read_bytes()).hexdigest()==sha, rel
    q=dst/rel
    q.parent.mkdir(parents=True,exist_ok=True)
    if not q.exists(): shutil.copy2(p,q)
config=dst/"lakefile.toml"
old=config.read_text()
if 'name = "PaperRoute"' not in old:
    config.write_text(old+'\n[[lean_lib]]\nname = "PaperRoute"\n',encoding="utf-8")
(dst/"PaperRoute").mkdir(exist_ok=True)
(root/"dual_proofs/logs").mkdir(exist_ok=True)
for filename in ("AuditSemantic.lean","AuditRegression.lean"):
    shutil.copy2(root/"audit_packing20/isolated/strong_edge_lean_starter"/filename,dst/filename)
(root/"dual_proofs/original_source_hashes.json").write_text(
    json.dumps(before,indent=2),encoding="utf-8")
print(f"Copied {len(before)} original source/config files; original tree unchanged.")
