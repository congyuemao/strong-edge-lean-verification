# Strong-edge packing: Lean formalisation

C4 and the `high24`, `high23`, and `high22` clique bounds are complete. In every finite
simple graph of maximum degree four, every original edge has full conflict
degree at most 24. Every conflict clique whose members all have full conflict
degree at least 22 has at most **17** edges; at threshold 23 the proved bound
is **16**, and at threshold 24 it is **13**, supplying the required `high24 ≤15` field.
The unconditional 20-packing theorem is **not yet proved**: `high20` and `high21`
remain open in this formalisation.

Verified on 9 October 2026: the full build passed (1,144 jobs) and all 145 audited
theorems use only `propext`, `Classical.choice`, and `Quot.sound`. No proof gaps
or custom axioms occur in these dependency closures. Current evidence is in
`verification/high22-build.log` and `verification/high22-axioms.log`.
All previous logs and checkpoint archives are preserved. See the
[high22 handoff](HIGH22_HANDOFF.md) for this stage's 51 new theorem names,
exact exported signatures, checks, and remaining work. The earlier
[high23 handoff](HIGH23_HANDOFF.md),
[high24 handoff](verification/high24-handoff.md), and
[C4 report](verification/NEXT_STAGE_REPORT.md) record the preceding stages.

## Verified mathematical core

- `Basic.lean`: all-original-edge conflicts and the private-clique exchange.
- `Conflict.lean`: independence/induced-matching equivalence and the inequality
  from candidate conflict degree to full conflict degree.
- `PrivateExchange.lean`: existence of a maximum independent set with minimum
  ambient degree sum, and the degree-monotonicity exchange.
- `DoubleCount.lean`: closed-neighbourhood incidence counting and
  `2 * Fintype.card W ≤ ∑ v ∈ M, (degree v + 1 + privateCard v)`;
  an explicit local bound implies packing, including the conditional 20 bound.
- `Tests.lean`: in the path 0-1-2-3 the outer edges conflict; after removing 1-2
  they do not. Restricting candidates retains the original conflict.
- `Bounds/ConflictDegree.lean`: an incidence cover proves
  `conflict_degree_le_24` directly from the original maximum-degree-four bound.
- `Bounds/ConflictRigidity.lean`: equality at 24 forces both endpoints and their
  six other neighbours to have degree four; those six vertices are independent,
  neither endpoint lies in a triangle, and the fixed edge lies in no four-cycle.
- `MinimalPacking.lean`: a separate, weaker interface suffices for 20-packing;
  the degree-24 clique bound need only be 15. The new original-edge wrapper
  supplies C4 automatically and retains the five clique bounds explicitly.
- `Bounds/High24.lean`: mixed branches cannot contain a fork; each side has
  at most three external clique edges, giving `high24_clique_card_le_thirteen`
  and its `high24_clique_card_le_fifteen` corollary.
- `High24Packing.lean`: constructs `MinimalCliqueBounds20` using the proved
  high24 bound and four explicit lower-threshold hypotheses, then exports the
  corresponding original-edge packing theorem.
- `Bounds/EdgeCounting.lean`: exact incidence counting, with one duplicate
  per internal edge, and clique bounds from selected incidence degrees.
- `Bounds/High23Local.lean`: a high23 edge has degree-four endpoints, lies in
  no triangle, and lies in at most one four-cycle.
- `Bounds/High23Support.lean`: root-neighbour types have size at most two;
  double types sharing a selected root label belong to the same vertex.
- `Bounds/High23Outer.lean`: at most two clique edges lie outside a root's
  closed neighbourhood when it has at least three selected incident edges;
  selected incidence degrees at most three imply a clique bound of 14.
- `Bounds/High23Four.lean`: a four-edge root star has at most six singleton-type
  edges and at most four multiple-type edges meeting its neighbourhood.
- `Bounds/High23.lean`: combines the support-degree cases to prove
  `high23_clique_card_le_sixteen` from the original degree bound alone.
- `High23Packing.lean`: supplies both high23 and high24 to the unchanged minimal
  record, leaving only high20, high21, and high22 explicit in the packing wrapper.
- `Bounds/High22Local.lean`: degree-four endpoints, no triangle on a selected
  high22 edge, and at most two internal cover edges and four-cycles.
- `Bounds/RootCounting.lean`: a singleton-type selected edge restricts all
  selected tips to at most six vertices; generic root and outer incidence counts.
- `Bounds/High22Support.lean`: proves the root-label two-loss budget and bounds
  multiple-type vertices, including the triple-type case.
- `Bounds/High22RootFour.lean`: a clique containing a four-edge root star has
  at most 17 edges, by selected-tip counts and original-degree saturation.
- `Bounds/High22Heavy.lean`: for a three-edge root, at most three vertices meet
  two selected root labels; at most six selected edges lie outside its closed
  neighbourhood, with precise equality consequences.
- `Bounds/High22Subcubic.lean`: excludes the equality case to prove high22 ≤17
  when selected support degrees are at most three. This theorem retains the
  high22 hypothesis; a threshold-free subcubic bound is not claimed.
