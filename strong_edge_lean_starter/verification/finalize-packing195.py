"""Validate saved Lean evidence and preserve a source-only stage checkpoint.

This validates logs and source consistency; it does not execute Lean or replace
kernel checking. Run the commands in PACKING195_PROGRESS.md first.
"""

import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
VERIFY = PROJECT / "verification"
BASELINE = "8de26d2d6cb17354af7fb5919fcdbbc79c8aaf6f"
ALLOW = {"propext", "Classical.choice", "Quot.sound"}
NEW_MODULES = ["MinimalPacking195", "Packing195", "Tests195", "Audit195",
               "Bounds/High20Improved", "Bounds/High23Improved"]
PINS = ["lean-toolchain", "lake-manifest.json", "lakefile.toml", "lean.ps1"]


def read(path):
    return path.read_text(encoding="utf-8-sig")


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_log(stem, build=False):
    code = int(read(VERIFY / (stem + ".exitcode")).strip())
    assert code == 0, (stem, code)
    text = read(VERIFY / (stem + ".log"))
    assert not re.search(r"(?im)^(error|warning):", text), stem
    if build:
        found = re.search(r"Build completed successfully \((\d+) jobs\)", text)
        assert found, stem
        return int(found.group(1))
    return text


def axioms(text):
    matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", text)
    clean = re.findall(r"'([^']+)' does not depend on any axioms", text)
    result = {name: [x.strip() for x in body.split(",") if x.strip()]
              for name, body in matches}
    result.update({name: [] for name in clean})
    for name, dependencies in result.items():
        assert set(dependencies) <= ALLOW, (name, dependencies)
    return result


def main():
    baseline_jobs = check_log("packing195-baseline-build", True)
    final_jobs = check_log("packing195-build", True)
    old_audit = axioms(check_log("packing195-baseline-axioms"))
    new_audit = axioms(check_log("packing195-axioms"))
    check_log("packing195-tests")
    check_log("packing195-path4-regression")
    assert len(old_audit) == 225, len(old_audit)

    declarations = []
    for name in NEW_MODULES:
        text = read(PROJECT / "StrongEdge" / (name + ".lean"))
        namespace = "StrongEdge.Tests195" if name == "Tests195" else "StrongEdge"
        declarations += [namespace + "." + n for n in re.findall(r"(?m)^theorem (\w+)", text)]
    assert len(declarations) == len(set(declarations)) == 22
    assert set(declarations) == set(new_audit), (set(declarations) ^ set(new_audit))
    audit_source = read(PROJECT / "StrongEdge/Audit195.lean")
    for name in declarations:
        assert "#check " + name in audit_source
        assert "#print axioms " + name in audit_source

    tracked = git("ls-tree", "-r", "--name-only", BASELINE).decode().splitlines()
    previous_lean = [p for p in tracked if p.endswith(".lean")]
    assert len(previous_lean) == 45
    changed = []
    for name in previous_lean + ["strong_edge_lean_starter/" + p for p in PINS]:
        old = git("show", BASELINE + ":" + name)
        current = (REPO / name).read_bytes()
        if old != current:
            changed.append(name)
            assert name == "strong_edge_lean_starter/StrongEdge.lean", name
            assert current.startswith(old), "Public entry point must only append imports"

    # No proof-gap syntax or native evaluator trust is permitted in any Lean source.
    lean_sources = [PROJECT / "StrongEdge.lean"] + sorted((PROJECT / "StrongEdge").rglob("*.lean"))
    for path in lean_sources:
        assert not re.search(r"\b(sorry|admit|axiom|unsafe|native_decide)\b", read(path)), path

    source_paths = lean_sources + [PROJECT / p for p in PINS]
    source_hashes = {str(p.relative_to(PROJECT)).replace("\\", "/"): digest(p)
                     for p in source_paths}
    (VERIFY / "packing195-source-sha256.json").write_text(
        json.dumps(source_hashes, indent=2) + "\n", encoding="utf-8")
    audit_report = {"baseline_count": len(old_audit), "new_count": len(new_audit),
                    "allowed_axioms": sorted(ALLOW), "new_declarations": new_audit}
    (VERIFY / "packing195-audit-checks.json").write_text(
        json.dumps(audit_report, indent=2) + "\n", encoding="utf-8")
    search = json.loads(read(VERIFY / "packing195-search.json"))
    assert not search["counterexamples"]
    status = {
        "baseline_commit": BASELINE,
        "branch": git("branch", "--show-current").decode().strip(),
        "baseline_build_jobs": baseline_jobs, "final_build_jobs": final_jobs,
        "baseline_audited_theorems": len(old_audit), "new_audited_theorems": len(new_audit),
        "lean_source_files": len(lean_sources), "preserved_old_lean_files": 44,
        "changed_old_lean_files": changed, "preserved_pinned_environment_files": PINS,
        "proof_gap_scan": "clean", "T1": "kernel-checked conditional theorem",
        "T2": "kernel-checked conditional theorem", "high20_le_18": "kernel-checked",
        "high23_le_15": "kernel-checked", "high24_le_13": "reused baseline theorem",
        "unconditional_packing195_complete": False,
        "remaining": ["high21 <= 17", "high22 <= 16", "twenty-clique rigidity",
                      "C5[2] component counting and final assembly"],
        "finite_search": {"graphs": search["graphs"], "counterexamples": 0,
                          "role": "falsification search only; not a proof dependency"},
    }
    (VERIFY / "packing195-status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (VERIFY / "packing195-tracked-source.diff").write_bytes(git("diff", BASELINE, "--", "*.lean"))

    # All Lean sources (including new untracked files) and pins are packaged.
    artifacts = source_paths + [PROJECT / "PACKING195_PROGRESS.md", PROJECT / "PACKING195_BLOCKERS.md",
        PROJECT / "README.md", Path(__file__).resolve(), VERIFY / "search-packing195.py"]
    artifacts += sorted(VERIFY.glob("packing195-*"))
    archive = REPO / "strong_edge_lean_packing195_checkpoint.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(set(artifacts)):
            if path.is_file():
                z.write(path, str(path.relative_to(REPO)).replace("\\", "/"))
    print(json.dumps(status, indent=2))
    print("Checkpoint SHA-256: " + digest(archive))


if __name__ == "__main__":
    main()
