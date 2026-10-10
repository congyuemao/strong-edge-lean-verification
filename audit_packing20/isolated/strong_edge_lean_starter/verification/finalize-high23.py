"""Validate saved Lean evidence and package the high23 source checkpoint.

Run only after lean.ps1 build and the explicit Audit.lean invocation finish.
This script checks evidence and packages files; it does not prove mathematics.
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


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


build = read(verification / "high23-build.log")
audit = read(verification / "high23-axioms.log")
baseline_audit = read(verification / "high23-baseline-axioms.log")
match = re.search(r"Build completed successfully \((\d+) jobs\)", build)
assert match, "The final build has not completed successfully."
assert not re.search(r"^(?:error|warning):", build, re.M), build
jobs = int(match.group(1))
pattern = r"'([^']+)' depends on axioms: \[([^\]]*)\]"
entries = re.findall(pattern, audit, re.S)
previous_entries = re.findall(pattern, baseline_audit, re.S)
assert len(previous_entries) == 51
assert entries[:51] == previous_entries
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert all({a.strip() for a in deps.split(",")} <= allowed for _, deps in entries)

lean_files = [root / "StrongEdge.lean", *sorted((root / "StrongEdge").rglob("*.lean"))]
configs = [root / n for n in ["lean-toolchain", "lakefile.toml", "lake-manifest.json"]]
manifest = {p.relative_to(root).as_posix(): sha(p) for p in lean_files + configs}
old = json.loads(read(verification / "high23-baseline-source-sha256.json"))
changed = [n for n, h in old.items() if manifest[n] != h]
assert changed == ["StrongEdge.lean", "StrongEdge/Audit.lean"], changed
new_theorems = {
    rel: re.findall(r"^(?:@\[[^\]]*\]\s*)?theorem\s+(\w+)", read(root / rel), re.M)
    for rel in manifest if rel.endswith(".lean") and rel not in old
}
new_count = sum(map(len, new_theorems.values()))
audit_names = re.findall(r"^#print axioms (\S+)", read(root / "StrongEdge/Audit.lean"), re.M)
assert len(entries) == len(audit_names) == len(set(audit_names)) == 51 + new_count
assert [name for name, _ in entries] == audit_names
assert all("StrongEdge." + n in audit_names for names in new_theorems.values() for n in names)
scan = []
for path in lean_files:
    for line, text in enumerate(read(path).splitlines(), 1):
        if re.search(r"\b(sorry|admit|axiom|constant|unsafe|native_decide)\b", text):
            scan.append({"file": path.relative_to(root).as_posix(), "line": line, "text": text})
assert not scan, scan
save_json(verification / "high23-source-sha256.json", manifest)
save_json(verification / "high23-source-checks.json", {
    "lean_file_count": len(lean_files), "new_theorems": new_theorems,
    "new_theorem_count": new_count, "forbidden_token_matches": scan,
    "audit_entry_count": len(entries), "all_new_theorems_in_audit": True,
    "changed_preexisting_lean_files": changed,
    "unchanged_preexisting_sources_and_configs": [n for n in old if n not in changed],
})
save_json(verification / "high23-audit-checks.json", {
    "audited_theorems": len(entries), "previous_51_entries_preserved": True,
    "all_axioms_standard": True, "allowed_axioms": sorted(allowed),
    "new_audited_theorems": [name for name, _ in entries[51:]],
})

signature_blocks = re.split(r"(?=^StrongEdge\.)", audit, flags=re.M)
signature_names = [
    "high23_clique_card_le_sixteen",
    "minimalCliqueBounds20_of_high20_high21_high22",
    "induced_matching_packing20_of_high20_high21_high22",
]
signatures = []
for name in signature_names:
    blocks = [b for b in signature_blocks if b.startswith("StrongEdge." + name + ".")]
    assert len(blocks) == 1, name
    signatures.append(blocks[0].strip())
assert "MinimalCliqueBounds20" not in signatures[0]
assert "high23 :" not in signatures[2] and "high24 :" not in signatures[2]
assert all(n + " :" in signatures[2] for n in ["high20", "high21", "high22"])

inventory = []
for rel, names in new_theorems.items():
    inventory.append("### " + rel + "\n\n" + "\n".join("- `StrongEdge." + n + "`" for n in names))
report = f"""# C5 high23: verified handoff