- `Bounds/High22.lean`: combines the two support-degree branches to prove
  `high22_clique_card_le_seventeen` under exactly the requested assumptions.
- `High22Packing.lean`: supplies high22 to the preserved constructor and exports
  packing with only high20 and high21 as explicit structural assumptions.

`Packing.lean` extends the conditional result to every candidate subset and
states it in terms of original edges. It passed the full build and axiom audit.
Both threshold records and all eighteen earlier mathematical source modules
are unchanged. No claim is made that a maximum-degree-four original graph has
yet been shown to satisfy either threshold record without the two remaining
clique hypotheses. The original record's stronger high24 bound 7 is still open.

## Pinned environment

- Lean: `leanprover/lean4:v4.35.0-rc4`
- Lean compiler commit: `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`
- mathlib: `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`
- Dependency lockfile: `lake-manifest.json`

The Windows compiler was downloaded from the official Lean release and verified
against SHA-256 `549c0d70f58346be61d9353b5ff8b3d89430b49184d1833244ba2f3afca3dabd`.
It lives beside this project in `../.tools/lean-4.35.0-rc4-windows`; `lean.ps1`
uses it when available, otherwise it uses Lake from PATH. Compiler binaries,
dependency checkouts, and caches are excluded from the source archive.

## Reproduce

In this project's Windows PowerShell directory:

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

With Lean/elan already installed on another system:

```sh
lake exe cache get Mathlib.Combinatorics.SimpleGraph.Clique Mathlib.Combinatorics.SimpleGraph.LineGraph Mathlib.Tactic.ByContra Mathlib.Tactic.Linarith Mathlib.Tactic.Tauto Mathlib.Algebra.Order.BigOperators.Group.Finset
lake build
lake env lean StrongEdge/Audit.lean
```

Keep the supplied lockfile; `lake update` is not needed for an ordinary rebuild.
The first build may need network access to materialize locked dependencies.

## Checked endpoint

The current endpoint is
`StrongEdge.induced_matching_packing20_of_high20_high21`.
It takes the original degree bound `hΔ` and exactly two explicit clique-bound
parameters, with the meanings in the table below. It constructs the old `hb`
record by supplying `high22_clique_card_le_seventeen`, `high23_clique_card_le_sixteen`, and
`high24_clique_card_le_fifteen` automatically and calls the
preserved `StrongEdge.induced_matching_packing20_of_minimal_clique_bounds`:

```lean
(hΔ : ∀ x, G.degree x ≤ 4)
(hb : MinimalCliqueBounds20 (conflictGraph G)) (F : Finset G.edgeSet) :
  ∃ M ⊆ F, IsInducedMatching G (M : Set G.edgeSet) ∧ F.card ≤ 20 * M.card
```

The finite-vertex and decidability instances are shown in full in the axiom log.
The old wrapper still takes `hb`; the new wrapper discharges its high22, high23,
and high24 fields and retains high20 and high21 explicitly. The old
`induced_matching_packing20_of_thresholds` is also preserved and audited.
The private-clique, degree-exchange and double-counting proofs have no such
structural premises. Empty graphs and empty candidate sets require no exception.

The source scan found no `sorry`, `admit`, `axiom`, `constant`, `unsafe`, or
`native_decide` tokens in the twenty-eight project Lean files. The axiom audit, rather than that textual
scan alone, checks the exported proof dependencies. Source/configuration SHA-256
fingerprints are saved in `verification/high22-source-sha256.json`.
Earlier source manifests are retained as historical snapshots.

## Still required

For every clique `Q` in the **full** conflict graph, `MinimalCliqueBounds20`
requires the following five facts. The last three have now been proved universally.

| Field | Lower bound on every member's full conflict degree | Required bound on `Q.card` | Status |
|---|---:|---:|---|
| `high20` | 20 | 19 | Open |
| `high21` | 21 | 18 | Open |
| `high22` | 22 | 17 | Proved |
| `high23` | 23 | 16 | Proved |
| `high24` | 24 | 15 | Proved, with stronger bound 13 |

Next, formalise `high21`, followed by `high20`.
Discharging the two open fields yields the unconditional theorem through the
new wrapper. The original
record additionally includes maximum degree 24 (now proved for these conflict
graphs) and uses the stronger degree-24 clique bound 7. The 19.5 strengthening
remains a later, separate goal.

The current result is conditional; it proves neither unconditional 20-packing
nor integer strong-edge 20-colourability. The input handoff is retained in
`LEAN_20_PACKING_HANDOFF.md`; its original uncompiled-starter descriptions are
historical. This README and the saved build/audit logs describe the current code.

## Mathematical source

[Research proof at the supplied commit](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/packing_private_cliques.md).

[High23 proof at the same commit](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_23_improved.md).
This implementation uses a uniform outer-edge bound of two to obtain the
required 16; the optional strengthening to 15 is not exported.

[High22 threshold proof at the same commit](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_thresholds.md).
The high22 implementation uses shorter selected-tip and equality arguments
described in `HIGH22_HANDOFF.md`. The optional high22 bound 16 is not exported.
