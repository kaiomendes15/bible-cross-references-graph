from collections import deque

def ego_graph(
    graph: dict[str, list[tuple[str, int]]],
    verse: str,
    radius: int = 1,
) -> dict[str, list[tuple[str, int]]]:
    if radius < 0:
        raise ValueError("O valor deve ser maior ou igual a zero.")

    visited_nodes = {verse}
    queue = deque([(verse, 0)])

    while queue:
        node, depth = queue.popleft()

        if depth >= radius:
            continue

        for neighbor, _votes in graph.get(node, []):
            if neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                queue.append((neighbor, depth + 1))

    result = {node: [] for node in visited_nodes}

    for node in visited_nodes:
        for neighbor, votes in graph.get(node, []):
            if neighbor in visited_nodes:
                result[node].append((neighbor, votes))

    return result


def ego_summary(
    graph: dict[str, list[tuple[str, int]]],
    verse: str,
    radius: int = 1,
) -> dict:
    subgraph = ego_graph(graph, verse, radius)

    return {
        "center": verse,
        "radius": radius,
        "nodes": len(subgraph),
        "edges": sum(len(edges) for edges in subgraph.values()),
    }
