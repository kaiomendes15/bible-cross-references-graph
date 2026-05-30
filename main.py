import os

from analysis.queries import ego_graph, ego_summary, shortest_path
from graph.builder import build_graph
from graph.community import community_summary, detect_communities
from graph.loader import load_cross_references
from graph.metrics import (
    compute_betweenness,
    compute_pagerank,
    top_in_degree,
    top_pagerank,
    top_weighted_in_degree,
)
from visualization.plot import (
    plot_community_top_pagerank,
    plot_ego_graph,
    plot_overview,
)

OUTPUT_DIR = "output"
DEFAULT_COMMUNITY_ID = 19


def print_count_table(title: str, results: list[tuple[str, int | float]]) -> None:
    print(f"\n=== {title} ===")
    print(f"{'Rank':<6} {'Verse':<25} {'Count':>12}")
    print("-" * 45)
    for rank, (verse, count) in enumerate(results, 1):
        print(f"{rank:<6} {verse:<25} {count:>12,}")


def print_score_table(title: str, results: list[tuple[str, float]]) -> None:
    print(f"\n=== {title} ===")
    print(f"{'Rank':<6} {'Verse':<25} {'Score':>12}")
    print("-" * 45)
    for rank, (verse, score) in enumerate(results, 1):
        print(f"{rank:<6} {verse:<25} {score:>12.4f}")


def select_community_id(summary: dict[int, int]) -> int:
    if DEFAULT_COMMUNITY_ID in summary:
        return DEFAULT_COMMUNITY_ID
    return max(summary.items(), key=lambda item: item[1])[0]


def top_pagerank_in_community(
    pagerank_scores: dict[str, float],
    partition: dict[str, int],
    community_id: int,
    limit: int,
) -> list[tuple[str, float]]:
    community_scores = [
        (verse, pagerank_scores.get(verse, 0.0))
        for verse, node_community_id in partition.items()
        if node_community_id == community_id
    ]
    return sorted(community_scores, key=lambda item: item[1], reverse=True)[:limit]


def save_community_pagerank_table(
    community_id: int,
    results: list[tuple[str, float]],
    output_path: str,
) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(f"Community {community_id} - top {len(results)} by PageRank\n")
        file.write("Rank\tVerse\tPageRank\n")
        for rank, (verse, score) in enumerate(results, 1):
            file.write(f"{rank}\t{verse}\t{score:.10f}\n")


def main() -> None:
    print("Carregando dados...")
    graph = load_cross_references("data/cross_references.txt")

    print("Construindo grafo...")
    nx_graph = build_graph(graph)
    print(f"Vertices: {nx_graph.number_of_nodes()}")
    print(f"Arestas:  {nx_graph.number_of_edges()}")

    print_count_table("Top 20 by In-Degree", top_in_degree(graph, 20))
    print_count_table("Top 20 by Weighted In-Degree", top_weighted_in_degree(graph, 20))

    print("\nCalculando PageRank...")
    pagerank_scores = compute_pagerank(graph)
    top_20_pagerank = top_pagerank(graph, 20)
    print_score_table("Top 20 by PageRank", top_20_pagerank)

    print("\nCalculando Betweenness Centrality...")
    print("(approximate, k=200 samples)")
    top_betweenness = compute_betweenness(graph, n=20, k=200)
    print_score_table("Top 20 by Betweenness Centrality", top_betweenness)

    print("\nDetectando comunidades...")
    partition = detect_communities(graph)
    summary = community_summary(partition)
    sizes = list(summary.values())

    print("\n=== Community Summary ===")
    print(f"Total communities: {len(summary)}")
    print(f"Largest community: {max(sizes):,} verses")
    print(f"Smallest community: {min(sizes):,} verses")

    print("\n=== Shortest Path: Gen.1.1 -> John.1.1 ===")
    try:
        path_result = shortest_path(graph, "Gen.1.1", "John.1.1")
        print(f"Path:  {' -> '.join(path_result['path'])}")
        print(f"Cost:  {path_result['cost']:.4f}")
        print(f"Hops:  {path_result['hops']}")
    except ValueError as error:
        print(error)

    top_pagerank_verse = top_20_pagerank[0][0]
    ego_sub = ego_graph(graph, top_pagerank_verse, radius=1)
    print(f"\n=== Ego Graph Summary: {top_pagerank_verse} ===")
    print(ego_summary(graph, top_pagerank_verse, radius=1))

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    top_100_pagerank_nodes = [
        verse
        for verse, _score in sorted(
            pagerank_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:100]
    ]

    ego_output_path = os.path.join(OUTPUT_DIR, "ego_graph.png")
    overview_output_path = os.path.join(OUTPUT_DIR, "overview.png")
    plot_ego_graph(
        ego_sub,
        partition,
        f"Ego graph: {top_pagerank_verse}",
        ego_output_path,
    )
    plot_overview(graph, top_100_pagerank_nodes, partition, overview_output_path)

    community_id = select_community_id(summary)
    community_top_50 = top_pagerank_in_community(
        pagerank_scores,
        partition,
        community_id,
        50,
    )
    community_top_50_nodes = [verse for verse, _score in community_top_50]
    community_table_output_path = os.path.join(
        OUTPUT_DIR,
        f"community_{community_id}_top50_pagerank.txt",
    )
    community_image_output_path = os.path.join(
        OUTPUT_DIR,
        f"community_{community_id}_top50_pagerank.png",
    )
    save_community_pagerank_table(
        community_id,
        community_top_50,
        community_table_output_path,
    )
    plot_community_top_pagerank(
        graph,
        community_top_50_nodes,
        partition,
        community_id,
        community_image_output_path,
    )

    print("\n=== Saved visualizations ===")
    print(ego_output_path)
    print(overview_output_path)
    print(community_table_output_path)
    print(community_image_output_path)


if __name__ == "__main__":
    main()
