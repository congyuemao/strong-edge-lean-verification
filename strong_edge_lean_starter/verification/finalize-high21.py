"""Verify saved Lean evidence and package high21 sources; this is not a proof."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import subprocess
import zipfile

root = Path(__file__).resolve().parents[1]
verification = root / "verification"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


build = read(verification / "high21-build.log")
audit = read(verification / "high21-axioms.log")
baseline_build = read(verification / "high21-baseline-build.log")
baseline_audit = read(verification / "high21-baseline-axioms.log")
assert int(read(verification / "high21-build-exit-code.txt")) == 0
assert int(read(verification / "high21-audit-exit-code.txt")) == 0
assert "Build completed successfully (1144 jobs)" in baseline_build
match = re.search(r"Build completed successfully \((\d+) jobs\)", build)
assert match
jobs = int(match.group(1))
for text in (build, audit, baseline_build, baseline_audit):
    assert not re.search(r"(?:error:|warning:|sorryAx)", text)
pattern = r"'([^']+)' depends on axioms: \[([^\]]*)\]"
entries = re.findall(pattern, audit, re.S)
baseline_entries = re.findall(pattern, baseline_audit, re.S)
assert len(baseline_entries) == 145 and entries[:145] == baseline_entries
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert all({a.strip() for a in deps.split(",") if a.strip()} <= allowed for _, deps in entries)

lean_files = [root / "StrongEdge.lean", *sorted((root / "StrongEdge").rglob("*.lean"))]
configs = [root / n for n in ["lean-toolchain", "lakefile.toml", "lake-manifest.json", "lean.ps1"]]
manifest = {p.relative_to(root).as_posix(): sha(p) for p in lean_files + configs}
old = json.loads(read(verification / "high21-baseline-source-sha256.json"))
high22 = json.loads(read(verification / "high22-source-sha256.json"))
assert all(old[n] == h for n, h in high22.items())
changed = [n for n, h in old.items() if manifest[n] != h]
assert set(changed) == {"StrongEdge.lean", "StrongEdge/Audit.lean"}
new_theorems = {rel: re.findall(r"^theorem\s+(\w+)", read(root / rel), re.M)
                for rel in manifest if rel.endswith(".lean") and rel not in old}
new_defs = {rel: re.findall(r"^def\s+(\w+)", read(root / rel), re.M) for rel in new_theorems}
new_count = sum(map(len, new_theorems.values()))
assert len(new_theorems) == 9 and new_count == 47
audit_source = read(root / "StrongEdge/Audit.lean")
audit_names = re.findall(r"^#print axioms (\S+)", audit_source, re.M)
check_names = re.findall(r"^#check (\S+)", audit_source, re.M)
assert len(entries) == len(audit_names) == len(set(audit_names)) == 145 + new_count
assert [name for name, _ in entries] == audit_names
assert all("StrongEdge." + n in audit_names and "StrongEdge." + n in check_names
           for names in new_theorems.values() for n in names)
scan = []
for path in lean_files:
    for line, text in enumerate(read(path).splitlines(), 1):
        if re.search(r"\b(sorry|admit|sorryAx|axiom|constant|unsafe|native_decide)\b", text):
            scan.append({"file": path.relative_to(root).as_posix(), "line": line, "text": text})
assert not scan, scan
assert read(root / "lean-toolchain").strip() == "leanprover/lean4:v4.35.0-rc4"
assert "c29b6dda4f7c20e3eeaa717c4e565663c5cfa364" in read(verification / "high21-compiler-version.log")
assert read(verification / "high21-mathlib-commit.txt").strip() == "49fd9dee36e7bbf345fe7981d2de6aeeb591f75b"
save(verification / "high21-source-sha256.json", manifest)
save(verification / "high21-source-checks.json", {
    "lean_file_count": len(lean_files), "new_theorems": new_theorems, "new_definitions": new_defs,
    "new_theorem_count": new_count, "forbidden_token_matches": scan,
    "audit_entry_count": len(entries), "all_new_theorems_checked_and_audited": True,
    "baseline_matches_high22_manifest": True, "changed_preexisting_sources": changed,
    "unchanged_preexisting_sources_and_configs": [n for n in old if n not in changed],
})
save(verification / "high21-audit-checks.json", {
    "audited_theorems": len(entries), "previous_145_entries_preserved": True,
    "all_axioms_standard": True, "allowed_axioms": sorted(allowed),
    "new_audited_theorems": [name for name, _ in entries[145:]],
})


def signature(name):
    start = re.search(r"^StrongEdge\." + re.escape(name) + r"(?:\.\{|\s)", audit, re.M)
    assert start, name
    end = audit.index("\n'StrongEdge." + name + "' depends on axioms:", start.start())
    return audit[start.start():end].strip()


main_names = ["high21_clique_card_le_eighteen", "minimalCliqueBounds20_of_high20",
              "induced_matching_packing20_of_high20"]
signatures = [signature(n) for n in main_names]
assert "MinimalCliqueBounds20" not in signatures[0]
assert "high20 :" in signatures[2]
assert not any(n + " :" in signatures[2] for n in ["high21", "high22", "high23", "high24"])
assert "h21" in signatures[0] and "21 ≤" in signatures[0] and "Q.card ≤ 18" in signatures[0]
assert "h22" not in signatures[0] and "hQdeg" not in signatures[0] and "hR" not in signatures[0]
appendix = []
for rel, names in new_theorems.items():
    appendix.append("### " + rel + "\n\n```lean\n" + "\n\n".join(signature(n) for n in names) + "\n```")
report = f"""# C5 high21: verified handoff

