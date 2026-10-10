# C5 high20 and C6: verified handoff

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
StrongEdge.high20_clique_card_le_nineteen.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 19
StrongEdge.minimalCliqueBounds20_of_maxDegree_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) :
  StrongEdge.MinimalCliqueBounds20 (StrongEdge.conflictGraph G)
StrongEdge.induced_matching_packing20.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (F : Finset ↑G.edgeSet) : ∃ M ⊆ F, StrongEdge.IsInducedMatching G ↑M ∧ F.card ≤ 20 * M.card
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
   a is therefore exactly {a}, and similarly for b. Any selected outer edge
   would have to cover all four root labels with its endpoint types, which is
   impossible after covering a and b by these singleton types. Thus no selected
   outer edge exists and |Q|≤16. This contradiction establishes independence of A
   for every such high20 clique of size at least seventeen. Triangle exclusion is
   not assumed from the degree-twenty threshold alone.
3. **Four-loss label budget.** The endpoint cover contains at most four internal
   original edges. Independence of A makes the oriented cross-edge map injective,
   giving sum(|T(x)\{a}|)≤4 over all non-root original neighbours of each label a.
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
   most ten root edges. Otherwise choose o in A\T(x). Every selected o-y edge
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
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
.\lean.ps1 env lean StrongEdge/Tests.lean
python verification/finalize-high20.py
```

The baseline build and audit passed: 1,162 jobs and 192 audited declarations.
The final full build and audit both exited 0: **1,170 jobs and 225
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

### StrongEdge/Bounds/High20.lean

```lean
StrongEdge.clique_card_le_eighteen_of_independent_root_types_le_two.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4)
  (hN : G.IsIndepSet (G.neighborSet r)) (ht : ∀ (x : V), x ≠ r → (StrongEdge.rootType G r x).card ≤ 2) : Q.card ≤ 18

StrongEdge.high20_clique_card_le_nineteen_of_root_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4) :
  Q.card ≤ 19

StrongEdge.high20_clique_card_le_nineteen.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 19
```

### StrongEdge/Bounds/High20Four.lean

```lean
StrongEdge.high20_other_type_le_two_of_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r : V}
  (hN : G.IsIndepSet (G.neighborSet r)) (hfull : StrongEdge.rootLabels G Q r = G.neighborFinset r) {x : V} (hxr : x ≠ r)
  (hx : 4 ≤ (StrongEdge.rootType G r x).card) {y : V} (hyr : y ≠ r) (hyx : y ≠ x) : (StrongEdge.rootType G r y).card ≤ 2

StrongEdge.high20_multiple_unique_at_four_label.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r : V}
  (hN : G.IsIndepSet (G.neighborSet r)) {a x y z : V} (ha : a ∈ StrongEdge.rootLabels G Q r) (hxr : x ≠ r)
  (hx : 4 ≤ (StrongEdge.rootType G r x).card) (hy : y ∈ StrongEdge.multipleTips G r)
  (hz : z ∈ StrongEdge.multipleTips G r) (hyx : y ≠ x) (hzx : z ≠ x) (hax : a ∈ StrongEdge.rootType G r x)
  (hay : a ∈ StrongEdge.rootType G r y) (haz : a ∈ StrongEdge.rootType G r z) : y = z

StrongEdge.high20_multipleTips_subset_four_outer_endpoints.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {x : V} (hxr : x ≠ r) (hx : 4 ≤ (StrongEdge.rootType G r x).card)
  {u v : V} (e : ↑G.edgeSet) (heo : e ∈ StrongEdge.outerEdges G Q r) (he : ↑e = s(u, v)) (hxe : x ∉ ↑e) :
  StrongEdge.multipleTips G r ⊆ {x, u, v}

StrongEdge.high20_outer_card_le_two_of_root_type_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {x : V} (hxr : x ≠ r) (hx : 4 ≤ (StrongEdge.rootType G r x).card) :
  (StrongEdge.outerEdges G Q r).card ≤ 2

StrongEdge.high20_clique_card_le_eighteen_of_root_type_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {x : V} (hxr : x ≠ r) (hx : 4 ≤ (StrongEdge.rootType G r x).card) :
  Q.card ≤ 18
```

### StrongEdge/Bounds/High20Local.lean

```lean
StrongEdge.endpointNeighbourCover_card_le_five_of_triangle.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v w : V} (huv : G.Adj u v)
  (huw : G.Adj u w) (hvw : G.Adj v w) : (StrongEdge.endpointNeighbourCover G u v).card ≤ 5

