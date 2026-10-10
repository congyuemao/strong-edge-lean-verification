# C5 high23: verified handoff

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
StrongEdge.high23_clique_card_le_sixteen.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h23 : ∀ e ∈ Q, 23 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 16
StrongEdge.minimalCliqueBounds20_of_high20_high21_high22.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (high20 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 19)
  (high21 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 18)
  (high22 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 22 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 17) :
  StrongEdge.MinimalCliqueBounds20 (StrongEdge.conflictGraph G)
StrongEdge.induced_matching_packing20_of_high20_high21_high22.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (high20 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 19)
  (high21 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 18)
  (high22 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 22 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 17)
  (F : Finset ↑G.edgeSet) : ∃ M ⊆ F, StrongEdge.IsInducedMatching G ↑M ∧ F.card ≤ 20 * M.card
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

This stage adds 43 theorems, each individually included in the axiom
audit. Their finite and decidability instances are visible in the source.
Only the final universal theorem and its wrappers constitute the delivered
bound; helper lemmas state their local premises explicitly.

### StrongEdge/Bounds/EdgeCounting.lean

- `StrongEdge.card_le_via_relation`
- `StrongEdge.edgeIncidences_univ_card`
- `StrongEdge.edgeIncidences_card_le_degree`
- `StrongEdge.edge_endpoint_count`
- `StrongEdge.incidence_sum_eq_meeting_add_inside`
- `StrongEdge.conflict_degree_add_inside_le_sum`
- `StrongEdge.clique_card_le_one_add_incidence_sum`
- `StrongEdge.clique_card_le_thirteen_of_support_degree_le_two`

### StrongEdge/Bounds/High23.lean

- `StrongEdge.meeting_edges_subset_root_single_double`
- `StrongEdge.high23_meeting_card_le_fourteen_of_root_four`
- `StrongEdge.high23_clique_card_le_sixteen_of_root_four`
- `StrongEdge.high23_clique_card_le_sixteen`

### StrongEdge/Bounds/High23Four.lean

- `StrongEdge.root_edge_tip_not_neighbor`
- `StrongEdge.root_single_edges_outer_adj`
- `StrongEdge.high23_singleTips_card_le_six`
- `StrongEdge.singleRootEdges_card_le_singleTips`
- `StrongEdge.high23_doubleRootEdges_card_le_four`

### StrongEdge/Bounds/High23Local.lean

- `StrongEdge.high23_cover_card_eq_six`
- `StrongEdge.high23_endpoints_degree_four`
- `StrongEdge.high23_other_neighbor_sets_disjoint`
- `StrongEdge.high23_no_triangle_on_edge`
- `StrongEdge.high23_cover_inside_card_le_one`
- `StrongEdge.high23_cross_edges_unique`
- `StrongEdge.high23_at_most_one_four_cycle_on_edge`

### StrongEdge/Bounds/High23Outer.lean

- `StrongEdge.outerEdges_endpoints`
- `StrongEdge.outer_edge_types_cover_root_labels`
- `StrongEdge.high23_outer_edges_incident_double_root`
- `StrongEdge.high23_outer_card_le_two_of_double_root_type`
- `StrongEdge.high23_outer_edges_card_le_two`
- `StrongEdge.selected_edges_card_le_meeting_add_outer`
- `StrongEdge.high23_clique_card_le_fourteen_of_support_degree_le_three`

### StrongEdge/Bounds/High23Support.lean

- `StrongEdge.mem_rootType`
- `StrongEdge.rootLabels_subset_neighbors`
- `StrongEdge.rootLabels_card`
- `StrongEdge.high23_root_degree_four`
- `StrongEdge.high23_root_neighborhood_independent`
- `StrongEdge.high23_root_cross_unique`
- `StrongEdge.high23_type_meets_root_labels`
- `StrongEdge.high23_root_type_card_le_two`
- `StrongEdge.high23_double_type_unique`
- `StrongEdge.high23_type_singleton_of_sharing_double`

### StrongEdge/High23Packing.lean

- `StrongEdge.minimalCliqueBounds20_of_high20_high21_high22`
- `StrongEdge.induced_matching_packing20_of_high20_high21_high22`

## Checks and preservation

From the project directory, both baseline commands exited 0:

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

The baseline had 1,129 build jobs and 51 audited theorems. Logs:
`verification/high23-baseline-build.log` and
`verification/high23-baseline-axioms.log`.

The same two final commands exited 0. The final build completed **1136 jobs**
without warnings; the final audit checked **94 theorems**, preserving
all previous 51 entries and adding all 43 new ones. Evidence:
`verification/high23-build.log` and `verification/high23-axioms.log`.
Every audited dependency list contains only `propext`, `Classical.choice`, and
`Quot.sound`. No proof gaps or custom mathematical axioms occur in those closures.

The source scan of all 20 project Lean files found no `sorry`,
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
