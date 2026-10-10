# Induced Matchings in Prescribed Edge Sets of Graphs of Maximum Degree Four

@subtitle A proof manuscript
@date 10 October 2026

@abstract
Let $G$ be a finite simple graph of maximum degree at most four. We prove that every prescribed set $F\subseteq E(G)$ contains an induced matching $M$ of the original graph such that $|F|\leq 20|M|$. Equivalently, every induced subgraph of the square of the line graph of $G$ has an independent set containing at least one twentieth of its vertices. The proof establishes five clique bounds, according to the degrees of their vertices in the full conflict graph, and combines them with a private-neighbourhood counting argument. All structural bounds needed for the argument are proved below. The constant is sharp by the familiar doubled five-cycle. The full-edge-set bound and this extremal example are already present in Joos and Nguyen (2016); the prescribed-set formulation retains all conflicts of the original graph. An appendix records the correspondence with the audited Lean development. No claim of priority over the entire literature is made.

@keywords Induced matching; prescribed edge set; square of a line graph; Hall ratio; maximum degree four; formal verification.

## 1. Statement and context

All graphs in this manuscript are finite, simple and undirected. An **induced matching** in $G$ is a set of pairwise vertex-disjoint edges such that no edge of $G$ joins endpoints of two different chosen edges. In particular, an edge outside a prescribed candidate set is still allowed to prohibit a pair of candidate edges.

**Theorem 1.1 (Prescribed-edge packing).** Let $\Delta(G)\leq 4$ and let $F\subseteq E(G)$. There is an induced matching $M$ in $G$ satisfying

$$ M\subseteq F,\qquad |F|\leq 20|M|. \tag{1.1}

Thus $|M|\geq \lceil |F|/20\rceil$. The constant $20$ cannot be replaced by any smaller real constant.

For distinct edges $e,f\in E(G)$, say that $e$ and $f$ **conflict** if they share an endpoint or if an endpoint of $e$ is adjacent in $G$ to an endpoint of $f$. The **conflict graph** $H_G$ has vertex set $E(G)$ and this adjacency relation; it is the square $L(G)^2$ of the line graph. Independent sets of $H_G$ are exactly induced matchings of $G$. Write $c(e)=d_{H_G}(e)$ for the full conflict degree of an edge.

If $\alpha(J)$ is the independence number of a graph $J$, its Hall ratio is

$$ \rho(J)=\max_{\varnothing\neq X\subseteq V(J)}\frac{|X|}{\alpha(J[X])}. \tag{1.2}

We set $\rho(J)=0$ when $J$ is empty. Theorem 1.1 is equivalent to $\rho(H_G)\leq 20$. Here $H_G[F]$ is obtained by restricting the vertices of the conflict graph, while its edges retain their meaning in the full original graph.

Joos and Nguyen [1, Theorem 1.1 and the corollary on p. 156] prove

$$ \nu_s(G)\geq \frac{n(G)-i(G)-c_5(G)}{9}, \tag{1.3}

where $i(G)$ counts isolated vertices and $c_5(G)$ counts components isomorphic to the doubled five-cycle. They explicitly deduce $\nu_s(G)\geq |E(G)|/20$, and obtain $|E(G)|/18$ when there is no such component. Their sharpness example and the optimality of the full-edge-set constant are therefore prior results. Theorem 1.1 extends the full-edge-set $20$-bound to prescribed sets; it does not subsume all the more refined assertions in (1.3).

The distinction between these formulations is visible on the path $0-1-2-3$. For $F=\{01,23\}$ the two candidates conflict through $12$, even though $12\notin F$. Deleting $12$ changes the question. Consequently, applying a full-edge-set theorem to the graph with edge set $F$ is not a proof of Theorem 1.1. Likewise, a large induced matching chosen without regard to $F$ may avoid $F$ entirely.

The private-neighbourhood and exchange ideas used here have methodological precedents; see, for example, the local-search analysis of Fürst, Leichter and Rautenbach [3]. The strong edge-colouring bound $21$ of Huang, Santana and Yu [2] directly gives the analogous prescribed-set bound with $21$. The argument below proves the bound $20$ by clique estimates and counting. It does not construct a strong edge-colouring with $20$ colours or prove a fractional strong chromatic bound of $20$. In general a Hall-ratio bound cannot be promoted to the corresponding fractional chromatic bound [4].

## 2. Edge covers and two elementary clique bounds

A **conflict clique** is a set $Q\subseteq E(G)$ of pairwise conflicting edges. Throughout the structural part of the proof, $Q$ denotes such a clique and

$$ q=|Q|,\qquad d_Q(x)=|\{e\in Q:x\in e\}|.

The number $d_Q(x)$ is the degree in the selected edge set, whereas $d_G(x)$ counts all original edges. These quantities will not be interchanged. For $S\subseteq V(G)$, let $e_G(S)$ be the number of original edges with both endpoints in $S$.

**Lemma 2.1 (Endpoint-neighbour cover).** For $uv\in E(G)$ put

$$ C(uv)=(N_G(u)\setminus\{v\})\cup(N_G(v)\setminus\{u\}).

