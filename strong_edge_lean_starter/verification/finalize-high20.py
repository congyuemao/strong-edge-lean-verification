"""Validate saved high20 Lean evidence and package sources; this is not a proof."""
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


def write(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")


def save(path, value):
    write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


build = read(verification / "high20-build.log")
audit = read(verification / "high20-axioms.log")
baseline_build = read(verification / "high20-baseline-build.log")
baseline_audit = read(verification / "high20-baseline-axioms.log")
regression = read(verification / "high20-path4-regression.log")
for name in ["build", "audit", "baseline-build", "baseline-audit", "path4-regression"]:
    assert int(read(verification / f"high20-{name}-exit-code.txt")) == 0, name
assert "Build completed successfully (1162 jobs)" in baseline_build
match = re.search(r"Build completed successfully \((\d+) jobs\)", build)
assert match
jobs = int(match.group(1))
for evidence in (build, audit, baseline_build, baseline_audit, regression):
    assert not re.search(r"(?:error:|warning:|sorryAx)", evidence)
pattern = r"'([^']+)' depends on axioms: \[([^\]]*)\]"
entries = re.findall(pattern, audit, re.S)
baseline_entries = re.findall(pattern, baseline_audit, re.S)
assert len(baseline_entries) == 192 and entries[:192] == baseline_entries
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert all({a.strip() for a in deps.split(",") if a.strip()} <= allowed for _, deps in entries)

lean_files = [root / "StrongEdge.lean", *sorted((root / "StrongEdge").rglob("*.lean"))]
configs = [root / n for n in ["lean-toolchain", "lakefile.toml", "lake-manifest.json", "lean.ps1"]]
manifest = {p.relative_to(root).as_posix(): sha(p) for p in lean_files + configs}
old = json.loads(read(verification / "high20-baseline-source-sha256.json"))
assert old == json.loads(read(verification / "high21-source-sha256.json"))
changed = [n for n, h in old.items() if manifest[n] != h]
assert set(changed) == {"StrongEdge.lean", "StrongEdge/Audit.lean"}
new_theorems = {rel: re.findall(r"^theorem\s+(\w+)", read(root / rel), re.M)
                for rel in manifest if rel.endswith(".lean") and rel not in old}
new_count = sum(map(len, new_theorems.values()))
assert len(new_theorems) == 8 and new_count == 33
assert len(lean_files) == 45 and len(manifest) == 49
audit_source = read(root / "StrongEdge/Audit.lean")
audit_names = re.findall(r"^#print axioms (\S+)", audit_source, re.M)
check_names = re.findall(r"^#check (\S+)", audit_source, re.M)
assert len(entries) == len(audit_names) == len(set(audit_names)) == 225
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
assert "c29b6dda4f7c20e3eeaa717c4e565663c5cfa364" in read(verification / "high20-compiler-version.log")
assert read(verification / "high20-mathlib-commit.txt").strip() == "49fd9dee36e7bbf345fe7981d2de6aeeb591f75b"


def signature(name):
    start = re.search(r"^StrongEdge\." + re.escape(name) + r"(?:\.\{|\s)", audit, re.M)
    assert start, name
    end = audit.index("\n'StrongEdge." + name + "' depends on axioms:", start.start())
    return audit[start.start():end].strip()


main_names = ["high20_clique_card_le_nineteen", "minimalCliqueBounds20_of_maxDegree_four",
              "induced_matching_packing20"]
signatures = [signature(n) for n in main_names]
assert "h20 :" in signatures[0] and "20 ≤" in signatures[0] and "Q.card ≤ 19" in signatures[0]
assert not any(n in signatures[0] for n in ["MinimalCliqueBounds20", "CliqueThresholds20", "hN :", "hR :", "hQdeg :"])
assert not any(n in signatures[1] for n in ["high20 :", "h20 :", "hb :", "hN :", "hQ :"])
assert not any(n in signatures[2] for n in ["MinimalCliqueBounds20", "CliqueThresholds20", "high20 :", "h20 :", "hQ :", "hN :"])
assert "F : Finset" in signatures[2] and "F.card ≤ 20 * M.card" in signatures[2]
save(verification / "high20-source-sha256.json", manifest)
save(verification / "high20-source-checks.json", {
    "lean_file_count": len(lean_files), "new_theorems": new_theorems,
    "new_theorem_count": new_count, "new_definitions": [], "forbidden_token_matches": scan,
    "audit_entry_count": len(entries), "all_new_theorems_checked_and_audited": True,
    "baseline_matches_high21_manifest": True, "changed_preexisting_sources": changed,
    "unchanged_preexisting_sources_and_configs": [n for n in old if n not in changed],
    "path4_regression_exit_code": 0,
})
save(verification / "high20-audit-checks.json", {
    "audited_theorems": len(entries), "previous_192_entries_preserved": True,
    "all_axioms_standard": True, "allowed_axioms": sorted(allowed),
    "new_audited_theorems": [name for name, _ in entries[192:]],
    "principal_actual_signatures": dict(zip(main_names, signatures)),
    "packing_has_no_extra_structural_parameter": True,
})

appendix = []
for rel, names in new_theorems.items():
    appendix.append("### " + rel + "\n\n```lean\n" + "\n\n".join(signature(n) for n in names) + "\n```")
report = f"""# C5 high20 and C6: verified handoff

Date: 2026-10-10, Australia/Sydney.

**Complete success: high20 ≤19 and unconditional induced-matching 20-packing
are proved and integrated.** For every finite simple graph G with original
maximum degree at most four and every candidate edge set F, there is an induced
matching M contained in F with |F| ≤ 20|M|. Conflict witnesses include every
original edge of G, including edges outside F and outside selected cliques.

All five fields of `MinimalCliqueBounds20 (conflictGraph G)` now follow from hΔ.
No additional clique bound, regularity, girth, maximality, support closure or
classification is a premise of the final packing theorem. This completes the
requested stage. Integer strong-edge 20-colourability, the 19.5 strengthening,
and algorithmic or originality claims are outside this result.

## Exact principal signatures

Copied from the successful final `#check` output:

```lean
{chr(10).join(signatures)}
```

The final constructor supplies the newly proved high20 theorem to the preserved
high21 constructor. It supplies high21 through high24 using previously verified
proofs. The packing wrapper then calls the preserved arbitrary-candidate packing
theorem. It has no high20 or threshold-record parameter and includes empty F.

## Proof route and departures from the proposed classification

The proof uses a direct threshold argument; it neither extracts exactly twenty
edges nor classifies a double-blown-up five-cycle.

1. **Choose a root.** If every selected vertex degree is at most three, the
   existing threshold-free subcubic bound gives |Q|≤18. Otherwise choose a root r
   with four selected incident edges. Its selected labels are all four original
   neighbours A=N(r). It suffices to treat a hypothetical |Q|≥20.
2. **Derive independence of A at threshold 20.** An original edge a-b within A
   makes the cover of the selected edge r-a have at most five vertices. Full
   conflict degree at least twenty and original degree at most four then force
   this cover to contain no original internal edge. Every non-root type containing
   a is therefore exactly {{a}}, and similarly for b. Any selected outer edge
   would have to cover all four root labels with its endpoint types, which is
   impossible after covering a and b by these singleton types. Thus no selected
   outer edge exists and |Q|≤16. This contradiction establishes independence of A
   for every such high20 clique of size at least seventeen. Triangle exclusion is
   not assumed from the degree-twenty threshold alone.
3. **Four-loss label budget.** The endpoint cover contains at most four internal
   original edges. Independence of A makes the oriented cross-edge map injective,
   giving sum(|T(x)\\{{a}}|)≤4 over all non-root original neighbours of each label a.
   All original neighbours participate, including those outside Q's support.
4. **A type of size four.** The budget forces every other non-root type to have
   size at most two. At a label of the four-element type, at most one other
   multiple-type vertex occurs. An outer edge avoiding the first vertex has
   complementary double types, and its endpoints capture every other multiple
   tip. There is at most one such outer edge; the exported bound of two outer
   edges suffices for |Q|≤18.
5. **Two types of size at least three.** They share at least two root labels.
   At a shared label their two loads use the entire budget of four. Any third
   non-root type containing that label must be a singleton. An outer edge avoiding
   both triple-type vertices would therefore have two singleton endpoints and
   could not cover A. Every outer edge meets one of the two vertices, each of
   which has at most one remaining original degree slot. Hence |Q|≤16+2=18.
6. **Exactly one triple type.** Let x have |T(x)|=3, all other non-root types
   having size at most two. Outer edges avoiding x have complementary double
   endpoints. Among all multiple tips, original internal degree is at most two;
   partition by one fixed root label. The existing selected-bipartition theorem
   bounds this outer clique by four, while at most one outer edge meets x.
   To bound root edges, count selected label incidences and missing selected
   edges from x to A. If at most one of the three x-label edges is selected,
   at least two of the twelve available non-star slots are unused, giving at
   most ten root edges. Otherwise choose o in A\\T(x). Every selected o-y edge
   with y≠r has a type of size at most two containing o. It misses one of x's
   two selected labels. The clique condition forces x-y adjacency. Such y lies
   outside A, and x has at most one neighbour outside A; o therefore has selected
   degree at most two. Again at least two slots are unused and there are at most
   ten root edges. This gives |Q|≤4+10+5=19. This counting branch needs no full
   extremal classification or stronger high20 ≤18 theorem.
7. **All types have size at most two.** The preserved full-double-tip and singleton
   arguments give at most ten root edges and four outer edges, hence |Q|≤18.
   The at-most-six multiple-tip bound is now proved without a threshold, directly
   from the twelve original label slots.

The local definitions, original conflict graph, matching definition and old
mathematical modules are unchanged. No finite graph enumeration, external
certificate, graph deletion or circular use of a high20 wrapper is involved.

## Verified evidence and reproduction

From the project directory:

```powershell
.\\lean.ps1 build
.\\lean.ps1 env lean StrongEdge/Audit.lean
.\\lean.ps1 env lean StrongEdge/Tests.lean
python verification/finalize-high20.py
```

The baseline build and audit passed: 1,162 jobs and 192 audited declarations.
The final full build and audit both exited 0: **{jobs:,} jobs and {len(entries)}
audited declarations**, with no errors or warnings. All 33 new theorems have
both `#check` and `#print axioms` entries; the earlier 192 entries are preserved.
Every audited dependency closure uses only `propext`, `Classical.choice` and
`Quot.sound`. The direct four-vertex-path regression also exited 0, checking
that removing a connecting edge changes conflict while restricting candidates
retains it. A gap-token scan of all 45 Lean files is clean.

Eight new modules contain 33 theorems and no new definitions. Only the public
entry point and audit file changed among old Lean files, both by appending text.
All **35 previous mathematical/test modules** and four pinned environment files
are byte-for-byte unchanged. Every high21 checkpoint member is compared with the
workspace, allowing only the current README, entry point and audit to change.
All six previous checkpoint ZIPs and historical logs remain unchanged.

Pins: Lean `leanprover/lean4:v4.35.0-rc4`, compiler
`c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`, mathlib
`49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`. No dependency update, Git reset,
commit or public push was performed.

The final source manifest contains 49 source/configuration hashes. The source diff
is against the preserved high21 ZIP, so it includes new files even when untracked.
The finalizer checks saved evidence and creates a source-only checkpoint, excluding
compiler binaries, dependency checkouts and caches. It does not replace Lean.
Early development logs retain failed tactic attempts; they are not acceptance logs.

Evidence is in `verification/high20-build.log`, `high20-axioms.log`, their exit-code
files, `high20-path4-regression.log`, `high20-source-sha256.json`,
`high20-source-checks.json`, `high20-audit-checks.json`, `high20-source.diff`,
`high20-change-summary.json`, and `high20-status.json`.
Checkpoint: `../strong_edge_lean_high20_checkpoint.zip`.
Repository inventory: `../docs/ARCHIVE_MANIFEST.json`; verifier:
`../scripts/verify_archive.py`. The baseline inventory is preserved under
`verification/high20-baseline-archive-manifest.json`.

The user brief is preserved unchanged at
`../docs/inputs/CODEX_LEAN_C5_HIGH20_FINAL_PROMPT.md`. The two pinned research
manuscripts were retrieved through GitHub at commit
`3a95c4a9c44475196c42b6eab4749c487d15d59b` and saved as
`verification/high20-research-clique20_rigidity.md` and
`verification/high20-research-high_conflict_20_21_improved.md`.
The [rigidity manuscript](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/clique20_rigidity.md)
and [improved threshold manuscript](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_20_21_improved.md)
provided research context; their assertions were not imported as trusted results.

## Completed threshold interface

| Field | Full conflict degree threshold | Required bound | Verified bound |
|---|---:|---:|---:|
| high20 | ≥20 | ≤19 | ≤19 |
| high21 | ≥21 | ≤18 | ≤18 |
| high22 | ≥22 | ≤17 | ≤17 |
| high23 | ≥23 | ≤16 | ≤16 |
| high24 | ≥24 | ≤15 | ≤13 |

There are no remaining assumptions to discharge for this 20-packing theorem.
The original stronger `CliqueThresholds20` record's high24 ≤7 field is not needed
and is not claimed. No full double-C5 classification or high20 ≤18 is exported.

## Complete new theorem inventory and actual types

{(chr(10) * 2).join(appendix)}
"""
write(root / "HIGH20_VERIFIED_HANDOFF.md", report)

previous_inventory = json.loads(read(verification / "high20-baseline-archive-manifest.json"))
old_zip_hashes = dict(previous_inventory["verification"]["preserved_checkpoints"])
old_zip_hashes["strong_edge_lean_high21_checkpoint.zip"] = previous_inventory["verification"]["latest_checkpoint_sha256"]
assert len(old_zip_hashes) == 6
assert all(sha(root.parent / n) == h for n, h in old_zip_hashes.items())
new_zip = root.parent / "strong_edge_lean_high20_checkpoint.zip"
save(verification / "high20-status.json", {
    "verified_date": "2026-10-10", "timezone": "Australia/Sydney",
    "build_exit_code": 0, "build_jobs": jobs, "axiom_audit_exit_code": 0,
    "audited_theorems": len(entries), "new_theorems": new_count, "axioms": sorted(allowed),
    "high20_clique_bound": 19, "minimal_high20_field_discharged": True,
    "high20_bound_eighteen_exported": False, "remaining_minimal_clique_bounds": {},
    "unconditional_packing20_proved": True, "integer_strong_edge_20_colourability_proved": False,
    "path4_regression_exit_code": 0, "source_archive": new_zip.name,
    "preserved_checkpoint_sha256": old_zip_hashes,
})
source_paths = [root / n for n in [
    ".gitignore", "README.md", "LEAN_20_PACKING_HANDOFF.md", "HIGH23_HANDOFF.md", "HIGH22_HANDOFF.md",
    "C5_HIGH21_VERIFIED_HANDOFF.md", "HIGH20_VERIFIED_HANDOFF.md", "lean-toolchain",
    "lakefile.toml", "lake-manifest.json", "lean.ps1", "StrongEdge.lean",
]] + sorted((root / "StrongEdge").rglob("*.lean"))
with zipfile.ZipFile(root.parent / "strong_edge_lean_high21_checkpoint.zip") as archive:
    previous = {}
    for name in archive.namelist():
        rel = name[len(root.name) + 1:]
        if rel not in {"README.md", "StrongEdge.lean", "StrongEdge/Audit.lean"}:
            assert archive.read(name) == (root / rel).read_bytes(), rel
        if rel in {"StrongEdge.lean", "StrongEdge/Audit.lean"}:
            assert (root / rel).read_bytes().startswith(archive.read(name)), rel
        if not rel.startswith("verification/"):
            previous[rel] = archive.read(name).decode("utf-8-sig").replace("\r\n", "\n")
changes, diff = [], []
for path in source_paths:
    rel = path.relative_to(root).as_posix()
    before, after = previous.get(rel, ""), read(path)
    if before != after:
        changes.append({"file": rel, "status": "modified" if rel in previous else "added"})
        diff.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
            fromfile="high21/" + rel if rel in previous else "/dev/null", tofile="high20/" + rel))
