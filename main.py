from numpy import partition

from graph.loader import load_cross_references
from graph.builder import build_graph
from graph.community import detect_communities, community_summary
from graph.metrics import compute_pagerank, top_in_degree, top_weighted_in_degree, top_pagerank, compute_betweenness
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

    print("Calculando métricas...")
    top_in = top_in_degree(graph_data, 10)
    top_weighted_in = top_weighted_in_degree(graph_data, 10)
    pagerank_scores = compute_pagerank(graph_data)

    print("Top 10 In-Degree:")
    for verse, degree in top_in:
        print(f"{verse}: {degree}")

    print("\nTop 10 Weighted In-Degree:")
    for verse, degree in top_weighted_in:
        print(f"{verse}: {degree:.2f}")

    print("\nTop 10 PageRank:")
    for verse, score in sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{verse}: {score:.6f}")

    print("\nCalculando Betweenness Centrality (k=200)...")
    top_betweenness = compute_betweenness(graph_data, n=10, k=200)
    print('\n Top 10 Betweenness Centrality:')
    for verse, score in top_betweenness:
       print(f"{verse}: {score:.8f}")


if __name__ == '__main__':
    main()