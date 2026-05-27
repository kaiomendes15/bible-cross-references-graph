# M6 — Community Detection

| | |
|---|---|
| **File** | `graph/community.py` (create new file) |
| **Depends on** | M1 (weighted adjacency list) |
| **Unblocks** | M9 (visualization uses community partition for node coloring) |
| **New dependency** | Add `python-louvain` to `requirements.txt` |

---

## Objective

Detect thematic clusters of verses using the Louvain algorithm. Because Louvain is complex to implement from scratch, this milestone uses the `python-louvain` library — but converts the result back to a plain Python dict so the rest of the project stays free of NetworkX as a data store.

NetworkX is used here **only as an intermediate for the algorithm**, not as a storage structure.

---

## What to Implement

### `build_undirected(graph: dict) -> nx.Graph`

Creates a `networkx.Graph` (undirected) from the custom directed adjacency dict. For each directed edge `(u, v, votes)`, add the undirected edge `(u, v)` with `weight=votes`. If the reverse edge `(v, u)` also exists in the original graph, accumulate the weights.

This is a private helper used only inside this module.

### `detect_communities(graph: dict) -> dict[str, int]`

1. Calls `build_undirected(graph)` to produce an `nx.Graph`.
2. Runs `community.best_partition(G, weight='weight')` from `python-louvain`.
3. Returns the result directly — a `{verse: community_id}` dict where `community_id` is an integer.

### `community_summary(partition: dict) -> dict[int, int]`

Takes the output of `detect_communities` and returns `{community_id: node_count}` — how many verses belong to each detected cluster.

---

## Why the Undirected Conversion

Louvain optimizes **modularity**, which is defined for undirected graphs. The directed structure encodes which verse *references* which, but for finding thematic clusters, the direction is less relevant than the presence of a connection. The temporary conversion is purely for the algorithm — the primary `graph` dict remains the project's data store.

---

## Why This Matters

Louvain finds groups of verses that reference each other more densely than they reference the rest of the graph. These groups should correspond to recognizable thematic or canonical clusters — Old Testament books, Pauline epistles, Gospels, etc. — emerging purely from the reference structure, with no prior knowledge of the Bible's organization.

Community IDs are used later to **color nodes** in the visualization (M9).

---

## Real-World Analogy

In a co-authorship network, Louvain identifies research communities — groups of scientists who collaborate with each other more than with outsiders. No prior knowledge of the groups is needed; they emerge from the graph structure. A neuroscience cluster and a machine learning cluster may occasionally collaborate, but each is internally much denser.

---

## What You Should Know

- `python-louvain` installation and usage: https://python-louvain.readthedocs.io/en/latest/
  - Install: `pip install python-louvain`
  - Import: `import community as community_louvain`
  - Usage: `partition = community_louvain.best_partition(G)`
- Louvain algorithm overview: https://en.wikipedia.org/wiki/Louvain_method
- NetworkX `Graph` (undirected) vs `DiGraph` (directed): https://networkx.org/documentation/stable/reference/classes/graph.html
- The `community_id` integers from Louvain are arbitrary labels — only equality matters (same cluster = same ID)

---

## Done When

- `graph/community.py` exists with all three functions
- `python-louvain` is added to `requirements.txt`
- `detect_communities(graph)` returns a dict where every verse in the graph has a community ID
- `community_summary(partition)` shows multiple communities with reasonable node counts (expect 10–100+ communities)
- The returned dicts are plain Python — no NetworkX objects leak outside this module