write(verification / "high20-source.diff", "".join(diff))
save(verification / "high20-change-summary.json", changes)
for label, args in [("status", ["git", "status", "--short"]), ("diff-stat", ["git", "diff", "--stat"])]:
    result = subprocess.run(args, cwd=root.parent, check=True, capture_output=True, text=True)
    write(verification / f"high20-git-{label}-after.txt", result.stdout)
paths = source_paths + sorted(p for p in verification.iterdir() if p.is_file())
with zipfile.ZipFile(new_zip, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in paths:
        archive.write(path, root.name + "/" + path.relative_to(root).as_posix())
with zipfile.ZipFile(new_zip) as archive:
    assert archive.testzip() is None
    for path in paths:
        assert archive.read(root.name + "/" + path.relative_to(root).as_posix()) == path.read_bytes()
    assert not any("/.lake/" in n or "/.cache/" in n or n.endswith((".exe", ".dll", ".olean", ".ilean", ".pyc"))
                   for n in archive.namelist())
print(json.dumps({"status": "verified", "build_jobs": jobs, "audited_theorems": len(entries),
                  "new_theorems": new_count, "lean_files": len(lean_files), "hashes": len(manifest),
                  "checkpoint_files": len(paths), "checkpoint_sha256": sha(new_zip)}, indent=2))
