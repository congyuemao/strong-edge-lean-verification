# Codex task: Lean C5 high21, eliminate the next structural premise

**Task type:** continue an existing Lean 4 + mathlib formalisation in the local workspace.  
**Primary acceptance goal:** prove the universal `high21` conflict-clique bound `Q.card ≤ 18` under original maximum degree four, then integrate it into the conditional 20-packing wrapper.  
**Status of this document:** an instruction for the *next* run, **not** a verified proof or a claim that the next stage succeeded.

## 0. Context and baseline to verify

The user-provided **C5 high22 verified handoff** dated 2026-10-09 reports:

- `StrongEdge.high22_clique_card_le_seventeen` is kernel-checked and integrated.
- Earlier kernel-checked stages establish full-conflict degree ≤24, high24 ≤13 (hence ≤15), and high23 ≤16.
- The generic private-clique, degree-exchange, and double-counting argument is already formalised.
- `StrongEdge.induced_matching_packing20_of_high20_high21` is conditional on **two** explicit clique bounds. It is not yet unconditional.
- Latest reported final build: **1,144 jobs**, **145 audited theorems**, no warnings; dependency closures use only `propext`, `Classical.choice`, and `Quot.sound`.
- Lean toolchain: `leanprover/lean4:v4.35.0-rc4`; Lean compiler commit `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`; mathlib commit `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`.
- Files `verification/high22-build.log`, `verification/high22-axioms.log`, `verification/high22-source-sha256.json`, `verification/high22-source.diff` and `../strong_edge_lean_high22_checkpoint.zip` are reported to exist locally.

**First inspect the actual local workspace and reproduce these claims.** The report has been pasted into the conversation; this prompt does not itself include the Lean sources or the logs. If the local project is absent, inconsistent, or the baseline commands fail, document the blocker and do not invent a successful result. Do not reset, overwrite, or discard the existing project.

In the project directory, run the established wrapper if available:

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

Check `lake-manifest.json`, the toolchain pin, Git status, and the latest audit declarations. Preserve all existing source/configuration and previous verification evidence. Avoid `lake update` unless a genuine toolchain incompatibility is diagnosed and explicitly documented.

## 1. Required mathematical theorem

Formalise a theorem with this **mathematical** signature (adapt Lean implicit instances/coercions to the actual codebase):

```lean
theorem StrongEdge.high21_clique_card_le_eighteen
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V)
    [DecidableRel G.Adj]
    [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4)
    (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique
      (Q : Set G.edgeSet))
    (h21 : ∀ e ∈ Q,
      21 ≤ (StrongEdge.conflictGraph G).degree e) :
    Q.card ≤ 18 := by
  ...
```

The displayed `...` illustrates the goal only. **No unfinished proof, `sorry`, extra axioms, hidden hypothesis, or unsupported computation is acceptable in an exported successful theorem.**

The quantified `Q` is any finite set of **original edges**, not necessarily all of `E(G)` and not assumed maximal. Every conflict degree is the degree in the **full** `conflictGraph G`, with original edges outside `Q` retained as possible conflict witnesses. Do not replace it with `conflictGraph` of a graph obtained by deleting edges not in `Q`.

No assumptions of girth, regularity, support closure, minimum size, 20-packing, other unproved clique bounds, or a classification theorem may appear in the final theorem.

Only the **≤18** bound is required. The paper's stronger `high21 ≤17` is an optional later strengthening; do not let it block the present stage.

## 2. Source of the intended proof and the precise gap

**Pinned mathematical source revision**: `3a95c4a9c44475196c42b6eab4749c487d15d59b` of:

- Primary: [research/high_conflict_thresholds.md, §1–§3](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_thresholds.md)
- Related stronger result: [research/high_conflict_20_21_improved.md, §1–§2 and §4](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_20_21_improved.md)
- Subcubic fallback: [research/strong_clique_subcubic.md](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/strong_clique_subcubic.md)
- Packing interface: [research/packing_private_cliques.md](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/packing_private_cliques.md)

The older proof proposes `high21 ≤18`, by excluding a 19-edge high21 clique. Its key difference from `high22`: an edge with full conflict degree ≥21 allows up to **three** local incidence-count losses; the previously proved two-loss arguments generally cannot be reused with their threshold simply lowered.

