"""Deterministic finite falsification search, not a proof of universal bounds.

Original edges outside each candidate clique remain conflict witnesses.
No third-party libraries are required. Run with Python 3.12.
"""

import hashlib
import itertools
import json
import random
from pathlib import Path

SEED = 19520261010
LIMITS = {20: 18, 21: 17, 22: 16, 23: 15, 24: 13}


def conflicts(n, edges):
    edges = sorted(edges)
    neighbors = [set() for _ in range(n)]
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    assert max(map(len, neighbors), default=0) <= 4
    direct = [0] * len(edges)
    line = [0] * len(edges)
    for i, (u, v) in enumerate(edges):
        for j, (a, b) in enumerate(edges):
            if i == j:
                continue
            if {u, v} & {a, b}:
                line[i] |= 1 << j
            if {u, v} & {a, b} or any(
                y in neighbors[x] for x in (u, v) for y in (a, b)
            ):
                direct[i] |= 1 << j
    # Independently check the line-graph-square construction.
    for i in range(len(edges)):
        square = line[i]
        for j in range(len(edges)):
            if line[i] >> j & 1:
                square |= line[j]
        square &= ~(1 << i)
        assert square == direct[i]
    return edges, direct


def maximum_clique(adj, eligible):
    best = []

    def visit(chosen, possible, excluded):
        nonlocal best
        if len(chosen) + possible.bit_count() <= len(best):
            return
        if not possible:
            if len(chosen) > len(best):
                best = chosen
            return
        union = possible | excluded
        pivot = max(
            (i for i in range(len(adj)) if union >> i & 1),
            key=lambda i: (possible & adj[i]).bit_count(),
        )
        branches = possible & ~adj[pivot]
        while branches:
            bit = branches & -branches
            v = bit.bit_length() - 1
            visit(chosen + [v], possible & adj[v], excluded & adj[v])
            possible &= ~bit
            excluded |= bit
            branches &= ~bit

    visit([], eligible, 0)
    return best


def blowup5():
    return {
        tuple(sorted((2 * i + a, 2 * ((i + 1) % 5) + b)))
        for i in range(5) for a in range(2) for b in range(2)
    }


def switched(n, rng):
    edges = {tuple(sorted((i, (i + d) % n))) for i in range(n) for d in (1, 2)}
    for _ in range(30 * n):
        (a, b), (c, d) = rng.sample(sorted(edges), 2)
        if len({a, b, c, d}) != 4:
            continue
        if rng.randrange(2):
            c, d = d, c
        e, f = tuple(sorted((a, c))), tuple(sorted((b, d)))
        if e in edges or f in edges:
            continue
        edges.difference_update({tuple(sorted((a, b))), tuple(sorted((c, d)))})
        edges.update({e, f})
    for e in list(sorted(edges)):
        if rng.random() < 0.04:
            edges.remove(e)
    return edges


def main():
    rng = random.Random(SEED)
    tight = blowup5()
    samples = [(10, tight)] + [(10, tight - {e}) for e in sorted(tight)]
    samples += [(n, switched(n, rng)) for n in (10, 11, 12, 14, 18, 24) for _ in range(80)]
    maxima = {k: 0 for k in LIMITS}
    counterexamples = []
    digest = hashlib.sha256()
    for index, (n, raw_edges) in enumerate(samples):
        edges, adj = conflicts(n, raw_edges)
        digest.update(json.dumps([n, edges], separators=(",", ":")).encode())
        degrees = [mask.bit_count() for mask in adj]
        for k, bound in LIMITS.items():
            eligible = sum(1 << i for i, d in enumerate(degrees) if d >= k)
            clique = maximum_clique(adj, eligible)
            assert all(adj[i] >> j & 1 for i, j in itertools.combinations(clique, 2))
            assert all(degrees[i] >= k for i in clique)
            maxima[k] = max(maxima[k], len(clique))
            if len(clique) > bound:
                counterexamples.append({"sample": index, "n": n, "edges": edges,
                    "threshold": k, "Q": [edges[i] for i in clique],
                    "conflict_degrees": [degrees[i] for i in clique]})
    edges, adj = conflicts(10, tight)
    assert len(edges) == 20 and all(m.bit_count() == 19 for m in adj)
    # Restricting candidates must keep the middle edge of a four-vertex path.
    edges, adj = conflicts(4, {(0, 1), (1, 2), (2, 3)})
    assert adj[edges.index((0, 1))] >> edges.index((2, 3)) & 1
    edges, adj = conflicts(4, {(0, 1), (2, 3)})
    assert adj == [0, 0]
    result = {"kind": "finite falsification search; not a universal proof", "seed": SEED,
        "graphs": len(samples), "sample_sha256": digest.hexdigest(),
        "threshold_bounds_tested": LIMITS, "largest_cliques_observed": maxima,
        "counterexamples": counterexamples,
        "tight_C5_blowup_and_full_graph_witness_checks": "passed"}
    dest = Path(__file__).with_name("packing195-search.json")
    dest.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return bool(counterexamples)


if __name__ == "__main__":
    raise SystemExit(main())