Date: 2026-10-10, Australia/Sydney.

**Complete success: high21 ≤18 is proved and integrated.** In every finite
simple graph with original maximum degree at most four, every clique of original
edges whose degrees in the full conflict graph are at least 21 has at most 18 edges.
No maximality, regularity, girth, support closure or structural record is assumed.

The new packing wrapper retains exactly **high20** as an explicit clique-bound
parameter. Unconditional 20-packing, the 19.5 strengthening, and integer strong-edge
20-colourability remain unproved. The optional high21 ≤17 bound is not exported.

## Exact principal signatures

Copied from the final `#check` output in `verification/high21-axioms.log`:

```lean
{chr(10).join(signatures)}
```

The constructor supplies high21 to the preserved high22 constructor, which already
supplies high22, high23 and high24. Both threshold records and all earlier mathematical
declarations are unchanged. The result applies to every original candidate subset F.

## Proof and departures from the proposed case analysis

1. **Three-loss budget.** The full-conflict incidence bound forces a six-vertex
   endpoint-neighbour cover, original endpoint degrees four, and no triangle on a
   selected high21 edge. The exact incidence identity leaves at most three original
   edges inside this cover. Oriented four-cycle opposites inject into those edges.
   The checked root-load identity then gives a budget of three at each selected root
   label. In a four-edge star, at most six vertices have root type of size at least two.
2. **Threshold-free subcubic bound 18.** The six-vertex cover and selected degrees
   at most three first give |Q|≤19. Equality forces all cover vertices to have selected
   degree three. For a supported vertex x, choose another original neighbour a of x;
   cover saturation gives selected degree three at a. A selected edge a-b with b≠x
   then puts x into a saturated cover. Thus every supported vertex has selected degree
   three, but the handshake sum 2·19=38 is not divisible by three. This proves the
   needed bound without high21 and without the manuscript's stronger subcubic ≤17.
3. **A root type of size at least three.** Two large types must share a root label;
   the three-loss budget excludes a second type of size at least three. At any label
   of the first type, at most one other multiple type can occur. If an outer edge
   avoids the large-type vertex, its two double types cover all four labels. Every
   other multiple-type vertex must therefore equal one of these endpoints or the
   original large-type vertex. There is at most one outer edge avoiding the large
   vertex and at most one incident to it. At most 16 selected edges meet the root
   neighbourhood, giving |Q|≤18. This also covers a type of size four.
4. **Outer edges when all types have size at most two.** Every outer selected edge
   has two double-type endpoints whose types are complementary. Let P be all multiple
   tips, including any outside Q's support. Independence of the root neighbourhood
   and original degree four give at most two original neighbours inside P at each
   vertex of P. All original edges between P vertices remain available as conflict
   witnesses. A generic restricted-cover argument bounds a full-conflict clique in
   this setting by five. Equality would force selected degree two at every supported
   vertex. Partition selected endpoints by membership of one fixed root label;
   each outer selected edge crosses this partition. Summing selected degrees on one
   side makes five even, a contradiction. Hence there are at most four outer edges.
   The original witness edges need not respect the selected bipartition.
5. **At most four fully selected double tips.** A tip is fully selected when both
   original edges joining its two root labels belong to Q. Distinct double types force
   adjacency between their fully selected tips by the clique condition. If all types
   coincide, any common root label has at most three such non-root neighbours. If two
   types differ, every fully selected tip is an original neighbour of at least one of
   these two tips, outside the root neighbourhood. Each has only two such available
   neighbours, so there are at most four fully selected tips. This lemma uses maximum
   degree four and independent root neighbours; it does not need a high21 hypothesis.
