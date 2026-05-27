# M9 — Visualization

| | |
|---|---|
| **File** | `visualisation/plot.py` (create new file) |
| **Depends on** | M6 (community partition for node colors), M8 (ego graph subdict to render), M4 (top-PageRank nodes for overview) |
| **Unblocks** | M10 (main calls these functions to save PNGs) |
| **New dependency** | Add `matplotlib` to `requirements.txt` if not already present |

---

## Objective

Create the visualization module. This is the **only place in the project where NetworkX is used as a computation tool** — the custom dict is converted to `nx.DiGraph` purely for rendering via matplotlib. All outputs are saved as PNG files.

---

## What to Implement

### `subdict_to_digraph(subgraph: dict) -> nx.DiGraph`

Converts a custom dict (ego graph or any sub-dict) to an `nx.DiGraph` for rendering. Adds `weight=votes` to each edge.

```python
G = nx.DiGraph()
for from_verse, edges in subgraph.items():
    for to_verse, votes in edges:
        G.add_edge(from_verse, to_verse, weight=votes)
return G
```

This is a private helper used only inside this module.

### `plot_ego_graph(subgraph: dict, partition: dict, title: str, output_path: str)`

Renders a small subgraph (typically an ego graph from M8) as a PNG:

1. Call `subdict_to_digraph(subgraph)` to get an `nx.DiGraph`.
2. Compute node positions with `nx.spring_layout(G, seed=42)`.
3. Map each node to a color using the `partition` dict and a matplotlib colormap (see below).
4. Call `nx.draw_networkx(G, pos, node_color=colors, ...)`.
5. Add a title and save with `plt.savefig(output_path, dpi=150, bbox_inches='tight')`.
6. Call `plt.close()` after saving to free memory.

### `plot_overview(graph: dict, top_nodes: list[str], partition: dict, output_path: str)`

Renders a sampled overview showing only the `top_nodes` subset:

1. Filter the main graph to include only edges where both endpoints are in `top_nodes`: build a sub-dict from the main `graph`.
2. Call `subdict_to_digraph` on the filtered dict.
3. Choose layout: `kamada_kawai_layout` if `len(top_nodes) <= 300`, else `spring_layout(seed=42)`.
4. Map colors from `partition`, render, save, close.

---

## Node Color Mapping

Map integer community IDs to colors using a matplotlib colormap:

```python
import matplotlib.pyplot as plt
import matplotlib.cm as cm

colormap = cm.get_cmap('tab20', max(partition.values()) + 1)
node_list = list(G.nodes())
colors = [colormap(partition.get(node, 0)) for node in node_list]
```

Pass `node_color=colors` and `nodelist=node_list` to `nx.draw_networkx` to ensure alignment.

---

## Why This Matters

The analysis document needs images. Rendering the full 31k-node graph produces an unreadable hairball — instead:
- `plot_ego_graph` shows the local neighborhood of a specific verse (e.g., the top PageRank verse).
- `plot_overview` shows the top-100 verses by PageRank as a macro structural overview, colored by community.

Both images will be included in the analysis document to visually communicate the project findings.

---

## Real-World Analogy

In a protein-interaction network paper: the authors don't render all 20,000 proteins. They show the ego graph of a key protein of interest, and a separate overview of the top 100 by degree — colored by cellular compartment. Same strategy here.

---

## What You Should Know

- `nx.draw_networkx` reference (node_color, nodelist, pos parameters): https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html
- `nx.spring_layout` and `nx.kamada_kawai_layout`: https://networkx.org/documentation/stable/reference/drawing.html#layout
- `matplotlib.pyplot.savefig` and `dpi` parameter: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
- `plt.close()` after each save to avoid memory leaks: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.close.html
- `cm.get_cmap` for discrete colormaps: https://matplotlib.org/stable/gallery/color/colormap_reference.html

---

## Done When

- `visualisation/plot.py` exists with `subdict_to_digraph`, `plot_ego_graph`, and `plot_overview`
- `matplotlib` is in `requirements.txt`
- `plot_ego_graph(ego_sub, partition, "Test", "output/test_ego.png")` produces a readable PNG
- `plot_overview(graph, top_100_verses, partition, "output/test_overview.png")` produces a PNG showing colored nodes
- `plt.close()` is called after each save — verify by calling both functions back-to-back without a memory error
