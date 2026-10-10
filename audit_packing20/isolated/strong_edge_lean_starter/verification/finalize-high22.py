"""Check saved Lean build/audit evidence and package the high22 checkpoint.

Run after the two Lean verification commands. This is packaging, not a proof.
"""
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


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


build = read(verification / "high22-build.log")
audit = read(verification / "high22-axioms.log")
baseline_build = read(verification / "high22-baseline-build.log")
baseline_audit = read(verification / "high22-baseline-axioms.log")
assert "Build completed successfully (1136 jobs)" in baseline_build
match = re.search(r"Build completed successfully \((\d+) jobs\)", build)
assert match, "No successful final build."
assert not re.search(r"^(?:error|warning):", build, re.M), build
assert not re.search(r"(?:error:|warning:|sorryAx)", audit)
jobs = int(match.group(1))
pattern = r"'([^']+)' depends on axioms: \[([^\]]*)\]"
entries = re.findall(pattern, audit, re.S)
baseline_entries = re.findall(pattern, baseline_audit, re.S)
assert len(baseline_entries) == 94 and entries[:94] == baseline_entries
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert all({a.strip() for a in deps.split(",")} <= allowed for _, deps in entries)

lean_files = [root / "StrongEdge.lean", *sorted((root / "StrongEdge").rglob("*.lean"))]
configs = [root / n for n in ["lean-toolchain", "lakefile.toml", "lake-manifest.json"]]
manifest = {p.relative_to(root).as_posix(): sha(p) for p in lean_files + configs}
old = json.loads(read(verification / "high22-baseline-source-sha256.json"))
changed = [n for n, h in old.items() if manifest[n] != h]
assert changed == ["StrongEdge.lean", "StrongEdge/Audit.lean"], changed
new_theorems = {
    rel: re.findall(r"^(?:@\[[^\]]*\]\s*)?theorem\s+(\w+)", read(root / rel), re.M)
    for rel in manifest if rel.endswith(".lean") and rel not in old
}
new_defs = {
    rel: re.findall(r"^def\s+(\w+)", read(root / rel), re.M)
    for rel in new_theorems
}
new_count = sum(map(len, new_theorems.values()))
assert new_count == 51 and sum(map(len, new_defs.values())) == 4
audit_names = re.findall(r"^#print axioms (\S+)", read(root / "StrongEdge/Audit.lean"), re.M)
assert len(entries) == len(audit_names) == len(set(audit_names)) == 94 + new_count
assert [name for name, _ in entries] == audit_names
assert all("StrongEdge." + n in audit_names for ns in new_theorems.values() for n in ns)
scan = []
for path in lean_files:
    for line, text in enumerate(read(path).splitlines(), 1):
        if re.search(r"\b(sorry|admit|sorryAx|axiom|constant|unsafe|native_decide)\b", text):
            scan.append({"file": path.relative_to(root).as_posix(), "line": line, "text": text})
assert not scan, scan
save(verification / "high22-source-sha256.json", manifest)
save(verification / "high22-source-checks.json", {
    "lean_file_count": len(lean_files), "new_theorems": new_theorems, "new_definitions": new_defs,
    "new_theorem_count": new_count, "forbidden_token_matches": scan,
    "audit_entry_count": len(entries), "all_new_theorems_in_audit": True,
    "changed_preexisting_lean_files": changed,
    "unchanged_preexisting_sources_and_configs": [n for n in old if n not in changed],
})
save(verification / "high22-audit-checks.json", {
    "audited_theorems": len(entries), "previous_94_entries_preserved": True,
    "all_axioms_standard": True, "allowed_axioms": sorted(allowed),
    "new_audited_theorems": [name for name, _ in entries[94:]],
})

blocks = re.split(r"(?=^StrongEdge\.)", audit, flags=re.M)


def signature(name):
    matches = [b for b in blocks if b.startswith("StrongEdge." + name + ".")]
    assert len(matches) == 1, name
    return matches[0].strip()


main_names = ["high22_clique_card_le_seventeen", "minimalCliqueBounds20_of_high20_high21",
              "induced_matching_packing20_of_high20_high21"]
signatures = [signature(n) for n in main_names]
assert "MinimalCliqueBounds20" not in signatures[0]
assert all(n + " :" in signatures[2] for n in ["high20", "high21"])
assert not any(n + " :" in signatures[2] for n in ["high22", "high23", "high24"])
branch_signatures = [signature(n) for n in [
    "high22_root_label_budget_two", "high22_clique_card_le_seventeen_of_root_four",
    "high22_clique_card_le_seventeen_of_support_degree_le_three"]]
