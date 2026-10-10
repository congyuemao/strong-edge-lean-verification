"""Typeset the corrected 19.5 manuscript using the companion PDFs' renderer.

The common renderer and the earlier manuscript outputs remain unchanged.
Corollary statements receive the same pagination treatment as other statements.
"""
from pathlib import Path
import re
import build_manuscript as renderer

if __name__ == "__main__":
    stem = "packing195_unconditional_manuscript"
    source = Path(renderer.__file__).with_name(f"{stem}.md").read_text(encoding="utf-8")
    author = re.search(r"^@author (.+)$", source, re.M).group(1).strip()
    code = Path(renderer.__file__).read_text(encoding="utf-8")
    code = code.replace('"packing20_manuscript.md"', f'"{stem}.md"')
    code = code.replace('"packing20_proof_manuscript.pdf"', f'"{stem}.pdf"')
    code = code.replace('"manuscript_build.json"', f'"{stem}_build.json"')
    code = code.replace(
        'title="Induced Matchings in Prescribed Edge Sets of Graphs of Maximum Degree Four"',
        'title="A Corrected 19.5 Bound for Induced Matchings in Prescribed Edge Sets"',
    )
    code = code.replace(
        "(Theorem|Lemma|Proposition)", "(Theorem|Lemma|Proposition|Corollary)"
    )
    code = code.replace('author="", subject=', f'author={author!r}, subject=')
    code = code.replace(
        '    "date": ParagraphStyle(',
        '    "author": ParagraphStyle("author", fontName="TimesBody", '
        'fontSize=12, leading=15, alignment=TA_CENTER, spaceBefore=5, '
        'spaceAfter=5, keepWithNext=True),\n'
        '    "credit": ParagraphStyle("credit", fontName="TimesBody-Italic", '
        'fontSize=10, leading=13, alignment=TA_CENTER, spaceAfter=5, '
        'keepWithNext=True),\n'
        '    "date": ParagraphStyle(',
    )
    code = code.replace(
        '                elif line.startswith("@date "):',
        '                elif line.startswith("@author "):\n'
        '                    story.append(paragraph(line[len("@author "):],"author"))\n'
        '                elif line.startswith("@credit "):\n'
        '                    story.append(paragraph(line[len("@credit "):],"credit"))\n'
        '                elif line.startswith("@date "):',
    )
    namespace = {"__name__": "__main__", "__file__": str(Path(renderer.__file__))}
    exec(compile(code, str(Path(__file__)), "exec"), namespace)
