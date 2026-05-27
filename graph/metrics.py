from collections import defaultdict

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