Then $u,v\notin C(uv)$, $|C(uv)|\leq 6$, and

$$ c(uv)=\sum_{x\in C(uv)}d_G(x)-e_G(C(uv))\leq 24-e_G(C(uv)). \tag{2.1}

For $uv\in Q$ one also has

$$ q\leq 1+\sum_{x\in C(uv)}d_Q(x). \tag{2.2}

**Proof.** An edge other than $uv$ conflicts with $uv$ exactly when it has an endpoint in $C(uv)$. Indeed, an edge sharing $u$ or $v$ has its other endpoint in that set; for a disjoint conflicting edge the cross-adjacent endpoint lies in the set. The converse follows immediately from the definition of $C(uv)$. The incidence sum counts an edge meeting $C(uv)$ once, with one extra count precisely when both endpoints lie there. This proves the identity. Each of the two sets forming the cover has at most three vertices. Applying the same cover to $Q\setminus\{uv\}$ proves (2.2). ∎

**Lemma 2.2 (Triangles and local slack).** All edges have $c(e)\leq 24$. An edge in a triangle has $c(e)\leq 20$. If $c(uv)\geq t$, then $e_G(C(uv))\leq 24-t$. If a triangle edge has $c(uv)\geq 20$, its cover has no internal edge. If $c(uv)\geq 21$, then $d_G(u)=d_G(v)=4$ and $uv$ is in no triangle.

**Proof.** A common neighbour of $u,v$ reduces the cover size to at most five, so (2.1) gives the triangle assertion and the empty-cover assertion at equality. If either endpoint has degree at most three, the cover likewise has size at most five. The other statements follow from (2.1). ∎

**Lemma 2.3 (Selected support degree at most three).** If $d_Q(x)\leq 2$ for every $x$, then $q\leq 13$. If $d_Q(x)\leq 3$ for every $x$, then $q\leq 18$.

**Proof.** The empty clique is immediate. Otherwise (2.2) gives $q\leq 1+6s$ when all selected degrees are at most $s$. It remains to exclude $q=19$ for $s=3$.

Suppose $q=19$. For every selected edge $uv$, equality throughout (2.2) forces $|C(uv)|=6$ and $d_Q(a)=3$ for every $a\in C(uv)$. We show that every vertex supporting a selected edge has selected degree three. Let $xy\in Q$. Since its cover has size six, there is a neighbour $a\neq y$ of $x$. This vertex lies in $C(xy)$ and hence has three selected incident edges. Choose a selected edge $ab$ with $b\neq x$. Now $x\in C(ab)$, so $d_Q(x)=3$ as well. Thus every selected degree is either zero or three. The handshake identity $\sum_x d_Q(x)=2q=38$ would make $38$ divisible by three, a contradiction. ∎

The next lemma will be used inside a set of vertices while retaining every original edge between those vertices.

**Lemma 2.4 (A degree-two restriction).** Suppose $P\subseteq V(G)$, every edge of a conflict clique $Q'$ has both endpoints in $P$, and $|N_G(x)\cap P|\leq 2$ for every $x\in P$. Then $|Q'|\leq 5$. If there is a set $D\subseteq P$ such that each selected edge in $Q'$ has exactly one endpoint in $D$, then $|Q'|\leq 4$. Original edges outside $Q'$ need not respect this bipartition.

**Proof.** Conflicts between edges with endpoints in $P$ are unchanged in the vertex-induced graph $G[P]$. In that graph an endpoint-neighbour cover has at most two vertices, each of selected degree at most two. Hence $|Q'|\leq 1+2\cdot 2=5$.

If equality holds, every cover of a selected edge has two vertices of selected degree two. For a supported vertex $x$ choose $xy\in Q'$. Equality forces $x$ to have a neighbour $a\neq y$ in $P$; this neighbour lies in the cover and has two selected edges. Choose $ab\in Q'$ with $b\neq x$. Since $x$ belongs to the cover of $ab$, it too has selected degree two. Thus every supported vertex has selected degree two. If each selected edge crosses $D$, then $|Q'|=\sum_{x\in D}d_{Q'}(x)$ is even, contradicting $|Q'|=5$. ∎

## 3. Root notation and counting tools

Choose a vertex $r$, called the root, and write

$$ A=N_G(r),\qquad R=\{a\in A:ra\in Q\},\qquad s=|R|=d_Q(r).

When $A$ is independent, every selected edge has exactly one of the following forms: a root edge $ra$ with $a\in R$; an edge $ax$ with $a\in A$ and $x\notin A\cup\{r\}$; or an edge with both endpoints outside $A\cup\{r\}$. Denote the second set by $K$, the third by $O$, and put $k=|K|$, $o=|O|$. Thus

$$ q=s+k+o,\qquad s+k=\sum_{a\in A}d_Q(a). \tag{3.1}

Edges in $O$ will be called outer edges. Even without independence of $A$, every selected edge either meets $A$ or is outer, so

$$ q\leq \sum_{a\in A}d_Q(a)+o. \tag{3.2}

For $x\neq r$ define its **type**

$$ T(x)=N_G(x)\cap A.

