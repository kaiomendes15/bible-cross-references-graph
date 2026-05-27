from graph.loader import load_cross_references
from graph.builder import build_graph
from graph.metrics import top_in_degree, top_weighted_in_degree

def main():
    print("Carregando dados...")
    graph_data = load_cross_references('data/cross_references.txt')
    first_key = next(iter(graph_data))
    print(first_key, graph_data[first_key][:3])
  
    print("Construindo grafo...")
    G = build_graph(graph_data)

    print(f"Vértices: {G.number_of_nodes()}")
    print(f"Arestas:  {G.number_of_edges()}")

    print("Calculando métricas...")
    top_in = top_in_degree(graph_data, 10)
    top_weighted_in = top_weighted_in_degree(graph_data, 10)

    print("\nTop 10 Versículos por In-Degree:")
    for verse, degree in top_in:
        print(f"{verse}: {degree} referências")

    print("\nTop 10 Versículos por Weighted In-Degree:")
    for verse, weight in top_weighted_in:
        print(f"{verse}: {weight:.2f} votos acumulados")



if __name__ == '__main__':
    main()