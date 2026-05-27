# M7 — Dijkstra Shortest Path

| | |
|---|---|
| **File** | `analysis/queries.py` (create new file) |
| **Depends on** | M1 (weighted adjacency list), M2 (weight inversion utility) |
| **Unblocks** | M8 (same file), M10 (main calls this) |

---

## Objective

Implement Dijkstra's shortest-path algorithm **from scratch** using Python's `heapq`. The result is the chain of cross-references most strongly supported by the community between any two verses.

---

## What to Implement

### `shortest_path(graph: dict, source: str, target: str) -> dict`

Returns a dict describing the shortest path:
```python
{
    "path": ["Gen.1.1", "John.1.1", ...],  # ordered list of verses
    "cost": 0.045,                          # total accumulated cost (sum of 1/votes)
    "hops": 3                               # number of edges traversed
}
```

Raises `ValueError` with a descriptive message if no path exists between `source` and `target`.

**Algorithm — Dijkstra with a min-heap:**

1. Initialize:
   - `heap = [(0.0, source, [source])]` — (cost, current_node, path_so_far)
   - `visited = set()`

2. Loop until the heap is empty:
   - Pop the entry with the lowest cost: `(cost, node, path)`
   - If `node == target`: return `{"path": path, "cost": cost, "hops": len(path) - 1}`
   - If `node` is already in `visited`: skip
   - Mark `node` as visited
   - For each `(neighbor, votes)` in `graph.get(node, [])`:
     - If `neighbor` not visited:
       - `new_cost = cost + invert_weight(votes)`
       - Push `(new_cost, neighbor, path + [neighbor])` to heap

3. If the heap empties without finding `target`: raise `ValueError`

**Import from M2:**
```python
from utils.weight_utils import invert_weight
```

---

## Why This Matters

Dijkstra with inverted weights finds the **canonical chain of references** between two verses — the path where every step is strongly supported by community confidence. A low-cost path means every cross-reference along the way has high `votes`, forming a "most trusted" thematic connection.

---

## Real-World Analogy

GPS navigation: cities are nodes, roads are edges with travel-time cost. Dijkstra finds the fastest route from city A to city B by always expanding the cheapest unexplored path first. Here, `cost = 1 / votes` means the "fastest" route traverses high-confidence references.

**Concrete example of cost semantics:**

| Edge | votes | cost |
|------|-------|------|
| Gen.1.1 → John.1.1 | 100 | 0.010 |
| Gen.1.1 → Rom.1.20 | 10 | 0.100 |
| John.1.1 → Rom.8.28 | 50 | 0.020 |

Path `Gen.1.1 → John.1.1 → Rom.8.28` costs `0.010 + 0.020 = 0.030`.  
Path `Gen.1.1 → Rom.1.20 → Rom.8.28` costs `0.100 + ...` — likely more expensive.

---

## What You Should Know

- Python `heapq` module (min-heap operations): https://docs.python.org/3/library/heapq.html
- Dijkstra pseudocode and correctness proof: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
- Why storing the full path in the heap is memory-heavy for large graphs (acceptable here given we query specific pairs, not all-pairs shortest paths)
- `ValueError` vs `KeyError` — use `ValueError` when the input values are logically invalid for the operation

---

## Done When

- `analysis/queries.py` exists with `shortest_path`
- `shortest_path(graph, "Gen.1.1", "John.1.1")` returns a dict with `path`, `cost`, and `hops`
- `shortest_path(graph, "Gen.1.1", "Gen.1.1")` returns the trivial path `["Gen.1.1"]` with cost `0` and hops `0`
- Calling with a non-existent target raises `ValueError`
- `heapq` is used; no NetworkX pathfinding functions
