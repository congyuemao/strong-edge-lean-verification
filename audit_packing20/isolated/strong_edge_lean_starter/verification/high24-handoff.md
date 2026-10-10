# C5 high24: verified handoff

Date: 2026-10-09, Australia/Sydney.

**The high24 stage is complete.** For any finite simple graph of maximum
original degree at most four, a clique of original edges whose full conflict
degrees are all at least 24 has at most **13 edges**, hence at most 15. The
proved bound now supplies `MinimalCliqueBounds20.high24`. The other four fields
remain explicit assumptions. Unconditional 20-packing is still not proved.

## Exact mathematical result

In `StrongEdge/Bounds/High24.lean`, the main declaration is:

```lean
theorem StrongEdge.high24_clique_card_le_thirteen
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h24 : ∀ e ∈ Q, 24 ≤ (StrongEdge.conflictGraph G).degree e) :
    Q.card ≤ 13
```

The companion `StrongEdge.high24_clique_card_le_fifteen` has exactly the same
hypotheses and conclusion `Q.card ≤15`. Both signatures are printed in
`high24-axioms.log`. Neither depends on a threshold record, a further clique
bound, a global girth assumption, a classification hypothesis, or an external
computation. Original edges outside `Q` remain available as conflict witnesses.

## Proof and all new declarations

All names below are in namespace `StrongEdge`. This stage adds 13 theorems and
one finite-set definition. All 13 theorems have individual `#print axioms`
entries in `StrongEdge/Audit.lean`.

`StrongEdge/Bounds/High24.lean` contains:

| Declaration | Meaning and important assumptions |
|---|---|
| `conflict_degree_eq_24_of_ge` | C4 turns degree ≥24 into degree =24 under original maximum degree four. |
| `branchEdges` (definition) | Filters `Q` for edges incident to a branch vertex `a` and avoiding its centre `u`. |
| `mem_branchEdges` | Exact membership equivalence for that filter. |
| `high24_edge_not_between_neighbors` | A degree-24 edge cannot join two neighbours of a common vertex; uses local triangle exclusion. |
| `high24_external_conflict_adj` | Distinct branches at one centre, conflicting degree-24 edges, and outer endpoints distinct from the centre force adjacency of those outer endpoints. |
| `high24_distinct_branches_ne` | Edges incident to different neighbours of one centre are distinct if the first has degree 24; equality would create a forbidden triangle. |
| `high24_mixed_branches_cannot_have_fork` | In an all-degree-24 conflict clique, two distinct edges in one branch exclude an edge in a different branch of the same centre. |
| `branchEdges_card_le_three` | Under maximum original degree four, a branch adjacent to its centre contains at most three edges avoiding that centre; no clique premise is needed. |
| `high24_branch_union_card_le_three` | For an all-degree-24 conflict clique and at most three neighbours of a centre, their branch union has at most three edges. |
| `high24_side_card_le_three` | Applies the preceding result to the three other neighbours on one side of any fixed original edge. The same theorem applies after swapping endpoints. |
| `high24_clique_card_le_thirteen` | The universal high24 clique bound stated above. |
| `high24_clique_card_le_fifteen` | The bound required by the minimal packing interface. |

The structural lemmas use the existing original maximum-degree-four hypothesis
and the stated edges' full conflict degree 24. The branch-union lemmas also
explicitly require the clique condition. These premises are all discharged in
the final theorem from `hΔ`, `hQ`, and `h24`.

The local argument follows the branch portion of
[critical_support.md, section 2, at the supplied commit](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/critical_support.md).
For two edges from distinct branches, local triangle and four-cycle exclusions
eliminate every conflict connection except adjacency of their outer endpoints.
A third edge forming a fork in one branch would then create a forbidden
four-cycle through a degree-24 edge. If every branch has at most one edge,
three branches give at most three edges. If a branch has two edges, all other
branches are empty, and the degree-four bound gives at most three again.

For nonempty `Q`, fix `uv∈Q`. The full-conflict cover places every other member
in one of the two extra centre stars or two branch unions. Each of those four
sets has cardinality at most three, so `Q.card ≤1+3+3+3+3=13`. The Lean proof
uses a cover and upper bounds on union sizes; it does not assume unproved
disjointness. Empty `Q` is handled explicitly. The stronger seven-edge bound
from the paper was not needed or formalised in this stage.

## Interface integration and remaining obligations

`StrongEdge/High24Packing.lean` contains the two additional theorems:

- `minimalCliqueBounds20_of_high20_high21_high22_high23`: takes `hΔ` and four
  explicitly typed clique-bound hypotheses. It constructs the unchanged
  `MinimalCliqueBounds20` record with
  `high24 := high24_clique_card_le_fifteen G hΔ`.
