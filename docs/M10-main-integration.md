# M10 — Main Integration

| | |
|---|---|
| **File** | `main.py` (extend existing file) |
| **Depends on** | All previous milestones (M1–M9) |
| **Unblocks** | Nothing — this is the final deliverable |

---

## Objective

Expand `main.py` to orchestrate the complete analysis pipeline. When `python main.py` runs, it should produce all terminal output (rankings, summaries, path results) and save two PNG visualization files — the full deliverable for the analysis document.

---

## What to Implement

Extend the existing `main()` function in `main.py` with the following steps in order:

### Step 1 — Load the graph
Already implemented. Confirm `graph` is `dict[str, list[tuple[str, int]]]` after M1.

### Step 2 — Print degree rankings

Call `top_in_degree(graph, 20)` and `top_weighted_in_degree(graph, 20)` from `graph.metrics`. Print a formatted table for each:

```
=== Top 20 by In-Degree ===
Rank   Verse                   Count
------------------------------------------
1      Rom.8.28                   892
2      John.3.16                  841
...
```

### Step 3 — Print PageRank ranking

Call `top_pagerank(graph, 20)`. Print same format with `Score` column (4 decimal places).

### Step 4 — Print betweenness ranking

Call `compute_betweenness(graph, n=20, k=200)`. Print same format. Add a note in the output:
```
(approximate, k=200 samples)
```

### Step 5 — Print community summary

Call `detect_communities(graph)` → `partition`. Call `community_summary(partition)` and print:
```
=== Community Summary ===
Total communities: 42
Largest community: 1,204 verses
Smallest community: 3 verses
```

### Step 6 — Print shortest path

Call `shortest_path(graph, "Gen.1.1", "John.1.1")`. Print:
```
=== Shortest Path: Gen.1.1 → John.1.1 ===
Path:  Gen.1.1 → Heb.11.3 → John.1.1
Cost:  0.0342
Hops:  2
```

### Step 7 — Print ego graph summary

Call `ego_graph` and `ego_summary` on the top-1 PageRank verse at `radius=1`. Print the summary dict.

### Step 8 — Save visualizations

Create the `output/` directory if it does not exist. Call:
- `plot_ego_graph(ego_sub, partition, title, "output/ego_graph.png")`
- `plot_overview(graph, top_100_pagerank_nodes, partition, "output/overview.png")`

Print the saved file paths.

---

## Table Formatting

Use f-strings with alignment specs — no extra library needed:

```python
print(f"{'Rank':<6} {'Verse':<25} {'Score':>12}")
print("-" * 45)
for i, (verse, score) in enumerate(results, 1):
    print(f"{i:<6} {verse:<25} {score:>12.4f}")
```

For integer counts, use `{count:>12,}` (comma as thousands separator).

---

## Suggested Import Block

```python
import os
from graph.loader import load_cross_references
from graph.metrics import top_in_degree, top_weighted_in_degree, top_pagerank, compute_betweenness
from graph.community import detect_communities, community_summary
from analysis.queries import shortest_path, ego_graph, ego_summary
from visualisation.plot import plot_ego_graph, plot_overview
```

---

## Why This Matters

This milestone is the proof that all previous milestones work together end-to-end. Every module written in M1–M9 is exercised here. The terminal output and PNG files are the raw material for the analysis document — rankings to interpret, images to include, paths to discuss.

---

## What You Should Know

- `os.makedirs(path, exist_ok=True)` to safely create output directory: https://docs.python.org/3/library/os.html#os.makedirs
- Python f-string format spec mini-language (alignment, width, precision): https://docs.python.org/3/library/string.html#format-specification-mini-language
- Wrapping the whole pipeline in a `try/except` to surface which module fails first is useful during integration

---

## Done When

Running `python main.py` from the project root:

- Prints node/edge count for the loaded graph
- Prints three top-20 ranking tables (in-degree, PageRank, betweenness)
- Prints community summary with total cluster count
- Prints a shortest-path result for `Gen.1.1 → John.1.1`
- Prints an ego-graph summary for the top PageRank verse
- Creates `output/ego_graph.png` and `output/overview.png`
- Exits without errors

**Spot-check:** `"Rom.8.28"` should appear in at least one of the top-20 rankings.
