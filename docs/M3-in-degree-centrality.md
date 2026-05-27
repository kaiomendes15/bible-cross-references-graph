# M3 — In-Degree and Weighted In-Degree Centrality

| | |
|---|---|
| **File** | `graph/metrics.py` (create new file) |
| **Depends on** | M1 (weighted adjacency list) |
| **Unblocks** | M4 (same file), M9 (visualization uses top nodes) |

---

## Objective

Create `graph/metrics.py` and implement two functions that identify the most-cited verses in the graph. Both functions iterate the custom adjacency dict directly — **do not use NetworkX**.

---

## What to Implement

### `top_in_degree(graph: dict, n: int) -> list[tuple[str, int]]`

Counts how many times each verse appears as a destination (`to_verse`) across all edges. Returns the top-`n` as `[(verse, count), ...]` sorted descending by count.

**Algorithm — single pass over all edges:**
```
in_degree = {}
for each from_verse in graph:
    for each (to_verse, votes) in graph[from_verse]:
        in_degree[to_verse] += 1
return sorted top-n by count descending
```

### `top_weighted_in_degree(graph: dict, n: int) -> list[tuple[str, float]]`

Same structure, but accumulates `votes` instead of a plain count. Returns `[(verse, total_votes), ...]` sorted descending.

```
weighted_in = {}
for each from_verse in graph:
    for each (to_verse, votes) in graph[from_verse]:
        weighted_in[to_verse] += votes
return sorted top-n by total_votes descending
```

Use `collections.defaultdict(int)` or `collections.Counter` to avoid key-not-found errors during accumulation.

---

## Why This Matters

**In-degree** answers: *which verses are referenced by the most other verses?* This is the simplest measure of structural importance.

**Weighted in-degree** goes further: *which verses accumulate the most total community confidence?* A verse cited 10 times with an average of 80 votes each scores higher than one cited 100 times with an average of 5 votes.

These two rankings reveal different things and will both appear in the analysis document.

---

## Real-World Analogy

In an academic citation network:
- **In-degree** = how many papers cite this paper (raw citation count).
- **Weighted in-degree** = the sum of the impact factors of all papers that cite this one. A paper cited only by *Nature* might rank higher by weighted in-degree than one cited by 50 obscure journals.

---

## What You Should Know

- `collections.defaultdict` and `collections.Counter`: https://docs.python.org/3/library/collections.html
- `sorted()` with `key=` and `reverse=True`: https://docs.python.org/3/howto/sorting.html
- In-degree definition in directed graphs: https://en.wikipedia.org/wiki/Directed_graph#Indegree_and_outdegree

---

## Done When

- `graph/metrics.py` exists with both functions
- Both accept the `dict[str, list[tuple[str, int]]]` structure from M1
- Calling `top_in_degree(graph, 5)` returns a list of 5 `(verse, count)` tuples sorted highest first
- Calling `top_weighted_in_degree(graph, 5)` returns a list of 5 `(verse, total_votes)` tuples sorted highest first
- No NetworkX import in this file
