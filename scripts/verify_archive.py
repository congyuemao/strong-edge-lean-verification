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
]
paths = [root / n for n in [".gitignore", ".gitattributes", "README.md", *checkpoint_names]]
paths += list(walk_files(project)) + list(walk_files(root / "docs")) + list(walk_files(root / "scripts"))
paths = sorted(set(p for p in paths if p != manifest_path))
assert all(p.is_file() and p.is_relative_to(root) for p in paths)
assert not any(p.suffix.lower() in {".exe", ".dll", ".olean", ".ilean", ".pyc"} for p in paths)
assert not any(p.name == ".env" or p.name.startswith(".env.") for p in paths)

source_manifest = json.loads(read(project / "verification/high20-source-sha256.json"))
assert len(source_manifest) == 49
assert all(sha(project / name) == value for name, value in source_manifest.items()), "Current source hash changed."
lean_files = [p for p in paths if p.suffix == ".lean"]
assert len(lean_files) == 45
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

old_hashes = json.loads(read(project / "verification/high20-status.json"))["preserved_checkpoint_sha256"]
previous_verification = json.loads(read(project / "verification/high20-baseline-archive-manifest.json"))["verification"]
historical_hashes = dict(previous_verification["preserved_checkpoints"])
historical_hashes["strong_edge_lean_high21_checkpoint.zip"] = previous_verification["latest_checkpoint_sha256"]
assert old_hashes == historical_hashes
for name in checkpoint_names:
    if name in old_hashes:
        assert sha(root / name) == old_hashes[name], name
    with zipfile.ZipFile(root / name) as archive:
        assert archive.testzip() is None, name

with zipfile.ZipFile(root / checkpoint_names[-1]) as archive:
    latest_zip_files = [name for name in archive.namelist() if not name.endswith("/")]
    for name in latest_zip_files:
        assert (root / name).is_relative_to(root)
        assert archive.read(name) == (root / name).read_bytes(), name
    assert len(latest_zip_files) >= 205

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
    "lean_source_files": 45, "source_and_config_hashes_matched": 49,
    "latest_build_jobs": 1170, "latest_audited_theorems": 225,
    "allowed_axioms": sorted(allowed), "prohibited_lean_tokens_found": 0,
    "common_credential_patterns_found": 0,
    "preserved_checkpoints": old_hashes,
    "latest_checkpoint_sha256": sha(root / checkpoint_names[-1]),
    "latest_zip_files_matching_workspace": len(latest_zip_files),
    "stages": stages, "unconditional_packing20_proved": True,
    "remaining_explicit_bounds": {},
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
