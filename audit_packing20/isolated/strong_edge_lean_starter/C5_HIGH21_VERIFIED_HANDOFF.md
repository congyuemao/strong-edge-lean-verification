# C5 high21: verified handoff

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
StrongEdge.high21_clique_card_le_eighteen.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 18
StrongEdge.minimalCliqueBounds20_of_high20.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (high20 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 19) :
  StrongEdge.MinimalCliqueBounds20 (StrongEdge.conflictGraph G)
StrongEdge.induced_matching_packing20_of_high20.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (high20 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 19)
  (F : Finset ↑G.edgeSet) : ∃ M ⊆ F, StrongEdge.IsInducedMatching G ↑M ∧ F.card ≤ 20 * M.card
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
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
python verification/finalize-high21.py
```

The baseline build and audit both exited 0: **1,144 jobs, 145 audited declarations**.
The final build and audit both exited 0: **1,162 jobs, 192 audited declarations**.
Both final logs contain no errors or warnings. Every new theorem has both a `#check`
and a `#print axioms` entry. All 192 dependency closures use only
`propext`, `Classical.choice`, and `Quot.sound`; all 145 previous audit entries remain.

The source scan covers **37 Lean files** and finds no prohibited proof-gap
tokens. The dependency audit is the decisive proof check. Nine new modules contain
**47 theorems** and one definition, `fullDoubleTips`. A supplementary direct
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

### StrongEdge/Bounds/DegreeTwoClique.lean

```lean
StrongEdge.restricted_incidence_card_le.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (P : Finset V) (hP : ∀ e ∈ Q, ∀ x ∈ ↑e, x ∈ P) (x : V) :
  (StrongEdge.edgeIncidences G Q x).card ≤ (G.neighborFinset x ∩ P).card

StrongEdge.restricted_cover_card_le_two.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (P : Finset V) (hd : ∀ x ∈ P, (G.neighborFinset x ∩ P).card ≤ 2) {u v : V} (hu : u ∈ P)
  (hv : v ∈ P) (huv : G.Adj u v) : (StrongEdge.endpointNeighbourCover G u v ∩ P).card ≤ 2

StrongEdge.clique_card_le_one_add_restricted_incidence_sum.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (P : Finset V) (hP : ∀ e ∈ Q, ∀ x ∈ ↑e, x ∈ P) {u v : V} (e : ↑G.edgeSet) (heQ : e ∈ Q) (he : ↑e = s(u, v)) :
  Q.card ≤ 1 + ∑ w ∈ StrongEdge.endpointNeighbourCover G u v ∩ P, (StrongEdge.edgeIncidences G Q w).card

StrongEdge.degree_two_clique_card_le_five.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (P : Finset V)
  (hP : ∀ e ∈ Q, ∀ x ∈ ↑e, x ∈ P) (hd : ∀ x ∈ P, (G.neighborFinset x ∩ P).card ≤ 2) : Q.card ≤ 5

StrongEdge.degree_two_five_cover_saturated.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (P : Finset V)
  (hP : ∀ e ∈ Q, ∀ x ∈ ↑e, x ∈ P) (hd : ∀ x ∈ P, (G.neighborFinset x ∩ P).card ≤ 2) (h5 : Q.card = 5) {u v : V}
  (e : ↑G.edgeSet) (heQ : e ∈ Q) (he : ↑e = s(u, v)) :
  (StrongEdge.endpointNeighbourCover G u v ∩ P).card = 2 ∧
    ∀ w ∈ StrongEdge.endpointNeighbourCover G u v ∩ P, (StrongEdge.edgeIncidences G Q w).card = 2

StrongEdge.degree_two_five_supported_degree_two.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (P : Finset V)
  (hP : ∀ e ∈ Q, ∀ x ∈ ↑e, x ∈ P) (hd : ∀ x ∈ P, (G.neighborFinset x ∩ P).card ≤ 2) (h5 : Q.card = 5) {x : V}
  (hx : 0 < (StrongEdge.edgeIncidences G Q x).card) : (StrongEdge.edgeIncidences G Q x).card = 2

StrongEdge.degree_two_clique_card_le_four_of_selected_bipartition.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (P : Finset V) (hP : ∀ e ∈ Q, ∀ x ∈ ↑e, x ∈ P) (hd : ∀ x ∈ P, (G.neighborFinset x ∩ P).card ≤ 2) (L : Finset V)
  (hL : ∀ e ∈ Q, {x ∈ L | x ∈ ↑e}.card = 1) : Q.card ≤ 4
```

