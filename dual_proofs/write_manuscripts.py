from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output'/'pdf'
old=(OUT/'packing20_manuscript.md').read_text(encoding='utf-8')
refs=old[old.index('## References'):]
core=old[:old.index('## Appendix A.')]
a=core.replace('@subtitle A proof manuscript','@subtitle Route A: the paper-first proof, with a matching Lean formalization')
a=a.replace('An appendix records the correspondence with the audited Lean development.','An appendix identifies the corresponding declarations in the PaperRoute formalization.')
a+=r'''## Appendix A. Formalization of this manuscript

This manuscript retains the mathematical proof of the earlier paper-first exposition. Its corresponding entry point is now **PaperRoute.induced_matching_packing20**, rather than the original **StrongEdge** endpoint. The two developments share mathematical ingredients, but this route explicitly proves the stronger intermediate statements used in the exposition. This is a correspondence between mathematical arguments and formal declarations, not a claim that the prose itself is machine-checked.

The file **ExactCover.lean** proves both directions of the cover characterization and the exact additive identity $c(e)+e_G(C(e))=\sum_{x\in C(e)}d_G(x)$. Natural subtraction in (2.1) is derived from that identity. **UniformLoad.lean** proves one theorem with an arbitrary natural threshold $t$. Its more general internal interface assumes disjointness of the two erased neighbour sets; independence of $A$ supplies that hypothesis in (3.5). The specialized root-load interfaces used by the supporting local proofs instantiate this uniform argument.

**Foundations.lean** proves both exact identities in (3.1), the unspecialized incidence estimate in (3.4), and the triangle degree bound. **Thresholds.lean** assembles Propositions 4.2–4.6, uses the same threshold-free small-type lemma in the $21$ and $20$ cases, and establishes $o\leq1$ and $q\leq17$ in the four-element-type case of Proposition 4.6. **Packing.lean** contains the five-field criterion, its induced-subgraph transfer and the final theorem. **PrivateSemantics.lean** identifies the code's private-vertex predicate with the singleton closed-neighbourhood intersection in Section 5. **Sharpness.lean** proves the doubled-cycle witness and the lower bound on an arbitrary real constant.

@table Manuscript statement | Declaration or module in PaperRoute
@row Exact cover, (2.1) | ExactCover: conflict_iff_meets_cover; conflict_degree_add_inside_eq_sum
@row Uniform slack and load, (3.5) | inside_cover_budget; UniformLoad: root_load_budget
@row Exact root partition, (3.1) | Foundations: selected_card_eq_star_root_outer; root_incidence_eq_star_add_root
@row Lemmas 2.3–2.4 | Library/Bounds/SubcubicEighteen; DegreeTwoClique
@row Lemmas 3.3–3.4 | Library/Bounds/RootCounting; High21Double
@row Lemma 3.5, arbitrary outer subset | OuterSubsets: outer_subset_card_le_four
@row Lemma 3.6 | Thresholds: small_type_clique_bound
@row Propositions 4.2–4.6 | Thresholds: proposition_4_2 through proposition_4_6
@row Stronger four-type case | Thresholds: outer_card_le_one_of_type_four; clique_card_le_seventeen_of_type_four
@row Lemmas 5.1–5.3 | Library/Basic; PrivateExchange; DoubleCount; Packing; PaperRoute/Packing
@row Theorem 1.1 | Packing: induced_matching_packing20
@row Proposition 6.1, real sharpness | Sharpness: doubleC5_matching_card_le_one; twenty_is_necessary_real

The directory **PaperRoute/Library** began as an explicitly recorded namespace fork of the original elementary and local proofs. Its supporting files were then refactored where this route needs exact counting and the unified budget. These shared arguments are not presented as independently discovered proofs. The manuscript-level propositions and the final packing theorem have their own proof terms. The dependency audit checks that this endpoint does not call any **StrongEdge** declaration or the copied library's final packing theorem. The two root-count identities also have their own proofs, even where a later argument only needs their inequality consequences.

The project uses Lean **4.35.0-rc4** and mathlib revision **49fd9dee36e7bbf345fe7981d2de6aeeb591f75b**. The delivery includes build logs, exact source hashes, a declaration-dependency audit and a numbered crosswalk. The accepted foundational axioms are **propext**, **Classical.choice** and **Quot.sound**. The companion Route B manuscript follows the unchanged original formal development. Neither route claims a different global strategy or a new historical priority.

'''+refs
(OUT/'route_a_paper_first.md').write_text(a,encoding='utf-8')

