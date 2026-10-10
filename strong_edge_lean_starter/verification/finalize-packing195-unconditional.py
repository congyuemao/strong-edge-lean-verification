"""Validate saved Lean evidence and create the source-only 19.5 checkpoint.

This validates compiler logs and source provenance; it does not replace Lean.
Run the commands in PACKING195_UNCONDITIONAL.md before running this script.
"""
import hashlib
import json
import re
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
VERIFY = PROJECT / "verification"
PREFIX = "packing195-unconditional-"
ALLOW = {"propext", "Classical.choice", "Quot.sound"}
PINS = ["lean-toolchain", "lake-manifest.json", "lakefile.toml", "lean.ps1"]
AUDITS = {"Audit": 225, "Audit195": 22, "Audit195Continuation": 31,
          "Audit195Thresholds": 34, "Audit195Unconditional": 64}
PRIOR = REPO / "strong_edge_lean_packing195_continuation_checkpoint.zip"


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
    pairs = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", value)
    result = {name: [a.strip() for a in body.split(",") if a.strip()] for name, body in pairs}
    result.update({name: [] for name in re.findall(r"'([^']+)' does not depend on any axioms", value)})
    assert all(set(axioms) <= ALLOW for axioms in result.values())
    return result


def main():
    build = checked_log("build")
    jobs = int(re.search(r"Build completed successfully \((\d+) jobs\)", build)[1])
    assert jobs == 1197
    audited = {}
    for module, count in AUDITS.items():
        entries = parse_audit(checked_log(module))
        directives = re.findall(r"(?m)^#print axioms (\S+)", read(PROJECT / "StrongEdge" / (module + ".lean")))
        assert len(entries) == len(directives) == len(set(directives)) == count
        assert set(entries) == set(directives)
        assert not (set(entries) & set(audited))
        audited.update(entries)
    assert len(audited) == 376
    for stem in ["path4", "tests195", "tight-example"]:
        checked_log(stem)
    prior_hashes = json.loads(read(VERIFY / "packing195-continuation-source-sha256.json"))
    assert len(prior_hashes) == 62
    assert digest(PRIOR) == "4d0d5cda0526a46c850aaa452382b55a8afc7fc7791d2cc929430fc3617cc60f"
    preserved = []
    with zipfile.ZipFile(PRIOR) as archive:
        assert archive.testzip() is None
        for name, expected in prior_hashes.items():
            original = archive.read("strong_edge_lean_starter/" + name)
            assert hashlib.sha256(original).hexdigest() == expected
            current = (PROJECT / name).read_bytes()
            if name == "StrongEdge.lean":
                assert current.startswith(original), "Public entrypoint may only append imports"
            else:
                assert current == original, name
                preserved.append(name)
    assert len(preserved) == 61
    sources = [PROJECT / "StrongEdge.lean"] + sorted((PROJECT / "StrongEdge").rglob("*.lean"))
    assert len(sources) == 75
    for path in sources:
        assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|native_decide)\b", read(path)), path
    new_declarations = {}
    for path in sources:
        relative = path.relative_to(PROJECT).as_posix()
        if relative in prior_hashes or path.name.startswith("Audit"):
            continue
        namespace = "StrongEdge.Tests195Unconditional." if path.stem == "Tests195Unconditional" else "StrongEdge."
        for kind, name in re.findall(r"(?m)^(?:noncomputable )?(def|theorem) (\w+)", read(path)):
            new_declarations[namespace + name] = {"kind": kind, "module": relative}
    new_audited = set(parse_audit(checked_log("Audit195Thresholds"))) | set(parse_audit(checked_log("Audit195Unconditional")))
    assert set(new_declarations) == new_audited
    paths = sources + [PROJECT / p for p in PINS]
    hashes = {p.relative_to(PROJECT).as_posix(): digest(p) for p in paths}
    assert len(hashes) == 79
    save("source-sha256", hashes)
    save("audit-checks", {"count": len(audited), "allowed_axioms": sorted(ALLOW),
                          "dependencies": audited, "new_declarations": new_declarations})
    status = {
        "verification_date": "2026-10-10", "timezone": "Australia/Sydney",
        "build_jobs": jobs, "build_exit_code": 0, "audit_exit_code": 0,
        "audited_declarations": len(audited), "new_audited_declarations": len(new_declarations),
        "new_theorems": sum(d["kind"] == "theorem" for d in new_declarations.values()),
        "new_definitions": sum(d["kind"] == "def" for d in new_declarations.values()),
        "lean_source_files": len(sources), "source_and_config_hashes": len(hashes),
        "preserved_prior_lean_files": 57, "preserved_pinned_files": PINS,
        "changed_prior_lean_files": ["StrongEdge.lean (appended public imports only)"],
        "prior_checkpoint_sha256": digest(PRIOR),
        "proof_gap_scan": "clean", "allowed_axioms_only": True,
        "unconditional_packing195_complete": True,
        "endpoint": "StrongEdge.induced_matching_packing195_with_connected_component_count",
        "remaining_endpoint_hypotheses": ["maximum original degree at most four"],
        "statement": "For every F, exists an induced matching M subset F with 2|F| <= 39|M| + t_G(F)",
        "correction": "Actual original connected C5[2] components with every edge in F",
        "remaining": [], "finite_search_dependency": False,
        "regressions": {"original_path4_witness": "passed", "previous_195_tests": "passed",
                        "C5_double_degree_card_shape": "passed", "C5_double_requires_correction": "passed"},
    }
    save("status", status)
    artifacts = paths + [PROJECT / "README.md", PROJECT / "PACKING195_UNCONDITIONAL.md",
                         PROJECT / "PACKING195_CONTINUATION.md", Path(__file__).resolve()]
    artifacts += sorted(VERIFY.glob(PREFIX + "*"))
    target = REPO / "strong_edge_lean_packing195_unconditional_checkpoint.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(artifacts)):
            if path.is_file():
                archive.write(path, path.relative_to(REPO).as_posix())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            assert archive.read(name) == (REPO / name).read_bytes()
    print(json.dumps(status, indent=2))
    print("Checkpoint SHA-256: " + digest(target))


if __name__ == "__main__":
    main()
