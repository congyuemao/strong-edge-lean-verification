"""Check the saved continuation evidence and write a source-only checkpoint.

Run Lean first using PACKING195_CONTINUATION.md. This script validates evidence;
it does not execute the compiler or substitute for kernel checking.
"""

import hashlib
import json
import re
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
VERIFY = PROJECT / "verification"
PREFIX = "packing195-continuation-"
ALLOW = {"propext", "Classical.choice", "Quot.sound"}
MODULES = ["Bounds/High21ImprovedRoot", "Bounds/High22ImprovedRoot",
           "Bounds/SubcubicBoundary", "Bounds/SubcubicSeventeen",
           "Bounds/High21Improved", "Packing195Continuation"]
PINS = ["lean-toolchain", "lake-manifest.json", "lakefile.toml", "lean.ps1"]
PRIOR = REPO / "strong_edge_lean_packing195_checkpoint.zip"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (VERIFY / (PREFIX + name + ".json")).write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def checked_log(stem):
    assert int(read(VERIFY / (PREFIX + stem + ".exitcode"))) == 0, stem
    value = read(VERIFY / (PREFIX + stem + ".log"))
    assert not re.search(r"\b(?:error|warning):", value), stem
    return value


def parse_audit(value):
    entries = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", value)
    result = {name: [a.strip() for a in body.split(",") if a.strip()]
              for name, body in entries}
    result.update({name: [] for name in re.findall(
        r"'([^']+)' does not depend on any axioms", value)})
    for name, dependencies in result.items():
        assert set(dependencies) <= ALLOW, (name, dependencies)
    return result


def main():
    build = checked_log("build")
    jobs = int(re.search(r"Build completed successfully \((\d+) jobs\)", build)[1])
    assert jobs == 1181
    baseline = parse_audit(checked_log("baseline-axioms"))
    previous = parse_audit(checked_log("prior-axioms"))
    new = parse_audit(checked_log("axioms"))
    assert len(baseline) == 225 and len(previous) == 22 and len(new) == 31
    checked_log("path4")
    checked_log("tests")

    declarations = {}
    for module in MODULES:
        for kind, name in re.findall(r"(?m)^(theorem|def) (\w+)",
                                    read(PROJECT / "StrongEdge" / (module + ".lean"))):
            qualified = "StrongEdge." + name
            assert qualified not in declarations
            declarations[qualified] = {"kind": kind, "module": module}
    assert sum(d["kind"] == "theorem" for d in declarations.values()) == 28
    assert sum(d["kind"] == "def" for d in declarations.values()) == 3
    assert set(declarations) == set(new)
    directives = re.findall(r"(?m)^#print axioms (\S+)",
                            read(PROJECT / "StrongEdge/Audit195Continuation.lean"))
    assert len(directives) == len(set(directives)) == 31
    assert set(directives) == set(declarations)

    sources = [PROJECT / "StrongEdge.lean"] + sorted((PROJECT / "StrongEdge").rglob("*.lean"))
    assert len(sources) == 58
    for path in sources:
        assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|unsafe|native_decide)\b",
                             read(path)), path

    preserved = []
    prior_hashes = json.loads(read(VERIFY / "packing195-source-sha256.json"))
    assert len(prior_hashes) == 55
    with zipfile.ZipFile(PRIOR) as archive:
        assert archive.testzip() is None
        for name, value in prior_hashes.items():
            original = archive.read("strong_edge_lean_starter/" + name)
            assert hashlib.sha256(original).hexdigest() == value, name
            current = (PROJECT / name).read_bytes()
            if name == "StrongEdge.lean":
                assert current.startswith(original), "Only append public imports"
            else:
                assert current == original, name
                preserved.append(name)
    assert len(preserved) == 54
    current_paths = sources + [PROJECT / p for p in PINS]
    hashes = {p.relative_to(PROJECT).as_posix(): digest(p) for p in current_paths}
    assert len(hashes) == 62
    save("source-sha256", hashes)
    save("audit-checks", {
        "baseline_count": len(baseline), "previous_count": len(previous),
        "new_count": len(new), "new_theorems": 28, "new_definitions": 3,
        "allowed_axioms": sorted(ALLOW), "declarations": declarations,
        "new_dependencies": new,
    })
    status = {
        "verification_date": "2026-10-10", "timezone": "Australia/Sydney",
        "build_jobs": jobs, "build_exit_code": 0, "audit_exit_code": 0,
        "audited_declarations": 278, "new_audited_declarations": 31,
        "new_theorems": 28, "new_definitions": 3,
        "lean_source_files": 58, "source_and_config_hashes": 62,
        "preserved_prior_lean_files": 50, "preserved_pinned_files": PINS,
        "changed_prior_lean_files": ["StrongEdge.lean (appended import only)"],
        "prior_checkpoint_sha256": digest(PRIOR),
        "proof_gap_scan": "clean", "allowed_axioms_only": True,
        "subcubic_clique_le_17": "kernel-checked, no conflict-degree threshold",
        "high21_le_17": "kernel-checked, complete universal local threshold",
        "high22_root_four_le_16": "kernel-checked, root-four branch only",
        "unconditional_packing195_complete": False,
        "remaining": ["high22 subcubic clique with exactly 17 selected edges",
                      "twenty-clique C5[2] rigidity",
                      "actual tight-component count and corrected 19.5 assembly"],
        "current_conditional_endpoint": "StrongEdge.induced_matching_packing195_of_subcubic_high22",
        "remaining_endpoint_hypotheses": ["High22SubcubicSeventeenExcluded G", "candidate no20"],
        "regressions": {"full_graph_path4": "passed", "previous_195_tests": "passed"},
        "finite_search_dependency": False,
    }
    save("status", status)

    artifacts = current_paths + [PROJECT / "README.md", PROJECT / "PACKING195_PROGRESS.md",
        PROJECT / "PACKING195_BLOCKERS.md", PROJECT / "PACKING195_CONTINUATION.md",
        Path(__file__).resolve()]
    artifacts += sorted(VERIFY.glob(PREFIX + "*"))
    target = REPO / "strong_edge_lean_packing195_continuation_checkpoint.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(artifacts)):
            if path.is_file():
                archive.write(path, path.relative_to(REPO).as_posix())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            assert archive.read(name) == (REPO / name).read_bytes(), name
    print(json.dumps(status, indent=2))
    print("Checkpoint SHA-256: " + digest(target))


if __name__ == "__main__":
    main()
