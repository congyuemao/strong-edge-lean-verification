# A Corrected 19.5 Bound for Induced Matchings in Prescribed Edge Sets

@subtitle A complete proof manuscript with a correspondence to the verified Lean development
@date 10 October 2026

@abstract

Let $G$ be a finite simple graph of maximum degree at most four, and let $F\subseteq E(G)$ be a prescribed set of candidate edges. We prove that $F$ contains an induced matching $M$ of the original graph satisfying $2|F|\leq39|M|+t_G(F)$, where $t_G(F)$ counts the connected components of $G$ isomorphic to the doubled five-cycle whose entire edge sets belong to $F$. In particular, $|F|\leq19.5|M|$ whenever no such component is fully selected. The proof combines five strengthened conflict-clique bounds with an exchange and private-neighbourhood argument. The main structural steps exclude an eighteen-edge clique of selected maximum degree three, exclude its seventeen-edge boundary at full conflict degree at least twenty-two, and classify every twenty-edge conflict clique as the complete edge set of an isolated doubled five-cycle. All these steps are proved in the manuscript. An appendix relates the argument to the audited Lean declarations and states the precise scope of the formal verification.

@keywords Induced matching; prescribed edge set; square of a line graph; doubled five-cycle; Hall ratio; formal verification.

## 1. Statement and conventions

All graphs are finite, simple and undirected. An **induced matching** in $G$ is a set of pairwise vertex-disjoint edges such that no edge of $G$ joins endpoints of two different chosen edges. Every adjacency and every conflict in this manuscript is evaluated in the full original graph $G$. Edges outside the candidate set are retained as possible conflict witnesses.

The **doubled five-cycle**, denoted by $C_5[2]$, has five disjoint independent pairs $V_0,\ldots,V_4$. Every vertex of $V_i$ is adjacent to both vertices in $V_{i-1}$ and both vertices in $V_{i+1}$, with indices taken modulo five, and there are no other edges. It is connected, has ten vertices and twenty edges, and is four-regular.

Let $\mathcal{C}(G)$ be the set of connected components of $G$. For a candidate set $F\subseteq E(G)$ define

$$ t_G(F)=|\{D\in\mathcal{C}(G):D\cong C_5[2],\ E(D)\subseteq F\}|. \tag{1.1}

Components are counted once each, independently of the labelling of their five pairs. A proper subset of the edges of a doubled-five-cycle component contributes zero.

**Theorem 1.1 (Unconditional corrected 19.5 packing).** If $\Delta(G)\leq4$, then every $F\subseteq E(G)$ contains an induced matching $M$ of $G$ such that

$$ M\subseteq F,\qquad 2|F|\leq39|M|+t_G(F). \tag{1.2}

Consequently one may choose $|M|\geq\lceil(2|F|-t_G(F))/39\rceil$. In particular, $t_G(F)=0$ implies $|F|\leq19.5|M|$.

The word *unconditional* refers to the absence of unproved structural assumptions or restrictions beyond $\Delta(G)\leq4$ and the stated definitions. It does not mean that the correction term can be removed. For $G=C_5[2]$ and $F=E(G)$ every two edges conflict, so the largest induced matching has size one. Formula (1.2) is then the equality $40=39+1$.

For distinct edges $e,f$, say that they **conflict** if they share an endpoint or an endpoint of one is adjacent to an endpoint of the other. The **conflict graph** $H=H_G$ has vertex set $E(G)$ and this adjacency relation; thus $H=L(G)^2$. Write $c(e)=d_H(e)$ for the full conflict degree. Independent sets in $H[F]$ are exactly induced matchings of $G$ contained in $F$.

The prescribed-set distinction matters even on the path $0-1-2-3$: the candidates $01$ and $23$ conflict through the original edge $12$, even when $12\notin F$. Deleting edges outside $F$ would change the problem. The full-edge-set twenty-packing bound and the doubled-five-cycle extremal example occur in Joos and Nguyen [1]. The earlier companion manuscripts [4] gave a complete prescribed-set twenty-packing proof. The present manuscript supplies the additional structural arguments for (1.2). It is self-contained mathematically and makes no claim of historical priority over the entire literature.

The proof has three parts. Sections 2-5 establish clique bounds at full conflict-degree thresholds $20,21,22,23,24$. Section 6 classifies twenty-edge conflict cliques. Sections 7-8 apply private-neighbourhood counting after removing the fully selected exceptional components. Throughout, the original graph $G$ is assumed to satisfy $\Delta(G)\leq4$; the auxiliary graph $J$ introduced in Section 7 has its own explicitly stated hypotheses.

## 2. Covers and elementary selected-degree bounds

A **conflict clique** is a set $Q\subseteq E(G)$ of pairwise conflicting edges. Put $q=|Q|$ and let $d_Q(x)$ be the number of edges of $Q$ incident with $x$. Its **support** is $S=\{x:d_Q(x)>0\}$. The selected degree $d_Q(x)$ is distinct from the original degree $d_G(x)$. For a vertex set $U$, write $e_G(U)$ and $e_Q(U)$ for the numbers of original and selected edges, respectively, with both endpoints in $U$.

**Lemma 2.1 (Exact endpoint-neighbour cover).** For $uv\in E(G)$ define

$$ C(uv)=(N_G(u)\setminus\{v\})\cup(N_G(v)\setminus\{u\}).

Neither $u$ nor $v$ belongs to this set, and $|C(uv)|\leq6$. Moreover,

$$ c(uv)+e_G(C(uv))=\sum_{x\in C(uv)}d_G(x)\leq24. \tag{2.1}

If $uv\in Q$, then

$$ q-1+e_Q(C(uv))=\sum_{x\in C(uv)}d_Q(x). \tag{2.2}

**Proof.** An edge other than $uv$ conflicts with $uv$ if and only if it meets $C(uv)$. For an edge sharing an endpoint with $uv$, its other endpoint belongs to the cover. For a disjoint conflicting edge, the endpoint adjacent to $u$ or $v$ belongs to the cover. Conversely, meeting this cover supplies such a conflict. The incidence sum over a vertex set counts every edge meeting the set once, and counts an additional copy precisely for edges entirely inside the set. Applying this observation to all original edges gives (2.1). Every edge of $Q\setminus\{uv\}$ meets the cover, whereas $uv$ does not; applying the same observation to $Q$ gives (2.2). The cover is the union of two sets of size at most three. ∎

**Lemma 2.2 (Triangles and slack).** Every edge has $c(e)\leq24$. If $uv$ is in a triangle, or if one of its endpoints has original degree at most three, then $c(uv)\leq20$. If $c(uv)\geq t$, then $e_G(C(uv))\leq24-t$. For a triangle edge of conflict degree at least twenty the cover contains no original internal edge; for a triangle edge of conflict degree at least nineteen it contains at most one.

**Proof.** In either of the first two special situations the cover has at most five vertices. Apply (2.1), using the degree bound four, to a cover of size at most six or at most five as appropriate. ∎

**Lemma 2.3 (Preliminary selected-degree bounds).** If $d_Q(x)\leq2$ for all $x$, then $q\leq13$. If $d_Q(x)\leq3$ for all $x$, then $q\leq18$.

**Proof.** For nonempty $Q$, (2.2) gives $q\leq1+6s$ when all selected degrees are at most $s$. This proves the first assertion and reduces the second to excluding $q=19$. In that case equality forces every cover of a selected edge to have six vertices, all of selected degree three.

Let $xy\in Q$. The six-vertex cover implies that $x$ has an original neighbour $a\neq y$. Then $a\in C(xy)$ and $d_Q(a)=3$. Choose $ab\in Q$ with $b\neq x$. Now $x\in C(ab)$, so $d_Q(x)=3$. Thus every supported vertex has selected degree three. The handshake identity gives $3|S|=2q=38$, which is impossible. The empty clique causes no difficulty. ∎

**Lemma 2.4 (A degree-two restriction).** Suppose all endpoints of a conflict clique $Q'$ lie in a set $P$ and $|N_G(x)\cap P|\leq2$ for all $x\in P$. Then $|Q'|\leq5$. If some $D\subseteq P$ meets each selected edge of $Q'$ in exactly one endpoint, then $|Q'|\leq4$.

