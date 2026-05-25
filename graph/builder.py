import networkx as nx


def build_graph(graph_data: dict[str, list[str]]) -> nx.DiGraph:
    G = nx.DiGraph()

    for from_verse, to_verses in graph_data.items():
        for to_verse in to_verses:
            G.add_edge(from_verse, to_verse)
    
    return G
