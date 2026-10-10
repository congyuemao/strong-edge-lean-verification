# Codex task: discharge `high20` and finish the unconditional 20-packing theorem

**Stage:** C5 `high20 ≤ 19` → C6 unconditional 20-packing  
**Input checkpoint:** `C5 high21: verified handoff`, dated 2026-10-10 (Australia/Sydney)  
**Language/toolchain:** Lean 4 + pinned mathlib, using the existing Windows project  
**Scope:** Modify the existing Lean workspace in place. Do not restart the project or silently substitute a different theorem.

## 0. What you must deliver

The current Lean project has kernel-checked the following universal *full-original-graph* clique bounds for finite simple graphs of maximum original degree at most four:

| Field in `MinimalCliqueBounds20` | Premise for every `e ∈ Q` | Verified bound |
|---|---:|---:|
| `high24` | full conflict degree ≥24 | `Q.card ≤ 15` (indeed ≤13) |
| `high23` | full conflict degree ≥23 | `Q.card ≤ 16` |
| `high22` | full conflict degree ≥22 | `Q.card ≤ 17` |
| `high21` | full conflict degree ≥21 | `Q.card ≤ 18` |
| **`high20`** | full conflict degree ≥20 | **`Q.card ≤ 19`, not yet proved** |

The existing theorem `StrongEdge.induced_matching_packing20_of_high20` already proves the original-edge 20-packing theorem, **conditional on the single explicit `high20` premise**. Your task is to prove that premise from the maximum original degree four assumption and then export a theorem with no clique-bound parameter.

The final unconditional result must assert, for **every** finite simple graph `G` of maximum degree four and **every** finite candidate edge set `F`:

```lean
(hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
  ∃ M : Finset G.edgeSet,
    M ⊆ F ∧ StrongEdge.IsInducedMatching G (M : Set G.edgeSet) ∧
    F.card ≤ 20 * M.card
```

`IsInducedMatching G` and strong conflicts must always be evaluated in the **whole original graph `G`**, including original edges outside `F` or outside a clique `Q`.

A success report requires an actual successful `lake build`, an actual Lean kernel axiom audit, and the exact printed unconditional theorem signature. Merely supplying a conditional wrapper or a manually verified computation **does not count**.

## 1. Repository and baseline: inspect before editing

Work in the user's **current, existing** `strong_edge_lean_starter` workspace and start with its most recent high21 checkpoint; the previous 2026-10-10 report is authoritative for checkpoint identity, but not a substitute for inspecting current files.

Before changing code:

1. Read `README.md`, the current `StrongEdge.lean`, `StrongEdge/Audit.lean`, the pinned `lean-toolchain`, `lake-manifest.json`, and the most recent `verification/high21-*.log` / source hashes.
2. Inspect declarations in `StrongEdge/Bounds/High21.lean`, `StrongEdge/Bounds/SubcubicEighteen.lean`, `StrongEdge/Bounds/High21Support.lean`, `StrongEdge/Bounds/High21Double.lean`, `StrongEdge/Bounds/High21RootFour.lean`, `StrongEdge/Bounds/RootCounting.lean`, `StrongEdge/High21Packing.lean`, and older counting / type modules. Follow existing names and definitions rather than rebuilding equivalents.
3. Verify the baseline with the actual workspace and record logs, exit status, and baseline file hashes:

   ```powershell
   .\lean.ps1 build
   .\lean.ps1 env lean StrongEdge/Audit.lean
   ```

4. Preserve the existing 192 audited declarations and all historical checkpoints. Do **not** silently reset the repository, update mathlib, or overwrite user changes. Save a reproducible baseline snapshot of the files you intend to touch.
5. If the current files differ from the reported high21 state, inspect and reconcile the differences first. Do not pretend that a previous local report guarantees the current tree is unchanged.

Pinned environment from the supplied report:

- Lean: `leanprover/lean4:v4.35.0-rc4`.
- Compiler commit: `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`.
- mathlib commit: `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`.

Do not run `lake update` merely to make a proof compile.

## 2. Exact mathematical target

Aim for a theorem with this *mathematical* signature; retain the project's actual type class and coercion conventions:

