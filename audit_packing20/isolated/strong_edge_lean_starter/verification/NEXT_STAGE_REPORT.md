# Next-stage Lean verification report

Date: 2026-10-09, Australia/Sydney.

C4 is complete. C5 now has verified local equality structure, but none of its
five universal clique-size bounds is yet discharged. The unconditional
20-packing theorem (C6) is not proved. This stage adds 25 proved theorems in
three modules and preserves all six earlier mathematical core files byte for
byte. No definitions of conflict or induced matching were changed.

## Status and evidence

| Status | Claim | Evidence |
|---|---|---|
| Kernel verified | Every original edge has full conflict degree at most 24 when every original vertex has degree at most four. | `StrongEdge/Bounds/ConflictDegree.lean`; `next-stage-degree-build.log`; final build and audit below. |
| Kernel verified | Equality at 24 forces both endpoints and their six other neighbours to have degree four, disjoint endpoint neighbourhoods, independence of those six neighbours, no triangle at either endpoint, and no four-cycle through the fixed edge. | `StrongEdge/Bounds/ConflictRigidity.lean`; `next-stage-rigidity-build.log`; final build and audit. |
| Explicitly conditional | The new, separate `MinimalCliqueBounds20` interface suffices for 20-packing of every candidate subset. Its original-edge wrapper derives the maximum conflict degree from C4, but still takes all five clique bounds as an explicit parameter. | `StrongEdge/MinimalPacking.lean`; `next-stage-minimal-build.log`; warning-free final build and audit. |
| Unfinished | Universal high20/high21/high22/high23/high24 clique bounds; unconditional 20-packing; later 19.5 strengthening. | No theorem claiming any of these has been added. |
| Counterexamples found | None found in this stage. This is not a claim that the remaining research arguments have been verified. | No exhaustive search or external certificate was used. The old P4 regression remains compiled and audited. |

All file paths in this report are relative to the project directory unless they
name a verification artifact, in which case they are relative to `verification/`.

## Main new theorem and proof

The actual exported signature, also printed in `next-stage-axioms.log`, is:

```lean
StrongEdge.conflict_degree_le_24
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (e : G.edgeSet) :
    (StrongEdge.conflictGraph G).degree e ≤ 24
```

For `e = {u,v}`, put `S = (N(u) \ {v}) ∪ (N(v) \ {u})`. Every edge
conflicting with `e` meets `S`, including immediately incident edges. There are
at most six vertices in `S`, and each has at most four incident edges. Thus
the union of their incidence sets has at most 24 edges. This counts conflicts
in the complete original graph, including connecting witnesses outside any
candidate set. Triangles, four-cycles, shared neighbours, and repeated coverage
need no extra hypotheses.

When the bound is attained, both cardinality inequalities must be equalities.
An edge joining two members of `S` would be counted twice in the incidence sum,
contradicting equality. This proves independence of `S`; the other local
structure conclusions follow from this and equality in the neighbour counts.

## Every new top-level theorem

All names below are in namespace `StrongEdge`; every one is listed explicitly
in `StrongEdge/Audit.lean`. Finite and decidability instances are as in the
source signatures. Here `e = {u,v}` means the explicit parameter
`he : e.val = s(u,v)`; all degrees of edges mean **full** conflict degrees.

### `StrongEdge/Bounds/ConflictDegree.lean` — 11 theorems

The first nine do not assume a bound on original degrees.

| Exact name | Additional assumptions and conclusion |
|---|---|
| `endpointNeighbourCover_comm` | Swapping `u,v` preserves the cover. |
| `incident_edge_meets_cover` | An original edge through `u`, distinct from `{u,v}`, meets the cover. |
| `lineGraph_adj_meets_cover` | `e={u,v}` and line-graph adjacency imply that the other edge meets the cover. |
| `left_notMem_endpointNeighbourCover` | `u` is outside the cover. |
| `right_notMem_endpointNeighbourCover` | `v` is outside the cover. |
| `strongConflict_meets_cover` | `e={u,v}` and strong conflict imply that the other edge meets the cover. |
| `conflict_neighbors_subset_incidence_cover` | `e={u,v}`; embeds all conflict neighbours into the incidence union. |
| `conflict_degree_le_incidence_cover_card` | `e={u,v}`; conflict degree is bounded by the incidence union's cardinality. |
| `conflict_degree_le_incidence_sum` | `e={u,v}`; conflict degree is bounded by the sum of original degrees over the cover. |
| `endpointNeighbourCover_card_le_six` | `G.Adj u v` and `∀x, G.degree x ≤4`; cover size is at most six. |
| `conflict_degree_le_24` | Only `∀x, G.degree x ≤4` and an arbitrary original edge; full conflict degree is at most 24. |