Date: 2026-10-09, Australia/Sydney.

**High23 ≤16 is complete and integrated.** For every finite simple graph of
original maximum degree at most four, every full-conflict clique whose edges
all have full conflict degree at least 23 has at most 16 edges. No other clique
bound or extra graph-structure hypothesis is assumed in that theorem.
The optional ≤15 strengthening was not exported. Unconditional 20-packing
remains unfinished: high20, high21, and high22 are still explicit assumptions.

## Exact exported signatures

The following are copied from the actual final `#check` output in
`verification/high23-axioms.log`:

```lean
{chr(10).join(signatures)}
```

The new constructor fills `MinimalCliqueBounds20.high23` using
`high23_clique_card_le_sixteen` and fills high24 using the preserved
`high24_clique_card_le_fifteen`. The existing records, old wrappers, and conflict
definitions are unchanged. The new wrapper still works for every candidate
edge set F, retaining all original graph edges as possible conflict witnesses.

## Proof structure

1. **Exact incidence counting.** `edgeIncidences`, `edgesMeeting`, and
   `edgesInside` count selected edges at a vertex, meeting a vertex set, or
   entirely inside it. The proved identity says the incidence sum equals the
   meeting-edge count plus the inside-edge count. Each internal original edge
   accounts for exactly one duplicate. Applied to the existing six-neighbour
   cover, conflict degree at least 23 permits at most one inside edge.
2. **Local restrictions.** A high23 edge has degree-four endpoints and lies in
   no triangle. `fourCycleOpposites G u v` represents a four-cycle through the
   oriented edge u-v by an ordered opposite edge (x,y), where x is an other
   neighbour of u and y an other neighbour of v. Its cardinality is at most one.
   Distinct such pairs cannot represent the same unordered edge, because the
   two other-neighbour sets are disjoint. These are local conclusions, not
   assumptions that the whole graph has large girth.
3. **Root types.** `rootLabels` records neighbours joined to a root by a Q edge;
   its cardinality equals the selected incidence degree. `rootType` records all
   original neighbours of a vertex within the root neighbourhood. With at least
   three root Q labels, the root neighbourhood is independent and non-root types
   have size at most two. Two types of size at least two sharing a root Q label
   must belong to the same vertex, by the unique four-cycle budget.
4. **Outer edges.** Every Q edge outside the root's closed neighbourhood has
   endpoint types covering all root Q labels. With at least three labels, some
   endpoint covers two of them. Every outer Q edge must be incident to that
   vertex; otherwise its two endpoint types become two singletons and cannot
   cover three labels. The common vertex has two original neighbours among the
   root labels, so original degree four leaves at most two outer Q edges.
5. **Support degree at most two.** Any chosen Q edge covers all other Q edges
   by at most six vertices, each incident to at most two Q edges: |Q|≤1+6·2=13.
6. **Support degree at most three.** If a root has three Q edges, all Q edges
   meeting its four-neighbour set number at most 4·3=12 by selected incidence
   counting. At most two outer edges remain, so |Q|≤14.
7. **A four-edge root star.** Singleton-type Q edges number at most six: fixing
   one such edge, the other singleton tips lie in two original neighbour sets
   of size at most three. Multiple-type Q edges inject into the four root
   labels by type uniqueness, so there are at most four. Including the four
   root edges gives at most 14 edges meeting the neighbourhood; the uniform
   outer-edge bound gives |Q|≤14+2=16.

The final theorem splits on the maximum selected incidence degree. No original
graph is replaced by a graph obtained by deleting non-Q edges. The counting
uses covers and inequalities, so it needs no unproved disjoint partition.