A vertex of type size one is a singleton, of type size two a double, and of type size three a triple. Let $P=\{x\neq r:|T(x)|\geq 2\}$ be the set of multiple vertices. When $A$ is independent, any vertex of nonempty type is outside $A\cup\{r\}$. Let $B$ consist of the vertices $x$ incident with an edge $ax\in K$; these are the selected tips.

**Lemma 3.1 (Root identities).** Assume $A$ is independent. For $xy\in O$,

$$ R\subseteq T(x)\cup T(y). \tag{3.3}

Moreover,

$$ d_O(x)+|T(x)|\leq 4,\qquad \sum_{x\in P}|T(x)|\leq 3|A|\leq 12,\qquad |P|\leq 6. \tag{3.4}

If all edges of $Q$ have conflict degree at least $t$, then, for every $a\in R$,

$$ L_a:=\sum_{\substack{x\neq r\\a\in T(x)}}(|T(x)|-1)\leq 24-t. \tag{3.5}

**Proof.** The outer edge $xy$ conflicts with every selected $ra$. Its endpoints are not adjacent to $r$ and are distinct from $r,a$, so at least one is adjacent to $a$. This proves (3.3).

The neighbours counted by $d_O(x)$ lie outside $A$, disjoint from those in $T(x)$, proving the first inequality in (3.4). Each label $a\in A$ has at most three neighbours other than $r$. Counting incidences between $A$ and $P$ proves the other two inequalities.

For (3.5), the sets $A\setminus\{a\}$ and $N_G(a)\setminus\{r\}$ are disjoint, because $A$ is independent. For each $x\neq r$ adjacent to $a$ and each $b\in T(x)\setminus\{a\}$, the original edge $bx$ lies inside $C(ra)$. All these edges are distinct: their endpoints lie in the two disjoint sets just described. Their number is $L_a$. Lemma 2.2 therefore bounds it by $24-t$. ∎

The summation with two conditions in (3.5) runs over all original vertices of the specified type, not merely selected tips. This is essential when a later outer edge uses a vertex whose edges to $A$ were not selected.

**Lemma 3.2 (Independence around a high-degree root).** Suppose every selected edge has conflict degree at least $21$ and $s\geq 3$. Then $|A|=4$ and $A$ is independent.

**Proof.** A selected edge incident with $r$ gives $d_G(r)=4$ by Lemma 2.2. Every pair of vertices of the four-element set $A$ has at least one endpoint in $R$, since $|R|\geq 3$. An edge inside $A$ would therefore form a triangle with a selected edge incident with $r$, contradicting Lemma 2.2. ∎

**Lemma 3.3 (A singleton controls the selected tips).** Assume $A$ is independent. If $ax\in K$ and $T(x)=\{a\}$, then every $y\in B$ with $a\notin T(y)$ is adjacent to $x$. Consequently $|B|\leq 6$.

**Proof.** Choose $by\in K$. As $a\notin T(y)$, we have $b\neq a$. The edges $ax$ and $by$ have no common endpoint. Independence of $A$, the singleton type of $x$, and the exclusion of $a$ from $T(y)$ rule out, respectively, the cross-edges $ab$, $xb$ and $ay$. Their required conflict must therefore be witnessed by $xy$. Thus

$$ B\subseteq (N_G(a)\setminus\{r\})\cup(N_G(x)\setminus\{a\}),

whose two sets each have size at most three. ∎

**Lemma 3.4 (Fully selected doubles).** Assume $A$ is independent. Call a double $x$ fully selected if both edges from $x$ to $T(x)$ belong to $K$, and let $D_2$ be the set of such vertices. Then $|D_2|\leq 4$.

**Proof.** If two fully selected doubles $x,y$ have different types, choose $a\in T(x)\setminus T(y)$ and $b\in T(y)\setminus T(x)$. Conflict between $ax$ and $by$ forces $xy$, since all other possible witnesses are excluded by the two type differences and independence of $A$.

If all vertices of $D_2$ have the same type, choose a label in that type. Its at most three neighbours other than $r$ contain $D_2$, so $|D_2|\leq 3$. Otherwise choose $x,y\in D_2$ with different types. Every $z\in D_2$ has a type different from at least one of $T(x),T(y)$, so is adjacent to at least one of $x,y$. This includes $z=x$ or $z=y$, since $xy$ is an edge. All such vertices lie outside $A$. Each of $x,y$ has at most two neighbours outside $A$, yielding $|D_2|\leq 4$. ∎

**Lemma 3.5 (Complementary doubles on outer edges).** Suppose $s=|A|=4$, $A$ is independent, and both endpoints of every edge in $O'\subseteq O$ have type size at most two. Then $|O'|\leq 4$.

**Proof.** Equation (3.3) implies that the endpoint types of each edge in $O'$ are disjoint two-element sets whose union is $A$. Both endpoints lie in $P$. Every vertex of $P$ has at least two neighbours in $A$, so it has at most two neighbours in $P$, because $A\cap P=\varnothing$. Fix $a\in A$ and put $D=\{x\in P:a\in T(x)\}$. Each edge of $O'$ has exactly one endpoint in $D$. Lemma 2.4, applied with the full original graph on $P$, proves the bound. ∎

