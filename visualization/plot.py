import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
from math import sqrt

HIGH_CONTRAST_COLORS = [
    "#1f77b4",  # blue
    "#d62728",  # red
    "#2ca02c",  # green
    "#9467bd",  # purple
    "#ff7f0e",  # orange
    "#17becf",  # cyan
    "#bcbd22",  # olive
    "#e377c2",  # pink
    "#8c564b",  # brown
    "#7f7f7f",  # gray
    "#003f5c",
    "#ffa600",
    "#58508d",
    "#ff6361",
    "#00a676",
    "#6a4c93",
    "#1982c4",
    "#ffca3a",
    "#8ac926",
    "#c1121f",
]


def subdict_to_digraph(subgraph: dict[str, list[tuple[str, int]]]) -> nx.DiGraph:
    G = nx.DiGraph()

    for from_verse, edges in subgraph.items():
        G.add_node(from_verse)
        for to_verse, votes in edges:
            G.add_edge(from_verse, to_verse, weight=votes)

    return G


def plot_ego_graph(
    subgraph: dict[str, list[tuple[str, int]]],
    partition: dict[str, int],
    title: str,
    output_path: str,
) -> None:
    G = subdict_to_digraph(subgraph)
    pos = nx.spring_layout(G, seed=42, k=_repulsion_k(G, multiplier=2.0), iterations=100)
    node_list, colors = _node_colors(G, partition)

    plt.figure(figsize=(12, 8))
    nx.draw_networkx(
        G,
        pos,
        nodelist=node_list,
        node_color=colors,
        node_size=450,
        font_size=8,
        arrows=True,
        arrowsize=12,
        edge_color="#999999",
        width=0.8,
    )
    _add_community_legend(G, partition)
    plt.title(title)
    plt.axis("off")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_overview(
    graph: dict[str, list[tuple[str, int]]],
    top_nodes: list[str],
    partition: dict[str, int],
    output_path: str,
) -> None:
    top_node_set = set(top_nodes)
    subgraph = {}

    for from_verse in top_nodes:
        edges = [
            (to_verse, votes)
            for to_verse, votes in graph.get(from_verse, [])
            if to_verse in top_node_set
        ]
        subgraph[from_verse] = edges

    G = subdict_to_digraph(subgraph)
    pos = nx.spring_layout(G, seed=42, k=_repulsion_k(G, multiplier=2.8), iterations=150)

    node_list, colors = _node_colors(G, partition)

    plt.figure(figsize=(14, 10))
    nx.draw_networkx(
        G,
        pos,
        nodelist=node_list,
        node_color=colors,
        node_size=220,
        font_size=6,
        arrows=True,
        arrowsize=8,
        edge_color="#BBBBBB",
        width=0.5,
    )
    _add_community_legend(G, partition)
    plt.axis("off")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def _node_colors(G: nx.DiGraph, partition: dict[str, int]) -> tuple[list[str], list]:
    node_list = list(G.nodes())
    colormap = _community_colormap(partition)
    colors = [colormap(partition.get(node, 0)) for node in node_list]

    return node_list, colors


def _add_community_legend(G: nx.DiGraph, partition: dict[str, int]) -> None:
    communities = sorted({partition.get(node, 0) for node in G.nodes()})
    colormap = _community_colormap(partition)
    handles = [
        mpatches.Patch(color=colormap(community_id), label=f"Community {community_id}")
        for community_id in communities
    ]

    plt.legend(
        handles=handles,
        title="Communities",
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
        borderaxespad=0,
        fontsize=8,
        title_fontsize=9,
    )


def _community_colormap(partition: dict[str, int]):
    max_community_id = max(partition.values(), default=0)

    if max_community_id < len(HIGH_CONTRAST_COLORS):
        return mcolors.ListedColormap(HIGH_CONTRAST_COLORS[: max_community_id + 1])

    return cm.get_cmap("nipy_spectral", max_community_id + 1)


def _repulsion_k(G: nx.DiGraph, multiplier: float) -> float:
    node_count = max(G.number_of_nodes(), 1)
    return multiplier / sqrt(node_count)
