from graph.loader import load_cross_references
from graph.builder import build_graph

def main():
    print("Carregando dados...")
    df = load_cross_references('data/cross_references.txt')

    print("Construindo grafo...")
    G = build_graph(df)

    print(f"Vértices: {G.number_of_nodes()}")
    print(f"Arestas:  {G.number_of_edges()}")

if __name__ == '__main__':
    main()