import networkx as nx


def build_graph(graph_data: dict[str, list[tuple[str, int]]]) -> nx.DiGraph:
    G = nx.DiGraph()

    for from_verse, edges in graph_data.items():
        for to_verse, votes in edges:
            G.add_edge(from_verse, to_verse, weight=votes)
    
    return G