### StrongEdge/Bounds/High21.lean

```lean
StrongEdge.high21_clique_card_le_eighteen.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 18
```

### StrongEdge/Bounds/High21Double.lean

```lean
StrongEdge.rootType_eq_neighbor_inter.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (r x : V) : StrongEdge.rootType G r x = G.neighborFinset x ∩ G.neighborFinset r

StrongEdge.multipleTips_not_neighbor.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] {r x : V} (hN : G.IsIndepSet (G.neighborSet r)) (hx : x ∈ StrongEdge.multipleTips G r) :
  ¬G.Adj r x

StrongEdge.residual_neighbors_add_type_card.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (r x : V) :
  (G.neighborFinset x \ G.neighborFinset r).card + (StrongEdge.rootType G r x).card = G.degree x

StrongEdge.root_selected_edges_force_adj.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) {r a b x y : V}
  (hN : G.IsIndepSet (G.neighborSet r)) (ha : G.Adj r a) (hb : G.Adj r b) (hxb : b ∉ StrongEdge.rootType G r x)
  (hya : a ∉ StrongEdge.rootType G r y) (e f : ↑G.edgeSet) (heQ : e ∈ Q) (hfQ : f ∈ Q) (he : ↑e = s(a, x))
  (hf : ↑f = s(b, y)) : G.Adj x y

StrongEdge.fullDoubleTips_adj_of_types_ne.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) {r x y : V}
  (hN : G.IsIndepSet (G.neighborSet r)) (hx : x ∈ StrongEdge.fullDoubleTips G Q r)
  (hy : y ∈ StrongEdge.fullDoubleTips G Q r) (hne : StrongEdge.rootType G r x ≠ StrongEdge.rootType G r y) : G.Adj x y

StrongEdge.high21_full_double_types_equal_or_disjoint.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) {r x y : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hx : x ∈ StrongEdge.fullDoubleTips G Q r) (hy : y ∈ StrongEdge.fullDoubleTips G Q r) :
  StrongEdge.rootType G r x = StrongEdge.rootType G r y ∨
    Disjoint (StrongEdge.rootType G r x) (StrongEdge.rootType G r y)

StrongEdge.fullDoubleTips_card_le_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) {r : V} (hN : G.IsIndepSet (G.neighborSet r)) :
  (StrongEdge.fullDoubleTips G Q r).card ≤ 4
```

### StrongEdge/Bounds/High21LargeType.lean

```lean
StrongEdge.high21_large_types_share_label.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {r x y : V} (hx : 3 ≤ (StrongEdge.rootType G r x).card)
  (hy : 2 ≤ (StrongEdge.rootType G r y).card) : (StrongEdge.rootType G r x ∩ StrongEdge.rootType G r y).Nonempty

StrongEdge.high21_multipleTips_eq_of_type_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V)
  (hfull : StrongEdge.rootLabels G Q r = G.neighborFinset r) {x : V} (hxr : x ≠ r)
  (hx : 4 ≤ (StrongEdge.rootType G r x).card) {y : V} (hy : y ∈ StrongEdge.multipleTips G r) : y = x

StrongEdge.high21_other_type_le_two_of_triple.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V)
  (hfull : StrongEdge.rootLabels G Q r = G.neighborFinset r) {x : V} (hxr : x ≠ r)
  (hx : 3 ≤ (StrongEdge.rootType G r x).card) {y : V} (hyr : y ≠ r) (hyx : y ≠ x) : (StrongEdge.rootType G r y).card ≤ 2

StrongEdge.high21_multiple_unique_at_triple_label.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) {r a x y z : V}
  (ha : a ∈ StrongEdge.rootLabels G Q r) (hxr : x ≠ r) (hx : 3 ≤ (StrongEdge.rootType G r x).card)
  (hy : y ∈ StrongEdge.multipleTips G r) (hz : z ∈ StrongEdge.multipleTips G r) (hyx : y ≠ x) (hzx : z ≠ x)
  (hax : a ∈ StrongEdge.rootType G r x) (hay : a ∈ StrongEdge.rootType G r y) (haz : a ∈ StrongEdge.rootType G r z) :
  y = z

StrongEdge.high21_multipleTips_subset_triple_outer_endpoints.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4)
  {x : V} (hxr : x ≠ r) (hx : 3 ≤ (StrongEdge.rootType G r x).card) {u v : V} (e : ↑G.edgeSet)
  (heo : e ∈ StrongEdge.outerEdges G Q r) (he : ↑e = s(u, v)) (hxe : x ∉ ↑e) : StrongEdge.multipleTips G r ⊆ {x, u, v}

StrongEdge.high21_outer_card_le_two_of_root_triple.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4)
  {x : V} (hxr : x ≠ r) (hx : 3 ≤ (StrongEdge.rootType G r x).card) : (StrongEdge.outerEdges G Q r).card ≤ 2

StrongEdge.high21_clique_card_le_eighteen_of_root_triple.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4)
  {x : V} (hxr : x ≠ r) (hx : 3 ≤ (StrongEdge.rootType G r x).card) : Q.card ≤ 18
```