**Use prior checked lemmas where their actual Lean hypotheses permit.** Especially inspect:

- `StrongEdge/Bounds/ConflictDegree.lean`, `ConflictRigidity.lean`;
- `StrongEdge/Bounds/EdgeCounting.lean`;
- `StrongEdge/Bounds/High23*.lean`;
- `StrongEdge/Bounds/High22*.lean`, especially `High22Support.lean`, `High22Heavy.lean`, `High22RootFour.lean`, `High22Subcubic.lean`, and `RootCounting.lean`;
- `StrongEdge/High22Packing.lean`, `StrongEdge/MinimalPacking.lean`, and `StrongEdge/Audit.lean`.

**Avoid assuming names or precise signatures beyond those present in the actual source.** The lists here describe reported modules, not an independently inspected local codebase.

## 3. Suggested proof architecture

### A. Local structure of a high21 original edge

Prove under `hΔ` and `21 ≤ (conflictGraph G).degree e`:

1. Both endpoints of `e` have **original degree four**. A smaller endpoint degree gives too few possible conflicting edges.
2. `e` cannot belong to a triangle in the original graph. Under maximum degree four, a triangle edge has full conflict degree at most 20.
3. Its endpoint-neighbour cover has six distinct vertices. This depends on the preceding degree and triangle facts; check the exact equality argument rather than assuming global triangle-freeness.
4. The exact incidence counting identity gives at most three original edges lying inside the six-vertex cover. In particular, there are at most three oriented opposite edges (four-cycles through `e`).
5. For a root `r` joined by a selected Q-edge to `a`, the cross-neighbour/root-type contribution consumes some of that at-most-three budget. Prove the exact contribution inequality before making any multiplicity claim.

Reuse `endpointNeighbourCover`, `edgesInside`, `fourCycleOpposites`, `rootLabels`, `rootType`, `edgeIncidences`, and the existing incidence identity. Keep all counts in the full original graph.

**Regression risk:** `high22` establishes ≤2 local losses. A `high21` bound must be derived from its own ≥21 hypothesis. No reused theorem may silently retain `h22` or an equivalent stronger premise.

### B. Selected support degree at most three

Let `d_Q(x) = (StrongEdge.edgeIncidences G Q x).card`, always distinguished from `G.degree x` and `(conflictGraph G).degree e`.

If `∀ x, d_Q(x) ≤ 2`, the previous general covering lemma already gives `Q.card ≤13` (verify exact hypotheses).

If `∀ x, d_Q(x) ≤3`, the primary paper points to the universal lemma:

> For every degree-four original graph and every full-conflict clique `Q`, if all selected incidence degrees are ≤3, then `Q.card ≤17`, **without a high21 hypothesis**.

This is proved on paper in `research/strong_clique_subcubic.md`; it has **not** been reported as kernel-verified in previous stages. Its counting proof uses selected-incidence degree distribution, local conflict covers, saturation of the original support, and an eventual four-cycle contradiction.

Two permissible paths:

- **Path B1 (prefer if economical):** derive the threshold-specific `high21` subcubic `Q.card ≤18` directly, reusing the high22 root-counting machinery with a fresh three-loss budget. The proof is acceptable if it uses `h21` explicitly and does not assume `h22`.
- **Path B2 (general and reusable):** formalise the threshold-free `strong_clique_subcubic.md` bound `Q.card ≤17`, then use it for high21 and later high20. This may require substantially more work. If started, keep all proved intermediate lemmas even if the final subcubic theorem is unfinished.

Do not claim the threshold-free `≤17` lemma until its entire four-cycle counting proof has been checked. Either route is sufficient for the main task if it yields the needed `≤18` with correct hypotheses.

### C. Four-edge root star: set-up

The remaining case has a root `r` with **four selected Q-edges**. Hence `A = N_G(r)` has exactly four vertices, all four edges `r-a` belong to `Q`, and `A` is independent because those Q-edges have full conflict degree ≥21.

Define `B` as the vertices outside `{r} ∪ A` **incident to Q**, not as every other vertex of the original graph. For `x∈B` define its type `T_x=N_G(x)∩A`. Any necessary reduction to supported vertices is only for bookkeeping: it must never change the full original conflict graph or its degrees.

Prove:

- Every `T_x` is nonempty. Otherwise an edge of `Q` incident to `x`, in order to conflict with all four root-star edges, would force an endpoint to have at least five neighbours, or violate the previously proved type constraints.
- Let `c_j` count type-`j` vertices in `B`, `j=1,2,3,4`. Let `S = Σ_{x∈B}|T_x|`, `T` count selected `A`–`B` edges, and `h` count selected `B`–`B` edges.
- With `A` independent, `S ≤12`, `T ≤ S`, and `Q.card = 4 + T + h`.
- Any selected `B`–`B` edge `xy` must satisfy `T_x ∪ T_y = A`. This forces the familiar type pairings: a type-1 point can pair with a type-3 point; two type-2 points must have complementary types; type-4 vertices have no residual original degree for a `B`–`B` edge.
- Derive an upper bound `h ≤ c₂ + c₃` (with a formally correct finite-set injection or incidence argument).

Define these quantities as convenient finite sets/functions in Lean; if a paper variable `B` is better represented as a support-set filter, specify the actual domain unambiguously.

### D. Three-loss budget at each root label

For every `a∈A`, the high21 root edge `r-a` has at most three possible four-cycle/opposite-edge losses. The primary source gives a stronger usable budget:

```text
Σ_{x∈B, a∈T_x} (|T_x| - 1)
  + (number of original edges inside N_G(a) ∩ B)
≤ 3.
```

The expression is a **nonnegative integer budget**, not permission to treat all potential support connections as selected edges. Prefer deriving the first term as a direct count of distinct four-cycles via `fourCycleOpposites` and the existing type load identity. Derive the second term only after proving that it counts additional, distinct lost incidences, so the two terms do not accidentally count the same loss twice.

If the full strengthened budget is difficult, start with the weaker cross-edge part:

```text
Σ_{x∈B, a∈T_x} (|T_x| - 1) ≤ 3.
```

Use the full budget only where absolutely needed. When a claimed equality uses all three losses, verify that original edges outside the support cannot contribute additional unaccounted repeated incidences.

### E. Four-edge root: exclude a clique of 19 or more edges

The primary paper performs a case split on `c₄`, `c₃`, and `c₂`. Use a direct global contradiction under `Q.card ≥19` if convenient. Alternatively, prove an extraction lemma selecting **exactly nineteen Q-edges while retaining all four root-star Q-edges**; this is needed if following paper equalities such as `T+h=15` verbatim. Extracted Q membership must preserve the full-conflict ≥21 condition and clique property. Never quietly set `Q.card=19` when the theorem assumes only `Q.card≥19`.

With exactly nineteen selected edges, `T+h=15` and `T≤12` imply `h≥3`.

**Case E1. `c₄ ≥1`:** type-4 contribution consumes all three units of the budget at every root label; remaining multiple types are limited and `h=0`, contradictory to `h≥3`. Prove the bound with original degree constraints and type union, not merely a tabular assertion.

**Case E2. `c₃ ≥1`:** there is at most one triple-type vertex. Its three labels each have only one unit of remaining budget; at most three compatible double-type vertices may remain. Show that either `h≤2` or, if there are three double types, they cannot supply the necessary complementary pair. Thus `h<3`.

**Case E3. `c₃=c₄=0`:** all types are singleton or double. Put `k=c₂`; derive `3≤k≤6` in a 19-edge candidate. Selected `B`–`B` edges join only complementary double types and form a graph of maximum degree ≤2. Analyse:

- `k=3`: too few double-type vertices to supply the ≥3 required `B`–`B` edges.
- `k=4`: `h=3` gives a four-vertex path with internal saturated tips; `h=4` gives a four-cycle. Use selected singleton edges and degree saturation/missing-edge budget to exclude both.
- `k=5`: `h=3` or `4`. For `h=3`, all twelve `A`–`B` original edges must be selected and a singleton tip has more than four original neighbours. For `h=4`, a path or four-cycle-plus-isolated-tip structure yields a saturated complementary-type tip whose missing selected `A`–`B` edges exceed the budget.
- `k=6`: there are six double types and no singleton types. The root budget is used up at every label, so edges inside `B` may only join complementary types. Their maximum original degree is two. Prove the selected `B`–`B` strong clique has size ≤4 (path/even-cycle argument). Then show at least five double-type vertices would need to have **both** root-neighbour edges selected, whereas a separate lemma allows at most four such fully selected vertices. Contradiction.