The mathematical route adapts
[high_conflict_23_improved.md at the supplied commit](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_23_improved.md).
The implementation keeps the simpler uniform outer-edge bound two, obtaining
the required 16 without formalising the paper's additional one-edge bound for
the four-star case. The older defect-counting proof was read as a cross-check.

## Verified declarations

The ten new finite-set definitions are:

| Definition | Meaning |
|---|---|
| `edgeIncidences` | Selected edges incident to a vertex |
| `edgesMeeting` | Selected edges meeting a vertex set |
| `edgesInside` | Selected edges with both endpoints in a vertex set |
| `fourCycleOpposites` | Ordered opposite edges of four-cycles through an oriented edge |
| `rootLabels` | Neighbours joined to the root by selected edges |
| `rootType` | A vertex's original neighbours within the root neighbourhood |
| `outerEdges` | Selected edges outside the root's closed neighbourhood |
| `singleTips` | Tips of selected root-neighbourhood edges with singleton type |
| `singleRootEdges` | Selected root-neighbourhood edges with singleton-type non-root tip |
| `doubleRootEdges` | Selected root-neighbourhood edges with non-root tip of type size at least two |

This stage adds {new_count} theorems, each individually included in the axiom
audit. Their finite and decidability instances are visible in the source.
Only the final universal theorem and its wrappers constitute the delivered
bound; helper lemmas state their local premises explicitly.

{(chr(10) * 2).join(inventory)}

## Checks and preservation

From the project directory, both baseline commands exited 0:

```powershell
.\\lean.ps1 build
.\\lean.ps1 env lean StrongEdge/Audit.lean
```

The baseline had 1,129 build jobs and 51 audited theorems. Logs:
`verification/high23-baseline-build.log` and
`verification/high23-baseline-axioms.log`.

The same two final commands exited 0. The final build completed **{jobs} jobs**
without warnings; the final audit checked **{len(entries)} theorems**, preserving
all previous 51 entries and adding all {new_count} new ones. Evidence:
`verification/high23-build.log` and `verification/high23-axioms.log`.
Every audited dependency list contains only `propext`, `Classical.choice`, and
`Quot.sound`. No proof gaps or custom mathematical axioms occur in those closures.

The source scan of all {len(lean_files)} project Lean files found no `sorry`,
`admit`, `axiom`, `constant`, `unsafe`, or `native_decide` tokens. Results are in
`verification/high23-source-checks.json` and `verification/high23-audit-checks.json`.
Run `python verification/finalize-high23.py` after the two Lean commands to
recheck the saved evidence and regenerate this handoff and source checkpoint.
The script checks evidence; it is not a mathematical proof certificate itself.
The packaging and evidence check completed with exit status 0.

The final source/configuration hashes are in
`verification/high23-source-sha256.json`; the initial snapshot is
`verification/high23-baseline-source-sha256.json`. All eleven earlier
mathematical modules and all three configuration/lock files are byte-for-byte
unchanged. Among old Lean files, only `StrongEdge.lean` and `StrongEdge/Audit.lean`
changed. Seven new Lean modules were added; README and this handoff document the
new status. Dependency pins remain Lean `leanprover/lean4:v4.35.0-rc4`, compiler
commit `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`, and mathlib commit
`49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`. No `lake update` was run.

The `high23-git-*-before.txt` and `high23-git-*-after.txt` snapshots record Git
state. The project remains untracked, so Git's diff-stat is empty. The real
source/documentation comparison against the high24 checkpoint is
`verification/high23-source.diff`, with a file summary in
`verification/high23-change-summary.json`. Earlier logs, handoffs, manifests,
and checkpoint ZIPs are preserved. Intermediate development logs can describe
earlier errors or linter warnings; the two final logs are the acceptance evidence.

