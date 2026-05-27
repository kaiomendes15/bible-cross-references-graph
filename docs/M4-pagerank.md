# M4 — PageRank

| | |
|---|---|
| **File** | `graph/metrics.py` (extend from M3) |
| **Depends on** | M3 (same file must already exist) |
| **Unblocks** | M5 (same file), M9 (top PageRank nodes used for overview visualization) |

---

## Objective

Add a PageRank implementation to `graph/metrics.py` using the **power iteration algorithm from scratch** on the custom adjacency dict. Do not use `nx.pagerank` or any library function for the computation.

---

## What to Implement

### `compute_pagerank(graph: dict, damping: float = 0.85, max_iter: int = 100, tol: float = 1e-6) -> dict[str, float]`

Returns a dict mapping every verse to its PageRank score. All scores sum to 1.0.

**Algorithm — power iteration:**

1. **Collect all nodes.** Nodes appear both as keys (sources) and as values inside tuples (destinations). Build the full node set by scanning both.

2. **Initialize scores.** Set `score[node] = 1 / N` for all `N` nodes.

3. **Build out-degree totals.** For weighted PageRank, compute `out_weight[node]` = sum of `votes` on all outgoing edges. For unweighted fallback, `out_degree[node]` = number of outgoing edges.

4. **Iterate.** At each step, compute a new score for every node `v`:
   ```
   new_score[v] = (1 - damping) / N
                  + damping * sum(score[u] * votes(u→v) / out_weight[u]
                                  for every u with edge u → v)
   ```
   For unweighted: replace `votes(u→v) / out_weight[u]` with `1 / out_degree[u]`.

5. **Check convergence.** If `max(|new_score[v] - score[v]|) < tol` for all `v`, stop early.

6. **Repeat** up to `max_iter` times.

**Note on dangling nodes:** Nodes with no outgoing edges (sinks) do not propagate score in the standard formulation. Distribute their score uniformly across all nodes at each iteration, or simply accept the minor inaccuracy for this dataset size.

### `top_pagerank(graph: dict, n: int, **kwargs) -> list[tuple[str, float]]`

Calls `compute_pagerank(graph, **kwargs)` and returns the top-`n` as `[(verse, score), ...]` sorted descending.

---

## Why This Matters

PageRank captures **recursive importance**: a verse is important not just if many others reference it, but if those referencing verses are themselves important. This distinguishes true theological hubs from verses that happen to receive many low-confidence references.

The `damping` factor (0.85) models the idea that a reader following references will sometimes jump to a random verse instead of continuing the chain — without it, isolated clusters would trap all the score.

---

## Real-World Analogy

Google's original web ranking: a page is important if important pages link to it. A page linked to by three authoritative sources can rank higher than one linked to by a thousand spam blogs. The same logic applies here — a verse cited by Paul's central epistles carries more weight than one cited by marginal cross-references.

---

## What You Should Know

- PageRank algorithm description and pseudocode: https://en.wikipedia.org/wiki/PageRank#Algorithm
- Power iteration convergence: https://en.wikipedia.org/wiki/Power_iteration
- Building reverse adjacency (which nodes point TO `v`) from a forward adjacency dict requires a preprocessing pass or iterating the whole graph each iteration — the latter is simpler, the former faster
- Damping factor rationale: https://en.wikipedia.org/wiki/PageRank#Damping_factor

---

## Done When

- `compute_pagerank` and `top_pagerank` are added to `graph/metrics.py`
- `sum(compute_pagerank(graph).values())` is approximately `1.0`
- `top_pagerank(graph, 5)` returns 5 tuples sorted highest first
- The top verse is plausibly a high-citation verse (e.g. `"Rom.8.28"`, `"John.3.16"`)
- No NetworkX import used for the computation
