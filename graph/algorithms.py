import heapq
import networkx as nx


def dijkstra(G: nx.DiGraph, source: str, target: str) -> tuple[list[str], float]:
    """
    Encontra o caminho mais relevante entre dois versículos.
    Usa peso 1/votos: arestas com mais votos são tratadas como mais próximas.
    Retorna (caminho, distância_total). Lança ValueError se não houver caminho.
    """
    if source not in G:
        raise ValueError(f"Versículo de origem não encontrado: {source}")
    if target not in G:
        raise ValueError(f"Versículo de destino não encontrado: {target}")

    dist = {source: 0.0}
    prev = {source: None}
    heap = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)

        if d > dist.get(u, float('inf')):
            continue

        if u == target:
            break

        for v, data in G[u].items():
            votes = data.get('weight', 1)
            edge_cost = 1.0 / votes if votes > 0 else float('inf')
            new_dist = d + edge_cost

            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    if target not in dist:
        raise ValueError(f"Nenhum caminho encontrado entre {source} e {target}")

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    return path, dist[target]
