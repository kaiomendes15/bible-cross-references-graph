import networkx as nx


def build_graph(graph_data: dict[str, list[tuple[str, int]]]) -> nx.DiGraph:
    G = nx.DiGraph()

    for from_verse, to_verses in graph_data.items():
        for to_verse, weight in to_verses:
            G.add_edge(from_verse, to_verse, weight=weight)
    
    return G