**Lemma 3.6 (All types at most two).** Suppose $s=|A|=4$, $A$ is independent, and $|T(x)|\leq 2$ for all $x\neq r$. Then $q\leq 18$.

**Proof.** If there is a selected singleton tip, Lemma 3.3 gives $|B|\leq 6$. Otherwise $B\subseteq P$, so (3.4) gives the same bound. Every selected tip supports one edge of $K$, with a second edge possible only for a fully selected double. Therefore $k\leq |B|+|D_2|\leq 10$ by Lemma 3.4. Lemma 3.5 gives $o\leq 4$. Equation (3.1) yields $q\leq 4+10+4=18$. ∎

## 4. The five structural bounds

We now prove the estimates used in the packing argument. All degrees in the hypotheses of the following theorem are full degrees in $H_G$, irrespective of the selected clique.

**Theorem 4.1 (Clique bounds by full conflict degree).** Let $\Delta(G)\leq 4$ and let $Q$ be a conflict clique. For each row of the following table, the condition $c(e)\geq t$ for every $e\in Q$ implies $|Q|\leq b_t$.

@table Threshold $t$ | 20 | 21 | 22 | 23 | 24
@row Bound $b_t$ | 19 | 18 | 17 | 16 | 13

The cases are proved in the next five subsections. They use no regularity, girth, or nonemptiness hypothesis on the original graph.

### 4.1. Conflict degree at least 24

**Proposition 4.2.** If every $e\in Q$ has $c(e)\geq 24$, then $q\leq 13$.

**Proof.** Equation (2.1) shows that a selected edge has a six-vertex cover with no internal edge. Such an edge belongs to no triangle and no four-cycle: a triangle reduces the cover size, and the edge opposite it in a four-cycle lies inside its cover.

Fix a vertex $u$ and consider selected edges $ax$ with $a\in N_G(u)$ and $x\neq u$. We call all such selected edges with a fixed $a$ a branch at $u$. Each branch has at most three edges. We claim that a branch containing two edges excludes any nonempty branch with a different label.

Suppose $ax_1,ax_2,by$ are selected, where $a,b$ are distinct neighbours of $u$ and $x_1\neq x_2$. For either $i$, the equality $x_i=b$ or $y=a$ would put a selected edge in the triangle $uab$; equality $x_i=y$ would put $ax_i$ in a four-cycle through $u$. Thus these selected edges have disjoint endpoints. If $ab$ were an edge, both $u$ and $b$ would belong to $C(ax_i)$, with the original edge $ub$ internal to this cover, which is impossible. The cross-edge $ay$ would form a four-cycle $u-a-y-b-u$ containing $by$, and $bx_i$ would form a four-cycle containing $ax_i$. All are excluded. Their conflict must be witnessed by $x_i y$. But then $a-x_1-y-x_2-a$ is a four-cycle containing a selected edge, again impossible.

Hence the union of branches with any prescribed set of at most three labels has at most three edges: either all nonempty branches are singletons, or only one branch is nonempty and it has size at most three.

If $Q$ is nonempty, choose $uv\in Q$. Besides $uv$, there are at most three selected edges incident with $u$ and at most three incident with $v$. Every remaining selected edge meets $C(uv)$ by Lemma 2.1. Those meeting $N_G(u)\setminus\{v\}$ belong to at most three branches at $u$ and number at most three; the analogous family at $v$ also numbers at most three. Counting these covering families, with any overlaps harmless, gives $q\leq 1+3+3+3+3=13$. ∎

### 4.2. Conflict degree at least 23

**Proposition 4.3.** If every $e\in Q$ has $c(e)\geq 23$, then $q\leq 16$.

**Proof.** If all selected degrees are at most two, Lemma 2.3 gives $q\leq 13$. Otherwise take a vertex $r$ of maximum selected degree, so $s=3$ or $s=4$. Lemma 3.2 gives an independent four-element neighbourhood $A$. Equation (3.5) gives $L_a\leq 1$ for each $a\in R$.

No type has size at least three. Indeed, such a type meets $R$, and at a common label it contributes at least two to the load. Also, two distinct multiple vertices cannot have a common label in $R$, since they would contribute at least two to its load.

We first show $o\leq 2$. If there is an outer edge $xy$, (3.3) and $|R|\geq 3$ imply that one endpoint, say $x$, contains at least two labels $a,b$ of $R$ in its type. Consider an outer edge avoiding $x$. To cover $a$ and $b$, its endpoints must include vertices having these labels in their types. Any such vertex other than $x$ must be a singleton, by the preceding load observation. Thus the two endpoints would have types $\{a\}$ and $\{b\}$, leaving a third label of $R$ uncovered. This is impossible. All outer edges therefore meet $x$, and (3.4) bounds their number by two.

If $s=3$, maximality of the selected degree gives $\sum_{a\in A}d_Q(a)\leq 12$. Equation (3.2) then gives $q\leq 14$.

If $s=4$, each label in $A=R$ occurs in the type of at most one multiple vertex. The total number of selected edges from $A$ to multiple vertices is therefore at most four. If singleton tips occur, their number is at most six by Lemma 3.3; otherwise their contribution is zero. Hence $k\leq 6+4=10$, and $q\leq 4+10+2=16$. ∎

