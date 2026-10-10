"""Transparent source fork for the paper-first proof, before its new additions."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
src=root/"lean"
records=[]
for p in sorted((src/"StrongEdge").rglob("*.lean"))+[src/"StrongEdge.lean"]:
    rel=p.relative_to(src)
    target=src/"PaperRoute"/Path(str(rel).replace("StrongEdge","Library",1))
    target.parent.mkdir(parents=True,exist_ok=True)
    original=p.read_text(encoding="utf-8")
    copied=original.replace("StrongEdge","PaperRoute.Library")
    target.write_text(copied,encoding="utf-8")
    records.append({"original":str(rel),"copy":str(target.relative_to(src)),
                    "operation":"StrongEdge -> PaperRoute.Library; otherwise same text",
                    "source_sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
f=src/"PaperRoute/Foundations.lean"
s=f.read_text(encoding="utf-8").replace("public import StrongEdge.Bounds.High20",
    "public import PaperRoute.Library.Bounds.High20").replace(
    "open StrongEdge Finset","open PaperRoute.Library Finset")
s=s.replace("h ▸ hwf","h.symm ▸ hwf").replace("heg ▸ hwg","heg.symm ▸ hwg")
f.write_text(s,encoding="utf-8")
(root/"source_fork_manifest.json").write_text(json.dumps(records,indent=2),encoding="utf-8")
print(len(records),"Lean sources forked; all shared proof text explicitly recorded.")
