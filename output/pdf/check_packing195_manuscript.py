"""Check manuscript references, PDF layout, and preservation of verified sources.

This script does not prove the English mathematical argument. The argument is
reviewed separately against the cited Lean files.
"""
from pathlib import Path
import hashlib
import json
import re

from PIL import Image, ImageDraw
from pypdf import PdfReader
import pdfplumber
import pypdfium2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROJECT = ROOT / "strong_edge_lean_starter"
STEM = "packing195_unconditional_manuscript"
SOURCE = HERE / f"{STEM}.md"
PDF = HERE / f"{STEM}.pdf"
RENDERS = ROOT / "tmp/pdfs/packing195"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    text = SOURCE.read_text(encoding="utf-8")
    build = json.loads((HERE / f"{STEM}_build.json").read_text(encoding="utf-8"))
    assert build["sha256"] == sha(PDF)
    assert build["source_sha256"] == sha(SOURCE)
    assert not build["math_width_diagnostics"]
    definitions = re.findall(
        r"^\*\*(Theorem|Lemma|Proposition|Corollary) (\d+\.\d+)\b", text, re.M
    )
    assert len(definitions) == len(set(definitions)) == 37
    mentions = re.findall(
        r"\b(Theorem|Lemma|Proposition|Corollary) (\d+\.\d+)", text
    )
    assert not (set(mentions) - set(definitions))
    equations = re.findall(r"\\tag\{(\d+\.\d+)\}", text)
    assert len(equations) == len(set(equations))
    equation_refs = re.findall(r"(?<!\\tag)\((\d+\.\d+)\)", text)
    assert not (set(equation_refs) - set(equations))
    assert text.count("$") % 2 == 0
    assert not re.search(r"\b(TODO|FIXME|TBD)\b", text)

    hashes = json.loads(
        (PROJECT / "verification/packing195-unconditional-source-sha256.json")
        .read_text(encoding="utf-8")
    )
    assert len(hashes) == 79
    assert all(sha(PROJECT / path) == value for path, value in hashes.items())
    lean_sources = {p: p.read_text(encoding="utf-8") for p in
                    (PROJECT / "StrongEdge").rglob("*.lean")}
    declarations = {}
    for path, content in lean_sources.items():
        for name in re.findall(r"^(?:theorem|def|noncomputable def) (\w+)", content, re.M):
            declarations[name] = path
    crosswalk = []
    appendix = text.split("@table Manuscript step |", 1)[1].split(
        "The exact cover identity", 1
    )[0]
    for line in appendix.splitlines():
        if not line.startswith("@row "):
            continue
        statement, items = line[5:].split("|", 1)
        paths = []
        for item in items.strip().split(";"):
            item = item.strip()
            possible = [
                PROJECT / "StrongEdge" / f"{item}.lean",
                PROJECT / "StrongEdge/Bounds" / f"{item}.lean",
            ]
            path = next((p for p in possible if p.is_file()), None)
            if path is None:
                assert item in declarations, item
                path = declarations[item]
            paths.append(path.relative_to(ROOT).as_posix())
        crosswalk.append({"statement": statement.strip(), "sources": paths})
    assert len(crosswalk) == 19
    for name in [
        "induced_matching_packing195_with_connected_component_count",
        "IsFiveCycleBlowupComponent",
        "five_cycle_blowup_is_connected_component",
        "tightComponentCount_eq_connected_component_count",
        "twenty_clique_conflict_closed",
        "twentyCliquesIn_sdiff",
        "tightComponentsIn",
    ]:
        assert name in declarations, name

    reader = PdfReader(PDF)
    pages = len(reader.pages)
    extracted = "\n".join(p.extract_text() for p in reader.pages)
    assert reader.metadata.author == "Congyue Mao"
    assert build["author"] == "Congyue Mao"
    first_page = reader.pages[0].extract_text()
    assert "Congyue Mao" in first_page
    assert "Proof completed using GPT-6 Astra" in first_page
    assert "AI assistance and verification" in extracted
    normalized = " ".join(extracted.split())
    assert (
        "This research was conducted predominantly using generative AI systems, "
        "including mathematical exploration, proof development, Lean formalization, "
        "and manuscript preparation."
    ) in normalized
    assert sum(len(p.images) for p in reader.pages) == 0
    for token in ["@abstract", "@author", "@credit", "@row", "@table", "@ref", "@@", "\ufffd"]:
        assert token not in extracted, token
    for kind, number in definitions:
        assert f"{kind} {number}" in extracted, (kind, number)
    assert "References" in extracted and "Appendix A." in extracted

    page_checks = []
    with pdfplumber.open(PDF) as document:
        for number, page in enumerate(document.pages, 1):
            footer = page.crop((0, page.height - 50, page.width, page.height))
            assert footer.extract_text().strip() == str(number)
            outside = [c for c in page.chars if c["x0"] < 60 or
                       c["x1"] > page.width - 60 or c["top"] < 25 or
                       c["bottom"] > page.height - 25]
            assert not outside, (number, outside[:3])
            page_checks.append({
                "page": number,
                "characters": len(page.chars),
                "outside_safe_area": len(outside),
                "minimum_x": round(min(c["x0"] for c in page.chars), 2),
                "maximum_x": round(max(c["x1"] for c in page.chars), 2),
            })

    RENDERS.mkdir(parents=True, exist_ok=True)
    document = pypdfium2.PdfDocument(PDF)
    render_paths = []
    for number in range(len(document)):
        path = RENDERS / f"page-{number + 1:02}.png"
        document[number].render(scale=1.5).to_pil().save(path)
        render_paths.append(path)
    for start in range(0, pages, 4):
        contact = Image.new("RGB", (1260, 1810), "#d5d5d5")
        draw = ImageDraw.Draw(contact)
        for offset, path in enumerate(render_paths[start:start + 4]):
            with Image.open(path) as page:
                page.thumbnail((610, 865))
                x, y = 10 + (offset % 2) * 630, 28 + (offset // 2) * 900
                contact.paste(page, (x, y))
                draw.text((x + 5, y - 20), f"Page {start + offset + 1}", fill="black")
        contact.save(RENDERS / f"contact-{start // 4 + 1}.png")

    result = {
        "pdf_sha256": sha(PDF),
        "source_sha256": sha(SOURCE),
        "pages": pages,
        "numbered_statements": len(definitions),
        "numbered_equations": len(equations),
        "source_and_config_hashes_preserved": len(hashes),
        "vector_math_only": True,
        "author": "Congyue Mao",
        "author_visible_on_first_page": True,
        "ai_assistance_disclosure": "GPT-6 Astra; title page and dedicated statement",
        "manuscript_references_resolved": True,
        "crosswalk": crosswalk,
        "page_checks": page_checks,
        "scope": "Source integrity, reference resolution and PDF layout checks; not a proof of the English prose.",
        "visual_review": "Rendered pages are inspected separately in the authoring task.",
    }
    (HERE / f"{STEM}_validation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {"crosswalk", "page_checks"}}, indent=2))


if __name__ == "__main__":
    main()