### StrongEdge/Bounds/High21Local.lean

```lean
StrongEdge.high21_cover_card_eq_six.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v : V}
  (e : ↑G.edgeSet) (he : ↑e = s(u, v)) (h21 : 21 ≤ (StrongEdge.conflictGraph G).degree e) :
  (StrongEdge.endpointNeighbourCover G u v).card = 6

StrongEdge.high21_endpoints_degree_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v : V}
  (e : ↑G.edgeSet) (he : ↑e = s(u, v)) (h21 : 21 ≤ (StrongEdge.conflictGraph G).degree e) :
  G.degree u = 4 ∧ G.degree v = 4

StrongEdge.high21_other_neighbor_sets_disjoint.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v : V}
  (e : ↑G.edgeSet) (he : ↑e = s(u, v)) (h21 : 21 ≤ (StrongEdge.conflictGraph G).degree e) :
  Disjoint ((G.neighborFinset u).erase v) ((G.neighborFinset v).erase u)

StrongEdge.high21_no_triangle_on_edge.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v : V}
  (e : ↑G.edgeSet) (he : ↑e = s(u, v)) (h21 : 21 ≤ (StrongEdge.conflictGraph G).degree e) {w : V} (huw : G.Adj u w) :
  ¬G.Adj v w

StrongEdge.high21_cover_inside_card_le_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v : V}
  (e : ↑G.edgeSet) (he : ↑e = s(u, v)) (h21 : 21 ≤ (StrongEdge.conflictGraph G).degree e) :
  (StrongEdge.edgesInside G Finset.univ (StrongEdge.endpointNeighbourCover G u v)).card ≤ 3

StrongEdge.high21_at_most_three_four_cycles_on_edge.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) {u v : V}
  (e : ↑G.edgeSet) (he : ↑e = s(u, v)) (h21 : 21 ≤ (StrongEdge.conflictGraph G).degree e) :
  (StrongEdge.fourCycleOpposites G u v).card ≤ 3
```

### StrongEdge/Bounds/High21RootFour.lean

```lean
StrongEdge.outer_card_le_four_of_double_types.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4)
  (hN : G.IsIndepSet (G.neighborSet r)) (ht : ∀ (x : V), x ≠ r → (StrongEdge.rootType G r x).card ≤ 2) :
  (StrongEdge.outerEdges G Q r).card ≤ 4

StrongEdge.rootLabels_rootEdges_at_tip_subset_type.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) {r x : V} (hN : G.IsIndepSet (G.neighborSet r))
  (hx : x ∈ StrongEdge.rootTips G Q r) :
  StrongEdge.rootLabels G (StrongEdge.rootEdges G Q r) x ⊆ StrongEdge.rootType G r x

StrongEdge.root_incidence_two_mem_fullDoubleTips.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) {r x : V} (hN : G.IsIndepSet (G.neighborSet r))
  (ht : (StrongEdge.rootType G r x).card ≤ 2) (hx : x ∈ StrongEdge.rootTips G Q r)
  (hd : (StrongEdge.edgeIncidences G (StrongEdge.rootEdges G Q r) x).card = 2) : x ∈ StrongEdge.fullDoubleTips G Q r

StrongEdge.rootEdges_card_le_tips_add_fullDoubleTips.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (Q : Finset ↑G.edgeSet) (r : V) (hN : G.IsIndepSet (G.neighborSet r))
  (ht : ∀ (x : V), x ≠ r → (StrongEdge.rootType G r x).card ≤ 2) :
  (StrongEdge.rootEdges G Q r).card ≤ (StrongEdge.rootTips G Q r).card + (StrongEdge.fullDoubleTips G Q r).card

StrongEdge.high21_clique_card_le_eighteen_of_root_types_le_two.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4)
  (ht : ∀ (x : V), x ≠ r → (StrongEdge.rootType G r x).card ≤ 2) : Q.card ≤ 18

StrongEdge.high21_clique_card_le_eighteen_of_root_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4) :
  Q.card ≤ 18
```

