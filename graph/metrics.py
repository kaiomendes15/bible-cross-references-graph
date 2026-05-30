import random 
from collections import defaultdict, deque

"""
    **In-degree** answers: *which verses are referenced by the most other verses?* This is the simplest measure of structural importance.

    **Weighted in-degree** goes further: *which verses accumulate the most total community confidence?* A verse cited 10 times with an average of 80 votes each scores higher than one cited 100 times with an average of 5 votes.
"""

def top_in_degree(graph: dict, n: int) -> list[tuple[str, int]]:
    """
    Returns the top n verses with the highest in-degree.
    """
    in_degree = defaultdict(int)
    for from_verse in graph:
        for (to_verse, weight) in graph[from_verse]:
            in_degree[to_verse] += 1

    return sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:n]

def top_weighted_in_degree(graph: dict, n: int) -> list[tuple[str, float]]:
    """
    Returns the top n verses with the highest weighted in-degree.
    weight represents the strength of the connection between verses, the verses with higher weighted in-degree are more central in the graph, as they are referenced by many other verses with strong connections.
    """
    weighted_in_degree = defaultdict(float)
    for from_verse in graph:
        for to_verse, weight in graph[from_verse]:
            weighted_in_degree[to_verse] += weight

    return sorted(weighted_in_degree.items(), key=lambda x: x[1], reverse=True)[:n]
def compute_pagerank(graph: dict,
                     damping: float = 0.85,
                     max_iter: int = 100,
                     tol: float = 1e-6
                     ) -> dict[str, float]:
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        for to_verse, _ in neighbors:
            all_nodes.add(to_verse)

    N = len(all_nodes)
    score = {node: 1 / N for node in all_nodes}
    out_weight = {node: sum(w for _, w in graph.get(node, [])) for node in all_nodes}
    dangling_nodes = {node for node in all_nodes if not graph.get(node)}

    for _ in range(max_iter):
        dangling_sum = sum(score[node] for node in dangling_nodes)
        new_score = {node: (1 - damping) / N + damping * dangling_sum / N for node in all_nodes}

        for u in graph:
            if out_weight[u] == 0:
                continue
            for v, votes in graph[u]:
                new_score[v] += damping * score[u] * votes / out_weight[u]

        if max(abs(new_score[v] - score[v]) for v in all_nodes) < tol:
            break
        score = new_score

    return score


def top_pagerank(graph: dict, n: int, **kwargs) -> list[tuple[str, float]]:
    scores = compute_pagerank(graph, **kwargs)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]


def compute_betweenness(graph: dict, n: int, k:int = 200) -> list[tuple[str,float]]:
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        for to_verse, _ in neighbors:
            all_nodes.add(to_verse)

    all_nodes = sorted(all_nodes)
    N = len(all_nodes)
    betweenness = defaultdict(float)

    random.seed(42)
    sources = random.sample(all_nodes, min(k, N))

    for s in sources:
        pred = defaultdict(list)
        sigma = defaultdict(int)
        sigma[s] = 1
        dist = defaultdict(lambda: -1)
        dist[s] = 0

        queue = deque([s])
        order = []

        while queue:
            v = queue.popleft()
            order.append(v)
            for neighbor, _ in graph.get(v, []):
                if dist[neighbor] == -1:
                    dist[neighbor] = dist[v] + 1
                    queue.append(neighbor)
                if dist[neighbor] == dist[v] + 1:
                    sigma[neighbor] += sigma[v]
                    pred[neighbor].append(v)
        
        delta = defaultdict(float)
        for v in reversed(order):
            for u in pred[v]:
                delta[u] += (sigma[u] / sigma[v]) * (1 + delta[v])
            if v != s:
                betweenness[v] += delta[v]
        
    scale = N / k
    norm = 1 / ((N - 1) * (N - 2)) if N > 2 else 1.0
        
    for v in betweenness:
        betweenness[v] *= scale * norm

    return sorted(betweenness.items(), key=lambda x: x[1], reverse=True) [:n]