```lean
theorem StrongEdge.high20_clique_card_le_nineteen
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj]
    [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4)
    (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) :
    Q.card ≤ 19
```

The final theorem must have no hypotheses about: girth, regularity, connectedness, a maximal clique, equality of selected and full conflict degree, a support-closure property, a preclassified extremal graph, or any previously unproved clique bound. All such properties, if needed, must be **derived** from `hΔ`, `hQ`, and `h20`.

Prove `MinimalCliqueBounds20 (conflictGraph G)` from `hΔ` by supplying all five verified fields, then apply the existing packing theorem for an arbitrary `F`.

### Equivalent intermediate target that may be easier

The following statement is enough, and is likely simpler than classifying all 20-edge strong cliques:

> Every strong clique `Q₀` of **exactly 20** original edges in a maximum-degree-four graph contains at least one edge whose **full original** conflict degree is at most 19.

In symbols,

```text
Δ(G) ≤ 4 ∧ IsClique(Q₀) ∧ |Q₀| = 20
    ⇒ ∃ e ∈ Q₀, fullConflictDegree_G(e) ≤ 19.
```

Given a high20 clique of size at least 20, extract a 20-element subclique. Its selected edges still have full conflict degree at least 20. The intermediate target yields a contradiction. Do not assume the precise name of a mathlib `Finset` extraction lemma; search the pinned local source and compile the actual proof.

**Do not accidentally weaken** the intermediate statement to a bound on a degree in the induced conflict graph on `Q₀`. The degree bound must be for the full `conflictGraph G`.

## 3. Relevant mathematical source files (fixed GitHub commit)

Use the unchanged archived research at commit
`3a95c4a9c44475196c42b6eab4749c487d15d59b`:

- [20-edge strong-clique equality classification](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/clique20_rigidity.md) — primary proof of the stronger fact that every 20-edge strong clique is an isolated ten-vertex double-blow-up of `C₅`, and each of its edges has full conflict degree 19.
- [High20/21 stronger bounds](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_20_21_improved.md) — alternate high20 proof with **stronger** bound 18, including the essential treatment of root-neighbourhood triangles at threshold 20. This is an alternate route, not a required target.
- [General support-degree ≤3 strong-clique argument](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/strong_clique_subcubic.md) — older proof; the current Lean checkpoint already supplies a threshold-free bound `≤18`, sufficient to force a four-star root for a 20-edge clique.
- [Original private-clique packing proof](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/packing_private_cliques.md) — target integration.

These are **research proof manuscripts, not Lean certificates**. Independently check all steps as you formalise them. A manuscript claim never substitutes for a kernel proof.

## 4. Proof route A: rule out a 20-clique with high20 degrees

This is the recommended first route because it avoids building a full isomorphism with the double-blown-up `C₅`.

### A1. Reduce the problem to a 20-element clique

Assume a counterexample `Q` with `Q.card ≥ 20`; take `Q₀ ⊆ Q` with `Q₀.card = 20`. All members of `Q₀` retain the same full original conflict degree, and `Q₀` remains a clique.

The high21 checkpoint supplies the **threshold-free** theorem:

```lean
StrongEdge.clique_card_le_eighteen_of_support_degree_le_three
```

Thus some original vertex `r` has selected incidence degree **four** in `Q₀`. Do not confuse selected incidence degree with the degree in the conflict graph. From `hΔ`, this accounts for the entire original neighbourhood `A = N_G(r)`, with four `Q₀` root edges.

### A2. Handle triangles and the original root neighbourhood honestly

**Critical difference from high21/high22/high23:** full conflict degree **20** does **not** automatically forbid triangles through selected edges. Existing high21 `no_triangle_on_edge` lemmas must not be applied by weakening their hypotheses.

Use the original edge-incidence identity and loss budget `24 - 20 = 4` to bound the edges inside relevant six-vertex endpoint covers. In particular, establish enough structure to handle possible edges among the four vertices of `A`.

Two alternative ways are documented in the original sources:

- The `high_conflict_20_21_improved.md` argument shows, under a sufficiently large high20 clique, that a four-Q-star root actually has an **independent original neighbourhood**, by first showing there can be at most one internal edge and then excluding exactly one.
- The `clique20_rigidity.md` proof first allows an internal edge `a = e(G[A])`, deduces `a ≤ 1` from exact clique counting, and then eliminates `a = 1`.