### 4.3. Conflict degree at least 22

**Proposition 4.4.** If every $e\in Q$ has $c(e)\geq 22$, then $q\leq 17$.

**Proof.** The case of maximum selected degree at most two follows from Lemma 2.3. Otherwise choose a root of maximum selected degree $s\in\{3,4\}$. Its neighbourhood is independent and has four vertices. For every selected root label, (3.5) gives $L_a\leq 2$.

**Case 1: $s=4$.** If some vertex $x$ has $|T(x)|\geq 3$, its type has exactly three elements, since a type of size four exceeds the load bound at each of its labels. Any other multiple vertex has a type meeting $T(x)$; at a common label their load is at least $2+1=3$, impossible. Thus $x$ is the only multiple vertex. Every outer edge covers four labels and must meet a multiple vertex, hence must meet $x$. It follows that $o\leq 1$. Since at most sixteen selected edges meet $A$, (3.2) gives $q\leq 17$.

We may therefore assume all types have size at most two. Every label occurs in at most two multiple types. The sum of the type sizes is at most eight, giving $|P|\leq 4$. Both endpoints of every outer edge belong to $P$, and each has outer degree at most two. The handshake count gives $2o\leq 2|P|\leq 8$, hence $o\leq 4$.

If there is no selected singleton tip, then $k\leq 2|P|\leq 8$, giving $q\leq 16$. Otherwise choose a selected singleton $ax$. Lemma 3.3 gives $|B|\leq 6$, and each multiple selected tip contributes at most one extra edge beyond its first. Therefore $k\leq |B|+|P|\leq 10$, so $q\leq 18$.

Suppose equality $q=18$ holds. The preceding bounds force $k=10$, $o=4$ and $|P|=4$. Every vertex of $P$ then has outer degree exactly two. Together with its two neighbours in $A$, these exhaust all four possible neighbours. In particular no vertex in $P$ is adjacent to the singleton $x$, since the two outer neighbours already belong to $P$. Lemma 3.3 therefore implies that every multiple selected tip has $a$ in its type. At most two multiple vertices contain $a$, by $L_a\leq 2$. There can be at most two extra selected edges beyond the first edge at each tip, so $k\leq |B|+2\leq 8$, contradicting $k=10$. Thus $q\leq 17$.

**Case 2: $s=3$.** Call a vertex heavy if its type contains at least two labels of $R$, and write $Z$ for the set of heavy vertices. A heavy vertex contributes at least one unit to $L_a$ at each of at least two labels $a\in R$. Since $\sum_{a\in R}L_a\leq 6$, there are at most three heavy vertices. Every outer edge covers the three labels of $R$, so has a heavy endpoint. Each heavy vertex has outer degree at most two. Hence $o\leq 2|Z|\leq 6$. The selected degree bound three gives $\sum_{a\in A}d_Q(a)\leq 12$, and consequently $q\leq 18$.

Suppose again that $q=18$. Equality forces $o=6$, $|Z|=3$, and outer degree two at each heavy vertex. Therefore every heavy vertex has type size exactly two, both labels lying in $R$. Its contributions to the three loads total two. The three heavy vertices saturate all three load bounds, so every label of $R$ occurs in exactly two heavy types.

Every multiple type meets $R$, since $|A\setminus R|=1$. A multiple vertex outside $Z$ would add positive load at a label already saturated by $Z$. Thus all multiple vertices are heavy. Each heavy vertex has two selected outer edges; because every selected degree is at most three, it supports at most one edge of $K$. A singleton tip also supports at most one edge of $K$. If singleton tips occur, Lemma 3.3 now gives $k\leq |B|\leq 6$. If none occurs, $B\subseteq Z$ gives $k\leq 3$. In either event $q=s+k+o\leq 3+6+6=15$, contrary to $q=18$. This excludes equality and proves $q\leq 17$. ∎

### 4.4. Conflict degree at least 21

**Proposition 4.5.** If every $e\in Q$ has $c(e)\geq 21$, then $q\leq 18$.

**Proof.** If every selected degree is at most three, Lemma 2.3 applies. Otherwise choose $r$ with $s=4$. Its four-element neighbourhood is independent, and (3.5) gives $L_a\leq 3$ for all $a\in A$.

If every type has size at most two, use Lemma 3.6. Otherwise choose $x$ with $|T(x)|\geq 3$. There is at most one such vertex, because two types of size at least three intersect, contributing at least four at a shared label. All other multiple types have size two. At a label of $T(x)$, there is at most one multiple vertex other than $x$: two would contribute at least $2+1+1=4$.

An outer edge incident with $x$ is one of at most one such edges, by (3.4). If there is an outer edge $yz$ avoiding $x$, its endpoint types are complementary doubles by (3.3). Every multiple vertex $w\neq x$ has a type meeting $T(x)$. A label in that intersection belongs to exactly one of $T(y),T(z)$. The preceding uniqueness at that label forces $w=y$ or $w=z$. Thus $y,z$ are the only possible multiple vertices other than $x$. Every outer edge avoiding $x$ has two multiple endpoints and consequently must be the single edge $yz$. There are at most two outer edges in total. At most sixteen selected edges meet $A$, so $q\leq 16+2=18$. ∎

