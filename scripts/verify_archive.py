"""Verify the collected Lean results without rewriting historical artifacts.

Run from any directory with Python 3. No third-party packages are required.
Use --write-manifest only when intentionally updating the archive inventory.
This script verifies saved evidence; run Lean separately to recheck proofs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import zipfile

root = Path(__file__).resolve().parents[1]
project = root / "strong_edge_lean_starter"
manifest_path = root / "docs/ARCHIVE_MANIFEST.json"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--write-manifest", action="store_true")
args = parser.parse_args()


def read(path):
    return path.read_text(encoding="utf-8-sig")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk_files(directory):
    for current, dirs, names in os.walk(directory):
        dirs[:] = sorted(d for d in dirs if d not in {".git", ".lake", ".cache", "__pycache__"})
        for name in sorted(names):
            yield Path(current) / name


checkpoint_names = [
    "strong_edge_lean_verified_checkpoint.zip", "strong_edge_lean_c4_checkpoint.zip",
    "strong_edge_lean_high24_checkpoint.zip", "strong_edge_lean_high23_checkpoint.zip",
    "strong_edge_lean_high22_checkpoint.zip",
    "strong_edge_lean_high21_checkpoint.zip",
    "strong_edge_lean_high20_checkpoint.zip",
    "strong_edge_lean_packing195_checkpoint.zip",
    "strong_edge_lean_packing195_continuation_checkpoint.zip",
    "strong_edge_lean_packing195_unconditional_checkpoint.zip",
]
paths = [root / n for n in [".gitignore", ".gitattributes", "README.md", *checkpoint_names]]
paths += list(walk_files(project)) + list(walk_files(root / "docs")) + list(walk_files(root / "scripts"))
for directory in ["audit_packing20", "dual_proofs", "output"]:
    paths += list(walk_files(root / directory))
paths = sorted(set(p for p in paths if p != manifest_path))
assert all(p.is_file() and p.is_relative_to(root) for p in paths)
assert not any(p.suffix.lower() in {".exe", ".dll", ".olean", ".ilean", ".pyc"} for p in paths)
assert not any(p.name == ".env" or p.name.startswith(".env.") for p in paths)

source_manifest = json.loads(read(project / "verification/packing195-unconditional-source-sha256.json"))
assert len(source_manifest) == 79
assert all(sha(project / name) == value for name, value in source_manifest.items()), "Current source hash changed."
lean_files = [p for p in paths if p.suffix == ".lean" and p.is_relative_to(project)]
assert len(lean_files) == 75
assert {p.relative_to(project).as_posix() for p in lean_files} == {
    name for name in source_manifest if name.endswith(".lean")
}
for p in lean_files:
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|unsafe|native_decide)\b", read(p)), p

audit = read(project / "verification/high20-axioms.log")
entries = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit, re.S)
audit_names = re.findall(r"^#print axioms (\S+)", read(project / "StrongEdge/Audit.lean"), re.M)
assert len(entries) == len(audit_names) == 225
assert [name for name, _ in entries] == audit_names
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert all({a.strip() for a in dependencies.split(",")} <= allowed for _, dependencies in entries)
build = read(project / "verification/high20-build.log")
assert "Build completed successfully (1170 jobs)" in build
assert not re.search(r"^(?:error|warning):", build, re.M)

stages = []
for label, stem, jobs, audited in [
    ("Initial", "", 1124, 13), ("C4", "next-stage-", 1127, 38),
    ("high24", "high24-", 1129, 51), ("high23", "high23-", 1136, 94),
    ("high22", "high22-", 1144, 145),
    ("high21", "high21-", 1162, 192),
    ("high20", "high20-", 1170, 225),
]:
    status = json.loads(read(project / f"verification/{stem}status.json"))
    assert status["build_jobs"] == jobs and status["audited_theorems"] == audited
    assert status["build_exit_code"] == status["axiom_audit_exit_code"] == 0
    stage_build = read(project / f"verification/{stem}build.log")
    stage_audit = read(project / f"verification/{stem}axioms.log")
    assert f"Build completed successfully ({jobs} jobs)" in stage_build
    assert len(re.findall(r"'([^']+)' depends on axioms:", stage_audit)) == audited
    stages.append({"stage": label, "build_jobs": jobs, "audited_theorems": audited})

new_audit = read(project / "verification/packing195-axioms.log")
new_entries = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", new_audit)
new_names = re.findall(r"^#print axioms (\S+)", read(project / "StrongEdge/Audit195.lean"), re.M)
assert len(new_entries) == len(new_names) == 22
assert [name for name, _ in new_entries] == new_names
assert all({a.strip() for a in dependencies.split(",")} <= allowed for _, dependencies in new_entries)
for stem in ["packing195-build", "packing195-axioms", "packing195-tests", "packing195-path4-regression"]:
    assert int(read(project / f"verification/{stem}.exitcode")) == 0
    assert not re.search(r"^(?:error|warning):", read(project / f"verification/{stem}.log"), re.M)
assert "Build completed successfully (1175 jobs)" in read(project / "verification/packing195-build.log")
stages.append({"stage": "packing195-conditional", "build_jobs": 1175, "audited_theorems": 247})

continuation_audit = read(project / "verification/packing195-continuation-axioms.log")
continuation_entries = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", continuation_audit)
continuation_names = re.findall(r"^#print axioms (\S+)",
                               read(project / "StrongEdge/Audit195Continuation.lean"), re.M)
assert len(continuation_entries) == len(continuation_names) == 31
assert [name for name, _ in continuation_entries] == continuation_names
assert all({a.strip() for a in dependencies.split(",")} <= allowed
           for _, dependencies in continuation_entries)
continuation_status = json.loads(read(project / "verification/packing195-continuation-status.json"))
assert continuation_status["new_theorems"] == 28 and continuation_status["new_definitions"] == 3
assert continuation_status["unconditional_packing195_complete"] is False
for stem in ["build", "axioms", "baseline-axioms", "prior-axioms", "path4", "tests"]:
    assert int(read(project / f"verification/packing195-continuation-{stem}.exitcode")) == 0
    assert not re.search(r"\b(?:error|warning):",
                         read(project / f"verification/packing195-continuation-{stem}.log"))
assert "Build completed successfully (1181 jobs)" in read(
    project / "verification/packing195-continuation-build.log")
for stem, count in [("baseline-axioms", 225), ("prior-axioms", 22)]:
    matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",
                         read(project / f"verification/packing195-continuation-{stem}.log"))
    assert len(matches) == count
    assert all({a.strip() for a in dependencies.split(",")} <= allowed for _, dependencies in matches)
stages.append({"stage": "packing195-high21-complete", "build_jobs": 1181,
               "audited_declarations": 278, "new_theorems": 28, "new_definitions": 3})

unconditional_status = json.loads(read(project / "verification/packing195-unconditional-status.json"))
assert unconditional_status["unconditional_packing195_complete"] is True
assert unconditional_status["remaining"] == []
assert unconditional_status["new_theorems"] == 87 and unconditional_status["new_definitions"] == 11
fresh_audits = {}
for module, count in [("Audit", 225), ("Audit195", 22), ("Audit195Continuation", 31),
                      ("Audit195Thresholds", 34), ("Audit195Unconditional", 64)]:
    log = read(project / f"verification/packing195-unconditional-{module}.log")
    assert int(read(project / f"verification/packing195-unconditional-{module}.exitcode")) == 0
    assert not re.search(r"\b(?:error|warning):", log)
    pairs = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", log)
    parsed = {name: [a.strip() for a in deps.split(",") if a.strip()] for name, deps in pairs}
    parsed.update({name: [] for name in re.findall(r"'([^']+)' does not depend on any axioms", log)})
    names = re.findall(r"(?m)^#print axioms (\S+)", read(project / "StrongEdge" / (module + ".lean")))
    assert len(parsed) == len(names) == count and set(parsed) == set(names)
    assert not (set(parsed) & set(fresh_audits))
    assert all(set(deps) <= allowed for deps in parsed.values())
    fresh_audits.update(parsed)
assert len(fresh_audits) == 376
for stem in ["build", "path4", "tests195", "tight-example"]:
    assert int(read(project / f"verification/packing195-unconditional-{stem}.exitcode")) == 0
    assert not re.search(r"\b(?:error|warning):", read(project / f"verification/packing195-unconditional-{stem}.log"))
assert "Build completed successfully (1197 jobs)" in read(project / "verification/packing195-unconditional-build.log")
stages.append({"stage": "packing195-unconditional-complete", "build_jobs": 1197,
               "audited_declarations": 376, "new_theorems": 87, "new_definitions": 11})

old_hashes = json.loads(read(project / "verification/high20-status.json"))["preserved_checkpoint_sha256"]
previous_verification = json.loads(read(project / "verification/high20-baseline-archive-manifest.json"))["verification"]
historical_hashes = dict(previous_verification["preserved_checkpoints"])
historical_hashes["strong_edge_lean_high21_checkpoint.zip"] = previous_verification["latest_checkpoint_sha256"]
assert old_hashes == historical_hashes
old_hashes["strong_edge_lean_high20_checkpoint.zip"] = "7dd2a102dda783f1ade4ec53096928bc52dcc246a6432c9221c9fe3ac4a41818"
old_hashes["strong_edge_lean_packing195_checkpoint.zip"] = "7f8334242f38f81cd671b6d516fe28c41a2a5ac65e2f78bc8da457c02937379a"
old_hashes["strong_edge_lean_packing195_continuation_checkpoint.zip"] = "4d0d5cda0526a46c850aaa452382b55a8afc7fc7791d2cc929430fc3617cc60f"
for name in checkpoint_names:
    if name in old_hashes:
        assert sha(root / name) == old_hashes[name], name
    with zipfile.ZipFile(root / name) as archive:
        assert archive.testzip() is None, name

with zipfile.ZipFile(root / "strong_edge_lean_high20_checkpoint.zip") as archive:
    baseline_members = [name for name in archive.namelist() if not name.endswith("/")]
    assert len(baseline_members) >= 205
    for name in baseline_members:
        assert (root / name).is_relative_to(root)
        original = archive.read(name)
        current = (root / name).read_bytes()
        if name == "strong_edge_lean_starter/StrongEdge.lean":
            assert current.startswith(original), name
        else:
            assert current == original, name
    baseline_sources = json.loads(read(project / "verification/high20-source-sha256.json"))
    assert len(baseline_sources) == 49
    for name, value in baseline_sources.items():
        original = archive.read("strong_edge_lean_starter/" + name)
        assert hashlib.sha256(original).hexdigest() == value, name
        current = (project / name).read_bytes()
        if name == "StrongEdge.lean":
            assert current.startswith(original), "Baseline imports must be preserved."
        else:
            assert current == original, name

with zipfile.ZipFile(root / "strong_edge_lean_packing195_checkpoint.zip") as archive:
    for name in archive.namelist():
        if name.endswith("/"):
            continue
        assert (root / name).is_relative_to(root)
        original, current = archive.read(name), (root / name).read_bytes()
        if name == "strong_edge_lean_starter/StrongEdge.lean":
            assert current.startswith(original), name
        else:
            assert current == original, name

with zipfile.ZipFile(root / checkpoint_names[-1]) as archive:
    latest_zip_files = [name for name in archive.namelist() if not name.endswith("/")]
    for name in latest_zip_files:
        assert (root / name).is_relative_to(root)
        assert archive.read(name) == (root / name).read_bytes(), name
    assert len(latest_zip_files) >= 79

secret_patterns = {
    "github_token": re.compile(rb"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(rb"(?:AKIA|ASIA)[A-Z0-9]{16}"),
}


def check_secrets(data, label):
    for kind, pattern in secret_patterns.items():
        assert not pattern.search(data), f"Potential {kind} in {label}; inspect before upload."


for path in paths:
    data = path.read_bytes()
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
            for name in archive.namelist():
                if not name.endswith("/"):
                    check_secrets(archive.read(name), path.name + "/" + name)
    else:
        check_secrets(data, path.relative_to(root).as_posix())

for md in [root / "README.md", root / "docs/RESULTS_INDEX.md", root / "docs/inputs/README.md"]:
    for target in re.findall(r"\]\(([^)]+)\)", read(md)):
        if "://" not in target and not target.startswith("#"):
            destination = (md.parent / target.split("#", 1)[0]).resolve()
            assert destination == manifest_path or destination.exists(), (md.name, target)

inventory = {p.relative_to(root).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p)} for p in paths}
verification = {
    "lean_source_files": 75, "source_and_config_hashes_matched": 79,
    "latest_build_jobs": 1197, "latest_audited_declarations": 376,
    "baseline_audited_theorems": 225, "prior_new_audited_theorems": 22,
    "new_audited_theorems": 87, "new_audited_definitions": 11,
    "allowed_axioms": sorted(allowed), "prohibited_lean_tokens_found": 0,
    "common_credential_patterns_found": 0,
    "preserved_checkpoints": old_hashes,
    "latest_checkpoint_sha256": sha(root / checkpoint_names[-1]),
    "latest_zip_files_matching_workspace": len(latest_zip_files),
    "stages": stages, "unconditional_packing20_proved": True,
    "unconditional_packing195_proved": True,
    "remaining_explicit_bounds": {},
    "high21_le_17_kernel_checked": True,
    "high22_root_four_le_16_kernel_checked": True,
    "high22_le_16_kernel_checked": True,
    "twenty_clique_rigidity_kernel_checked": True,
    "actual_connected_component_count_kernel_checked": True,
    "remaining_packing195_structure": [],
}
if args.write_manifest:
    manifest = {
        "archive_date": "2026-10-10", "timezone": "Australia/Sydney",
        "last_lean_verification_date": "2026-10-10",
        "note": "This inventory excludes itself. Historical Lean logs and checkpoint ZIPs are preserved unchanged.",
        "file_count_excluding_manifest": len(inventory),
        "total_bytes_excluding_manifest": sum(item["bytes"] for item in inventory.values()),
        "verification": verification, "files": inventory,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
else:
    manifest = json.loads(read(manifest_path))
    assert manifest["files"] == inventory, "Archive inventory changed."
    assert manifest["verification"] == verification, "Verification metadata changed."
print(json.dumps({"status": "verified", "files_including_manifest": len(inventory) + 1,
                  "total_bytes_excluding_manifest": sum(item["bytes"] for item in inventory.values()),
                  **verification}, indent=2))
