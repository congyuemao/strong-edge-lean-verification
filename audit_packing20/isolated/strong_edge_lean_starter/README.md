# Strong-edge packing: Lean formalisation

**Unconditional induced-matching 20-packing is proved.** For every finite simple
graph G of original maximum degree at most four and every candidate edge set F,
there is an induced matching M⊆F with |F|≤20|M|. All conflicts are evaluated in
the whole original graph, retaining edges outside the candidate set as witnesses.

Verified on 10 October 2026 (Australia/Sydney): the full build passed with
**1,170 jobs**, without warnings. All **225 audited declarations** use only
`propext`, `Classical.choice` and `Quot.sound`. The high20 stage adds 33 theorems
in eight modules. All 35 previous mathematical/test modules are unchanged.

See [HIGH20_VERIFIED_HANDOFF.md](HIGH20_VERIFIED_HANDOFF.md) for exact exported
types, the proof, complete new theorem inventory and preservation checks.
Evidence: [build](verification/high20-build.log), [audit](verification/high20-axioms.log),
[source checks](verification/high20-source-checks.json),
[source hashes](verification/high20-source-sha256.json), and
[checkpoint](../strong_edge_lean_high20_checkpoint.zip).

## Checked endpoint

```lean
theorem StrongEdge.induced_matching_packing20
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧
      StrongEdge.IsInducedMatching G (M : Set G.edgeSet) ∧ F.card ≤ 20 * M.card
```

The constructor `minimalCliqueBounds20_of_maxDegree_four` supplies all five
clique bounds from hΔ. There is no additional structural parameter in the final
packing theorem, and empty graphs or candidate sets need no exception.
The older conditional wrappers remain available and unchanged.

| Field | Full conflict degree threshold | Required clique bound | Verified bound |
|---|---:|---:|---:|
| high20 | ≥20 | ≤19 | ≤19 |
| high21 | ≥21 | ≤18 | ≤18 |
| high22 | ≥22 | ≤17 | ≤17 |
| high23 | ≥23 | ≤16 | ≤16 |
| high24 | ≥24 | ≤15 | ≤13 |

C4 separately proves full conflict degree at most 24. The weaker
`MinimalCliqueBounds20` interface suffices; the older `CliqueThresholds20`
record's stronger high24 ≤7 field is not asserted.

## New proof modules

- `Bounds/High20Local`: triangle-cover counting, derived root-neighbourhood
  independence, threshold-free multiple-tip counts and the four-loss label budget.
- `Bounds/High20Four`: handles a root type of size four.
- `Bounds/High20TwoTriples`: handles two distinct types of size at least three.
- `Bounds/High20Outer`: at most four outer edges avoiding a distinguished tip
  when all other types have size at most two.
- `Bounds/High20Slots`: original label slots and missing selected edges.
- `Bounds/High20UniqueTriple`: ten root edges and five outer edges in the unique
  triple case, giving 19 together with the four root-star edges.
- `Bounds/High20`: combines the cases with the previously proved threshold-free
  subcubic bound to export `high20_clique_card_le_nineteen`.
- `High20Packing`: the unconditional threshold constructor and packing theorem.

The definitions in `Basic` and `Conflict`, generic packing and exchange proofs,
and all high21–high24 modules are unchanged. The selected-bipartition and fully
selected double-tip bounds from high21 are reused under their actual hypotheses.
The proof does not require a double-C5 classification or the stronger high20 ≤18.

Earlier module inventories and stage-specific claims remain in
[high21](C5_HIGH21_VERIFIED_HANDOFF.md), [high22](HIGH22_HANDOFF.md),
[high23](HIGH23_HANDOFF.md), [high24](verification/high24-handoff.md), and
[C4](verification/NEXT_STAGE_REPORT.md). Historical conditional descriptions in
those files describe their respective stages.

## Pinned environment

- Lean: `leanprover/lean4:v4.35.0-rc4`.
- Compiler commit: `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`.
- mathlib: `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`.
- Dependency lockfile: `lake-manifest.json`.

The Windows wrapper uses `../.tools/lean-4.35.0-rc4-windows` when available,
otherwise Lake from PATH. The original compiler download has SHA-256
`549c0d70f58346be61d9353b5ff8b3d89430b49184d1833244ba2f3afca3dabd`.
Binaries, dependency checkouts and caches are excluded from the checkpoint.

## Reproduce

From this directory in Windows PowerShell:

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
.\lean.ps1 env lean StrongEdge/Tests.lean
```

With Lean/elan on another system:

```sh
lake exe cache get Mathlib.Combinatorics.SimpleGraph.Clique Mathlib.Combinatorics.SimpleGraph.LineGraph Mathlib.Tactic.ByContra Mathlib.Tactic.Linarith Mathlib.Tactic.Tauto Mathlib.Algebra.Order.BigOperators.Group.Finset
lake build
lake env lean StrongEdge/Audit.lean
lake env lean StrongEdge/Tests.lean
```

Keep the supplied lockfile. The first build may need network access for locked
dependencies. `Tests.lean` checks the four-vertex-path conflict regression using
kernel-checked computation. The final audit preserves all 192 previous entries
and checks all 33 new theorem signatures and dependency closures.

After saving successful logs and exit codes, run
`python verification/finalize-high20.py` to validate the evidence and package a
source-only checkpoint. From the repository root, `python scripts/verify_archive.py`
checks the inventory. These scripts inspect saved evidence and do not replace Lean.

## Scope

This completes the requested high20/C6 packing stage. Integer strong-edge
20-colourability, the 19.5 strengthening, a polynomial-time algorithm proof and
literature originality are separate questions. The optional stronger bounds
high20 ≤18, high21 ≤17, high22 ≤16, high23 ≤15 and threshold-free subcubic ≤17
are not exported. The proved threshold-free subcubic bound is 18.

The supplied brief and pinned research sources are indexed in
[the verified handoff](HIGH20_VERIFIED_HANDOFF.md). Their suggested arguments and
claims are distinguished from the actual Lean statements and proof dependencies.
