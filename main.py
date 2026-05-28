from numpy import partition

from graph.loader import load_cross_references
from graph.builder import build_graph
from graph.community import detect_communities, community_summary
from collections import defaultdict


def main():
    print("Carregando dados...")
    graph_data = load_cross_references('data/cross_references.txt')
    first_key = next(iter(graph_data))
    print(first_key, graph_data[first_key][:3])

    print("Construindo grafo...")
    G = build_graph(graph_data)
    print(f"Vértices: {G.number_of_nodes()}")
    print(f"Arestas:  {G.number_of_edges()}")

    print("Detectando comunidades...")
    partition = detect_communities(graph_data)
    communities = defaultdict(list)

    for verse, community_id in partition.items():
      communities[community_id].append(verse)

    community_id = 0

    print(f"10 itens da Comunidade {community_id}:")
    print(f"Total de versículos: {len(communities[community_id])}")

    for verse in sorted(communities[community_id])[:10]:
      print(verse)
    summary = community_summary(partition)

    print(f"Versículos com comunidade: {len(partition)}")
    print(f"Comunidades detectadas: {len(summary)}")
    print(dict(sorted(summary.items())[:10]))


if __name__ == '__main__':
    main()