"""Typeset the two manuscripts using the previously verified vector renderer."""
from pathlib import Path
import sys
import build_manuscript as m

def build(stem, title):
    code = Path(m.__file__).read_text(encoding="utf-8")
    code = code.replace('"packing20_manuscript.md"', f'"{stem}.md"')
    code = code.replace('"packing20_proof_manuscript.pdf"', f'"{stem}.pdf"')
    code = code.replace('"manuscript_build.json"', f'"{stem}_build.json"')
    code = code.replace('title="Induced Matchings in Prescribed Edge Sets of Graphs of Maximum Degree Four"',
                        f'title={title!r}')
    namespace = {"__name__": "__main__", "__file__": str(Path(m.__file__))}
    exec(compile(code, str(Path(__file__)), "exec"), namespace)

if __name__ == "__main__":
    stem = sys.argv[1]
    title = {
        "route_a_paper_first": "Prescribed-Edge Induced-Matching Packing: Route A",
        "route_b_lean_first": "Prescribed-Edge Induced-Matching Packing: Route B",
    }[stem]
    build(stem, title)
