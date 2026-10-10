"""Check the final PDF and preserve the original Lean source hashes."""
from pathlib import Path
import json, hashlib, re
from PIL import Image, ImageOps, ImageDraw
import pdfplumber
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
pdfpath = HERE/"packing20_proof_manuscript.pdf"
reader = PdfReader(str(pdfpath))
texts = [page.extract_text() for page in reader.pages]
alltext = "\n".join(texts)
bad_tokens = [s for s in ["@abstract","@table","@@MATH","\ufffd"] if s in alltext]
assert not bad_tokens, bad_tokens
assert not (reader.metadata.author or "")
assert len(reader.pages) == 12
assert sum(len(p.images) for p in reader.pages) == 0
assert all(x in alltext for x in [
    "Theorem 1.1", "Theorem 4.1", "Proposition 4.2",
    "Proposition 4.3", "Proposition 4.4", "Proposition 4.5",
    "Proposition 4.6", "Lemma 5.3", "Proposition 6.1", "References",
])

source_hashes = json.loads((ROOT/"audit_packing20/source-sha256-before.json").read_text())
changed = []
for rel, expected in source_hashes.items():
    actual = hashlib.sha256((ROOT/"strong_edge_lean_starter"/rel).read_bytes()).hexdigest()
    if actual != expected:
        changed.append(rel)
assert not changed, changed

page_checks = []
with pdfplumber.open(pdfpath) as doc:
    for i,p in enumerate(doc.pages,1):
        assert p.crop((0,p.height-50,p.width,p.height)).extract_text().strip() == str(i)
        # Include headers and page numbers; exclude no visible text.
        outside = [
            {"text":c["text"],"box":[c["x0"],c["top"],c["x1"],c["bottom"]]}
            for c in p.chars if c["x0"] < 60 or c["x1"] > p.width-60
            or c["top"] < 25 or c["bottom"] > p.height-25
        ]
        assert not outside, (i,outside[:5])
        page_checks.append({
            "page":i, "characters":len(p.chars), "outside_safe_area":len(outside),
            "minimum_x":round(min(c["x0"] for c in p.chars),2),
            "maximum_x":round(max(c["x1"] for c in p.chars),2),
        })

paths = sorted((ROOT/"tmp/pdfs").glob("page-*.png"))
if len(paths) == 12:
    for group in range(3):
        canvas = Image.new("RGB",(1220,1740),"#d5d5d5")
        draw = ImageDraw.Draw(canvas)
        for j,path in enumerate(paths[group*4:group*4+4]):
            im=Image.open(path).convert("RGB")
            im.thumbnail((595,842))
            x,y=10+(j%2)*610,25+(j//2)*870
            canvas.paste(im,(x,y))
            draw.text((x+4,y-17),f"Page {group*4+j+1}",fill="black")
        canvas.save(ROOT/f"tmp/pdfs/contact-{group+1}.png")

result = {
    "pdf_sha256":hashlib.sha256(pdfpath.read_bytes()).hexdigest(),
    "pages":len(reader.pages), "author_field_empty":True,
    "vector_math_only":True, "original_sources_unchanged":len(source_hashes),
    "unexpanded_markup":bad_tokens, "page_checks":page_checks,
    "visual_review":"See final rendered-page inspection in the task; checked separately.",
}
(HERE/"manuscript_validation.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