6. **Finish the double-type branch.** A selected singleton tip bounds all selected
   root tips by six using the preserved singleton-cover lemma. If there is none, all
   selected tips belong to the at-most-six multiple tips. Selected root-edge incidence
   at a tip is at most one plus the indicator that the tip is fully selected. There
   are thus at most 6+4=10 root edges avoiding the root, in addition to four star edges
   and at most four outer edges. This gives |Q|≤18 directly.

The proof uses neither extraction of an exactly nineteen-edge subclique nor a
classification of paths and cycles. It needs only the cross-edge part of the root
budget; the additional inside-neighbourhood triangle term is unnecessary. All new
lemmas were checked with their actual hypotheses. No graph deletion, finite graph
enumeration, unproved classification, or native computation is used.

The pinned mathematical source is the local preserved snapshot
`verification/high22-research-high_conflict_thresholds.md`, corresponding to
[the threshold manuscript](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_thresholds.md).
The preserved `high22-research-strong_clique_subcubic.md` was also inspected.
An attempted web fetch of the optional improved 20/21 manuscript failed; none of
its uninspected claims is used. The Lean proof certifies the shorter arguments above.

## Reproduction and actual checks

Run from the project directory in PowerShell:

```powershell
.\\lean.ps1 build
.\\lean.ps1 env lean StrongEdge/Audit.lean
python verification/finalize-high21.py
```

The baseline build and audit both exited 0: **1,144 jobs, 145 audited declarations**.
The final build and audit both exited 0: **{jobs:,} jobs, {len(entries)} audited declarations**.
Both final logs contain no errors or warnings. Every new theorem has both a `#check`
and a `#print axioms` entry. All {len(entries)} dependency closures use only
`propext`, `Classical.choice`, and `Quot.sound`; all 145 previous audit entries remain.

The source scan covers **{len(lean_files)} Lean files** and finds no prohibited proof-gap
tokens. The dependency audit is the decisive proof check. Nine new modules contain
**{new_count} theorems** and one definition, `fullDoubleTips`. A supplementary direct
Lake baseline build also passed with 1,144 jobs. Early development logs retain real
failed attempts; final acceptance uses only `high21-build.log` and `high21-axioms.log`.

Pins are unchanged:

- Toolchain: `leanprover/lean4:v4.35.0-rc4`.
- Compiler commit: `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`.
- mathlib commit: `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`.

No dependency update, repository reset, Git commit or public push was performed.

## Preservation and checkpoint

All **26 pre-existing mathematical modules** are byte-for-byte unchanged. The only
modified old Lean files are `StrongEdge.lean` (appended imports) and
`StrongEdge/Audit.lean` (appended checks and audits). All four environment/wrapper
files are unchanged. Every high22 checkpoint file is compared byte-for-byte against
the workspace except the intentionally updated project README, entry point and audit.
Earlier checkpoints, handoffs and verification logs are preserved.

The project README, repository overview, result index and archive verifier now
describe high21. The old archive manifest is preserved in
`verification/high21-baseline-archive-manifest.json`. The supplied task document is
copied unchanged to `../docs/inputs/CODEX_LEAN_C5_HIGH21_NEXT_PROMPT.md`.

Evidence:

- `verification/high21-baseline-build.log`, `high21-baseline-axioms.log`.
- `verification/high21-build.log`, `high21-axioms.log`, and explicit exit-code files.
- `verification/high21-source-sha256.json`, `high21-source.diff`, `high21-change-summary.json`.
- `verification/high21-source-checks.json`, `high21-audit-checks.json`, `high21-status.json`.
- `verification/high21-compiler-version.log`, `high21-mathlib-commit.txt`.
- `../strong_edge_lean_high21_checkpoint.zip`: sources, documentation, pinned configuration
  and verification evidence, excluding binaries, dependency checkouts and caches.

The packaging script verifies archive integrity and byte-for-byte agreement with all
packaged workspace files. The repository-wide verifier is `../scripts/verify_archive.py`;
it checks the updated inventory and historical ZIP hashes, not the mathematics itself.

## Remaining work

| Field | Full conflict degree threshold | Required clique bound | Status |
|---|---:|---:|---|
| high24 | ≥24 | ≤15 | Proved via ≤13 |
| high23 | ≥23 | ≤16 | Proved |
| high22 | ≥22 | ≤17 | Proved |
| high21 | ≥21 | ≤18 | Proved and integrated in this run |
| high20 | ≥20 | ≤19 | Only remaining explicit structural premise |