The new archive is `../strong_edge_lean_high23_checkpoint.zip`. It contains
source, documentation, configuration, and verification evidence, and excludes
compiler binaries, dependency checkouts, and caches. ZIP integrity and byte
equality with the delivered workspace files are checked when packaging.

## Remaining assumptions and next step

| Field | Full conflict degree of every clique member | Required clique bound | Status |
|---|---:|---:|---|
| high20 | ≥20 | ≤19 | Explicit, unproved |
| high21 | ≥21 | ≤18 | Explicit, unproved |
| high22 | ≥22 | ≤17 | Explicit, unproved |
| high23 | ≥23 | ≤16 | Proved and supplied |
| high24 | ≥24 | ≤15 | Previously proved with bound 13; supplied |

No counterexample or unresolved mathematical gap remains in this stage's
high23 proof or interface integration. The other three structural bounds remain
unformalised; no claim about their correctness follows from this checkpoint.
Next prove high22 ≤17, then high21 ≤18 and high20 ≤19. Degree 22 allows two
counting losses, so the high23 one-four-cycle budget cannot simply be weakened.
The exact incidence identity can be reused to begin a two-loss analysis.
Unconditional 20-packing, the 19.5 strengthening, and integer strong-edge
20-colourability are not established here.
"""
(root / "HIGH23_HANDOFF.md").write_text(report, encoding="utf-8")

old_zip = root.parent / "strong_edge_lean_high24_checkpoint.zip"
new_zip = root.parent / "strong_edge_lean_high23_checkpoint.zip"
old_archives = [root.parent / n for n in [
    "strong_edge_lean_verified_checkpoint.zip", "strong_edge_lean_c4_checkpoint.zip",
    "strong_edge_lean_high24_checkpoint.zip",
]]
old_zip_hashes = {p.name: sha(p) for p in old_archives}
save_json(verification / "high23-status.json", {
    "verified_date": "2026-10-09", "timezone": "Australia/Sydney",
    "build_exit_code": 0, "build_jobs": jobs, "axiom_audit_exit_code": 0,
    "audited_theorems": len(entries), "new_theorems": new_count,
    "axioms": sorted(allowed), "high23_clique_bound": 16,
    "high23_bound_fifteen_exported": False, "minimal_high23_field_discharged": True,
    "remaining_minimal_clique_bounds": {"high20": 19, "high21": 18, "high22": 17},
    "unconditional_packing20_proved": False, "source_archive": new_zip.name,
    "preserved_checkpoint_sha256": old_zip_hashes,
})
source_paths = [root / n for n in [
    ".gitignore", "README.md", "LEAN_20_PACKING_HANDOFF.md", "HIGH23_HANDOFF.md",
    "lean-toolchain", "lakefile.toml", "lake-manifest.json", "lean.ps1", "StrongEdge.lean",
]] + sorted((root / "StrongEdge").rglob("*.lean"))
with zipfile.ZipFile(old_zip) as archive:
    previous = {}
    for name in archive.namelist():
        rel = name[len(root.name) + 1:]
        if rel.startswith("verification/"):
            assert archive.read(name) == (root / rel).read_bytes(), rel
        else:
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
        diff.extend(difflib.unified_diff(
            before.splitlines(keepends=True), after.splitlines(keepends=True),
            fromfile="high24/" + rel if rel in previous else "/dev/null", tofile="high23/" + rel))
(verification / "high23-source.diff").write_text("".join(diff), encoding="utf-8")
save_json(verification / "high23-change-summary.json", changes)


def package():
    paths = source_paths + sorted(p for p in verification.iterdir() if p.is_file())
    with zipfile.ZipFile(new_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, root.name + "/" + path.relative_to(root).as_posix())
    return paths


package()
for label, args in [("status", ["git", "status", "--short"]), ("diff-stat", ["git", "diff", "--stat"])]:
    result = subprocess.run(args, cwd=root.parent, check=True, capture_output=True, text=True)
    (verification / f"high23-git-{label}-after.txt").write_text(result.stdout, encoding="utf-8")
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