### 4.5. Conflict degree at least 20

**Proposition 4.6.** If every $e\in Q$ has $c(e)\geq 20$, then $q\leq 19$.

**Proof.** If all selected degrees are at most three, Lemma 2.3 gives the stronger bound eighteen. Otherwise choose a root $r$ with $s=4$, so $A=R$ has four vertices. We may assume $q\geq 20$ and derive a contradiction.

We first prove that $A$ is independent; the threshold twenty alone does not exclude triangles. Suppose $ab$ is an edge inside $A$. The selected edge $ra$ lies in a triangle, so Lemma 2.2 says that $C(ra)$ has no internal edge. If $x\neq r$ and $a\in T(x)$, any $c\in T(x)\setminus\{a\}$ would give an internal edge $cx$ of $C(ra)$. Hence $T(x)=\{a\}$. Interchanging $a,b$ gives the corresponding assertion for $b$. An outer edge must cover all four labels of $R$. To cover $a,b$, its endpoints would have to have the singleton types $\{a\}$ and $\{b\}$, which cannot cover four labels. Thus $o=0$, and (3.2) gives $q\leq 16$, a contradiction. This proves independence.

Equation (3.5) now supplies the load bound $L_a\leq 4$ for every $a\in A$. We distinguish all possible sizes of the types.

**Case 1: a type has size four.** Choose $x$ with $T(x)=A$. Any other type of size at least three would contribute, together with $x$, at least $3+2=5$ at a shared label. Thus every other multiple vertex is a double. At each label there is at most one such other multiple vertex, since $x$ already contributes three units.

No outer edge meets $x$, as all its neighbours lie in $A$. If an outer edge $yz$ exists, its endpoint types are complementary doubles. Any other multiple vertex has a label in common with one of these types, and uniqueness at that label forces it to be $y$ or $z$. Therefore $yz$ is the only possible outer edge. Equation (3.2) gives $q\leq 17$, a contradiction.

**Case 2: there are two triple types and no type of size four.** Let $x,y$ be two distinct triples. Their types share at least two labels; choose distinct shared labels $a,b$. At either shared label, $x$ and $y$ already contribute $2+2=4$. Hence any other vertex containing that label in its type is a singleton.

An outer edge avoiding $x,y$ would have to cover $a,b$ using two singleton endpoints of types $\{a\},\{b\}$. This fails to cover the other two labels. Therefore every outer edge meets $x$ or $y$. Each has at most one neighbour outside $A$, so $o\leq 2$. Again $q\leq 16+2=18$, a contradiction.

**Case 3: exactly one triple type and no type of size four.** Let $x$ be the unique triple, and let $a_0$ be the label in $A\setminus T(x)$. Every outer edge avoiding $x$ has complementary double endpoint types. Lemma 3.5 bounds these edges by four. At most one outer edge meets $x$, giving $o\leq 5$.

We claim $k\leq 10$. The total number of original edges from $A$ to vertices other than $r$ is at most twelve. If at most one of the three edges between $x$ and $T(x)$ is selected, at least two of these original edges are absent from $K$, proving $k\leq 10$.

Otherwise choose two selected edges $ax,bx$ with distinct $a,b\in T(x)$. Consider any selected edge $a_0y\in K$. We have $y\neq x$, and the type of $y$ has size at most two. As it contains $a_0$, it misses at least one of $a,b$, say $a$. The selected edges $ax$ and $a_0y$ have no common endpoint. Their possible cross-edges $aa_0$, $xa_0$ and $ay$ are excluded by independence of $A$ and by the types. Their conflict forces $xy$. But $x$ has at most one neighbour outside $A$, so there is at most one possible selected edge $a_0y\in K$. Each of the other three labels supports at most three edges of $K$. Therefore $k\leq 1+3+3+3=10$, as claimed.

Now (3.1) gives $q\leq 4+10+5=19$, contradicting $q\geq 20$.

**Case 4: every type has size at most two.** Lemma 3.6 gives $q\leq 18$, the final contradiction. These four cases exhaust all type configurations, completing the proof. ∎

Propositions 4.2–4.6 prove every row of Theorem 4.1. In particular, the last row gives thirteen, although the final counting argument only needs fifteen.

## 5. Private neighbourhoods and the packing argument

We temporarily work with an arbitrary finite simple graph $J$. Closed neighbourhoods are denoted by $N_J[v]$. A maximum independent set means one of largest cardinality, not merely an inclusion-maximal set.

**Lemma 5.1 (Optimal independent set and private vertices).** Choose a maximum independent set $I$ in $J$ for which $\sum_{v\in I}d_J(v)$ is as small as possible. For $v\in I$ define

$$ P_v=\{x\in V(J):N_J[x]\cap I=\{v\}\}.

Then $v\in P_v\subseteq N_J[v]$, the set $P_v$ is a clique, and

$$ d_J(x)\geq d_J(v)\quad\hbox{for every }x\in P_v. \tag{5.1}