The preceding is a **research proof plan**, not an inventory of Lean facts already established. Review every saturation argument. The full constraints in the source are more precise than this summary; consult them whenever a type case appears ambiguous.

### F. Auxiliary lemmas to prioritise

A useful order, subject to local code reuse:

1. `high21_local_no_triangle` and `high21_cover_inside_card_le_three`.
2. `high21_root_label_budget_three` with exact finite-set summation.
3. `root_types_nonempty_of_root_four` and `outer_edge_types_cover_four`.
4. `root_type_counts` and the arithmetic `S ≤12`, `T≤S`, `Q.card=4+T+h`, `h≤c₂+c₃`.
5. `high21_full_double_tips_card_le_four`, including the case in which two different double types overlap at a root label.
6. `high21_selected_double_edges_bipartite`, with complementary-type pairs and selected support degree ≤2.
7. `high21_root_four_card_le_eighteen`.
8. A bound `high21_support_degree_le_three` proven either via Path B1 or Path B2.
9. `high21_clique_card_le_eighteen` by splitting selected support degree ≤3 vs four.

These are **suggested names**, not mandatory declarations. Use existing checked helper lemmas and avoid reproducing a large complex generic library unnecessarily.

## 4. The essential integration task

After obtaining the unconditional high21 theorem, build a new constructor accepting only `high20`:

```lean
-- Illustration of the desired logical dependency. Adapt to actual record/API.
theorem StrongEdge.minimalCliqueBounds20_of_high20
    (G : SimpleGraph V)
    (hΔ : ∀ x, G.degree x ≤ 4)
    (high20 : ∀ (Q : Finset G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet) →
      (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) →
      Q.card ≤ 19) :
    StrongEdge.MinimalCliqueBounds20 (StrongEdge.conflictGraph G) := by
  ...
```

Fill the record with the newly proved high21 bound and the previously proved high22/high23/high24 bounds. Never weaken the record by removing fields or changing conflict-degree semantics. Add an original-edge result with the intended shape:

```lean
theorem StrongEdge.induced_matching_packing20_of_high20
    (G : SimpleGraph V)
    (hΔ : ∀ x, G.degree x ≤ 4)
    (high20 : ∀ (Q : Finset G.edgeSet),
      (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet) →
      (∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) →
      Q.card ≤ 19)
    (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet,
      M ⊆ F ∧
      StrongEdge.IsInducedMatching G (M : Set G.edgeSet) ∧
      F.card ≤ 20 * M.card := by
  ...
```

This remains a **conditional** 20-packing theorem because high20 has not yet been discharged. Do not export an unconditional `packing20` unless a fully verified proof of high20 is also available.

## 5. Formal correctness and engineering constraints

**Forbidden ways of obtaining an apparently successful build:**

- No `sorry`, `admit`, `sorryAx`, custom `axiom`, `constant` used as a proof, `unsafe`, `native_decide`, or opaque native computations masquerading as kernel proofs.
- No importing a theorem whose signature contains an extra unproved structural condition and then hiding it behind typeclass arguments, instance inference, structures, or coercions.
- No changing the definitions of original graph adjacency, line graph, conflict graph, induced matching, clique, or candidate-set restrictions.
- No replacing `G` with a subgraph without proving exactly which original conflicts are preserved. Removing a non-Q edge can remove a conflict witness.
- No assuming `G` is 4-regular, triangle-free globally, 4-cycle-free globally, connected, or support-closed.
- No equating selected incidence degree in `Q` with original vertex degree or with full edge conflict degree.
- No acceptance based on test graphs, random enumeration, Python brute force, or `decide` on a finite number of examples in place of the universal theorem.
- No counting an internal edge twice in an injective cardinality bound, and no treating `S=T` merely because `S≤12`.

Normal uses of Lean proof automation, `omega`, `linarith`, `simp`, `aesop`, `finite` counting, and appropriately proved finite lemmas are welcome. Preserve source-level clarity over excessive tactic compression in the most delicate arguments.

Existing validated declarations should stay intact. Prefer new modules, importing earlier checked bounds. If a pre-existing definition truly must change for correctness, stop and explain the change and its consequences before claiming the old results still apply. Do not overwrite earlier checkpoint ZIPs or logs.

