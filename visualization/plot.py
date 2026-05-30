import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
from math import cos, pi, sin, sqrt

HIGH_CONTRAST_COLORS = [
    "#4E79A7",  # blue
    "#F28E2B",  # orange
    "#59A14F",  # green
    "#E15759",  # red
    "#76B7B2",  # teal
    "#EDC948",  # yellow
    "#B07AA1",  # purple
    "#FF9DA7",  # pink
    "#9C755F",  # brown
    "#BAB0AC",  # gray
    "#86BCB6",
    "#F1CE63",
    "#8CD17D",
    "#D4A6C8",
    "#FFBE7D",
    "#A0CBE8",
    "#FFB5A7",
    "#CFCFCF",
    "#B6992D",
    "#F4A261",
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
    pos = _ego_radial_layout(G, partition)
    node_list, colors = _node_colors(G, partition)

    plt.figure(figsize=(18, 12))
    nx.draw_networkx(
        G,
        pos,
        nodelist=node_list,
        node_color=colors,
        node_size=300,
        font_size=6,
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
    pos = nx.spring_layout(
        G,
        seed=42,
        k=_repulsion_k(G, multiplier=6.0),
        iterations=300,
        weight=None,
    )

    node_list, colors = _node_colors(G, partition)

    plt.figure(figsize=(18, 12))
    nx.draw_networkx(
        G,
        pos,
        nodelist=node_list,
        node_color=colors,
        node_size=190,
        font_size=5,
        arrows=True,
        arrowsize=8,
        edge_color="#BBBBBB",
        width=0.5,
    )
    _add_community_legend(G, partition)
    plt.axis("off")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_community_top_pagerank(
    graph: dict[str, list[tuple[str, int]]],
    top_nodes: list[str],
    partition: dict[str, int],
    community_id: int,
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
    pos = nx.spring_layout(
        G,
        seed=42,
        k=_repulsion_k(G, multiplier=6.0),
        iterations=300,
        weight=None,
    )

    node_list, colors = _node_colors(G, partition)

    plt.figure(figsize=(24, 12))
    nx.draw_networkx(
        G,
        pos,
        nodelist=node_list,
        node_color=colors,
        node_size=220,
        font_size=6,
        arrows=True,
        arrowsize=9,
        edge_color="#BBBBBB",
        width=0.7,
    )
    colormap = _community_colormap(partition)
    handles = [
        mpatches.Patch(
            color=colormap(community_id),
            label=f"Community {community_id}",
        )
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

    return cm.get_cmap("Set3", max_community_id + 1)


def _repulsion_k(G: nx.DiGraph, multiplier: float) -> float:
    node_count = max(G.number_of_nodes(), 1)
    return multiplier / sqrt(node_count)


def _ego_radial_layout(
    G: nx.DiGraph,
    partition: dict[str, int],
) -> dict[str, tuple[float, float]]:
    if G.number_of_nodes() == 0:
        return {}

    center = max(G.nodes(), key=lambda node: G.in_degree(node) + G.out_degree(node))
    neighbors = [node for node in G.nodes() if node != center]
    neighbors.sort(key=lambda node: (partition.get(node, 0), node))

    pos = {center: (0.0, 0.0)}
    ring_capacity = 18

    for index, node in enumerate(neighbors):
        ring = index // ring_capacity
        ring_index = index % ring_capacity
        nodes_in_ring = min(ring_capacity, len(neighbors) - ring * ring_capacity)
        angle = (2 * pi * ring_index / nodes_in_ring) + (ring * pi / ring_capacity)
        radius = 3.2 + ring * 2.1
        pos[node] = (radius * cos(angle), radius * sin(angle))

    return pos