**Proof.** A choice with both optimization properties exists because there are finitely many subsets. Since $I$ is independent, $v$ is private to itself. The defining intersection implies $x=v$ or $x$ is adjacent to $v$, proving the containment.

If distinct $x,y\in P_v$ were nonadjacent, neither could equal $v$. Replacing $v$ by $x,y$ would give an independent set larger than $I$, because each has no neighbour in $I\setminus\{v\}$. Thus $P_v$ is a clique.

For $x\in P_v\setminus\{v\}$, the set $(I\setminus\{v\})\cup\{x\}$ is independent and has the same size as $I$. Minimality of the degree sum then implies $d_J(v)\leq d_J(x)$. The case $x=v$ is immediate. ∎

**Lemma 5.2 (Private-neighbourhood count).** For a maximum independent set $I$ and the associated private sets,

$$ 2|V(J)|\leq \sum_{v\in I}\bigl(d_J(v)+1+|P_v|\bigr). \tag{5.2}

**Proof.** Put $t(x)=|N_J[x]\cap I|$. Maximality of $I$ gives $t(x)\geq 1$ for every vertex. The sets $P_v$ are pairwise disjoint and their union consists exactly of the vertices with $t(x)=1$. A vertex in that union contributes one to $t(x)$ and one to the private-set count; every other vertex contributes at least two to $t(x)$. Thus

$$ 2|V(J)|\leq \sum_{x\in V(J)}t(x)+\sum_{v\in I}|P_v|.

Double-counting pairs $(x,v)$ with $v\in N_J[x]\cap I$ gives $\sum_x t(x)=\sum_{v\in I}(d_J(v)+1)$, which proves (5.2). ∎

**Lemma 5.3 (A general twenty-packing criterion).** Suppose $\Delta(J)\leq 24$. Assume that every clique whose vertices all have degree at least $t$ has size at most $b_t$, where

$$ b_{20}=19,\quad b_{21}=18,\quad b_{22}=17,\quad b_{23}=16,\quad b_{24}=15.

Then $\alpha(J)\geq |V(J)|/20$.

**Proof.** Take $I$ as in Lemma 5.1. For $v\in I$ write $d=d_J(v)$. If $d\leq 19$, the containment $P_v\subseteq N_J[v]$ gives

$$ d+1+|P_v|\leq 2(d+1)\leq 40.

If $20\leq d\leq 24$, the private set is a clique all of whose vertices have degree at least $d$, by (5.1). Hence $|P_v|\leq b_d=39-d$, and again $d+1+|P_v|\leq 40$. Substituting into (5.2) yields $2|V(J)|\leq 40|I|$. Since $|I|=\alpha(J)$, this is the assertion. ∎

**Proof of Theorem 1.1.** Form $H_G$ using the full original graph and let $J=H_G[F]$. Lemma 2.1 gives $\Delta(H_G)\leq 24$, and therefore $\Delta(J)\leq 24$.

Let $Q$ be a clique in $J$ whose vertices have degree at least $t$ in $J$, where $20\leq t\leq 24$. It is also a clique in $H_G$, and for each $e\in Q$ we have $c(e)=d_{H_G}(e)\geq d_J(e)\geq t$. Theorem 4.1 applies. Its five bounds meet those in Lemma 5.3, with the stronger last bound $13\leq 15$. Thus $J$ has an independent set $M$ with $|F|=|V(J)|\leq 20|M|$. Its vertices are edges from $F$, and their independence in $J$ says that they are pairwise nonconflicting in the original graph. Therefore $M$ is the required induced matching in $G$. If $F$ is empty, the same argument or the choice $M=\varnothing$ applies. Sharpness is proved next. ∎

## 6. Sharpness and the precise scope of the conclusion

**Proposition 6.1 (Sharpness).** There is a $4$-regular graph $B$ with twenty edges for which every induced matching has size at most one.

**Proof.** Start with a cycle of length five. Replace each vertex by an independent pair $V_i$, indexed modulo five, and join every vertex of $V_i$ to every vertex of $V_{i+1}$. There are ten vertices, each with four neighbours, and twenty edges.

Every edge belongs to one of the five complete bipartite graphs between consecutive pairs. Consider two distinct edges. If they belong to the same such graph, they either meet or have cross-adjacent endpoints. If their corresponding cycle edges meet, an endpoint in their common cluster is adjacent to an endpoint of the other edge in a neighbouring cluster. If the corresponding cycle edges are disjoint, some endpoint cluster of one is adjacent on the five-cycle to an endpoint cluster of the other, again giving cross-adjacent endpoints. Thus every pair conflicts. A single edge is an induced matching, so $\nu_s(B)=1$. Taking $F=E(B)$ in an inequality $|F|\leq C|M|$ forces $C\geq 20$. ∎

@figure doubled_cycle

This is the doubled five-cycle already used by Joos and Nguyen [1]; neither the example nor the sharpness of the full-edge-set constant is new here.