StrongEdge.root_label_multiple_card_le_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {r a : V} (ha : G.Adj r a) :
  {x ∈ StrongEdge.multipleTips G r | a ∈ StrongEdge.rootType G r x}.card ≤ 3

StrongEdge.multipleTips_type_sum_le_twelve.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (r : V) :
  ∑ x ∈ StrongEdge.multipleTips G r, (StrongEdge.rootType G r x).card ≤ 12

StrongEdge.multipleTips_card_le_six.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (r : V) : (StrongEdge.multipleTips G r).card ≤ 6

StrongEdge.high20_cover_inside_card_le_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v : V}
  (e : ↑G.edgeSet) (he : ↑e = s(u, v)) (h20 : 20 ≤ (StrongEdge.conflictGraph G).degree e) :
  (StrongEdge.edgesInside G Finset.univ (StrongEdge.endpointNeighbourCover G u v)).card ≤ 4

StrongEdge.high20_triangle_cover_inside_empty.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v w : V}
  (e : ↑G.edgeSet) (he : ↑e = s(u, v)) (h20 : 20 ≤ (StrongEdge.conflictGraph G).degree e) (huw : G.Adj u w)
  (hvw : G.Adj v w) : StrongEdge.edgesInside G Finset.univ (StrongEdge.endpointNeighbourCover G u v) = ∅

StrongEdge.high20_triangle_root_type_singleton.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {r a b x : V}
  (e : ↑G.edgeSet) (he : ↑e = s(r, a)) (h20 : 20 ≤ (StrongEdge.conflictGraph G).degree e) (hrb : G.Adj r b)
  (hab : G.Adj a b) (hxr : x ≠ r) (hax : a ∈ StrongEdge.rootType G r x) : StrongEdge.rootType G r x = {a}

StrongEdge.high20_root_triangle_outer_empty.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4)
  {a b : V} (hra : G.Adj r a) (hrb : G.Adj r b) (hab : G.Adj a b) : StrongEdge.outerEdges G Q r = ∅

StrongEdge.high20_large_clique_root_neighborhood_independent.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) (hlarge : 17 ≤ Q.card) (r : V)
  (hR : (StrongEdge.rootLabels G Q r).card = 4) : G.IsIndepSet (G.neighborSet r)

StrongEdge.high20_root_label_budget_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r a : V}
  (hN : G.IsIndepSet (G.neighborSet r)) (ha : a ∈ StrongEdge.rootLabels G Q r) :
  ∑ x ∈ (G.neighborFinset a).erase r, ((StrongEdge.rootType G r x).erase a).card ≤ 4

StrongEdge.high20_shared_root_types_card_le_six.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r a x y : V}
  (hN : G.IsIndepSet (G.neighborSet r)) (ha : a ∈ StrongEdge.rootLabels G Q r) (hxr : x ≠ r) (hyr : y ≠ r) (hxy : x ≠ y)
  (hax : a ∈ StrongEdge.rootType G r x) (hay : a ∈ StrongEdge.rootType G r y) :
  (StrongEdge.rootType G r x).card + (StrongEdge.rootType G r y).card ≤ 6
```

### StrongEdge/Bounds/High20Outer.lean

```lean
StrongEdge.outer_avoiding_card_le_four_of_other_types_le_two.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4)
  (hN : G.IsIndepSet (G.neighborSet r)) (x : V) (ht : ∀ (y : V), y ≠ r → y ≠ x → (StrongEdge.rootType G r y).card ≤ 2) :
  {e ∈ StrongEdge.outerEdges G Q r | x ∉ ↑e}.card ≤ 4
```

### StrongEdge/Bounds/High20Slots.lean

```lean
StrongEdge.star_add_root_card_le_label_sum.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (r : V) :
  (StrongEdge.edgeIncidences G Q r).card + (StrongEdge.rootEdges G Q r).card ≤
    ∑ a ∈ G.neighborFinset r, (StrongEdge.edgeIncidences G Q a).card

StrongEdge.selected_degree_add_one_le_of_missing_label.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) {a x : V} (hax : G.Adj a x)
  (hx : x ∉ StrongEdge.rootLabels G Q a) : (StrongEdge.edgeIncidences G Q a).card + 1 ≤ G.degree a