No unresolved Lean obligation remains in high21 or its integration. The next target
is high20 ≤19. The new threshold-free subcubic ≤18 lemma is available for that work;
the stronger threshold-free subcubic ≤17 has not been claimed. The current packing
result is still conditional on high20.

## Complete new theorem inventory and actual types

{(chr(10) * 2).join(appendix)}
"""
(root / "C5_HIGH21_VERIFIED_HANDOFF.md").write_text(report, encoding="utf-8")

old_archives = [root.parent / n for n in [
    "strong_edge_lean_verified_checkpoint.zip", "strong_edge_lean_c4_checkpoint.zip",
    "strong_edge_lean_high24_checkpoint.zip", "strong_edge_lean_high23_checkpoint.zip",
    "strong_edge_lean_high22_checkpoint.zip",
]]
old_zip_hashes = {p.name: sha(p) for p in old_archives}
previous_inventory = json.loads(read(verification / "high21-baseline-archive-manifest.json"))
assert previous_inventory["verification"]["preserved_checkpoints"] == old_zip_hashes
new_zip = root.parent / "strong_edge_lean_high21_checkpoint.zip"
save(verification / "high21-status.json", {
    "verified_date": "2026-10-10", "timezone": "Australia/Sydney",
    "build_exit_code": 0, "build_jobs": jobs, "axiom_audit_exit_code": 0,
    "audited_theorems": len(entries), "new_theorems": new_count,
    "axioms": sorted(allowed), "high21_clique_bound": 18,
    "minimal_high21_field_discharged": True, "high21_bound_seventeen_exported": False,
    "threshold_free_subcubic_bound": 18, "threshold_free_subcubic_bound_seventeen_proved": False,
    "remaining_minimal_clique_bounds": {"high20": 19}, "unconditional_packing20_proved": False,
    "source_archive": new_zip.name, "preserved_checkpoint_sha256": old_zip_hashes,
})
source_paths = [root / n for n in [
    ".gitignore", "README.md", "LEAN_20_PACKING_HANDOFF.md", "HIGH23_HANDOFF.md", "HIGH22_HANDOFF.md",
    "C5_HIGH21_VERIFIED_HANDOFF.md", "lean-toolchain", "lakefile.toml", "lake-manifest.json", "lean.ps1",
    "StrongEdge.lean",
]] + sorted((root / "StrongEdge").rglob("*.lean"))
with zipfile.ZipFile(old_archives[-1]) as archive:
    previous = {}
    for name in archive.namelist():
        rel = name[len(root.name) + 1:]
        if rel not in {"README.md", "StrongEdge.lean", "StrongEdge/Audit.lean"}:
            assert archive.read(name) == (root / rel).read_bytes(), rel
        if not rel.startswith("verification/"):
            previous[rel] = archive.read(name).decode("utf-8-sig").replace("\r\n", "\n")
changes, diff = [], []
for path in source_paths:
    rel = path.relative_to(root).as_posix()
    before, after = previous.get(rel, ""), read(path)
    if before != after:
        changes.append({"file": rel, "status": "modified" if rel in previous else "added"})
        diff.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
            fromfile="high22/" + rel if rel in previous else "/dev/null", tofile="high21/" + rel))
(verification / "high21-source.diff").write_text("".join(diff), encoding="utf-8")
save(verification / "high21-change-summary.json", changes)
for label, args in [("status", ["git", "status", "--short"]), ("diff-stat", ["git", "diff", "--stat"])]:
    result = subprocess.run(args, cwd=root.parent, check=True, capture_output=True, text=True)
    (verification / f"high21-git-{label}-after.txt").write_text(result.stdout, encoding="utf-8")
paths = source_paths + sorted(p for p in verification.iterdir() if p.is_file())
with zipfile.ZipFile(new_zip, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in paths:
        archive.write(path, root.name + "/" + path.relative_to(root).as_posix())
with zipfile.ZipFile(new_zip) as archive:
    assert archive.testzip() is None
    for path in paths:
        assert archive.read(root.name + "/" + path.relative_to(root).as_posix()) == path.read_bytes()
    assert not any("/.lake/" in n or "/.cache/" in n or n.endswith((".exe", ".dll", ".olean")) for n in archive.namelist())
assert all(sha(root.parent / name) == h for name, h in old_zip_hashes.items())
print(json.dumps({"build_jobs": jobs, "audited_theorems": len(entries), "new_theorems": new_count,
    "old_sources_and_artifacts_preserved": True, "archive": str(new_zip), "archive_files": len(paths),
    "archive_bytes": new_zip.stat().st_size, "archive_sha256": sha(new_zip)}, indent=2))
