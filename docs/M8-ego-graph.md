# M8 — Ego Graph

| | |
|---|---|
| **File** | `analysis/queries.py` (extend from M7) |
| **Depends on** | M7 (same file must already exist) |
| **Unblocks** | M9 (visualization renders ego subgraphs), M10 (main calls ego_summary) |

---

## Objective

Add a BFS-based ego-graph extractor to `analysis/queries.py`. Given any verse and a radius, it returns the local neighborhood as a new custom dict — same format as the main graph, ready to be passed to any other function.

---

## What to Implement

### `ego_graph(graph: dict, verse: str, radius: int = 1) -> dict[str, list[tuple[str, int]]]`

Performs a BFS from `verse` up to `radius` hops. Returns a **new custom dict** containing only the nodes and edges within that neighborhood.

**Algorithm — BFS with depth tracking:**

```
queue = deque([(verse, 0)])   # (node, current_depth)
visited_nodes = {verse}
result = defaultdict(list)

while queue:
    node, depth = queue.popleft()
    if depth < radius:
        for (neighbor, votes) in graph.get(node, []):
            result[node].append((neighbor, votes))
            if neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                queue.append((neighbor, depth + 1))

return dict(result)
```

**Important:** The returned dict follows the same `dict[str, list[tuple[str, int]]]` format as the main graph. Any function that accepts the main graph also accepts an ego graph.

### `ego_summary(graph: dict, verse: str, radius: int = 1) -> dict`

Calls `ego_graph` internally and returns a summary:

```python
{
    "center": verse,
    "radius": radius,
    "nodes": int,   # total unique nodes in the subgraph
    "edges": int    # total edges in the subgraph
}
```

---

## Why This Matters

The full graph (31k nodes, 340k edges) is not renderable in a meaningful way. Ego graphs let us zoom into the local neighborhood of any verse and visualize it — seeing exactly which texts reference a verse and what it references back. This is the primary visualization unit for the analysis document.

A radius of 1 gives the immediate neighbors; radius of 2 includes neighbors of neighbors, quickly expanding to hundreds of nodes.

---

## Real-World Analogy

In a LinkedIn network, your ego graph at radius=1 is you plus your direct connections, plus all the connections *between* those connections. At radius=2, it expands to include your connections' connections. This subgraph gives a local picture of your professional community without needing the entire network.

---

## What You Should Know

- `collections.deque` for efficient BFS queue (O(1) popleft vs O(n) for lists): https://docs.python.org/3/library/collections.html#collections.deque
- BFS vs DFS — BFS is correct here because we want *all* nodes within a radius, not just one path
- Ego graph concept: https://en.wikipedia.org/wiki/Ego_network
- The returned dict is a deep copy of the relevant portion — modifying it should not affect the original graph

---

## Done When

- `ego_graph` and `ego_summary` are added to `analysis/queries.py`
- `ego_graph(graph, "Rom.8.28", radius=1)` returns a dict with only the direct neighbors of `Rom.8.28`
- `ego_summary` returns `nodes` and `edges` counts consistent with the returned subgraph
- The returned dict is the same type as the input graph — passing it to `top_in_degree` works without errors
- `radius=0` returns a dict containing only the center verse with no edges