inventory = []
for rel, names in new_theorems.items():
    inventory.append("### " + rel + "\n\n" +
                     "\n".join("- `StrongEdge." + n + "`" for n in names))

report = f"""# C5 high22: verified handoff

Date: 2026-10-09, Australia/Sydney.

**Complete success: high22 ≤17 is proved and integrated.** In every finite
simple graph with original maximum degree at most four, every full-conflict
clique whose edges have full conflict degree at least 22 has at most 17 edges.
The theorem assumes no extra girth, regularity, maximality, support closure,
or unproved clique bound. The optional ≤16 strengthening was not exported.

The new packing wrapper retains exactly high20 and high21 as explicit
structural parameters. Unconditional 20-packing remains unfinished.

## Exact exported signatures

Copied from the actual final `#check` output in `verification/high22-axioms.log`:

```lean
{chr(10).join(signatures)}
```

The constructor reuses the preserved high23 constructor, supplies the new
high22 theorem, and thereby retains the previously proved high23 ≤16 and
high24 ≤15 (proved with bound 13). The packing theorem applies to every
candidate set F. All conflicts and induced matchings use the complete original G.

## Proof and its departures from the suggested route

The implementation proves the universal bound directly, without first
extracting an 18-edge subclique or enumerating finite graphs.

1. **Local two-loss budget.** The existing exact incidence identity gives
   conflict degree plus the number of original edges inside the endpoint
   neighbour cover at most 24. At threshold 22, the cover has six vertices,
   endpoints have degree four, the edge lies in no triangle, and at most two
   original edges lie inside the cover. Oriented opposite edges inject into
   those inside edges, proving at most two four-cycles through the selected edge.
2. **Root-label load.** For a selected root label a, the number of four-cycles
   through r-a equals the sum, over all original neighbours x of a other than r,
   of |T_x minus a|. This sum is at most two. Thus at most two multiple-type
   vertices contain a. Distinct multiple-type vertices sharing a have type
   sizes with sum at most four. This uses only the cross-edge part of the
   paper's budget; the additional triangle term is unnecessary for this proof.
3. **Selected tips.** A singleton-type selected edge a-x forces every selected
   tip y whose type omits a to be adjacent to x. All selected tips therefore lie
   in (N(a) minus r) union (N(x) minus a), giving at most six selected tips.
   These sets count vertices; separate proved incidence bounds count edges.
4. **Four-edge root, a triple type exists.** Every multiple-type vertex must
   equal that triple-type vertex: any other type of size at least two meets the
   triple and exceeds a shared label's budget. Every outer selected edge meets
   this one vertex, which has at most one remaining original neighbour.
   At most 16 selected edges meet N(r), and at most one lies outside: |Q|≤17.
5. **Four-edge root, all types have size at most two.** There are at most four
   multiple-type vertices. Every outer edge has both endpoints among them;
   each has at most two outer incidences, so there are at most four outer edges.
   Without a singleton selected edge, the root-neighbourhood edges number at
   most eight. Otherwise the six-tip bound gives at most 6+4=10 such edges,
   hence |Q|≤4+10+4=18. Equality at 18 forces all multiple-type vertices to
   have two outer incidences, saturating their original degree four. A selected
   multiple-type tip must then contain the singleton edge's label, or its
   required adjacency would exceed degree four. At most two such tips contain
   that label, reducing 10 to 6+2=8 and contradicting equality.
6. **Support degree at most three.** If all selected incidence degrees are at
   most two, the preserved general cover theorem gives 13. Otherwise choose a
   root with three selected labels. Call a non-root vertex heavy when its type
   contains at least two of these three labels. Label budgets give at most three
   heavy vertices. Every outer edge meets a heavy vertex; each heavy vertex has
   at most two outer incidences, giving at most six outer edges. At most 12
   selected edges meet N(r), so a clique of size at least 18 forces exactly six
   outer edges, three heavy vertices, and two outer incidences at each.
7. **Exclude that equality case.** Every root label then occurs in exactly two
   heavy types, using all its multiplicity capacity. Every multiple type meets
   a selected root label, so every multiple-type vertex is heavy. Its two outer
   selected incidences leave at most one selected edge meeting N(r), because
   the selected support degree is at most three. All other tips have singleton
   type and also contribute at most one such edge. The six-tip lemma bounds
   these edges by six if a singleton selected edge exists; if none exists,
   all tips are heavy and there are at most three. Either gives |Q|≤15,
   contradicting the assumed |Q|≥18.

The two support-degree branches exhaust all possibilities because selected
incidence degree is at most original degree, hence at most four. No support
closure or induced deletion of original edges is used.

The support-degree-at-most-three theorem in this stage **retains h22**. It is
not the stronger threshold-free subcubic theorem suggested in the brief.
That more general theorem is unnecessary for the present universal high22 bound
and has not been claimed as proved.

Exact budget and branch signatures:

```lean
{chr(10).join(branch_signatures)}
```

The mathematical source was read at the fixed supplied commit:
[high_conflict_thresholds.md](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_thresholds.md).
The optional high22 improvement and general subcubic manuscript were also read.
Their downloaded source snapshots are retained as `verification/high22-research-*.md`.
The shorter counting steps above replace the manuscript's case enumerations;
the Lean proofs, rather than the manuscripts' review claims, certify the result.

## Definitions and individually audited declarations

Four new finite-set definitions use the unchanged original graph:

| Definition | Meaning |
|---|---|
| `rootTips` | Non-root tips of selected edges meeting the root neighbourhood |
| `rootEdges` | Selected edges meeting the root neighbourhood and avoiding the root |
| `multipleTips` | Non-root vertices whose root-neighbourhood type has size at least two |
| `labelHeavyTips` | Non-root vertices whose type contains at least two selected root labels |

The stage adds {new_count} theorems in eight modules. Every theorem is included
individually in the axiom audit:

{(chr(10) * 2).join(inventory)}

## Commands and verified evidence

The baseline and final checks both ran these actual PowerShell commands from
the project directory; all four invocations exited 0:

```powershell
.\\lean.ps1 build
.\\lean.ps1 env lean StrongEdge/Audit.lean
```

Baseline: **1,136 jobs and 94 audited theorems**, recorded in
`verification/high22-baseline-build.log` and `verification/high22-baseline-axioms.log`.
Final: **{jobs:,} jobs and {len(entries)} audited theorems**, recorded in
`verification/high22-build.log` and `verification/high22-axioms.log`.
The final build has no warnings. All 94 previous audit entries are preserved;
all {new_count} new entries depend only on `propext`, `Classical.choice`, and
`Quot.sound`. No proof gaps or custom axioms occur in these dependency closures.

The source scan of all {len(lean_files)} project Lean files found no `sorry`,
`admit`, `sorryAx`, `axiom`, `constant`, `unsafe`, or `native_decide` tokens.
This scan supplements the proof dependency audit. Detailed results are saved
in `verification/high22-source-checks.json` and `verification/high22-audit-checks.json`.

After the Lean commands, this reproducibility command checks the logs, hashes,
audit inventory, forbidden-token scan, old artifacts, source diff, and archive:

```powershell
python verification/finalize-high22.py
```

It completed with exit status 0. The script verifies saved evidence and packages
files; it does not itself prove mathematics. Intermediate development logs may
contain earlier errors or warnings. The final two Lean logs are the acceptance evidence.

## Preservation, differences, and checkpoint

All **18 pre-existing mathematical modules** are byte-for-byte unchanged.
The only modified old Lean files are `StrongEdge.lean` (new public imports) and
`StrongEdge/Audit.lean` (appended audits and signatures). Eight new Lean modules
implement the stage; README and this handoff record the current status.

The three environment files are unchanged. Pins remain:

- Lean `leanprover/lean4:v4.35.0-rc4`
- Compiler commit `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`
- mathlib commit `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`

No dependency update, repository reset, Git commit, or public push was performed.
All earlier checkpoints and verification artifacts are preserved.

Initial hashes: `verification/high22-baseline-source-sha256.json`.
Final source/configuration hashes: `verification/high22-source-sha256.json`.
Real diff against the high23 checkpoint: `verification/high22-source.diff`.
Added/modified file summary: `verification/high22-change-summary.json`.
The project is still untracked in the enclosing Git repository; the saved empty
Git diff-stat is not presented as evidence of unchanged source.

The new archive is `../strong_edge_lean_high22_checkpoint.zip`. It includes source,
locked configuration, documentation, and verification evidence. Compiler binaries,
dependency checkouts, and caches are excluded. Packaging checks ZIP integrity and
byte-for-byte equality with the corresponding workspace files.

## Remaining assumptions and next stage

| Field | Full conflict degree threshold | Required clique bound | Status |
|---|---:|---:|---|
| high20 | ≥20 | ≤19 | Explicit, unproved |
| high21 | ≥21 | ≤18 | Explicit, unproved |
| high22 | ≥22 | ≤17 | Proved and supplied |
| high23 | ≥23 | ≤16 | Previously proved and supplied |
| high24 | ≥24 | ≤15 | Previously proved with bound 13; supplied |

No mathematical gap or unresolved Lean obligation remains in the high22 theorem
or its integration. The next requested bound should be high21 ≤18, followed by
high20 ≤19. The generic root-tip counting lemmas are reusable. The high22
two-loss and heavy-type saturation conclusions must be reworked for high21's
three-loss budget; their hypotheses cannot simply be weakened.
Unconditional 20-packing, the 19.5 strengthening, and integer strong-edge
20-colourability are not established by this checkpoint.
"""
(root / "HIGH22_HANDOFF.md").write_text(report, encoding="utf-8")

