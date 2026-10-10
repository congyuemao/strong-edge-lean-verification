"""Typeset the corrected 19.5 manuscript using the companion PDFs' renderer.

The common renderer and the earlier manuscript outputs remain unchanged.
Corollary statements receive the same pagination treatment as other statements.
"""
from pathlib import Path
import build_manuscript as renderer

if __name__ == "__main__":
    stem = "packing195_unconditional_manuscript"
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
    namespace = {"__name__": "__main__", "__file__": str(Path(renderer.__file__))}
    exec(compile(code, str(Path(__file__)), "exec"), namespace)