**Proof.** Passing to the vertex-induced graph $G[P]$ preserves all conflicts between edges with endpoints in $P$. Its cover of a selected edge has at most two vertices, each of selected degree at most two, so the cover argument gives $|Q'|\leq5$. If equality holds, every such cover has two vertices of selected degree two. For any supported $x$, choose $xy\in Q'$. Equality gives an original neighbour $a\neq y$ of $x$ in $P$, with $d_{Q'}(a)=2$. Choose $ab\in Q'$ with $b\neq x$. Then $x\in C_{G[P]}(ab)$, forcing $d_{Q'}(x)=2$. Thus all nonzero selected degrees are two. If each selected edge crosses $D$, then $|Q'|=\sum_{x\in D}d_{Q'}(x)$ is even, contradicting five. The original graph $G[P]$ itself need not be bipartite. ∎

**Lemma 2.5 (Closed support of a large subcubic selection).** Suppose $q\geq17$ and $d_Q(x)\leq3$ everywhere. For every $uv\in Q$, the cover has six vertices and

$$ d_Q(x)\geq q-16\quad(x\in C(uv)). \tag{2.3}

Every supported vertex has original degree four, all its original neighbours lie in $S$, and no selected edge lies in an original triangle.

**Proof.** A cover with at most five vertices could have selected incidence sum at most fifteen, contrary to (2.2). Hence it has six vertices. Removing any one vertex from its selected incidence sum leaves at most fifteen, which proves (2.3). A six-vertex cover forces both endpoint degrees to be four and their other neighbour sets to be disjoint, excluding a triangle on the selected edge.

For $xy\in Q$, every original neighbour $z\neq y$ of $x$ lies in $C(xy)$ and has positive selected degree by (2.3); the neighbour $y$ is already supported. Every supported vertex occurs on some selected edge, so this proves both regularity and closure of $S$ in the full original graph. ∎

For later use, let $h(x)$ count the selected edges that meet $N_G(x)$ but are not incident with $x$. Under the assumptions of Lemma 2.5,

$$ h(x)+d_Q(x)=\sum_{y\in N_G(x)}d_Q(y). \tag{2.4}

Indeed, no selected edge can lie inside $N_G(x)$, since such an edge would be in a triangle. Thus the incidence sum counts each selected edge meeting this neighbourhood once. Also, a selected edge $uv$ is counted by $h(x)$ exactly when $x\in C(uv)$. Both observations hold for original neighbours, without deleting any unselected edge.

## 3. Root counting and saturation

Fix a vertex $r$ and write

$$ A=N_G(r),\qquad R=\{a\in A:ra\in Q\},\qquad s=|R|=d_Q(r).

When $A$ is independent, partition $Q$ into its $s$ edges at $r$, the set $K$ of selected edges $ax$ with $a\in A$ and $x\notin A\cup\{r\}$, and the set $O$ of **outer edges** with both endpoints outside $A\cup\{r\}$. Put $k=|K|$, $o=|O|$. Then

$$ q=s+k+o,\qquad s+k=\sum_{a\in A}d_Q(a). \tag{3.1}

For any root, including one with a non-independent neighbourhood, every selected edge either meets $A$ or is outer. In particular,

$$ q\leq\sum_{a\in A}d_Q(a)+o\leq16+o. \tag{3.2}

For $x\neq r$ put $T(x)=N_G(x)\cap A$, its **type**. Type sizes one, two, three and four will be called singleton, double, triple and quadruple types. Let $P=\{x\neq r:|T(x)|\geq2\}$, and let $B$ be the set of **selected tips**, namely the external endpoints of edges in $K$. When $A$ is independent, every vertex of nonempty type lies outside $A\cup\{r\}$.

**Lemma 3.1 (Type counts and root load).** For an outer edge $xy$ one has

$$ R\subseteq T(x)\cup T(y),\qquad d_O(x)+|T(x)|\leq4. \tag{3.3}

For every vertex set $U$ not containing $r$,

$$ \sum_{x\in U}|T(x)|\leq12,\qquad |P|\leq6. \tag{3.4}

If $A$ is independent and $c(e)\geq t$ for all $e\in Q$, then for each $a\in R$,

$$ L_a=\sum_{x\neq r,\ a\in T(x)}(|T(x)|-1)\leq24-t. \tag{3.5}

**Proof.** An outer edge must conflict with every selected $ra$. Neither endpoint is adjacent to $r$, so one of them must be adjacent to $a$, proving the cover of $R$. Outer neighbours and neighbours in $A$ are disjoint, proving the degree inequality.

Each $a\in A$ has at most three original neighbours other than $r$. Counting incidences between $A$ and $U$ proves the first bound in (3.4); each member of $P$ contributes at least two, proving the second.

For each $x\neq r$ with $a\in T(x)$ and each $b\in T(x)\setminus\{a\}$, the original edge $bx$ lies inside $C(ra)$. Independence of $A$ makes the two sets $A\setminus\{a\}$ and $N_G(a)\setminus\{r\}$ disjoint, so these are distinct edges indexed by the pairs $(x,b)$. There are $L_a$ such edges. Apply Lemma 2.2. The sum includes all original vertices, whether or not their edges to $A$ are selected. ∎

**Lemma 3.2 (Independence at high-degree roots).** If every selected edge has conflict degree at least twenty-one and $s\geq3$, then $|A|=4$ and $A$ is independent. The same independence conclusion holds when $q\geq17$, all selected degrees are at most three, and $s=3$.

**Proof.** In the first case a selected root edge forces original degree four and lies in no triangle, by Lemma 2.2. In the second case Lemma 2.5 gives these facts. Any edge between two members of the four-element set $A$ has at least one endpoint in $R$, since $|R|\geq3$. It would form a triangle with that selected root edge. ∎

We will repeatedly use the following elementary witness rule. If $ax,by\in K$, $a\notin T(y)$ and $b\notin T(x)$, and $A$ is independent, then $xy\in E(G)$. The exclusions ensure distinct endpoints and rule out the other three possible cross-edges $ab,ay,bx$, so the required conflict has only this witness.

**Lemma 3.3 (Singleton control).** If $ax\in K$ has $T(x)=\{a\}$ and $A$ is independent, then every $y\in B$ with $a\notin T(y)$ is adjacent to $x$. Consequently $|B|\leq6$.

**Proof.** Choose $by\in K$ and apply the witness rule: $a\notin T(y)$ implies $b\neq a$, so $b\notin T(x)$. Thus

$$ B\subseteq(N_G(a)\setminus\{r\})\cup(N_G(x)\setminus\{a\}).

Both sets on the right have size at most three. ∎

A double tip is **fully selected** if both edges from it to its type lie in $K$. Denote the set of such tips by $D_2$.

**Lemma 3.4 (Fully selected doubles).** Suppose $A$ is independent. Then $|D_2|\leq4$. If $|D_2|=4$, it consists of two type classes of size two, and each tip has exactly the other class as its original neighbours outside $A$. If, in addition, every type has size at most two, then $B=D_2$.

**Proof.** Fully selected doubles with different types are adjacent: choose one label in each of the two type differences and use the witness rule. If all tips in $D_2$ have the same type, one label in that type has all of them as neighbours other than $r$, giving $|D_2|\leq3$. Otherwise choose tips $x,y$ of different types. Every tip has a type different from at least one of their types, and therefore belongs to $N_G(x)\setminus A$ or $N_G(y)\setminus A$. Each of these two sets has size at most two, proving $|D_2|\leq4$.

Now suppose there are four tips. For a fixed $x$, let $E$ be its type class and let $D=D_2\setminus E$. A label in $T(x)$ gives $|E|\leq3$, so $D$ is nonempty. A tip in $D$ is adjacent to every tip in $E$, whence $|E|\leq2$. The tip $x$ is adjacent to all of $D$, so $|D|\leq2$. Thus both sets have size two and exhaust the available two neighbours outside $A$ at every tip. Applying this to a member of $D$ also shows that the two members of $D$ have the same type.

Finally let $ay\in K$ and assume all types have size at most two. At least one $x\in D_2$ misses $a$ in its type, since $a$ cannot have four neighbours other than $r$. Since $a\in T(y)$, some $b\in T(x)$ is absent from $T(y)$. The witness rule forces $xy$. The preceding saturation says that every neighbour of $x$ outside $A$ belongs to $D_2$, so $y\in D_2$. This proves $B\subseteq D_2$; the reverse inclusion is definitional. ∎

**Lemma 3.5 (Complementary doubles).** Suppose $s=|A|=4$. If every endpoint of an outer subfamily $O'\subseteq O$ has type size at most two, then $|O'|\leq4$.

**Proof.** Equation (3.3) forces the two endpoint types of each edge to be disjoint pairs with union $A$. Let $P_0$ be the vertices outside $A\cup\{r\}$ having type size at least two. Every vertex of $P_0$ has at most two neighbours in $P_0$. Fix $a\in A$ and put $D=\{x\in P_0:a\in T(x)\}$. Every edge of $O'$ crosses $D$, so Lemma 2.4 applies. This proof does not require independence of $A$, provided the endpoints are external as stipulated. ∎

**Lemma 3.6 (Small types).** Suppose $A$ is independent, $s=4$, and every type has size at most two. Then $o\leq4$ and $k\leq9$. If $|D_2|=4$, the stronger bound $k\leq8$ holds. In particular $q\leq17$.

**Proof.** Lemma 3.5 gives $o\leq4$. If a selected singleton exists, Lemma 3.3 gives $|B|\leq6$; otherwise $B\subseteq P$ and (3.4) gives the same bound. Each tip contributes one selected edge to $K$, with a second possible precisely for members of $D_2$. Hence $k=|B|+|D_2|$. If $|D_2|\leq3$, this is at most nine. If $|D_2|=4$, Lemma 3.4 gives $B=D_2$, so $k=8$. Equation (3.1) finishes the proof. ∎

**Lemma 3.7 (A unique triple).** Suppose $A$ is independent, $s=4$, there is exactly one triple tip $x$ among all original vertices other than $r$, and all other types have size at most two. Then $k\leq10$, $o\leq4$, and $q\leq18$.

**Proof.** Let $a_0$ be the missing label of the triple $T(x)$. There are at most twelve original edges from $A$ to vertices other than $r$. If at most one of the three edges from $x$ to its type is selected, at least two of these twelve edges are unselected, giving $k\leq10$.

Otherwise choose two selected edges $ax,bx$ at distinct labels in $T(x)$. For any selected edge $a_0y$, its tip has type size at most two and contains $a_0$, so it misses at least one of $a,b$. The witness rule forces $xy$. The triple $x$ has at most one neighbour outside $A$, so at most one selected edge of $K$ uses $a_0$. The other three labels support at most three each, again giving $k\leq10$.

Outer edges avoiding $x$ join complementary doubles, and there are at most four by Lemma 3.5. At most one outer edge meets $x$. If $o\geq5$, there must be exactly four avoiding $x$ and one meeting it. The set $P\setminus\{x\}$ has size at most four, since its vertices use at least two type incidences each while $x$ uses three of the twelve available. The four avoiding edges have all endpoints in this set. Their eight incidences, with at most two at each vertex, force exactly four such vertices, each having two selected outer neighbours in the set and two original neighbours in $A$. These are all its neighbours.

Write the remaining outer edge as $xy$. Its endpoint $y$ cannot be one of those four vertices, since their external neighbours already lie among themselves. Neither endpoint of $xy$ is in $A$. Thus $xy$ is disjoint from, and has no cross-adjacency to, any of the four avoiding edges. This contradicts the clique property. Hence $o\leq4$, and $q\leq4+10+4=18$. ∎

**Lemma 3.8 (Charging outer edges).** Suppose $s=4$. Then $o\leq|P|$. More precisely, if $Z$ is the set of quadruple tips, then $o+|Z|\leq|P|$. If there are at least two vertices of type size at least three, then $o\leq4$.

**Proof.** Partition $P$ into double tips and tips of type size at least three. Charge an outer edge meeting the latter set to one such endpoint. Each triple has at most one available outer neighbour, and a quadruple has none. The remaining outer edges have two double endpoints by (3.3); the double tips have total outer incidence capacity twice their number. Thus these remaining edges number at most the number of double tips. Adding the two estimates proves $o+|Z|\leq|P|$.

If there are two tips of size at least three, the type sum is at least $2|P|+2$, so $|P|\leq5$. Suppose $o\geq5$. Then $|P|=o=5$, and the type sum over $P$ is exactly twelve. There can be no singleton type anywhere, as that would exceed the twelve-incidence bound (3.4). An outer endpoint cannot have type size zero: its partner would then need type size four to cover $A$, but a quadruple has no outer neighbour. Consequently all outer endpoints lie in $P$. Summing (3.3) over $P$ now gives $2o+12\leq4|P|=20$, contradicting $o\geq5$. ∎

## 4. The subcubic boundary

In this section the selected degrees satisfy $d_Q(x)\leq3$. This condition concerns the selected set only; original degrees may be four. Lemma 2.3 already gives $q\leq18$. We first exclude eighteen without any conflict-degree threshold, and then exclude seventeen under $c(e)\geq22$.

### 4.1. Excluding eighteen selected edges

**Lemma 4.1 (Cubic selection at equality).** If $q=18$, then every supported vertex has selected degree three and $|S|=12$.

**Proof.** Every cover has size six, and each of its vertices has selected degree at least two by (2.3). We claim that every supported vertex has selected degree at least two. Choose $xy\in Q$ through such a vertex $x$. By Lemma 2.5, $x$ has four original neighbours. Choose $a\in N_G(x)\setminus\{y\}$. The vertex $a$ is in $C(xy)$ and has at least two selected incident edges, so one of them is $ab$ with $b\neq x$. Now $x\in C(ab)$, proving the claim.

Let $L=\{x\in S:d_Q(x)=2\}$. A cover can contain at most one member of $L$, since its selected degree sum is at least seventeen and all six selected degrees are at most three. Double-counting the pairs $(x,e)$ with $x\in L$ and $x\in C(e)$ gives

$$ \sum_{x\in L}h(x)\leq18. \tag{4.1}

The support is closed and four-regular in $G$. All neighbour selected degrees are at least two, so (2.4) gives $h(x)\geq8-2=6$ for $x\in L$. Hence $|L|\leq3$. Such an $x$ has at most two neighbours in $L$, and all other neighbours have selected degree three; therefore $h(x)\geq2+2+3+3-2=8$. Equation (4.1) now gives $|L|\leq2$.

The handshake identity is $36+|L|=3|S|$. Thus $|L|$ is divisible by three, and the bound $|L|\leq2$ forces $L$ to be empty. Every supported vertex has selected degree three, and $|S|=12$. ∎

**Proposition 4.2 (Subcubic selections have at most seventeen edges).** If $d_Q(x)\leq3$ for every vertex, then $q\leq17$.

**Proof.** Suppose $q=18$, the only remaining possibility by Lemma 2.3. Lemmas 2.5 and 4.1 say that $S$ is closed and four-regular in $G$, has twelve vertices, and has selected degree three at every vertex.

Choose $r\in S$. Its original neighbourhood $A$ has four vertices, its selected labels $R$ have size three, and $A$ is independent by Lemma 3.2. Put $U=S\setminus(A\cup\{r\})$, so $|U|=7$. For $x\in U$, let $s_x=|N_G(x)\cap R|$ and let $t_x$ count the selected neighbours of $x$ in $A$.

Each $x$ has exactly one unselected original incident edge, and $A\setminus R$ has one vertex. These two facts give $s_x\leq t_x+1$ and $t_x\leq s_x+1$. For nonnegative integers satisfying these inequalities,

$$ s_x+t_x\leq1+s_xt_x. \tag{4.2}

If either count is zero the assertion follows from the difference bound. If both are positive it is equivalent to $(s_x-1)(t_x-1)\geq0$.

Each member of $R$ has three original neighbours other than $r$, all in $U$. Counting these incidences gives $\sum_{x\in U}s_x=9$. The four vertices of $A$ have total selected degree twelve, of which the three selected root edges account for three. Independence of $A$ and closure of $S$ therefore give $\sum_{x\in U}t_x=9$.

For each $a\in R$, the selected edge $ra$ has at most one selected internal edge in its cover, because (2.2) gives $17+e_Q(C(ra))\leq18$. The sum of $t_x$ over $x\in U\cap N_G(a)$ counts selected edges from those vertices to $A$. Exactly two of these edges go to $a$, since $d_Q(a)=3$ and $ra$ is selected. Every remaining counted edge joins $N_G(a)\setminus\{r\}$ to $A\setminus\{a\}$, and is therefore internal to $C(ra)$. No edge is counted twice because $A$ and $U$ are disjoint. It follows that

$$ \sum_{x\in U\cap N_G(a)}t_x\leq3,\qquad \sum_{x\in U}s_xt_x\leq9. \tag{4.3}

Summing (4.2) now gives the contradiction

$$ 18=\sum_{x\in U}(s_x+t_x)\leq|U|+\sum_{x\in U}s_xt_x\leq7+9=16.

This excludes eighteen and proves the proposition. ∎

### 4.2. Defect counting for seventeen edges

Assume for now that $q=17$. On $S$, define the selected-degree defect $w_x=3-d_Q(x)$, so $w_x\in\{0,1,2\}$. Set

$$ D=\sum_{x\in S}w_x,\quad E=\sum_{x\in S}w_x^2,\quad W=\sum_{x\in S}w_xh(x),

$$ A_w=\sum_{x\in S}w_x\sum_{y\in N_G(x)}w_y. \tag{4.4}

Also let $L=\{x\in S:w_x>0\}$ and $J=\{x\in S:w_x=2\}$, with $\ell=|L|$ and $j=|J|$. The letter $A_w$ here denotes a weighted adjacency sum, not the root neighbourhood.

**Lemma 4.3 (Defect identities and support bound).** Under these assumptions, $\ell\leq5$ and $|S|\leq13$. More precisely, the following identities and inequalities hold:

$$ D+34=3|S|,\qquad D=\ell+j,\qquad E=\ell+3j, \tag{4.5}

$$ W\leq34,\qquad W+A_w=9D+E,\qquad A_w\leq4E,\qquad A_w+E\leq D^2. \tag{4.6}

**Proof.** The first identity is the handshake count $\sum d_Q(x)=34$. The next two follow from the possible defect values zero, one and two.

Every selected-edge cover has six vertices and selected degree sum at least sixteen. Its total defect is therefore at most two. As $h(x)$ counts precisely the selected edges whose cover contains $x$, weighted double-counting gives

$$ W=\sum_{e\in Q}\sum_{x\in C(e)}w_x\leq2|Q|=34. \tag{4.7}

Closure and four-regularity of $S$, together with (2.4), yield

$$ h(x)+\sum_{y\in N_G(x)}w_y=9+w_x\quad(x\in S).

Multiplying by $w_x$ and summing proves $W+A_w=9D+E$.

For every adjacent ordered pair $(x,y)$, use $2w_xw_y\leq w_x^2+w_y^2$. Since the graph on $S$ is four-regular, summing over all ordered adjacent pairs gives $A_w\leq4E$. Also, the diagonal terms and the ordered adjacent pairs form a subset of all ordered pairs from $S$, so nonnegativity gives $A_w+E\leq D^2$.

The first three bounds in (4.6) imply $9D\leq34+3E$. Substituting (4.5) gives $6\ell\leq34$, hence $\ell\leq5$. Since $j\leq\ell$, we have $D\leq10$ and thus $|S|\leq14$. If $|S|=14$, then $D=8$. Since $D=\ell+j$ and $\ell\leq5$, one has $j\geq3$, so $E=D+2j\geq14$. On the other hand (4.6) gives

$$ 9D+2E\leq34+D^2. \tag{4.8}

With $D=8$, this says $E\leq13$, a contradiction. Therefore $|S|\leq13$. ∎

**Lemma 4.4 (High conflict degree forces thirteen support vertices).** If, in addition, $c(e)\geq22$ for every $e\in Q$, then $|S|=13$.

**Proof.** Lemma 2.3 shows that some vertex $r$ has selected degree three. Let $A=N_G(r)$ and let $R$ be its three selected labels. Lemmas 2.5 and 3.2 give closure, original degree four and independence of $A$. Put $U=S\setminus(A\cup\{r\})$, and write $A\setminus R=\{b\}$.

For $x\in U$, put $\kappa_x=|T(x)|$, $s_x=|T(x)\cap R|$, and let $\varepsilon_x$ be one if $x$ is adjacent to $b$, zero otherwise. Thus $\kappa_x=s_x+\varepsilon_x$. Each member of $A$ has exactly three original neighbours in $U$, so

$$ \sum_{x\in U}\kappa_x=12,\qquad \sum_{x\in U}\varepsilon_x=3. \tag{4.9}

The load bound (3.5) gives $L_a\leq2$ for each $a\in R$. Double-counting its contributions gives

$$ \sum_{x\in U}s_x(\kappa_x-1)=\sum_{a\in R}L_a\leq6. \tag{4.10}

For nonnegative $\kappa=s+\varepsilon$ with $\varepsilon\in\{0,1\}$,

$$ 2\kappa\leq2+s(\kappa-1)+\varepsilon. \tag{4.11}

For $\kappa=0,1,2$ this is direct; for $\kappa\geq3$, one has $s\geq2$, and the right side is at least $2+2(\kappa-1)$. When $\kappa=0$, the product with $s=0$ is zero. Summing (4.11) and using (4.9)-(4.10) yields $24\leq2|U|+9$, hence $|U|\geq8$. Thus $|S|=|U|+5\geq13$, and Lemma 4.3 supplies the opposite inequality. ∎

**Proposition 4.5 (The high22 subcubic boundary is impossible).** If all selected degrees are at most three and all selected edges have $c(e)\geq22$, then $q\leq16$.

**Proof.** Proposition 4.2 reduces the question to excluding $q=17$. In that case Lemma 4.4 gives $|S|=13$, and (4.5) gives $D=5$. The identities imply

$$ A_w\geq11+E,\qquad A_w\leq25-E,\qquad E=5+2j.

Hence $E\leq7$ and $j\leq1$. There are only two cases.

**Case 1: $j=0$.** Then $\ell=5$, every positive defect is one, and $A_w=\sum_{x\in L}d_{G[L]}(x)\geq16$. If a selected edge $uv$ lay inside $L$, it would be in no triangle by Lemma 2.5. In a graph on five vertices containing such an edge, each of the other three vertices is adjacent to at most one of $u,v$. There are at most three edges from $\{u,v\}$ to the other vertices and at most three among those other vertices, so there are at most $1+3+3=7$ edges altogether. Its degree sum would be at most fourteen, a contradiction.

Thus no selected edge lies inside $L$. Each $x\in L$ has selected degree two, so its original internal neighbours in $L$ and its selected neighbours are disjoint. Therefore $d_{G[L]}(x)\leq4-2=2$, and the internal degree sum is at most ten, again a contradiction.

**Case 2: $j=1$.** Now $\ell=4$, $E=7$, and the two bounds on $A_w$ force $A_w=18$. Thus $A_w+E=D^2=25$. Equality in the complete ordered-pair bound implies that every two distinct positive-defect vertices are adjacent: otherwise their positive product would be missing from the sum. Hence $G[L]$ is a complete graph on four vertices.

No selected edge can lie inside this clique, because any such edge would be in a triangle. As before, internal neighbours and selected neighbours are disjoint, so

$$ \sum_{x\in L}d_{G[L]}(x)\leq\sum_{x\in L}(4-d_Q(x))=\ell+D=9.

But a four-clique has degree sum twelve. This contradiction excludes the second case and proves the proposition. ∎

## 5. The five strengthened clique bounds

**Theorem 5.1 (Full conflict-degree thresholds).** Let $\Delta(G)\leq4$ and let $Q$ be a conflict clique. If every $e\in Q$ has $c(e)\geq t$, then $q\leq b_t$, with the following values:

@table Threshold $t$ | 20 | 21 | 22 | 23 | 24
@row Bound $b_t$ | 18 | 17 | 16 | 15 | 13

All five bounds refer to conflict degrees in the full original graph. We start with thresholds twenty-four and twenty-three. The high21 argument supplies a case needed for high22, so those two proofs follow in that order; high20 is treated last.

### 5.1. Threshold twenty-four

**Proposition 5.2.** If $c(e)\geq24$ for every $e\in Q$, then $q\leq13$.

**Proof.** Equations (2.1) and Lemma 2.2 show that each selected edge has a six-vertex cover with no internal original edge, and lies in no triangle or four-cycle. For a four-cycle, the opposite edge would be internal to its cover.

Fix a vertex $u$. A **branch with label $a$** consists of selected edges $ax$ with $a\in N_G(u)$ and $x\neq u$. Each branch has at most three edges. Suppose a branch contains $ax_1,ax_2$, and a distinct branch contains $by$. Here $a\neq b$ and $x_1\neq x_2$.

For each $i$, equality $x_i=b$ or $y=a$ would put a selected edge in the triangle $uab$, and equality $x_i=y$ would put a selected edge in the four-cycle $u-a-x_i-b-u$. The two selected edges therefore have disjoint endpoints. If $ab$ were an edge, $u$ and $b$ would both lie in $C(ax_i)$, making $ub$ an internal edge of that cover. The possible cross-edge $ay$ would create the four-cycle $u-a-y-b-u$ containing $by$; the cross-edge $bx_i$ would create a four-cycle containing $ax_i$. All are impossible. The conflict between $ax_i$ and $by$ must therefore use $x_iy$. But the two resulting edges produce the four-cycle $a-x_1-y-x_2-a$ containing selected edges, again impossible.

Thus a branch with at least two edges excludes every distinct nonempty branch. Any collection of at most three labels consequently supports at most three branch edges: either each nonempty branch is a singleton, or only one is nonempty.

Choose $uv\in Q$ if $Q$ is nonempty. Apart from $uv$, at most three selected edges meet $u$ and at most three meet $v$. Every remaining selected edge meets $C(uv)$. The edges meeting $N_G(u)\setminus\{v\}$ belong to at most three branches at $u$, giving at most three; the analogous count at $v$ also gives at most three. Overlaps only improve this upper bound. Hence $q\leq1+3+3+3+3=13$. ∎

### 5.2. Threshold twenty-three

**Proposition 5.3.** If $c(e)\geq23$ for every $e\in Q$, then $q\leq15$.

**Proof.** If all selected degrees are at most two, Lemma 2.3 applies. Otherwise choose a root of maximum selected degree $s\in\{3,4\}$. By Lemma 3.2, $A$ is independent and has four vertices. For $a\in R$, the load satisfies $L_a\leq1$.

Every type has size at most two: a larger type meets $R$ and contributes at least two at a common label. Moreover, distinct multiple vertices cannot share a label of $R$.

If an outer edge $xy$ exists, one endpoint, say $x$, contains at least two labels $a,b$ of $R$, since its endpoints together cover at least three labels. Any outer edge avoiding $x$ must cover $a$ and $b$ with other vertices. Such vertices must be singletons, since a second multiple vertex at either label is forbidden. Its two endpoints could then cover only these two labels, a contradiction. Thus every outer edge meets $x$, and $o\leq2$.

If $s=3$, maximality of the selected degree gives $\sum_{a\in A}d_Q(a)\leq12$, whence $q\leq14$ by (3.2).

If $s=4$, both endpoints of every outer edge are complementary doubles. Applying the preceding common-endpoint argument separately to its two endpoints shows that every outer edge contains both. Simplicity gives $o\leq1$. Each label in $A=R$ belongs to at most one multiple type, so multiple tips contribute at most four selected edges to $K$ in total. If singleton tips occur there are at most six of them by Lemma 3.3; otherwise they contribute zero. Thus $k\leq10$, and $q\leq4+10+1=15$. ∎

### 5.3. Threshold twenty-one

**Proposition 5.4.** If $c(e)\geq21$ for every $e\in Q$, then $q\leq17$. If a four-selected-edge root has a type of size at least three, then in fact $q\leq16$.

**Proof.** If all selected degrees are at most three, Proposition 4.2 applies. Otherwise choose $r$ with $s=4$. Its neighbourhood is independent and each load satisfies $L_a\leq3$.

If all types have size at most two, Lemma 3.6 proves $q\leq17$. Suppose instead that some $x$ has type size at least three. No other vertex has type size at least three, because two such types share a label and contribute at least four there.

If $T(x)=A$, it contributes three at every label, leaving no room for any other multiple vertex. Every outer edge has a multiple endpoint by (3.3), but $x$ has no neighbour outside $A$. Thus $o=0$, and (3.2) gives $q\leq16$.

Otherwise $x$ is the unique triple. Lemma 3.7 gives $k\leq10$. At each label in $T(x)$, at most one multiple vertex other than $x$ can occur. If an outer edge $yz$ avoids $x$, its endpoint types are complementary doubles. Every other multiple vertex has a label in common with $T(x)$; that label belongs to exactly one of $T(y),T(z)$, and uniqueness at the label forces the vertex to be $y$ or $z$. Thus $yz$ is the only possible outer edge avoiding $x$. At most one outer edge meets $x$, so $o\leq2$. Consequently $q\leq4+10+2=16$. ∎

### 5.4. Threshold twenty-two

**Proposition 5.5.** If $c(e)\geq22$ for every $e\in Q$, then $q\leq16$.

**Proof.** Proposition 4.5 handles selected maximum degree at most three. Otherwise take $r$ with $s=4$. A type of size at least three is covered by the stronger conclusion of Proposition 5.4. We may therefore assume all types have size at most two.

The neighbourhood $A$ is independent, and each load is at most two. Each double contributes one unit at each of its two labels, so summing the four load bounds gives $2|P|\leq8$, or $|P|\leq4$. Lemma 3.5 gives $o\leq4$.

If no selected singleton exists, $k\leq2|P|\leq8$, giving $q\leq16$. If $|D_2|=4$, the same bound follows from Lemma 3.4. In the remaining case choose a selected singleton $ax$, and assume $|D_2|\leq3$. Then $|B|\leq6$ and $k\leq9$. If $o\leq3$, the desired estimate follows from $q=4+k+o$.

It remains to consider $o=4$. All outer endpoints lie in $P$, and each has outer degree at most two. The eight outer incidences and $|P|\leq4$ force $|P|=4$ and outer degree two at every member of $P$. Its two type neighbours and two outer neighbours exhaust all its original neighbours. In particular, no member of $P$ is adjacent to the singleton $x$, which lies outside $P\cup A$.

Lemma 3.3 now forces every multiple selected tip to contain $a$ in its type. At most two multiple vertices contain $a$, since $L_a\leq2$. Thus at most two tips can contribute a second selected edge beyond the first edge at each member of $B$, and $k\leq|B|+2\leq8$. Therefore $q\leq4+8+4=16$ in the final case as well. ∎

### 5.5. Threshold twenty

**Proposition 5.6.** If $c(e)\geq20$ for every $e\in Q$, then $q\leq18$.

**Proof.** If all selected degrees are at most three, Proposition 4.2 is stronger than required. Otherwise choose $r$ with $s=4$. It suffices to assume $q\geq19$ and derive $q\leq18$.

First $A$ is independent. Suppose $ab$ is an edge inside $A$. Both $ra$ and $rb$ are selected triangle edges of conflict degree at least twenty, so their covers have no internal original edges. For an external vertex $x$ whose type contains $a$, every additional label $c\in T(x)\setminus\{a\}$ would make $cx$ internal to $C(ra)$. Hence such a type must be $\{a\}$; the same argument applies to $b$. An outer edge must cover all four labels of $A$. Covering $a$ and $b$ would force its two endpoints to have singleton types $\{a\}$ and $\{b\}$, which cannot cover the other two labels. Therefore $o=0$, and (3.2) gives $q\leq16$, a contradiction.

We now have independence and $L_a\leq4$ for all $a\in A$. Consider the possible type sizes.

**Case 1: a quadruple $x$ exists.** It contributes three at every label. Every other multiple vertex must be a double, and each label occurs in at most one of these other multiple types. The quadruple has no outer neighbour. If an outer edge $yz$ exists, its endpoint types are complementary doubles. Uniqueness at every label forces every other multiple vertex to be $y$ or $z$, and hence $yz$ is the only outer edge. Thus $q\leq16+1=17$.

**Case 2: at least two triples exist and no quadruple exists.** Choose two triples $x,y$ and two distinct labels $a,b$ common to their types. At either label these triples contribute $2+2=4$, exhausting the load. Any other vertex containing that label must therefore be a singleton. An outer edge avoiding $x,y$ would need two singleton endpoints to cover $a,b$, and would fail to cover all four labels. Every outer edge meets $x$ or $y$, each of which has at most one available outer neighbour. Hence $o\leq2$ and $q\leq18$.

**Case 3: exactly one triple exists and no quadruple exists.** Apply Lemma 3.7 to obtain $q\leq18$.

**Case 4: all types have size at most two.** Apply Lemma 3.6, which gives $q\leq17$.

The cases exhaust all possibilities, proving the proposition. Together with Propositions 5.2-5.5, this establishes Theorem 5.1. ∎

## 6. Rigidity of twenty-edge conflict cliques

The next argument has no conflict-degree threshold assumption. Its conclusion identifies actual components of $G$, including all original incident edges.

**Lemma 6.1 (Independent neighbourhoods in a large clique).** If $q\geq20$, there is a vertex of selected degree four. For every such vertex $r$, its original neighbourhood $A$ is independent.

**Proof.** If every selected degree were at most three, Proposition 4.2 would give $q\leq17$. Thus a root with $s=4$ exists. Every selected edge conflicts with the other $q-1$ selected edges, so it has full conflict degree at least nineteen.

Suppose $ab$ is an edge inside $A$. The triangle edges $ra,rb$ are selected, and each of their covers has at most one internal original edge by Lemma 2.2. For any $x\neq r$ with $a\in T(x)$, each label $c\in T(x)\setminus\{a\}$ contributes the distinct internal edge $cx$ to $C(ra)$. Hence $|T(x)|\leq2$. The same is true for a type containing $b$. A type containing neither $a$ nor $b$ is contained in the other two labels and also has size at most two.

Consequently all external types have size at most two, and Lemma 3.5 gives $o\leq4$. The number of original edges meeting $A$ is

$$ \sum_{a\in A}d_G(a)-e_G(A)\leq16-1=15.

Every selected edge either meets $A$ or is outer. Thus $q\leq15+4=19$, a contradiction. This proof applies at every selected-degree-four root. ∎

**Lemma 6.2 (A second vertex with the full root type).** If $q\geq20$ and $r$ has selected degree four, there exists $z\neq r$ with $T(z)=A$.

**Proof.** By Lemma 6.1 the four-element neighbourhood $A$ is independent. Suppose no quadruple type exists. If all types have size at most two, Lemma 3.6 contradicts $q\geq20$. If there is exactly one triple, Lemma 3.7 does the same. Therefore assume that at least two triples exist.

Lemma 3.8 gives $o\leq4$. Equations (3.1)-(3.2) and $q\geq20$ force equality: $q=20$, $o=4$, and $d_Q(a)=4$ for every $a\in A$. Every original edge incident with a member of $A$ is therefore selected. Moreover, $N_G(a)$ is independent for every $a\in A$, by Lemma 6.1 applied with root $a$.

We claim that two types are nested or disjoint. If $T(x),T(y)$ intersect but neither contains the other, choose $a\in T(x)\setminus T(y)$ and $b\in T(y)\setminus T(x)$. Both $ax$ and $by$ are selected, so the witness rule forces $xy$. A shared label $c$ makes both $x,y$ neighbours of $c$, contradicting independence of $N_G(c)$.

Choose a triple type $T(x)$. Every multiple type intersects it, since a set of size at least two cannot avoid a three-element subset of $A$. By the nesting assertion and the absence of quadruples, every multiple type is contained in $T(x)$. Let $b$ be the unique missing label.

The label $b$ has selected degree four, so it has a selected neighbour $y\neq r$. This external vertex has a type containing $b$. It cannot be multiple, and hence $T(y)=\{b\}$. Every member of $P$ has selected type edges and a type missing $b$, so Lemma 3.3 forces it to be adjacent to $y$. Since $y$ is already adjacent to $b$, it has at most three other neighbours; thus $|P|\leq3$. Lemma 3.8 gives $o\leq3$, and (3.2) gives $q\leq19$, the final contradiction. ∎

**Lemma 6.3 (Equality and saturation).** Under $q\geq20$, choose $r,z$ as in Lemma 6.2. Then $q=20$, $o=4$, and $P$ consists of $z$ and four fully selected double tips. These four tips are the endpoints of all outer edges. Every supported vertex has selected degree four, and the support has ten vertices.

**Proof.** The quadruple $z$ uses four type incidences, while every other member of $P$ uses at least two. Hence

$$ 2|P|+2\leq\sum_{x\in P}|T(x)|\leq12,\qquad o+1\leq|P|. \tag{6.1}

The second inequality is the strengthened charge in Lemma 3.8, using at least the quadruple $z$. Thus $|P|\leq5$, $o\leq4$, and $q\leq16+o\leq20$. All inequalities must be equalities: $q=20$, $o=4$, $|P|=5$, and the type sum is twelve.

Equality also gives $d_Q(a)=4$ for every $a\in A$, so all original type edges are selected. The four vertices in $P\setminus\{z\}$ have type size exactly two, and are therefore fully selected doubles. No other vertex has nonempty type: it would contribute a positive additional incidence beyond the total twelve.

A quadruple cannot be incident with an outer edge. An endpoint of type zero would require its partner to be a quadruple to cover $A$, again impossible. Hence every outer edge has both endpoints in the four doubles. Their eight outer incidences, with at most two per double, force outer degree exactly two at each double. Together with the two selected type edges, this gives selected degree four there.

Every endpoint of a selected edge belongs to $\{r,z\}\cup A\cup D_2$: this is immediate for root edges and edges in $K$, and was just proved for outer edges. Conversely all vertices of this union are supported. The sets are disjoint, with sizes two, four and four. The root has selected degree four, the quadruple has its four type edges selected, the labels in $A$ have selected degree four, and the double tips do as well. This proves every assertion. ∎

**Theorem 6.4 (Twenty-clique rigidity).** Every conflict clique has at most twenty edges. A clique of twenty edges is exactly the complete edge set of a connected component of $G$ isomorphic to $C_5[2]$.

**Proof.** If $q\geq20$, Lemmas 6.1-6.3 apply and force $q=20$. This proves the universal bound.

Now suppose $q=20$. The four fully selected doubles of Lemma 6.3 split, by Lemma 3.4, into two equal-type classes $X,Y$ of size two. Let $U$ be the type of the vertices in $X$, and let $V$ be the type of the vertices in $Y$. The two types are distinct pairs.

The types are disjoint. Indeed, tips in different classes are adjacent by the witness rule. A label shared by their types would put that adjacency inside the neighbourhood of a member of $A$. This neighbourhood is independent by Lemma 6.1, since every label has selected degree four. Thus $U$ and $V$ are complementary pairs in $A$.

Put $B_0=\{r,z\}$. The five pairwise disjoint pairs $B_0,U,X,Y,V$ have the following exact original neighbourhoods:

$$ N_G(v)=U\cup V\quad(v\in B_0),\qquad N_G(v)=B_0\cup X\quad(v\in U),

$$ N_G(v)=U\cup Y\quad(v\in X),\qquad N_G(v)=X\cup V\quad(v\in Y),

$$ N_G(v)=B_0\cup Y\quad(v\in V). \tag{6.2}

For $r,z$, their four neighbours are all of $A$. For members of $X,Y$, the exact equations follow from the saturation assertion in Lemma 3.4. Each member of $U$ is adjacent to $r,z$ and both members of $X$, which already give four distinct neighbours; the degree bound makes this the complete neighbourhood. The assertion for $V$ is identical with $Y$ in place of $X$.

These equations describe the doubled five-cycle in the cyclic order $B_0,U,X,Y,V$. They exclude every edge within a pair, every nonconsecutive-pair edge, and every edge to a vertex outside the five pairs. The graph on the union is connected: its consecutive pairs are joined completely, and every pair is nonempty. It is therefore a whole connected component of $G$.

Finally, Lemma 6.3 shows that every supported vertex has selected degree four. Every original edge incident with such a vertex is selected, because its original degree is at most four. Thus $Q$ is the complete edge set of this component, rather than merely a subset of its edges. ∎

**Corollary 6.5 (Isolation in the conflict graph).** No edge outside a twenty-edge conflict clique conflicts with an edge inside it. Two twenty-edge conflict cliques are either equal or disjoint, and distinct ones lie in distinct components of $G$.

**Proof.** Theorem 6.4 identifies each clique with all edges of one connected component. An original edge outside that component cannot share a vertex with it or join its vertices to another component. Thus it cannot witness a conflict across the two edge sets. If two such cliques meet, their components meet, so the components and their complete edge sets are equal. ∎

## 7. Private neighbourhoods and the 19.5 criterion

We now work temporarily in an arbitrary finite simple graph $J$. A maximum independent set has largest possible cardinality; this is stronger than being inclusion-maximal. Write $N_J[v]$ for a closed neighbourhood. Exchange arguments have methodological precedents such as [2]; every fact needed here is proved below.

**Lemma 7.1 (Private cliques and exchange).** Choose a maximum independent set $I$ minimizing $\sum_{v\in I}d_J(v)$. For each $v\in I$, define

$$ P_v=\{x\in V(J):N_J[x]\cap I=\{v\}\}. \tag{7.1}

Then $v\in P_v\subseteq N_J[v]$, the set $P_v$ is a clique, and every $x\in P_v$ satisfies $d_J(x)\geq d_J(v)$.

**Proof.** The optimized choice exists because the graph is finite. Independence of $I$ shows that $v$ is private to itself, and the defining condition gives the neighbourhood containment.

If distinct $x,y\in P_v$ were nonadjacent, neither could equal $v$, since every other member of $P_v$ is adjacent to $v$. Replacing $v$ by $x,y$ would give a larger independent set: neither new vertex is adjacent to any member of $I\setminus\{v\}$. This is impossible.

For $x\in P_v\setminus\{v\}$, replacing $v$ by $x$ preserves independence and cardinality. Minimality of the degree sum gives $d_J(v)\leq d_J(x)$. The case $x=v$ is immediate. ∎

**Lemma 7.2 (Private-neighbourhood count).** With $I$ and $P_v$ as above,

$$ 2|V(J)|\leq\sum_{v\in I}\bigl(d_J(v)+1+|P_v|\bigr). \tag{7.2}

**Proof.** Put $m(x)=|N_J[x]\cap I|$. Maximality gives $m(x)\geq1$ for every vertex. The private sets are pairwise disjoint, and their union is precisely the set of vertices for which $m(x)=1$. Such a vertex contributes one to $\sum_x m(x)$ and one to the total private-set size; every other vertex contributes at least two to the first sum. Therefore

$$ 2|V(J)|\leq\sum_{x\in V(J)}m(x)+\sum_{v\in I}|P_v|.

Counting pairs $(x,v)$ with $v\in I\cap N_J[x]$ gives $\sum_x m(x)=\sum_{v\in I}(d_J(v)+1)$, proving (7.2). ∎

**Lemma 7.3 (A 19.5 criterion without twenty-cliques).** Suppose $\Delta(J)\leq24$, every clique of $J$ has size at most nineteen, and its cliques satisfy the five bounds of Theorem 5.1 when the threshold is measured by degrees in $J$. Then

$$ 2|V(J)|\leq39\alpha(J). \tag{7.3}

**Proof.** Choose $I$ as in Lemma 7.1 and fix $v\in I$, writing $d=d_J(v)$. If $d\leq18$, then $|P_v|\leq d+1$ and $d+1+|P_v|\leq38$. If $d=19$, the global clique bound gives $|P_v|\leq19$, so this sum is at most thirty-nine.

If $20\leq d\leq24$, the private set is a clique all of whose vertices have degree at least $d$, by Lemma 7.1. The five bounds give respectively

$$ d+1+|P_v|\leq39,\ 39,\ 39,\ 39,\ 38\quad(d=20,21,22,23,24).

Thus every summand of (7.2) is at most thirty-nine. Since $|I|=\alpha(J)$, the result follows. ∎

The exclusion of twenty-cliques in Lemma 7.3 is a separate essential premise. The graph $K_{20}$ has degree nineteen at every vertex, so all five high-degree conditions are vacuous there, but $2|V(K_{20})|=40>39\alpha(K_{20})$.

**Proposition 7.4 (Candidates containing no twenty-clique).** If $F\subseteq E(G)$ contains no conflict clique of size twenty, then it contains an induced matching $M$ of $G$ with $2|F|\leq39|M|$.

**Proof.** Set $J=H_G[F]$. Lemma 2.1 gives $\Delta(J)\leq24$. Theorem 6.4 and the hypothesis imply that every clique of $J$ has size at most nineteen.

Let $Q$ be a clique in $J$ whose vertices have $J$-degree at least $t$, where $t$ is one of the five thresholds. It is also a conflict clique in the original graph, and

$$ c(e)=d_{H_G}(e)\geq d_J(e)\geq t\quad(e\in Q).

Theorem 5.1 therefore supplies all the bounds required by Lemma 7.3. Its independent set is a subset of $F$ consisting of pairwise nonconflicting original edges, hence is the desired induced matching. This proof includes $F=\varnothing$ with the empty matching. ∎

## 8. Actual components and the final bound

**Lemma 8.1 (The doubled-five-cycle obstruction).** In $C_5[2]$, every pair of distinct edges conflicts. Its complete edge set is consequently a twenty-edge conflict clique, and its largest induced matching has size one.

**Proof.** Each edge joins two consecutive pairs of the five-cycle. If two edges use the same pair of consecutive clusters, they meet or have cross-adjacent endpoints in that complete bipartite graph. If their corresponding cycle edges share a cluster, an endpoint in the shared cluster is adjacent to an endpoint of the other edge in a neighbouring cluster. If the two cycle edges are disjoint, one endpoint cluster of one is adjacent on the five-cycle to an endpoint cluster of the other, again supplying a cross-edge. These cases exhaust pairs of cycle edges. There are twenty original edges, and a single edge is itself an induced matching. ∎

@figure doubled_cycle

Together, Theorem 6.4 and Lemma 8.1 give a bijection between twenty-edge conflict cliques contained in $F$ and the components counted by $t_G(F)$. The forward map takes the support of the clique; the reverse map takes the complete edge set of the component. Neither map counts a choice of the five-pair labelling.

**Proof of Theorem 1.1.** List the components counted by $t=t_G(F)$ as $D_1,\ldots,D_t$, and put

$$ F_0=F\setminus\bigcup_{i=1}^{t}E(D_i),\qquad |F_0|=|F|-20t. \tag{8.1}

Every $E(D_i)$ is contained in $F$ by definition, and distinct components have disjoint edge sets, proving the cardinality identity.

The residual candidate set $F_0$ contains no twenty-edge conflict clique. If it contained one, Theorem 6.4 would identify it with the complete edge set of a doubled-five-cycle component of $G$. Since it is contained in $F$, that component would be one of the $D_i$, whose edges were removed in (8.1), a contradiction.

By Proposition 7.4 choose an induced matching $M_0\subseteq F_0$ with $2|F_0|\leq39|M_0|$. Choose one edge $e_i$ from each $D_i$, and put

$$ M=M_0\cup\{e_1,\ldots,e_t\}.

The chosen edges lie in different original components and do not conflict with any edge of $M_0$. Thus $M$ is an induced matching of the original graph, $M\subseteq F$, and $|M|=|M_0|+t$. Finally,

$$ 2|F|=2|F_0|+40t\leq39|M_0|+40t=39|M|+t.

This is exactly (1.2). If $t=0$, the same argument uses $F_0=F$ and $M=M_0$; if $F$ is empty, it gives the empty matching. No graph obtained by deleting unselected original edges has been substituted for $G$. ∎

**Corollary 8.2 (Pure 19.5 cases).** If no doubled-five-cycle component has its complete edge set contained in $F$, then $F$ contains an induced matching of size at least $\lceil2|F|/39\rceil$. In particular, if $G$ has no component isomorphic to $C_5[2]$, this holds for every candidate set $F$.

**Proof.** The hypothesis is precisely $t_G(F)=0$. Apply Theorem 1.1 and use the integrality of the matching size. ∎

**Corollary 8.3 (Necessity of the component correction).** With the coefficient thirty-nine fixed in (1.2), the coefficient one in front of $t_G(F)$ cannot be reduced uniformly. For a disjoint union of $t$ doubled five-cycles and $F=E(G)$, equality holds in (1.2).

**Proof.** Each component contributes twenty candidate edges and permits exactly one edge in an induced matching, by Lemma 8.1. Thus $|F|=20t$ and the maximum matching size is $t$, giving $40t=39t+t$. Already $t=1$ forces any proposed correction coefficient to be at least one. ∎

The construction also recovers the prescribed-set twenty-packing bound: it chooses one edge in each fully selected exceptional component, so $t_G(F)\leq|M|$, and (1.2) gives $|F|\leq20|M|$.

If $G$ has no doubled-five-cycle component, Corollary 8.2 says that the Hall ratio of its conflict graph is at most $19.5$:

$$ \rho(H_G)=\max_{\varnothing\neq F\subseteq E(G)}\frac{|F|}{\alpha(H_G[F])}\leq19.5,

with value zero when the edge set is empty. This is a separate cardinality guarantee for each candidate set. It is not a proof of an arbitrary nonnegative weighted analogue, a fractional strong chromatic bound of $19.5$, or an integer strong edge-colouring bound. Hall ratio and fractional chromatic number are different parameters; see [3]. We do not assert that the constant $19.5$ is optimal when the correction vanishes. The maximum-independent-set optimization in Section 7 is an existence argument and carries no polynomial running-time claim.

## Appendix A. Correspondence with the Lean development

The mathematical endpoint of this manuscript is the declaration

**StrongEdge.induced_matching_packing195_with_connected_component_count**

in **StrongEdge/TightComponents.lean**. Its graph hypothesis is that every original vertex has degree at most four; the candidate set is arbitrary. The remaining parameters specify a finite vertex type, decidable equality and adjacency. Its conclusion is an induced matching contained in the candidates and the inequality with the cardinality of **tightComponentsIn**.

The definition **IsFiveCycleBlowupComponent** gives five disjoint pairs and exact original-neighbour equations, the certificate used in (6.2). The declaration **five_cycle_blowup_is_connected_component** proves that their union is the support of an actual original connected component. The declaration **tightComponentCount_eq_connected_component_count** identifies the support-based finite count with the count of actual components. Thus the final correction does not count labelled presentations or arbitrary induced subgraphs.

The code first removes one twenty-clique at a time while keeping the original conflict graph fixed. Its recursion uses **twenty_clique_conflict_closed** and **twentyCliquesIn_sdiff**. The resulting count of twenty-cliques is bounded by the count of their distinct tight supports, which is then identified with the actual component count. Section 8 presents the equivalent simultaneous removal argument, and proves the reverse elementary correspondence as well using Lemma 8.1. The code needs only the forward counting inequality for its final bound.

@table Manuscript step | Principal StrongEdge module or declaration
@row Lemmas 2.1-2.2: covers and slack | Bounds/ConflictDegree; EdgeCounting; ConflictRigidity; High20Local
@row Lemmas 2.3-2.4: preliminary bounds | Bounds/SubcubicEighteen; Bounds/DegreeTwoClique
@row Lemma 2.5 and identity (2.4) | Bounds/SubcubicBoundary
@row Lemmas 3.1-3.3: roots, loads, singletons | Bounds/RootCounting; High21Local; High22Local; High20Local
@row Lemmas 3.4-3.6: double-tip saturation | Bounds/High21Double; Bounds/High21ImprovedRoot; Bounds/TwentyCliqueParts
@row Lemma 3.7: the unique triple | Bounds/High20UniqueTriple; Bounds/High20Improved
@row Lemma 3.8: outer-edge charging | Bounds/TwentyCliqueCounting
@row Lemma 4.1 and Proposition 4.2 | Bounds/SubcubicBoundary; Bounds/SubcubicSeventeen
@row Lemma 4.3: defect counts and inequalities | Bounds/SubcubicDefect
@row Lemma 4.4: thirteen support vertices | Bounds/High22SupportSize
@row Proposition 4.5: final high22 boundary | Bounds/LowSupportGeometry; Bounds/High22Improved
@row Theorem 5.1: five strengthened thresholds | Packing195Thresholds; Bounds/High20Improved; High21Improved; High22Improved; High23Improved; High24
@row Lemmas 6.1-6.2: root and quadruple | Bounds/TwentyCliqueRoot; TwentyCliqueCounting; TwentyCliqueTypes
@row Lemma 6.3: equality and saturation | Bounds/TwentyCliqueSaturation; TwentyCliqueComponent
@row Theorem 6.4 and Corollary 6.5 | Bounds/TwentyCliqueParts; TwentyCliqueRigidity; TwentyCliqueComponent
@row Lemmas 7.1-7.3: private-set criterion | PrivateExchange; DoubleCount; Packing195; MinimalPacking195
@row Proposition 7.4: prescribed-set transfer | induced_matching_packing195_of_no_twenty_clique
@row Theorem 1.1: component correction | Packing195Unconditional; TightComponents
@row The doubled-five-cycle regression | Tests195Unconditional

The exact cover identity in Lemma 2.1 is proved directly in the manuscript; the main StrongEdge development packages some uses as one-sided cover inequalities. The companion PaperRoute **ExactCover** module also records the exact identity. Likewise, Lemma 3.6 states the threshold-free conclusion of the displayed saturation argument, while the main StrongEdge seventeen-bound interface uses its high21 specialization. These are expository choices, not additional unproved premises of Theorem 1.1. The main endpoint depends only on the audited StrongEdge development.

The verified source snapshot is commit **1160b4529436efa82d579a2f7e4b97e57ae5d9f0** [5]. It uses Lean **4.35.0-rc4** and mathlib revision **49fd9dee36e7bbf345fe7981d2de6aeeb591f75b**. The saved full build contains **1,197 jobs**, and the five saved axiom audits cover **376 declarations**. The source inventory contains **75 Lean files** and four pinned configuration or launcher files. Accepted axiom dependencies are only **propext**, **Classical.choice** and **Quot.sound**. The recorded source checks contain no proof placeholders or user-supplied domain axioms.

The regression suite includes the path with an unselected conflict witness, the empty candidate set, the abstract twenty-clique obstruction to the uncorrected criterion, and the actual doubled five-cycle with its degree, edge count, five-pair structure, connected-component status and correction necessity. Finite evaluations in these examples use kernel-checked **decide**, not **native_decide**. The structural proof does not depend on a finite graph search or a probabilistic experiment.

This appendix identifies the mathematical arguments and their formal counterparts. The Lean kernel checks the formal proof terms; it does not check the English text or its typesetting. The manuscript therefore also gives the full reasoning needed to assess the proof independently of the software.

## References

@ref [1] F. Joos and V. H. Nguyen, *Induced Matchings in Graphs of Degree at Most 4*, SIAM Journal on Discrete Mathematics 30 (2016), no. 1, 154-165. DOI: <link href="https://doi.org/10.1137/140986980">10.1137/140986980</link>.

@ref [2] M. Fürst, M. Leichter and D. Rautenbach, *Locally Searching for Large Induced Matchings*, Theoretical Computer Science 720 (2018), 64-72. DOI: <link href="https://doi.org/10.1016/j.tcs.2018.02.006">10.1016/j.tcs.2018.02.006</link>. This is methodological context for local exchange arguments, not a lemma assumed in the proof.

@ref [3] R. Steiner, *Fractional Chromatic Number Vs. Hall Ratio*, Combinatorica 45 (2025), Article 37. DOI: <link href="https://doi.org/10.1007/s00493-025-00164-0">10.1007/s00493-025-00164-0</link>.

@ref [4] *Induced Matchings in Prescribed Edge Sets of Graphs of Maximum Degree Four*, Route A; and *A Formal-Development Proof of Prescribed-Edge Induced-Matching Packing*, Route B. Companion proof manuscripts, 10 October 2026, preserved in the <link href="https://github.com/congyuemao/strong-edge-lean-verification/tree/1160b4529436efa82d579a2f7e4b97e57ae5d9f0/output/pdf">verification repository</link>.

@ref [5] *StrongEdge: unconditional corrected 19.5 packing*, Lean source and verification archive, 10 October 2026. <link href="https://github.com/congyuemao/strong-edge-lean-verification/tree/1160b4529436efa82d579a2f7e4b97e57ae5d9f0/strong_edge_lean_starter">Pinned source snapshot and saved verification evidence</link>.