old_zip = root.parent / "strong_edge_lean_high23_checkpoint.zip"
new_zip = root.parent / "strong_edge_lean_high22_checkpoint.zip"
old_archives = [root.parent / n for n in [
    "strong_edge_lean_verified_checkpoint.zip", "strong_edge_lean_c4_checkpoint.zip",
    "strong_edge_lean_high24_checkpoint.zip", "strong_edge_lean_high23_checkpoint.zip",
]]
old_zip_hashes = {p.name: sha(p) for p in old_archives}
save(verification / "high22-status.json", {
    "verified_date": "2026-10-09", "timezone": "Australia/Sydney",
    "build_exit_code": 0, "build_jobs": jobs, "axiom_audit_exit_code": 0,
    "audited_theorems": len(entries), "new_theorems": new_count,
    "axioms": sorted(allowed), "high22_clique_bound": 17,
    "high22_bound_sixteen_exported": False, "minimal_high22_field_discharged": True,
    "threshold_free_subcubic_bound_proved": False,
    "remaining_minimal_clique_bounds": {"high20": 19, "high21": 18},
    "unconditional_packing20_proved": False, "source_archive": new_zip.name,
    "preserved_checkpoint_sha256": old_zip_hashes,
})
source_paths = [root / n for n in [
    ".gitignore", "README.md", "LEAN_20_PACKING_HANDOFF.md", "HIGH23_HANDOFF.md", "HIGH22_HANDOFF.md",
    "lean-toolchain", "lakefile.toml", "lake-manifest.json", "lean.ps1", "StrongEdge.lean",
]] + sorted((root / "StrongEdge").rglob("*.lean"))
with zipfile.ZipFile(old_zip) as archive:
    previous = {}
    for name in archive.namelist():
        rel = name[len(root.name) + 1:]
        if rel.startswith("verification/") or rel == "HIGH23_HANDOFF.md":
            assert archive.read(name) == (root / rel).read_bytes(), rel
        if not rel.startswith("verification/"):
            previous[rel] = archive.read(name).decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    for rel in old:
        if rel not in changed:
            assert archive.read(root.name + "/" + rel) == (root / rel).read_bytes(), rel