Also added the definition `endpointNeighbourCover`. Evidence for every row:
`next-stage-degree-build.log`, `next-stage-build.log`, `next-stage-axioms.log`.

### `StrongEdge/Bounds/ConflictRigidity.lean` — 8 theorems

Every theorem assumes `∀x, G.degree x ≤4`, `e={u,v}`, and full conflict degree
of `e` equal to 24. No clique-size bounds are assumed.

| Exact name | Conclusion / extra argument |
|---|---|
| `endpointNeighbourCover_card_eq_six_of_degree_eq_24` | Cover size is six. |
| `endpoint_degrees_eq_four_of_degree_eq_24` | Both endpoints have original degree four. |
| `cover_degree_eq_four_of_degree_eq_24` | A specified member of the cover has original degree four. |
| `cover_independent_of_degree_eq_24` | The cover is independent in the original graph. |
| `other_neighbor_sets_disjoint_of_degree_eq_24` | The two sets of other neighbours are disjoint. |
| `endpoint_neighbor_sets_disjoint_of_degree_eq_24` | The full neighbour sets of the endpoints are disjoint. |
| `endpoint_neighborhood_independent_of_degree_eq_24` | `N(u)` is independent; swapping endpoints gives the same result for `N(v)`. |
| `no_cross_edge_of_degree_eq_24` | For specified `x∈N(u)\{v}` and `y∈N(v)\{u}`, `¬G.Adj x y`. |

Evidence for every row: `next-stage-rigidity-build.log`, `next-stage-build.log`,
`next-stage-axioms.log`. These are local consequences of equality, not global
girth assumptions.

### `StrongEdge/MinimalPacking.lean` — 6 theorems

| Exact name | Explicit assumptions and conclusion |
|---|---|
| `minimalCliqueBounds20_of_thresholds` | The original `CliqueThresholds20 H` implies the new interface. |
| `local20_of_minimal_clique_bounds` | Maximum degree 24, the new interface, an optimal independent set `M`, and `v∈M` imply `degree v + 1 + privateCard v ≤40`. |
| `packing20_of_minimal_clique_bounds` | Maximum degree 24 and the new interface imply the whole-graph 20-packing bound. |
| `minimalCliqueBounds20_induce` | The new interface is inherited by an induced subgraph. |
| `subset_packing20_of_minimal_clique_bounds` | Maximum degree 24 and the new interface imply 20-packing for every finite candidate subset. |
| `induced_matching_packing20_of_minimal_clique_bounds` | Original maximum degree four and `MinimalCliqueBounds20 (conflictGraph G)` imply the original-edge induced-matching bound for every `F`. |

Also added the proposition structure `MinimalCliqueBounds20`. Evidence for
every row: `next-stage-minimal-build.log`, `next-stage-build.log`, and
`next-stage-axioms.log`. The module-only log contains an unused-instance linter
warning subsequently fixed with `omit [DecidableEq W]`; the final build has no
warnings. The new wrapper has this mathematical conclusion:

```lean
(hΔ : ∀ x, G.degree x ≤ 4)
(hb : MinimalCliqueBounds20 (conflictGraph G)) (F : Finset G.edgeSet) :
  ∃ M : Finset G.edgeSet, M ⊆ F ∧
    IsInducedMatching G (M : Set G.edgeSet) ∧ F.card ≤ 20 * M.card
```

## Exactly what remains assumed

For every finite clique `Q` of the full conflict graph:

| Field of `MinimalCliqueBounds20` | Premise for all members of `Q` | Required conclusion |
|---|---|---|
| `high20` | Full conflict degree ≥20 | `Q.card ≤19` |
| `high21` | Full conflict degree ≥21 | `Q.card ≤18` |
| `high22` | Full conflict degree ≥22 | `Q.card ≤17` |
| `high23` | Full conflict degree ≥23 | `Q.card ≤16` |
| `high24` | Full conflict degree ≥24 | `Q.card ≤15` |

None of these five fields is supplied by this stage. In the original
`CliqueThresholds20`, the maximum-degree field is now provable by C4, the first
four clique fields are identical, and `high24` requires the stronger bound 7.
That original definition and its conditional theorems are unchanged. The new
interface is inherited using degrees in the induced conflict graph bounded by
degrees in the full conflict graph, preserving the distinction between them.

## Checks actually run

From `C:\Users\21161\Documents\ChatGPT\math\strong_edge_lean_starter`:

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

Both commands exited successfully before edits (1,124 build jobs, 13 audited
theorems), saved in `next-stage-baseline-build.log` and
`next-stage-baseline-axioms.log`. Both exited successfully after edits (1,127
jobs, 38 audited theorems), saved in `next-stage-build.log` and
`next-stage-axioms.log`. Intermediate module builds used:

```powershell
.\lean.ps1 build StrongEdge.Bounds.ConflictDegree
.\lean.ps1 build StrongEdge.Bounds.ConflictRigidity
.\lean.ps1 build StrongEdge.MinimalPacking
```

Every audited theorem reports only `propext`, `Classical.choice`, and
`Quot.sound`. The audit includes all 25 new theorems and the 13 original audit
entries. A scan of all 11 project Lean files found no `sorry`, `admit`, `axiom`,
`constant`, `unsafe`, or `native_decide` tokens. Audit coverage and scan results
are recorded in `next-stage-source-checks.json`.

The pinned Lean version, compiler commit, and mathlib commit are unchanged:
`leanprover/lean4:v4.35.0-rc4`,
`c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`, and
`49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`. No `lake update` was run.

`next-stage-source-sha256.json` contains SHA-256 hashes of all 11 Lean files and
the three configuration/lock files. Comparison with the preserved original
manifest confirms that the six prior core files, `lean-toolchain`,
`lakefile.toml`, and `lake-manifest.json` are byte-for-byte unchanged. Only
`StrongEdge.lean` and `StrongEdge/Audit.lean` changed among previously hashed
files; three new proof modules were added.

Git status and diff-stat snapshots are saved with `next-stage-git-...` names.
The project is still untracked in the enclosing Git repository, so `git diff
--stat` is empty; it cannot describe the source changes. A separate
`next-stage-source.diff` compares source/configuration/documentation against
the preserved previous checkpoint ZIP. No existing changes were discarded,
and no commit was made. The new `strong_edge_lean_c4_checkpoint.zip` beside the
project contains source and verification evidence, excluding compilers,
dependency trees, and caches; the earlier ZIP is preserved.

## Shortest next path and mathematical risk

The following are proposed next lemmas, not existing Lean declarations:

1. Fix a degree-24 edge `uv` in an all-degree-24 conflict clique `Q`. For each
   side `A=N(u)\{v}`, prove that at most three edges of `Q` avoid `u,v` and meet
   `A`. Use the verified absence of triangles and four-cycles for **each**
   edge of `Q`, plus the conflict endpoint cases. Apply the same lemma to
   `B=N(v)\{u}`.
2. Combine those two side bounds with `uv` and at most six other edges incident
   to `u,v`. The resulting bound `1+6+3+3=13` would suffice for `high24 ≤15`.
   C4 turns the hypothesis of degree at least 24 into equality at 24. This
   would discharge one clique field while retaining the other four explicitly.

This follows the local structure and branch-counting route in the fixed
[research source, critical_support.md](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/critical_support.md).
Only the local equality structure has been formalised here. The side-counting
argument, the other high-conflict bounds, and the 20-clique rigidity still need
Lean proofs. No concrete mathematical flaw or counterexample was identified;
their current status is unfinished formalisation, not verified mathematics or
an established failure of the paper. No external computation is treated as a
universal proof. Nothing in this stage establishes integer strong-edge
20-colourability.