StrongEdge.root_label_mem_symm.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj]
  (Q : Finset ↑G.edgeSet) {x a : V} (ha : a ∈ StrongEdge.rootLabels G Q x) : x ∈ StrongEdge.rootLabels G Q a

StrongEdge.root_card_add_missing_type_le_twelve.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (r : V)
  (hR : (StrongEdge.rootLabels G Q r).card = 4) (x : V) :
  (StrongEdge.rootEdges G Q r).card + (StrongEdge.rootType G r x \ StrongEdge.rootLabels G Q x).card ≤ 12

StrongEdge.root_card_le_ten_of_label_selected_degree_le_two.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (r : V)
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {a : V} (ha : G.Adj r a)
  (ha2 : (StrongEdge.edgeIncidences G Q a).card ≤ 2) : (StrongEdge.rootEdges G Q r).card ≤ 10
```

### StrongEdge/Bounds/High20TwoTriples.lean

```lean
StrongEdge.high20_other_type_single_at_shared_triple_label.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e)
  {r a x y z : V} (hN : G.IsIndepSet (G.neighborSet r)) (ha : a ∈ StrongEdge.rootLabels G Q r) (hxr : x ≠ r)
  (hyr : y ≠ r) (hzr : z ≠ r) (hxy : x ≠ y) (hzx : z ≠ x) (hzy : z ≠ y) (hx : 3 ≤ (StrongEdge.rootType G r x).card)
  (hy : 3 ≤ (StrongEdge.rootType G r y).card) (hax : a ∈ StrongEdge.rootType G r x)
  (hay : a ∈ StrongEdge.rootType G r y) (haz : a ∈ StrongEdge.rootType G r z) : StrongEdge.rootType G r z = {a}

StrongEdge.high20_outer_meets_two_triples.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {x y : V} (hxr : x ≠ r) (hyr : y ≠ r) (hxy : x ≠ y)
  (hx : 3 ≤ (StrongEdge.rootType G r x).card) (hy : 3 ≤ (StrongEdge.rootType G r y).card) (e : ↑G.edgeSet)
  (heo : e ∈ StrongEdge.outerEdges G Q r) : x ∈ ↑e ∨ y ∈ ↑e

StrongEdge.high20_clique_card_le_eighteen_of_two_triples.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) {r : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {x y : V} (hxr : x ≠ r) (hyr : y ≠ r) (hxy : x ≠ y)
  (hx : 3 ≤ (StrongEdge.rootType G r x).card) (hy : 3 ≤ (StrongEdge.rootType G r y).card) : Q.card ≤ 18
```

### StrongEdge/Bounds/High20UniqueTriple.lean

```lean
StrongEdge.root_missing_label_selected_degree_le_two_of_unique_triple.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) {r : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {x : V} (hx : (StrongEdge.rootType G r x).card = 3)
  (ht : ∀ (y : V), y ≠ r → y ≠ x → (StrongEdge.rootType G r y).card ≤ 2)
  (hsel : 2 ≤ (StrongEdge.rootType G r x ∩ StrongEdge.rootLabels G Q x).card) {o : V} (ho : G.Adj r o)
  (hox : o ∉ StrongEdge.rootType G r x) : (StrongEdge.edgeIncidences G Q o).card ≤ 2

StrongEdge.root_card_le_ten_of_unique_triple.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) {r : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {x : V} (hx : (StrongEdge.rootType G r x).card = 3)
  (ht : ∀ (y : V), y ≠ r → y ≠ x → (StrongEdge.rootType G r y).card ≤ 2) : (StrongEdge.rootEdges G Q r).card ≤ 10

StrongEdge.clique_card_le_nineteen_of_unique_triple.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) {r : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hR : (StrongEdge.rootLabels G Q r).card = 4) {x : V} (hx : (StrongEdge.rootType G r x).card = 3)
  (ht : ∀ (y : V), y ≠ r → y ≠ x → (StrongEdge.rootType G r y).card ≤ 2) : Q.card ≤ 19
```

### StrongEdge/High20Packing.lean

```lean
StrongEdge.minimalCliqueBounds20_of_maxDegree_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) :
  StrongEdge.MinimalCliqueBounds20 (StrongEdge.conflictGraph G)

StrongEdge.induced_matching_packing20.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (F : Finset ↑G.edgeSet) : ∃ M ⊆ F, StrongEdge.IsInducedMatching G ↑M ∧ F.card ≤ 20 * M.card
```
