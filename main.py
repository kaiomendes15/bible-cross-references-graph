from graph.loader import load_cross_references
from graph.builder import build_graph

def main():
    print("Carregando dados...")
    graph_data = load_cross_references('data/cross_references.txt')
    first_key = next(iter(graph_data))
    print(first_key, graph_data[first_key][:3])
  
    print("Construindo grafo...")
    G = build_graph(graph_data)

    print(f"Vértices: {G.number_of_nodes()}")
    print(f"Arestas:  {G.number_of_edges()}")

if __name__ == '__main__':
    main()