Implement whichever leads to the fewest genuinely new dependencies. A convenient intermediate lemma would be a root-neighbourhood independence result **under the precise high20-and-large-clique hypotheses**, not an unqualified global assertion.

If the root neighbourhood cannot yet be proved independent, keep the number of internal root-neighbourhood edges in all counting identities. Never silently omit selected edges inside `A`.

### A3. Root-type accounting

After proving `A` is independent for the counterexample, use the existing `rootType`, `rootLabels`, `rootTips`, `multipleTips`, `outerEdges`, `rootEdges`, and incidence-counting definitions wherever feasible.

For a vertex `x` outside `{r} ∪ A`, its type is:

```text
T_x = N_G(x) ∩ A.
```

For selected endpoints outside the root-neighbourhood, derive `T_x ≠ ∅`, using the fact that their selected edges conflict with **all four** root-star edges. Every Q-selected outer edge `xy` must satisfy:

```text
T_x ∪ T_y = A.
```

Do not assume edges outside `Q₀` disappear; they remain original conflict witnesses and must count against the original degree-four budget.

The original rigidity proof uses:

```text
S = total number of original A-to-outside edges ≤ 12,
T = number of selected A-to-outside edges ≤ S,
h = number of selected outside-to-outside edges,
c_i = number of outside selected-support vertices of root type size i,
k = c_2 + c_3,
20 = 4 + T + h,
h ≤ k,
2k ≤ S ≤ 12.
```

It follows that `k ∈ {4,5,6}`. These equations depend on precise support and type definitions; **prove** each one and retain degree constraints for outside-support vertices.

### A4. Analyse `k = 4, 5, 6` only as far as needed

The original `clique20_rigidity.md` treats these three cases:

- **`k = 4`:** equality forces the known double-blown-up `C₅` configuration. For this stage, it is sufficient to derive that **one selected edge has full conflict degree ≤19**. A full graph isomorphism and global component classification are optional and should be avoided unless they genuinely simplify the Lean proof.
- **`k = 5`:** the recorded `S=11` and `S=12` subcases lead to degree-saturation or conflict contradictions.
- **`k = 6`:** all non-root support tips have double type. The possible `T,h` values yield a selected 6-cycle, a path/four-cycle-plus-edge configuration, or an impossible bipartite complete adjacency requirement. Each ultimately contradicts the clique condition or the original degree-four bound.

Use `omega`, `omega`-like finite integer arithmetic, `omega`-compatible formulations, and short finite-set counting lemmas rather than inventing an opaque exhaustive case search. Explicit finite enumeration is acceptable **only** when a proved reduction to an exhaustive finite set and a checkable certificate are supplied.

Do not claim that a complete `C₅` classification has been established unless the Lean statement genuinely proves that stronger conclusion.

### A5. Assemble `high20`

Combine the 20-element contradiction with the finite-set subclique-extraction step to export exactly:

```text
high20_clique_card_le_nineteen : Q.card ≤ 19.
```

This must work for empty/small cliques and graphs as well, and must require no new premise beyond original maximum degree, the clique condition, and the full-conflict-degree-at-least-20 condition.

## 5. Proof route B: a direct high20 threshold contradiction

If route A stalls at the full 20-clique classification, consider adapting the **stronger** argument in `high_conflict_20_21_improved.md`. It states that a high20 strong clique actually has size at most **18**.

The manuscript proceeds by excluding internal original edges in a four-edge-star root neighbourhood, then classifying the same external root types with a per-label budget of four repeated counts. The difficult cases are the triple-type configurations and the double-type/saturated-tip arrangements.

This stronger statement would certainly imply `high20 ≤19`, but **do not spend extra work merely to achieve the 18 bound**. A proof of the required 19 bound is a complete success for the present stage.

Useful already-verifed infrastructure:

- Exact original-edge incidence identities from `Bounds/EdgeCounting.lean`.
- Root-type and root-label tools from `High22Support`, `High21Support`, and adjacent modules.
- Selected-tip forcing adjacency, saturation and degree constraints from `RootCounting`, `High21Double`, and `High21RootFour`.
- Threshold-free support-degree-≤3 bound `≤18` from `SubcubicEighteen.lean`.