### StrongEdge/Bounds/High21Support.lean

```lean
StrongEdge.high21_root_degree_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V)
  (hR : (StrongEdge.rootLabels G Q r).Nonempty) : G.degree r = 4

StrongEdge.high21_root_neighborhood_independent.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V)
  (hR : 3 ≤ (StrongEdge.rootLabels G Q r).card) : G.IsIndepSet (G.neighborSet r)

StrongEdge.high21_root_label_budget_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) {r a : V}
  (ha : a ∈ StrongEdge.rootLabels G Q r) :
  ∑ x ∈ (G.neighborFinset a).erase r, ((StrongEdge.rootType G r x).erase a).card ≤ 3

StrongEdge.high21_root_type_erase_card_le_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) {r a x : V}
  (ha : a ∈ StrongEdge.rootLabels G Q r) (hxr : x ≠ r) (hax : a ∈ StrongEdge.rootType G r x) :
  ((StrongEdge.rootType G r x).erase a).card ≤ 3

StrongEdge.high21_root_label_multiple_card_le_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) {r a : V}
  (ha : a ∈ StrongEdge.rootLabels G Q r) : {x ∈ StrongEdge.multipleTips G r | a ∈ StrongEdge.rootType G r x}.card ≤ 3

StrongEdge.high21_shared_root_types_card_le_five.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) {r a x y : V}
  (ha : a ∈ StrongEdge.rootLabels G Q r) (hxr : x ≠ r) (hyr : y ≠ r) (hxy : x ≠ y) (hax : a ∈ StrongEdge.rootType G r x)
  (hay : a ∈ StrongEdge.rootType G r y) : (StrongEdge.rootType G r x).card + (StrongEdge.rootType G r y).card ≤ 5

StrongEdge.high21_multipleTips_card_le_six.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) (r : V)
  (hfull : StrongEdge.rootLabels G Q r = G.neighborFinset r) : (StrongEdge.multipleTips G r).card ≤ 6
```

### StrongEdge/Bounds/SubcubicEighteen.lean

```lean
StrongEdge.clique_card_le_nineteen_of_support_degree_le_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (hQdeg : ∀ (x : V), (StrongEdge.edgeIncidences G Q x).card ≤ 3) :
  Q.card ≤ 19

StrongEdge.subcubic_nineteen_cover_saturated.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (hQdeg : ∀ (x : V), (StrongEdge.edgeIncidences G Q x).card ≤ 3)
  (h19 : Q.card = 19) {u v : V} (e : ↑G.edgeSet) (heQ : e ∈ Q) (he : ↑e = s(u, v)) :
  (StrongEdge.endpointNeighbourCover G u v).card = 6 ∧
    ∀ w ∈ StrongEdge.endpointNeighbourCover G u v, (StrongEdge.edgeIncidences G Q w).card = 3

StrongEdge.subcubic_nineteen_supported_degree_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (hQdeg : ∀ (x : V), (StrongEdge.edgeIncidences G Q x).card ≤ 3)
  (h19 : Q.card = 19) {x : V} (hx : 0 < (StrongEdge.edgeIncidences G Q x).card) :
  (StrongEdge.edgeIncidences G Q x).card = 3

StrongEdge.clique_card_le_eighteen_of_support_degree_le_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet)
  (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q) (hQdeg : ∀ (x : V), (StrongEdge.edgeIncidences G Q x).card ≤ 3) :
  Q.card ≤ 18
```

### StrongEdge/High21Packing.lean

```lean
StrongEdge.minimalCliqueBounds20_of_high20.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (high20 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 19) :
  StrongEdge.MinimalCliqueBounds20 (StrongEdge.conflictGraph G)

StrongEdge.induced_matching_packing20_of_high20.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (high20 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 19)
  (F : Finset ↑G.edgeSet) : ∃ M ⊆ F, StrongEdge.IsInducedMatching G ↑M ∧ F.card ≤ 20 * M.card
```