- `induced_matching_packing20_of_high20_high21_high22_high23`: uses that
  constructor and the preserved packing theorem to obtain, for every original
  candidate edge set `F`, a subset `M` that is an induced matching in the full
  original graph and satisfies `F.card ≤20*M.card`.

Both full exported signatures are printed in `high24-axioms.log`. The only
remaining clique-bound parameters of these new theorems are:

| Parameter | Hypothesis on all members of a full-conflict clique `Q` | Required conclusion |
|---|---|---|
| `high20` | Full conflict degree ≥20 | `Q.card ≤19` |
| `high21` | Full conflict degree ≥21 | `Q.card ≤18` |
| `high22` | Full conflict degree ≥22 | `Q.card ≤17` |
| `high23` | Full conflict degree ≥23 | `Q.card ≤16` |

None of these four universal bounds was proved here. The original
`CliqueThresholds20` is unchanged and still asks for the stronger high24 bound
7. The minimal interface, which suffices for the 20-packing argument, only asks
for 15 and now receives a complete proof of that field.

## Verification actually performed

All commands were run from
`C:\Users\21161\Documents\ChatGPT\math\strong_edge_lean_starter`.

| Exact command | Exit result | Saved evidence in `verification/` |
|---|---|---|
| `.\lean.ps1 build` before edits | 0; 1,127 jobs | `high24-baseline-build.log` |
| `.\lean.ps1 env lean StrongEdge/Audit.lean` before edits | 0; all 38 prior audit entries | `high24-baseline-axioms.log` |
| `.\lean.ps1 build StrongEdge.Bounds.High24` | 0; 1,121 jobs | `high24-module-build.log` |
| `.\lean.ps1 build` after integration | 0; 1,129 jobs; no warnings | `high24-build.log` |
| `.\lean.ps1 env lean StrongEdge/Audit.lean` after integration | 0; 51 audit entries | `high24-axioms.log` |

The final audit contains all 38 previous entries plus all 13 new theorems.
Every dependency list contains only `propext`, `Classical.choice`, and
`Quot.sound`. It includes printed types of both high24 bounds, the constructor,
and the new packing wrapper. A scan of all 13 project Lean files found no
`sorry`, `admit`, `axiom`, `constant`, `unsafe`, or `native_decide` tokens.
`high24-source-checks.json` records the source scan and audit coverage;
`high24-audit-checks.json` records the dependency-list validation.

Intermediate development exposed only routine Lean equality/coercion and
section-parameter issues, all fixed before the final build. The early
`high24-local-build.log` has an unused-instance linter warning subsequently
fixed; `high24-fork-build.log` and the final module build pass without warnings.

The dependency pins remain unchanged:

- Lean: `leanprover/lean4:v4.35.0-rc4`.
- Compiler commit: `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`.
- mathlib commit: `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`.

No `lake update` was run. The new hash manifest,
`high24-source-sha256.json`, covers 13 Lean files and three configuration/lock
files. All nine pre-existing mathematical modules, including both threshold
records and both C4 modules, are byte-for-byte unchanged. Only the root import
module and audit file changed among pre-existing Lean sources.

Before/after Git status and diff-stat snapshots use the names
`high24-git-*-before.txt` and `high24-git-*-after.txt`. The project remains
untracked in the enclosing repository, so Git's diff-stat is empty. The
separate `high24-source.diff` and `high24-change-summary.json` compare source
and documentation against the preserved C4 checkpoint. No commit was made.

The new archive beside the project is
`C:\Users\21161\Documents\ChatGPT\math\strong_edge_lean_high24_checkpoint.zip`.
It contains source, configuration, documentation, and verification evidence;
it excludes compiler binaries, `.lake`, and caches. Earlier logs, manifests,
handoffs, and both earlier checkpoint ZIPs are preserved.

## Mathematical risk and next stage

No counterexample or unresolved mathematical step remains in the high24 proof
or its interface integration. The final bound is a universal Lean proof under
exactly the displayed assumptions, not a finite search result. No claim is made
about the correctness of the four remaining, unformalised clique bounds.

The next target is `high23`: original maximum degree four, a full-conflict
clique, and full conflict degrees at least 23 should imply clique size at most
16. Unlike degree 24, degree 23 does not force all incidence-count inequalities
to be equalities; a next proof must quantify the possible counting losses or
use the separate high-conflict structural argument. The present no-fork lemma
must not simply be reused with its degree-24 hypothesis weakened to 23.

Unconditional 20-packing, the 19.5 strengthening, and integer strong-edge
20-colourability are not established by this checkpoint.