**Important:** a per-label four-cycle budget of four is weaker than the three-loss high21 budget. Generalise the counting lemma carefully; do not reuse high21 uniqueness, triangle-free, or heavy-type capacity results by silently changing `21` to `20`.

## 6. Possible faster shortcut: use already-verified high21

For a hypothetical 20-edge high20 clique `Q₀`, the proven high21 theorem ensures that at least one member must have full conflict degree **exactly 20**: if all had full degree ≥21, the 20-edge clique would contradict `high21 ≤18`.

This may help focus the four-loss local analysis, especially if the degree-20 edge is chosen as the first local root. It does **not** automatically guarantee that a selected four-star root can be centred at an endpoint of such an edge. Prove any alignment or extra reduction you rely on.

If this shortcut is ineffective, abandon it and continue route A or B.

## 7. What must not happen

The project has repeatedly distinguished genuine Lean proofs from conditional statements. Enforce all of the following:

- **No** `sorry`, `admit`, `sorryAx`, `axiom`, `constant` introduced as a mathematical assumption, `unsafe`, `native_decide`, or trusted external result that hides a gap.
- **No** accidental reliance on the existing `MinimalCliqueBounds20.high20` field when proving that very field; avoid circular dependencies through wrappers.
- **No** hidden `h20` or arbitrary `IsClique` premise in the *final unconditional packing* theorem.
- **No** replacing `conflictGraph G` by a graph obtained after deleting `Q`-external or `F`-external original edges.
- **No** assumption of triangle-freeness, four-cycle-freeness, original regularity, or support closure merely because high21 happened to imply some of them.
- **No** proof from a finite sample list unless there is a formalised reduction to exactly those samples and an accepted verification certificate.
- **No** altering definitions to make the theorem easier or modifying the mathlib/toolchain pins without authorisation.
- **No** interpreting an existing theorem parameter as a discharged theorem; check the fully elaborated exported type.
- **No** claiming a formal proof of integer strong-edge 20-colourability. This stage targets **induced-matching 20-packing only**.

A no-gap text scan supplements, but does not replace, the Lean kernel's `#print axioms` dependency audit. Check the actual theorem type too: a wrongly weakened definition could pass an axiom audit while proving the wrong mathematical claim.

## 8. Integration and exact acceptance conditions

After proving `high20_clique_card_le_nineteen`:

1. Add a new wrapper or theorem exporting `MinimalCliqueBounds20 (conflictGraph G)` from **only** `hΔ`, using the existing verified high21→high24 constructors.
2. Export an unconditionally quantified original-edge packing theorem, for example:

   ```lean
   theorem StrongEdge.induced_matching_packing20
       {V : Type*} [Fintype V] [DecidableEq V]
       (G : SimpleGraph V)
       [DecidableRel G.Adj]
       [DecidableRel (StrongEdge.conflictGraph G).Adj]
       (hΔ : ∀ x, G.degree x ≤ 4)
       (F : Finset G.edgeSet) :
       ∃ M : Finset G.edgeSet,
         M ⊆ F ∧
         StrongEdge.IsInducedMatching G (M : Set G.edgeSet) ∧
         F.card ≤ 20 * M.card := by
       -- use the genuinely established high20 theorem and preserved wrappers
       ...
   ```

   The code above is a **target signature**, not prewritten Lean source; replace the pseudocode ellipsis with a complete proof. If a declaration with this name already exists, inspect it and choose an unambiguous final name rather than shadowing it.
3. Append `#check` and `#print axioms` for every new theorem to `StrongEdge/Audit.lean`. Keep all 192 old audited declarations.
4. Run at least:

   ```powershell
   .\lean.ps1 build
   .\lean.ps1 env lean StrongEdge/Audit.lean
   ```

   Save full final logs and exit codes. Run module builds incrementally as needed.
