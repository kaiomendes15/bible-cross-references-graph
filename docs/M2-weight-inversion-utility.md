# M2 — Weight Inversion Utility

| | |
|---|---|
| **File** | `utils/weight_utils.py` (create new file) |
| **Depends on** | M1 (weighted adjacency list must exist to test usage) |
| **Unblocks** | M7 (Dijkstra) |

---

## Objective

Create a utility module that converts `votes` (a confidence score) into `cost` (a distance suitable for Dijkstra). No algorithm file should repeat this inversion logic — it lives here and is imported by whoever needs it.

---

## What to Implement

Create `utils/weight_utils.py` with two pure functions:

### `invert_weight(votes: int) -> float`

Returns `1 / votes`. This is the core conversion: higher confidence = lower traversal cost.

Raises `ValueError` if `votes <= 0`, with a clear message like:
```
ValueError: votes must be positive, got 0
```

### `edge_cost(graph: dict, from_verse: str, to_verse: str) -> float`

Looks up the edge `from_verse → to_verse` in the adjacency list and returns `invert_weight(votes)` for that edge.

Raises `KeyError` if either the source node does not exist or the specific edge to `to_verse` is not found.

**Lookup pattern:**
```python
# Iterate graph[from_verse] looking for the matching to_verse
for neighbor, votes in graph.get(from_verse, []):
    if neighbor == to_verse:
        return invert_weight(votes)
raise KeyError(f"Edge {from_verse} -> {to_verse} not found")
```

---

## Why This Matters

Dijkstra finds minimum-cost paths. `votes` is a confidence measure — the more confident the community, the stronger (and therefore cheaper) the connection should be. Inverting converts this intuition into a valid distance metric:

| votes | cost = 1/votes |
|-------|---------------|
| 100 | 0.01 (cheap — strong reference) |
| 10 | 0.10 |
| 1 | 1.00 (expensive — weak reference) |

Encapsulating this in one place ensures that if the inversion formula ever changes (e.g. `1 / log(votes)`), only this file needs to be updated.

---

## Real-World Analogy

In network routing, each link has a `bandwidth` value. Routers store `cost = 1 / bandwidth` so that high-bandwidth links are preferred by Dijkstra. The inversion happens once, at the utility layer, not scattered across every routing algorithm.

---

## What You Should Know

- Why `1/x` converts strength to distance: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Related_problems
- Python `ValueError` and `KeyError` best practices: https://docs.python.org/3/tutorial/errors.html
- Python pure functions (no side effects, no global state): https://realpython.com/python-functional-programming/

---

## Done When

- `utils/weight_utils.py` exists with both functions
- `invert_weight(0)` raises `ValueError`
- `invert_weight(50)` returns `0.02`
- `edge_cost(graph, "Gen.1.1", "Heb.11.3")` returns the correct cost for that edge (verify against the raw data)
- No changes to any other file