## 6. Acceptance criteria and evidence

**Only mark `high21` DONE when all the following are true:**

1. The exported theorem `high21_clique_card_le_eighteen` has exactly the universal mathematical hypotheses in §1, with no structural record parameter.
2. The new theorem is used to populate `MinimalCliqueBounds20.high21` in a wrapper that leaves **only high20** as an explicit hypothesis.
3. All earlier checked theorems still compile; especially the conditional packing theorem for every original candidate subset, high22, high23 and high24.
4. Full build succeeds without Lean errors or warnings:
   ```powershell
   .\lean.ps1 build
   ```
5. The entire theorem audit succeeds:
   ```powershell
   .\lean.ps1 env lean StrongEdge/Audit.lean
   ```
6. Append `#check` and `#print axioms` entries for **each** new exported theorem and all helper theorems materially relied upon, in `StrongEdge/Audit.lean`. Verify their dependency closures list only the accepted Lean logical axioms (`propext`, `Classical.choice`, `Quot.sound`) or explain any additional dependency.
7. Scan all project `.lean` files for forbidden proof-gap tokens and inspect the exported signatures. The scan is supplementary; the dependency audit is decisive.
8. Check old and new source hashes and actual source diffs against the high22 checkpoint. Record preservation of previous checked modules, or explain every intentional modification.
9. Save the logs, source fingerprints and any useful independently checkable finite certificates under `verification/`.
10. Produce a source-only checkpoint ZIP (sources, docs, pinned configuration, verification logs; no compiler binaries, `.lake`, dependencies or caches).

Suggested artefact names:

```text
verification/high21-baseline-build.log
verification/high21-baseline-axioms.log
verification/high21-build.log
verification/high21-axioms.log
verification/high21-source-sha256.json
verification/high21-source.diff
verification/high21-source-checks.json
verification/high21-audit-checks.json
C5_HIGH21_VERIFIED_HANDOFF.md
../strong_edge_lean_high21_checkpoint.zip
```

These filenames are suggestions, not assumed existing paths. The final handoff must include complete theorem types, actual commands, return statuses, module inventory, preserved-source report, compiler/dependency pins, and the count of audited theorems.

## 7. Partial-progress and blocker protocol

If time, token, dependencies, or a mathematical gap prevents completion, **do not claim success and do not invent a follow-up run**. Save genuinely kernel-verified lemmas and hand off the exact remaining goal.

In that case write `C5_HIGH21_PARTIAL_HANDOFF.md`, including:

- Which declarations are complete and audited; exact theorem signatures.
- Where the current proof stops, the exact failed goal and its hypotheses.
- The mathematical reason for any blocked case and its relation to the pinned paper.
- Reproduction commands and real verification evidence.
- Any counterexample found to an intermediate lemma, with concrete original graph, Q, verified full conflict degrees, and a distinction between **counterexample to an attempted lemma** and **counterexample to the final packing theorem**.
- Any stronger hypothesis temporarily used in a *local* lemma; it must remain visible and must not be presented as the desired unconditional result.

Avoid large blind searches for smaller counterexamples if the proof is stuck. First inspect the mathematical inequality or type case responsible. A genuine counterexample to a proposed auxiliary lemma is useful evidence and must be retained.

## 8. Completion status to communicate precisely

If this task succeeds, the verified chain becomes:

| Structural field | Target | Expected after this task |
|---|---:|---|
| high24 | ≥24 implies clique ≤15 | Already proved via ≤13 |
| high23 | ≥23 implies clique ≤16 | Already proved |
| high22 | ≥22 implies clique ≤17 | Already proved |
| high21 | ≥21 implies clique ≤18 | **Goal of this task** |
| high20 | ≥20 implies clique ≤19 | **Still unproved** |

**Even a successful high21 run does not establish unconditional 20-packing, the 19.5 strengthening, or integer strong-edge 20-colourability.** The very next structural target would be high20 ≤19. Document that distinction explicitly.

## 9. Do the work in this run

Inspect the local project; reproduce its baseline; choose the most economical mathematically valid high21 proof; edit and compile the Lean modules; run the full audit; and prepare a truthful checkpoint or a precise partial handoff. **Do not ask for confirmation of details already specified by this document, and do not report a pending proof as a success.**