b=core.replace('# Induced Matchings in Prescribed Edge Sets of Graphs of Maximum Degree Four',
'# A Formal-Development Proof of Prescribed-Edge Induced-Matching Packing')
b=b.replace('@subtitle A proof manuscript','@subtitle Route B: a mathematical exposition of the original StrongEdge proof')
b=b.replace('An appendix records the correspondence with the audited Lean development.','The proof follows the original StrongEdge dependency structure: one-sided covers, specialized four-cycle budgets, branch estimates and a five-field packing criterion.')
pos=b.index('All graphs in this manuscript')
b=b[:pos]+'''This manuscript gives the full mathematical argument corresponding to the unchanged original **StrongEdge** proof. It is self-contained: no result from the companion Route A manuscript is assumed. The two expositions share the same overall clique-bound and private-neighbourhood strategy. Here the intermediate statements and case interfaces follow the original formal implementation, including bounds that the code deliberately states more weakly than its internal estimates permit.

'''+b[pos:]
b=b.replace(r'c(uv)=\sum_{x\in C(uv)}d_G(x)-e_G(C(uv))\leq 24-e_G(C(uv)).',
            r'c(uv)+e_G(C(uv))\leq\sum_{x\in C(uv)}d_G(x)\leq24.')
start=b.index('**Proof.** An edge other than $uv$ conflicts')
end=b.index('**Lemma 2.2',start)
b=b[:start]+r'''**Proof.** Every edge conflicting with $uv$ meets $C(uv)$. If it shares an endpoint with $uv$, its other endpoint lies in the cover. Otherwise a length-two path in the line graph supplies an original edge joining an endpoint of $uv$ to an endpoint of the other edge, and that latter endpoint lies in the cover. The converse implication is not needed here.

For any selected edge set $D$ and vertex set $S$, let $m_D(S)$ count edges of $D$ meeting $S$, and let $i_D(S)$ count those with both endpoints in $S$. Counting incidences gives the exact identity

$$ \sum_{x\in S}d_D(x)=m_D(S)+i_D(S).

The conflict neighbours of $uv$ are a subset of the original edges meeting $C(uv)$. Applying this identity with $D=E(G)$ proves the first inequality of (2.1). Each erased neighbour set has at most three vertices, giving the upper bound twenty-four. With $D=Q$, the inclusion of $Q\setminus\{uv\}$ in the edges meeting the cover gives (2.2). This proof only uses inclusions between these edge families. ∎

'''+b[end:]
b=b.replace('Conflicts between edges with endpoints in $P$ are unchanged in the vertex-induced graph $G[P]$. In that graph an endpoint-neighbour cover has at most two vertices, each of selected degree at most two. Hence',
r'''For a selected edge $uv$, use the restricted cover $C(uv)\cap P$. Since both endpoints of every selected edge lie in $P$, every conflicting selected edge other than $uv$ meets this restricted cover. Each endpoint has at most two original neighbours in $P$, so the restricted cover has at most two vertices. Each of these has selected degree at most two. The incidence covering inequality therefore gives''')
b=b.replace('Thus\n\n'+r'$$ q=s+k+o,\qquad s+k=\sum_{a\in A}d_Q(a). \tag{3.1}',
'The implementation uses the resulting covering estimate\n\n'+r'$$ q\leq s+k+o. \tag{3.1}')
start=b.index('If all edges of $Q$ have conflict degree at least $t$')
end=b.index('**Lemma 3.2',start)
b=b[:start]+r'''Write $L_a=\sum_{x\neq r,\ a\in T(x)}(|T(x)|-1)$ for the load at a selected label. The original development proves four specialized estimates. With $c(Q)\geq j$ meaning $c(e)\geq j$ for every $e\in Q$, these are

@table Hypothesis | Specialized load bound (3.5)
@row $c(Q)\geq23$ | $L_a\leq1$
@row $c(Q)\geq22$ | $L_a\leq2$
@row $c(Q)\geq21$ | $L_a\leq3$
@row $c(Q)\geq20$, with $A$ independent | $L_a\leq4$

The last implication requires independence of $A$. For the first three, it is sufficient that the selected root edge has the stated threshold, even without independence of the entire root neighbourhood.

**Proof.** An outer edge $xy$ conflicts with every selected $ra$. Since its endpoints are outside $A\cup\{r\}$, this requires $xa$ or $ya$. Thus $R\subseteq T(x)\cup T(y)$. The neighbours counted by $d_O(x)$ are outside $A$, disjoint from those counted by $T(x)$, proving $d_O(x)+|T(x)|\leq4$. Each label has at most three neighbours other than $r$; counting label--multiple-vertex incidences gives $\sum_{x\in P}|T(x)|\leq12$ and $|P|\leq6$.

To prove the specialized bounds, fix the selected edge $ra$. Let $X(ra)$ consist of ordered pairs $(b,x)$ with $b\in N_G(r)\setminus\{a\}$, $x\in N_G(a)\setminus\{r\}$ and $bx\in E(G)$. These are the ordered opposite edges of four-cycles through $ra$.

At thresholds $23$, $22$ and $21$, the cover has exactly six vertices: a smaller cover would give $c(ra)\leq20$. Consequently both endpoints have degree four and their two erased neighbour sets are disjoint. The map $(b,x)\mapsto bx$ is injective on $X(ra)$, since swapping the endpoints would violate this disjointness. Each image is an original edge inside $C(ra)$. Inequality (2.1) bounds the number of internal edges by one at threshold $23$, two at threshold $22$, and three at threshold $21$. Thus $|X(ra)|\leq1,2,3$, respectively.

At threshold $23$, the implementation also uses the following explicit uniqueness statement: any two ordered opposite edges are equal. Indeed their unordered images lie in a set of size at most one, and disjointness fixes the orientation. At thresholds $22$ and $21$, it uses the corresponding cardinality bounds on the full ordered family.

For threshold $20$, a triangle is still possible and the six-vertex argument cannot be used. Instead assume $A$ independent. Then $A\setminus\{a\}$ and $N_G(a)\setminus\{r\}$ are disjoint, so the same injection is valid. Inequality (2.1), using only $|C(ra)|\leq6$, bounds the internal edges by four. Finally, for each fixed $x$ adjacent to $a$ other than $r$, the possible first coordinates are exactly $T(x)\setminus\{a\}$. Hence $|X(ra)|=L_a$, proving all four specialized assertions. ∎

All these families use original neighbours, including vertices outside the support of $Q$. The first bound is implemented through ordered-pair uniqueness; the other thresholds retain separate cardinality and root-load declarations. No threshold-parametric theorem is assumed in this route.

'''+b[end:]
b=b.replace('Equation (3.5) gives','The corresponding specialized bound in (3.5) gives')
b=b.replace('Equation (3.5) now supplies','The threshold-twenty clause of (3.5) now supplies')
b=b.replace('If every type has size at most two, use Lemma 3.6. Otherwise choose',r'''Suppose first that every type has size at most two. At a selected label $a$, every multiple vertex containing $a$ contributes at least one to $L_a$. The threshold-twenty-one load bound therefore gives at most three such multiple vertices. Every label is selected because $s=4$. Double-counting incidences gives

$$ 2|P|\leq\sum_{x\in P}|T(x)|=\sum_{a\in A}|\{x\in P:a\in T(x)\}|\leq3|A|\leq12.

Thus $|P|\leq6$. If there is a selected singleton tip, Lemma 3.3 gives $|B|\leq6$; otherwise $B\subseteq P$ gives the same bound. Lemma 3.4 bounds fully selected doubles by four, so $k\leq|B|+|D_2|\leq10$. Lemma 3.5 gives $o\leq4$. The covering inequality (3.1) yields $q\leq4+10+4=18$. This is the specialized high21 small-type argument: its multiple-vertex bound is obtained from the high21 loads. The threshold-free count in Lemma 3.6 is used later in the high20 case.

Otherwise choose''')
b=b.replace(r'Therefore $yz$ is the only possible outer edge. Equation (3.2) gives $q\leq 17$, a contradiction.',
r'''Therefore there is at most one outer edge avoiding $x$. Partition $O$ into edges incident with $x$ and edges avoiding $x$. The degree inequality $d_O(x)+|T(x)|\leq4$ bounds the former family (in fact, it is empty). The original branch interface records the sufficient estimate $o\leq2$, and (3.2) gives its declared bound $q\leq18$, a contradiction. The stronger consequence seventeen is not needed by this interface.''')
b=b.replace(r'$q=s+k+o\leq',r'$q\leq s+k+o\leq')
b=b.replace('Equation (3.1) yields','The covering inequality (3.1) yields')
b=b.replace('Now (3.1) gives','Now the covering inequality (3.1) gives')
b=b.replace('Equation (2.1) shows','Inequality (2.1) shows')
b=b.replace(r"**Lemma 3.5 (Complementary doubles on outer edges).** Suppose $s=|A|=4$, $A$ is independent, and both endpoints of every edge in $O'\subseteq O$ have type size at most two. Then $|O'|\leq 4$.",
r"""**Lemma 3.5 (Two outer-edge bounds).** Suppose $s=|A|=4$ and $A$ is independent. If every type has size at most two, then $|O|\leq4$. If there is a vertex $x_0\neq r$ such that every type other than $T(x_0)$ has size at most two, then at most four outer edges avoid $x_0$.""")
b=b.replace(r"**Proof.** Equation (3.3) implies that the endpoint types of each edge in $O'$",
r"""**Proof.** Let $O'$ be all of $O$ in the first case and the outer edges avoiding $x_0$ in the second case. In either case all endpoints of its edges have type size at most two. Equation (3.3) implies that the endpoint types of each edge in $O'$""")
b+=r'''## Appendix A. Original Lean route and dependency structure

The formal endpoint for this manuscript is **StrongEdge.induced_matching_packing20**. Its original source and configuration files are delivered unchanged. The human argument above expands the finite-set injections, equality cases and exchange arguments into ordinary mathematical prose. It preserves the original proof's one-sided cover interface, ordered four-cycle families, specialized threshold bounds and the deliberately sufficient bound eighteen in the four-element-type high20 branch.

The code's selected root-edge family excludes edges incident with the root, despite the informal phrase “root edge” sometimes meaning an edge incident with $r$. Here the star consists of selected $ra$ edges and $K$ is the implementation's **rootEdges** family. **rootTips** corresponds to $B$, **multipleTips** to $P$, and **outerEdges** to $O$.

@table Manuscript result | Original StrongEdge module or declaration
@row Lemma 2.1, one-sided cover and incidence identity | Bounds/ConflictDegree; Bounds/EdgeCounting
@row Lemmas 2.3–2.4 | Bounds/SubcubicEighteen; Bounds/DegreeTwoClique
@row Ordered four-cycle uniqueness, threshold 23 | Bounds/High23Local; Bounds/High23Support
@row Specialized loads 22, 21 and 20 | Bounds/High22Support; Bounds/High21Support; Bounds/High20Local
@row Root covering counts, singleton tips | Bounds/RootCounting; Bounds/High22Subcubic
@row Doubles and complementary outer endpoints | Bounds/High21Double; Bounds/High21RootFour
@row Proposition 4.2 | Bounds/High24: high24_clique_card_le_thirteen
@row Proposition 4.3 | Bounds/High23: high23_clique_card_le_sixteen
@row Proposition 4.4 | Bounds/High22: high22_clique_card_le_seventeen
@row Proposition 4.5 | Bounds/High21: high21_clique_card_le_eighteen
@row Proposition 4.6 | Bounds/High20: high20_clique_card_le_nineteen
@row Optimality and double count | Basic; PrivateExchange; DoubleCount; Packing
@row Five-field criterion and candidate restriction | MinimalPacking
@row Final entry point | High20Packing: induced_matching_packing20

The implementation first proves the high24 bound thirteen and then exposes the weaker fifteen required by **MinimalCliqueBounds20**. The high23, high22, high21 and high20 packing modules successively assemble the remaining fields. The final theorem has no unresolved structural premise. A historical record demanding seven at threshold twenty-four is not used by this endpoint; importing a file containing that record does not mean the proof assumes it.

The private predicate in the code states that $x=v$ or $xv$ is an edge, and that no other member of $I$ equals or is adjacent to $x$. For $v\in I$ this is exactly $N_J[x]\cap I=\{v\}$. The degree-sum minimization is over maximum independent sets; it does not impose regularity or a minimum degree on $G$.

The sharpness witness in Section 6 is supplied in a separate checked audit file, because the original final theorem states existence and does not itself encode optimality of the constant. Its additional real-constant theorem does not modify the original sources. The graph is encoded on **Fin 10**, with adjacency between the two-vertex clusters consecutive modulo five.

The delivery pins Lean **4.35.0-rc4** and mathlib **49fd9dee36e7bbf345fe7981d2de6aeeb591f75b**. Original-source hashes are compared with the independent audit snapshot. The final theorem's actual type-and-proof dependency closure is checked for admitted terms, extra axioms, unsafe declarations and unexpected project endpoints. The companion route does not contribute any declaration to this original proof.

The global mathematical strategy is shared with Route A. The main differences are the intermediate interfaces, the organization of local estimates, the reuse of a threshold-free lemma, and the strength of one branch bound. These facts do not justify a claim of two unrelated discoveries. The literature qualifications in Section 1 apply equally to both routes.

'''+refs
(OUT/'route_b_lean_first.md').write_text(b,encoding='utf-8')
print('Wrote complete manuscripts:',len(a.split()),len(b.split()),'words.')
