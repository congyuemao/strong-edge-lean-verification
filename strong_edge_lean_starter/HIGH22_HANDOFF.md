# C5 high22: verified handoff

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
StrongEdge.high22_clique_card_le_seventeen.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h22 : ∀ e ∈ Q, 22 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 17
StrongEdge.minimalCliqueBounds20_of_high20_high21.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (high20 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 19)
  (high21 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 18) :
  StrongEdge.MinimalCliqueBounds20 (StrongEdge.conflictGraph G)
StrongEdge.induced_matching_packing20_of_high20_high21.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (high20 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 19)
  (high21 :
    ∀ (Q : Finset ↑G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique ↑Q → (∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) → Q.card ≤ 18)
  (F : Finset ↑G.edgeSet) : ∃ M ⊆ F, StrongEdge.IsInducedMatching G ↑M ∧ F.card ≤ 20 * M.card
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
StrongEdge.high22_root_label_budget_two.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (Q : Finset ↑G.edgeSet) (h22 : ∀ e ∈ Q, 22 ≤ (StrongEdge.conflictGraph G).degree e) {r a : V}
  (ha : a ∈ StrongEdge.rootLabels G Q r) :
  ∑ x ∈ (G.neighborFinset a).erase r, ((StrongEdge.rootType G r x).erase a).card ≤ 2
StrongEdge.high22_clique_card_le_seventeen_of_root_four.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h22 : ∀ e ∈ Q, 22 ≤ (StrongEdge.conflictGraph G).degree e) (r : V) (hR : (StrongEdge.rootLabels G Q r).card = 4) :
  Q.card ≤ 17
StrongEdge.high22_clique_card_le_seventeen_of_support_degree_le_three.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ (x : V), G.degree x ≤ 4) (Q : Finset ↑G.edgeSet) (hQ : (StrongEdge.conflictGraph G).IsClique ↑Q)
  (h22 : ∀ e ∈ Q, 22 ≤ (StrongEdge.conflictGraph G).degree e)
  (hQdeg : ∀ (x : V), (StrongEdge.edgeIncidences G Q x).card ≤ 3) : Q.card ≤ 17
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

The stage adds 51 theorems in eight modules. Every theorem is included
individually in the axiom audit:

### StrongEdge/Bounds/High22.lean

- `StrongEdge.high22_clique_card_le_seventeen`

### StrongEdge/Bounds/High22Heavy.lean

- `StrongEdge.labelHeavyTips_subset_multiple`
- `StrongEdge.root_type_inter_card_sum`
- `StrongEdge.outerEdges_meet_labelHeavyTips`
- `StrongEdge.high22_heavy_label_card_le_two`
- `StrongEdge.high22_labelHeavyTips_card_le_three`
- `StrongEdge.high22_outer_incidence_le_two_at_heavy`
- `StrongEdge.high22_outer_card_le_six_of_root_three`
- `StrongEdge.high22_heavy_card_and_degree_of_outer_six`
- `StrongEdge.high22_heavy_label_card_eq_two_of_three`
- `StrongEdge.high22_multiple_subset_heavy_of_three`

### StrongEdge/Bounds/High22Local.lean

- `StrongEdge.high22_cover_card_eq_six`
- `StrongEdge.high22_endpoints_degree_four`
- `StrongEdge.high22_other_neighbor_sets_disjoint`
- `StrongEdge.high22_no_triangle_on_edge`
- `StrongEdge.high22_cover_inside_card_le_two`
- `StrongEdge.high22_at_most_two_four_cycles_on_edge`

### StrongEdge/Bounds/High22RootFour.lean

- `StrongEdge.high22_clique_card_le_seventeen_of_root_triple`
- `StrongEdge.outer_endpoints_multiple_of_root_four`
- `StrongEdge.outer_incidence_sum_eq_twice`
- `StrongEdge.high22_outer_card_le_four_of_root_types_le_two`
- `StrongEdge.rootEdges_card_le_tips_add_multiple`
- `StrongEdge.rootEdges_card_le_twice_multiple_of_no_single`
- `StrongEdge.high22_outer_degree_eq_two_of_four`
- `StrongEdge.outer_saturated_neighbors`
- `StrongEdge.high22_active_multiple_card_le_two_of_outer_four`
- `StrongEdge.high22_clique_card_le_seventeen_of_root_four`

### StrongEdge/Bounds/High22Subcubic.lean

- `StrongEdge.root_outer_incidence_add_le`
- `StrongEdge.root_incidence_at_tip_le_type`
- `StrongEdge.rootEdges_card_le_tips_of_incidence_le_one`
- `StrongEdge.rootTips_subset_multiple_of_no_single`
- `StrongEdge.high22_clique_card_le_seventeen_of_support_degree_le_three`

### StrongEdge/Bounds/High22Support.lean

- `StrongEdge.high22_root_degree_four`
- `StrongEdge.high22_root_neighborhood_independent`
- `StrongEdge.fourCycleOpposites_card_eq_root_load`
- `StrongEdge.high22_root_label_budget_two`
- `StrongEdge.high22_root_type_erase_card_le_two`
- `StrongEdge.high22_root_type_card_le_three`
- `StrongEdge.high22_root_label_multiple_card_le_two`
- `StrongEdge.high22_shared_root_types_card_le_four`
- `StrongEdge.root_type_card_sum_eq_label_sum`
- `StrongEdge.high22_multipleTips_card_le_four`
- `StrongEdge.high22_multipleTips_eq_of_triple`

### StrongEdge/Bounds/RootCounting.lean

- `StrongEdge.root_single_edge_outer_adj`
- `StrongEdge.rootTips_adj_of_single`
- `StrongEdge.rootTips_card_le_six_of_single`
- `StrongEdge.rootEdges_card_le_tip_weight`
- `StrongEdge.clique_card_le_star_root_outer`
- `StrongEdge.outer_incidence_add_type_card_le_degree`

### StrongEdge/High22Packing.lean

- `StrongEdge.minimalCliqueBounds20_of_high20_high21`
- `StrongEdge.induced_matching_packing20_of_high20_high21`

## Commands and verified evidence

The baseline and final checks both ran these actual PowerShell commands from
the project directory; all four invocations exited 0:

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

Baseline: **1,136 jobs and 94 audited theorems**, recorded in
`verification/high22-baseline-build.log` and `verification/high22-baseline-axioms.log`.
Final: **1,144 jobs and 145 audited theorems**, recorded in
`verification/high22-build.log` and `verification/high22-axioms.log`.
The final build has no warnings. All 94 previous audit entries are preserved;
all 51 new entries depend only on `propext`, `Classical.choice`, and
`Quot.sound`. No proof gaps or custom axioms occur in these dependency closures.

The source scan of all 28 project Lean files found no `sorry`,
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