changes, diff = [], []
for path in source_paths:
    rel = path.relative_to(root).as_posix()
    before, after = previous.get(rel, ""), read(path)
    if before != after:
        changes.append({"file": rel, "status": "modified" if rel in previous else "added"})
        diff.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
            fromfile="high23/" + rel if rel in previous else "/dev/null", tofile="high22/" + rel))
(verification / "high22-source.diff").write_text("".join(diff), encoding="utf-8")
save(verification / "high22-change-summary.json", changes)


def package():
    paths = source_paths + sorted(p for p in verification.iterdir() if p.is_file())
    with zipfile.ZipFile(new_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, root.name + "/" + path.relative_to(root).as_posix())
    return paths


package()
for label, args in [("status", ["git", "status", "--short"]), ("diff-stat", ["git", "diff", "--stat"])]:
    result = subprocess.run(args, cwd=root.parent, check=True, capture_output=True, text=True)
    (verification / f"high22-git-{label}-after.txt").write_text(result.stdout, encoding="utf-8")
paths = package()
with zipfile.ZipFile(new_zip) as archive:
    assert archive.testzip() is None
    for path in paths:
        assert archive.read(root.name + "/" + path.relative_to(root).as_posix()) == path.read_bytes()
    assert not any("/.lake/" in n or "/.cache/" in n or n.endswith((".exe", ".dll", ".olean")) for n in archive.namelist())
assert all(sha(root.parent / name) == h for name, h in old_zip_hashes.items())
print(json.dumps({
    "build_jobs": jobs, "audited_theorems": len(entries), "new_theorems": new_count,
    "source_hashes_and_previous_artifacts_verified": True, "changes": changes,
    "archive": str(new_zip), "archive_files": len(paths),
    "archive_bytes": new_zip.stat().st_size, "archive_sha256": sha(new_zip),
}, indent=2))
