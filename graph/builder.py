# receber os dados do dataframe e construir um grafo direcionado
import networkx as nx
import pandas as pd

def build_graph(df: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_weighted_edges_from(
        zip(df['from_verse'], df['to_verse'], df['votes'])
    )
    return G