5. Inspect the **printed complete theorem type** to ensure that the result depends on `hΔ` and ordinary finite/decidable instances only, not on any parameter of type `CliqueThresholds20`, `MinimalCliqueBounds20`, a supplementary high20 lemma, or an unproved graph-property assumption.
6. Verify the complete proof dependency closures use only the permitted Lean logical foundations (`propext`, `Classical.choice`, `Quot.sound`) if that remains the project's accepted policy. Explain and investigate any new axiom rather than disguising it.
7. Preserve historical files and previous mathematical modules. Record any modifications to old proof modules precisely, and run regression tests for the four-vertex path example.
8. Generate SHA-256 manifests, a source diff against the high21 checkpoint, a clear theorem inventory, final pass/fail metadata, and a checkpoint ZIP without compiler binaries, `.lake`, dependency trees, or caches. Do not assume `git diff` captures changes if the workspace remains untracked.

Suggested deliverables:

```text
StrongEdge/Bounds/High20*.lean        # one or more completed proof modules
StrongEdge/High20Packing.lean         # unconditional construction and packing
StrongEdge.lean                       # public imports
StrongEdge/Audit.lean                 # appended type/axiom audits
verification/high20-build.log
verification/high20-axioms.log
verification/high20-source-sha256.json
verification/high20-source.diff
verification/high20-audit-checks.json
verification/high20-status.json
HIGH20_VERIFIED_HANDOFF.md
../strong_edge_lean_high20_checkpoint.zip
```

Adapt filenames to actual project conventions; do not misrepresent absent files as created.

## 9. If the full high20 proof is blocked

Do not end with a claim of success. Instead:

1. Save and kernel-verify every completed intermediate mathematical lemma.
2. State the **first precise unresolved mathematical lemma**, with full Lean type, exact definitions, current hypotheses, and attempted strategies.
3. Explicitly distinguish a Lean elaboration/type-class obstacle from a genuine mathematical gap or possible false lemma. Do not label a failed tactic as a counterexample.
4. If a candidate lemma looks false, seek a small original graph counterexample with actual original edges and full-conflict validation; any finite search result is evidence only for its stated domain.
5. Preserve the known-good high21 state, its hashes, and all old verification logs. If no new theorem is verified, report that candidly.
6. Produce a partial handoff with reproducible source, successful build/audit of the retained work, and exact remaining dependencies.

Avoid unproductive retries with increasingly long timeout windows. A saved, precisely localised mathematical obstacle is more useful than an undocumented failed rewrite.

## 10. Definition and independent-verification checklist

Before calling the final result complete, inspect these points directly:

- [ ] `StrongEdge.conflictGraph G` is defined using **all original edges** as witnesses.
- [ ] `StrongEdge.IsInducedMatching G` agrees with conflict independence on `G.edgeSet`.
- [ ] `high20_clique_card_le_nineteen` has **no** clique-threshold, girth, regularity, support-closure or preclassification parameter.
- [ ] All uses of `G.degree e` / `(conflictGraph G).degree e` are dimensionally correct: original vertex degree and full edge conflict degree are different.
- [ ] The high20 proof never assumes high21's triangle exclusion at degree exactly 20.
- [ ] The high20 proof never uses its own conclusion via an intermediate wrapper.
- [ ] Any extraction of a 20-element subclique preserves original full degree rather than recomputing degree inside the extracted clique.
- [ ] `MinimalCliqueBounds20` is constructed using only `hΔ` and verified structural results.
- [ ] The final packing theorem quantifies over **every** candidate `F`, including `F = ∅`.
- [ ] The full theorem type is printed and checked for hidden premises.
- [ ] The full source builds with the supplied pinned toolchain and mathlib.
- [ ] All new exported theorems pass the per-declaration axiom audit; all old audit entries still pass.
- [ ] Logs, hashes, source diff, and a reproducible handoff are delivered.

### Scope after success

Once the unconditional 20-packing theorem is kernel-checked, stop this stage and report success. The stronger `39/2` no-tight-component packing result, an explicit polynomial-time algorithm proof, possible literature originality, and the longstanding **integer strong-edge 20-colourability conjecture** are separate projects. None is required to declare this specific high20/C6 stage complete.

---

**Central instruction:** Finish the remaining *mathematical* `high20` proof. Do not conceal the missing result behind a parameter, a rewritten definition, or a build-only success report. If this last field is discharged and the final unrestricted wrapper passes Lean's kernel, the arbitrary-candidate-edge-set 20-packing theorem is formally verified.
