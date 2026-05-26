from graph.loader import load_cross_references
from graph.builder import build_graph
from graph.algorithms import dijkstra

def main():
    print("Carregando dados...")
    df = load_cross_references('data/cross_references.txt')

    print("Construindo grafo...")
    G = build_graph(df)

    print(f"Vértices: {G.number_of_nodes()}")
    print(f"Arestas:  {G.number_of_edges()}")

    print("\n--- Dijkstra ---")
    source = 'John.3.16'
    target = 'Rom.8.28'
    try:
        path, dist = dijkstra(G, source, target)
        print(f"Origem:  {source}")
        print(f"Destino: {target}")
        print(f"Caminho: {' -> '.join(path)}")
        print(f"Distância acumulada: {dist:.4f}")
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()