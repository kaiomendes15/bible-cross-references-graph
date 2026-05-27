# M5 — Betweenness Centrality (Approximate)

| | |
|---|---|
| **File** | `graph/metrics.py` (extend from M4) |
| **Depends on** | M4 (same file must already exist) |
| **Unblocks** | M6 (next milestone), M10 (main uses this result) |

---

## Objective

Add an **approximate** betweenness centrality function to `graph/metrics.py`. The approximation is mandatory — exact betweenness on a 31k-node graph takes hours. The function samples `k` source nodes and produces a statistically valid estimate.

---

## What to Implement

### `compute_betweenness(graph: dict, n: int, k: int = 200) -> list[tuple[str, float]]`

Returns the top-`n` verses by approximate betweenness centrality, sorted descending.

**Algorithm — sampled Brandes:**

1. **Sample** `k` random source nodes from the graph's key set.

2. **For each sampled source `s`**, run a single-source BFS (or Dijkstra for weighted variant) to compute:
   - `dist[v]` — shortest distance from `s` to `v`
   - `sigma[v]` — number of shortest paths from `s` to `v`
   - `pred[v]` — list of predecessors of `v` on shortest paths from `s`

3. **Accumulation pass** (back-propagation over the BFS tree):
   ```
   delta[v] = 0 for all v
   Process nodes in reverse BFS order (farthest from s first):
       for each predecessor u of v:
           delta[u] += (sigma[u] / sigma[v]) * (1 + delta[v])
       if v != s:
           betweenness[v] += delta[v]
   ```

4. **Scale** the result to account for sampling: multiply all scores by `N / k` where `N` is the total node count.

5. **Normalize** by `1 / ((N-1) * (N-2))` for directed graphs (optional but makes scores comparable across graphs of different sizes).

**Practical note:** Use unweighted BFS for speed. The weighted variant requires Dijkstra for each of the `k` pivots, which is significantly slower. For this project, unweighted BFS is acceptable.

**`k` guidelines:**

| k | Speed | Accuracy |
|---|-------|----------|
| 50 | Very fast | Rough estimate |
| 200 | Fast (default) | Good approximation |
| 500 | Slower | High accuracy |

---

## Why This Matters

Betweenness centrality answers: *which verses sit on the most paths between other verses?* High betweenness = a "bridge" verse that connects otherwise distant regions of the reference network.

This reveals verses that are theologically central not because they are frequently referenced directly, but because they sit at the intersection of different thematic clusters. Removing them would fragment the network.

---

## Real-World Analogy

In a social network, a person with high betweenness is a "broker" who connects different friend groups. They may not have the most connections, but all communication between groups flows through them. In an airport network, a hub airport has high betweenness — removing it disrupts many routes.

---

## What You Should Know

- Brandes algorithm (the accumulation step explained clearly): https://en.wikipedia.org/wiki/Betweenness_centrality#Algorithms
- Original Brandes paper (2001) — explains the back-propagation technique: https://doi.org/10.1080/0022250X.2001.9990249
- Why random sampling is statistically valid: https://doi.org/10.1145/1073204.1073208 (Bader et al.)
- Python `random.sample` for selecting k pivots without replacement: https://docs.python.org/3/library/random.html#random.sample
- Python `collections.deque` for BFS: https://docs.python.org/3/library/collections.html#collections.deque

---

## Done When

- `compute_betweenness` is added to `graph/metrics.py`
- Returns a list of `(verse, score)` tuples, length `n`, sorted descending
- Running with `k=200` completes in under 2 minutes on the full dataset
- Running twice with the same `k` and `random.seed(42)` produces identical results (use `random.seed` before sampling for reproducibility)
- No NetworkX import used for the computation
