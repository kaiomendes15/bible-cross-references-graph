# Bible Cross-Reference Graph — Project Context

## What This Project Does

Models the Bible's cross-reference network as a **directed weighted graph** using data from [OpenBible.info](https://www.openbible.info/labs/cross-references/) (CC-BY). Each node is a Bible verse (e.g. `"Rom.8.28"`), each edge is a cross-reference from one verse to another, and the edge weight is a community vote count expressing confidence in the connection.

**Scale:** ~31,000 nodes (unique verses), ~340,000 edges (cross-references).

---

## Core Architectural Decision

The **primary graph representation is a custom Python data structure** — a weighted adjacency list. **NetworkX is used only for rendering visualization images**, never as the graph store for algorithms.

```
graph: dict[str, list[tuple[str, int]]]
  key   → from_verse         (e.g. "Gen.1.1")
  value → list of (to_verse, votes)  (e.g. [("John.1.1", 50), ("Rom.1.1", 30)])
```

Iterating over edges always looks like:
```python
for neighbor, votes in graph.get(node, []):
    cost = 1 / votes  # for distance-based algorithms
```

---

## Project Structure

```
bible_graph/
├── data/
│   └── cross_references.txt      # TSV: from_verse, to_verse, votes (~344k rows)
├── graph/
│   ├── loader.py                 # Loads TSV → weighted adjacency dict
│   ├── builder.py                # Converts dict → nx.DiGraph (visualization only)
│   ├── metrics.py                # In-degree, PageRank, betweenness (M3–M5)
│   └── community.py              # Louvain community detection (M6)
├── utils/
│   ├── verse_utils.py            # Expands verse range notation (e.g. John.1.1-John.1.3)
│   └── weight_utils.py           # Weight inversion: cost = 1/votes (M2)
├── analysis/
│   └── queries.py                # Dijkstra shortest path, ego graph (M7–M8)
├── visualisation/
│   └── plot.py                   # matplotlib rendering via NetworkX (M9)
├── docs/                         # Milestone documentation (one file per milestone)
├── main.py                       # Orchestrates full pipeline (M10)
└── requirements.txt
```

---

## Current Implementation State

| File | Status | Notes |
|------|--------|-------|
| `graph/loader.py` | Needs update (M1) | Currently loses `votes`; must return weighted tuples |
| `graph/builder.py` | Done | Converts dict → nx.DiGraph for visualization |
| `utils/verse_utils.py` | Done | Handles `Book.Ch.V-Book.Ch.V` range expansion |
| `main.py` | Partial | Loads + builds + prints node/edge count; needs full pipeline (M10) |
| `utils/weight_utils.py` | Missing | M2 |
| `graph/metrics.py` | Missing | M3, M4, M5 |
| `graph/community.py` | Missing | M6 |
| `analysis/queries.py` | Missing | M7, M8 |
| `visualisation/plot.py` | Missing | M9 |

---

## Milestones

Each milestone is destined to one team member and must be completed before the next begins. See `docs/` for detailed specs.

| # | Title | File(s) | Doc |
|---|-------|---------|-----|
| M1 | Weighted Adjacency List | `graph/loader.py` | [docs/M1-weighted-adjacency-list.md](docs/M1-weighted-adjacency-list.md) |
| M2 | Weight Inversion Utility | `utils/weight_utils.py` | [docs/M2-weight-inversion-utility.md](docs/M2-weight-inversion-utility.md) |
| M3 | In-Degree Centrality | `graph/metrics.py` | [docs/M3-in-degree-centrality.md](docs/M3-in-degree-centrality.md) |
| M4 | PageRank | `graph/metrics.py` | [docs/M4-pagerank.md](docs/M4-pagerank.md) |
| M5 | Betweenness Centrality | `graph/metrics.py` | [docs/M5-betweenness-centrality.md](docs/M5-betweenness-centrality.md) |
| M6 | Community Detection | `graph/community.py` | [docs/M6-community-detection.md](docs/M6-community-detection.md) |
| M7 | Dijkstra Shortest Path | `analysis/queries.py` | [docs/M7-dijkstra-shortest-path.md](docs/M7-dijkstra-shortest-path.md) |
| M8 | Ego Graph | `analysis/queries.py` | [docs/M8-ego-graph.md](docs/M8-ego-graph.md) |
| M9 | Visualization | `visualisation/plot.py` | [docs/M9-visualization.md](docs/M9-visualization.md) |
| M10 | Main Integration | `main.py` | [docs/M10-main-integration.md](docs/M10-main-integration.md) |

---

## Running the Project

```bash
pip install -r requirements.txt
python main.py
```

Expected output: terminal tables for three centrality rankings, community summary, a shortest-path result, an ego-graph summary, and two PNG files saved to `output/`.

---

## Data Format

`data/cross_references.txt` — tab-separated, first row is a commented header:

```
From Verse    To Verse              Votes
Gen.1.1       Heb.11.3              63
Gen.1.1       John.1.1-John.1.3     38
```

Verse format: `BookAbbrev.Chapter.Verse`. Ranges (`John.1.1-John.1.3`) are expanded to individual verses by `verse_utils.expand_verse`.