The proof establishes a cardinality guarantee separately for each candidate set. It does not establish the analogous inequality for every assignment of arbitrary nonnegative edge weights. In conflict-graph language, the conclusion is the Hall-ratio bound (1.2). The general inequalities $\rho(J)\leq\chi_f(J)\leq\chi(J)$ point in the opposite direction from a proposed deduction of a fractional or ordinary colouring bound from a Hall-ratio bound. Known separations between Hall ratio and fractional chromatic number [4] reinforce the need to keep these statements distinct.

The optimization used in Lemma 5.1 is an existence argument. No running-time claim about the accompanying Lean theorem is made. The mathematical proof is independent of a particular implementation of maximum-independent-set search.

## Appendix A. Correspondence with the formal development

The accompanying project is named **StrongEdge**. Its final theorem, **StrongEdge.induced_matching_packing20**, quantifies over a finite vertex type, a simple graph of maximum degree at most four, and an arbitrary finite set of its edges. Its conclusion is the existence of a subset that is an induced matching in the original graph and satisfies the integer inequality in (1.1). Decidability instances support finite computation; they do not add graph-structural assumptions.

The manuscript gives a mathematical exposition of the audited development. It is not itself a kernel-checked document. Its compact root arguments combine several auxiliary declarations from the code; conversely, some intermediate estimates below are stated more directly than the corresponding implementation wrappers.

@table Manuscript result | Principal Lean source under StrongEdge/
@row Conflict definition and matching equivalence | Basic.lean
@row Lemmas 2.1–2.2 | Bounds/ConflictDegree.lean; Bounds/ConflictRigidity.lean; Bounds/High20Local.lean
@row Lemma 2.3 | Bounds/SubcubicEighteen.lean; Bounds/EdgeCounting.lean
@row Lemma 2.4 | Bounds/DegreeTwoClique.lean
@row Root notation, loads and singleton counts | Bounds/RootCounting.lean; Bounds/High23Local.lean; Bounds/High22Local.lean; Bounds/High21Local.lean
@row Lemmas 3.4–3.6 | Bounds/High21Double.lean; Bounds/High21RootFour.lean; Bounds/High20Local.lean
@row Proposition 4.2 | Bounds/High24.lean
@row Proposition 4.3 | Bounds/High23.lean and its local/support/outer/four modules
@row Proposition 4.4 | Bounds/High22.lean and its heavy/subcubic/root-four modules
@row Proposition 4.5 | Bounds/High21.lean and its large-type/root-four modules
@row Proposition 4.6 | Bounds/High20.lean and its local/four/two-triples/unique-triple/slots/outer modules
@row Lemmas 5.1–5.3 and candidate restriction | Basic.lean; PrivateExchange.lean; DoubleCount.lean; Packing.lean; MinimalPacking.lean

The verified endpoint uses the five bounds $19,18,17,16,15$ in the record **MinimalCliqueBounds20**. The last field is discharged by the stronger bound thirteen. It does not depend on a historical proposed bound of seven for the last threshold.

The independent audit used Lean **4.35.0-rc4** and the pinned mathlib revision **49fd9dee36e7bbf345fe7981d2de6aeeb591f75b**. A clean project build and separate audit elaborations succeeded. The audit inspected the final theorem's types and actual declaration dependency closure; the reported axioms were confined to Lean's standard **propext**, **Classical.choice**, and **Quot.sound**, with no admitted proof or additional axiom in that closure. An independent endpoint-based definition also checked the intended conflict and induced-matching semantics.

The detailed evidence is retained in the workspace's **audit_packing20** directory, especially **AUDIT_PACKING20_SUMMARY.md**, **AUDIT_PACKING20_REPRODUCIBILITY.md**, **AUDIT_PACKING20_SEMANTICS.md**, and **AUDIT_PACKING20_DEPENDENCIES.md**. The separate **joos2016_review/JOOS2016_ORIGINALITY_REVIEW.md** records the comparison with the supplied journal PDF. These audit records support the formal-status statements; they are not substituted for any mathematical step of the proof above.

The verified source files were not modified in preparing this manuscript. The manuscript date identifies this exposition, not a date of first discovery or a claim of publication priority.

## References

@ref [1] F. Joos and V. H. Nguyen, *Induced Matchings in Graphs of Degree at Most 4*, SIAM Journal on Discrete Mathematics 30 (2016), no. 1, 154–165. DOI: <link href="https://doi.org/10.1137/140986980">10.1137/140986980</link>.

@ref [2] M. Huang, M. Santana and G. Yu, *Strong Chromatic Index of Graphs With Maximum Degree Four*, Electronic Journal of Combinatorics 25 (2018), no. 3, Paper P3.31. DOI: <link href="https://doi.org/10.37236/7016">10.37236/7016</link>.

@ref [3] M. Fürst, M. Leichter and D. Rautenbach, *Locally Searching for Large Induced Matchings*, Theoretical Computer Science 720 (2018), 64–72. DOI: <link href="https://doi.org/10.1016/j.tcs.2018.02.006">10.1016/j.tcs.2018.02.006</link>.

@ref [4] R. Steiner, *Fractional Chromatic Number Vs. Hall Ratio*, Combinatorica 45 (2025), Article 37. DOI: <link href="https://doi.org/10.1007/s00493-025-00164-0">10.1007/s00493-025-00164-0</link>.
