# M1 — Update Loader to Weighted Adjacency List

| | |
|---|---|
| **File** | `graph/loader.py` (modify existing) |
| **Depends on** | Nothing — this is the foundation |
| **Unblocks** | All other milestones |

---

## Objective

Update `load_cross_references` to preserve the `votes` weight on every edge. The function must return a **weighted adjacency list** so downstream algorithms can use edge weights.

**Current return type:** `dict[str, list[str]]`  
**Required return type:** `dict[str, list[tuple[str, int]]]`

---

## What to Implement

Change the single line that appends to the adjacency list:

```python
# Before — loses votes
graph[from_verse].append(to_verse)

# After — preserves votes as a tuple
graph[from_verse].append((to_verse, int(row['votes'])))
```

The rest of the function (CSV loading, filtering `votes > 0`, expanding verse ranges, exploding rows) stays the same.

Update the type annotation in the function signature to reflect the new return type:

```python
def load_cross_references(filepath: str) -> dict[str, list[tuple[str, int]]]:
```

### Verifying the change

Add a temporary print in `main.py` to confirm the structure is correct:

```python
first_key = next(iter(graph_data))
print(first_key, graph_data[first_key][:3])
# Expected output: Gen.1.1 [('Heb.11.3', 63), ('John.1.1', 38), ...]
```

Remove this print after confirming.

---

## Why This Matters

Every weighted algorithm in the project (Dijkstra, weighted in-degree, PageRank with weights, betweenness) needs to access `votes` when iterating over neighbors. Without it, only unweighted computations are possible.

All algorithm code in the project iterates edges like this:

```python
for neighbor, votes in graph.get(node, []):
    cost = 1 / votes
```

If `votes` is missing from the tuple, this unpacking will fail at runtime.

---

## Real-World Analogy

In a road network where edge weight is road bandwidth, a GPS must store both the destination and the bandwidth per road segment. Dropping bandwidth at load time forces every later module to re-read the raw data — inefficient and error-prone. Storing it in the adjacency list once keeps the rest of the system clean.

---

## What You Should Know

- Python `defaultdict` and tuple values: https://docs.python.org/3/library/collections.html#collections.defaultdict
- `pandas` `iterrows` and row access: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html
- Python type hints for nested generics: https://docs.python.org/3/library/typing.html

---

## Done When

- `load_cross_references` returns `dict[str, list[tuple[str, int]]]`
- Each value list contains `(to_verse, votes)` tuples with `votes > 0`
- `main.py` prints the correct tuple structure for the first key
- No other file is changed
