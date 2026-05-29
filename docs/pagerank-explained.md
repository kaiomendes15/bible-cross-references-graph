# Understanding PageRank — From First Principles

## 1. The Core Intuition: What Is "Importance"?

There are two ways to measure how important a node is in a graph:

- **Strategy A — Raw in-degree:** count how many other nodes point to it.
- **Strategy B — Recursive importance:** count citations, but weight each citation by how important the citing node is.

Strategy B is better because it distinguishes **authoritative hubs** from nodes that simply accumulated many low-quality references. In the Bible graph: a verse cited by Romans 8 or John 3 carries more signal than one cited by an obscure genealogy passage.

**PageRank implements Strategy B.**

---

## 2. The Circular Dependency Problem

Strategy B has an inherent problem: to know if verse A is important, you need to know if verse B (which cites A) is important — but B's importance depends on who cites B, and so on recursively with no clear starting point.

**The fix:** break the circularity by starting with a guess, then refining it iteratively.

### Starting Values

Set every node's score to `1 / N`, where N is the total number of nodes. This is the "no information" prior — assume everyone is equally important at first.

```python
N = len(all_nodes)
score = {node: 1 / N for node in all_nodes}
```

---

## 3. Score Redistribution — The Water Analogy

Think of each node's score as a **bucket of water**. At each iteration, every node pours its entire bucket into its outgoing neighbors, splitting the water proportionally across them.

For **unweighted** graphs: split equally.

For **weighted** graphs (like the Bible graph, where edges have vote counts): split proportionally to votes.

```
contribution from u to v = score[u] × votes(u→v) / out_weight[u]
```

Where `out_weight[u]` = sum of all vote counts on u's outgoing edges.

**Example:**
- u has score 0.3
- u cites A with 90 votes and B with 10 votes → out_weight = 100
- A receives: `0.3 × 90/100 = 0.27`
- B receives: `0.3 × 10/100 = 0.03`
- Total redistributed: `0.27 + 0.03 = 0.30` ✓ — u's full score is passed on

The weights change *where* the score flows, not *how much total* is redistributed. Each node always passes on 100% of its score.

---

## 4. The Sink Problem — Why Pure Redistribution Fails

In a pure redistribution model, nodes that nobody cites will have their score drain to 0 after the first iteration. Worse, nodes with no outgoing edges (sinks) **trap** all score that flows into them — nothing comes back out.

A graph with isolated nodes or sinks makes pure water-redistribution unstable and biased.

---

## 5. The Damping Factor — The Fix

The damping factor `d` (typically `0.85`) models a **random surfer**: someone who follows links most of the time, but occasionally teleports to a completely random node.

The probability of teleporting at any step is `(1 - d) = 0.15`.

This modifies the score update formula to:

```
new_score[v] = (1 - d) / N
             + d × Σ( score[u] × votes(u→v) / out_weight[u] )
               for all u with edge u → v
```

The `(1 - d) / N` term is crucial: it gives **every node a baseline score** regardless of whether anyone cites it. This:
- Prevents any node from reaching exactly 0
- Ensures the scores sum to 1.0 at all times
- Prevents isolated clusters from trapping all the score

**What happens if `d = 1.0`?** No random jumps. Score drains into sinks and isolated clusters — the water-leak problem returns in full.

---

## 6. Power Iteration — Running the Algorithm

The process repeats the redistribution formula until scores stabilize:

```
1. Initialize: score[v] = 1/N for all v
2. Loop up to max_iter times:
   a. Compute new_score[v] for every v using the formula above
   b. Check convergence: max(|new_score[v] - score[v]|) < tol → stop
   c. Replace score with new_score
3. Return final scores
```

This is **power iteration**: each round produces slightly better estimates of the true importance. The scores converge because the damping factor `d < 1` acts as a contraction — each iteration brings all scores closer to the true fixed point.

### Convergence Check

At each step, compute the maximum absolute change:
```python
delta = max(abs(new_score[v] - score[v]) for v in all_nodes)
if delta < tol:
    break  # converged
```

`tol = 1e-6` means: stop when no node's score changes by more than one millionth. For ~31,000 nodes this usually happens well before 100 iterations.

---

## 7. Dangling Nodes

Nodes with no outgoing edges (sinks) receive score but never pass it on. This causes the total sum of scores to drift below 1.0.

**Fix:** at each iteration, collect the total score held by dangling nodes and redistribute it uniformly across all nodes, as if each dangling node teleported its score randomly:

```
dangling_sum = Σ score[u]  for all u with no outgoing edges

new_score[v] = (1 - d) / N + d × dangling_sum / N
             + d × Σ( score[u] × votes(u→v) / out_weight[u] )
```

---

## 8. Algorithm Summary

```
Input:  graph (adjacency dict with votes), damping d, max_iter, tol
Output: dict mapping every verse → PageRank score (sum ≈ 1.0)

1. Collect all nodes (from keys AND from edge destinations)
2. N = total node count
3. score[v] = 1/N for all v
4. out_weight[u] = sum of votes on all outgoing edges from u
5. dangling_nodes = nodes with no outgoing edges

6. For each iteration in range(max_iter):
   a. dangling_sum = sum of score[u] for u in dangling_nodes
   b. new_score[v] = (1-d)/N + d * dangling_sum/N   for all v
   c. For each u (non-dangling): for each (v, votes) in graph[u]:
          new_score[v] += d * score[u] * votes / out_weight[u]
   d. If max(|new_score[v] - score[v]|) < tol: break
   e. score = new_score

7. Return score
```

**Key invariant:** at every step, `sum(score.values()) ≈ 1.0`.

---

## 9. Why This Works for the Bible Graph

A verse like `John.3.16` ranks high in PageRank not just because many verses cite it, but because **those citing verses are themselves important** — cited by central Pauline epistles, Synoptic Gospels, and prophetic books that are themselves hub nodes.

A verse cited only by obscure marginal passages would score low even with a high raw citation count. PageRank separates **structural centrality** from raw popularity.

The vote weights add a third layer: a high-vote citation (strong community confidence) transfers more score than a low-vote citation. So `John.3.16` cited by `Rom.8.28` (a high-vote, high-PageRank node) accumulates more score than if cited by a peripheral verse with minimal votes.
