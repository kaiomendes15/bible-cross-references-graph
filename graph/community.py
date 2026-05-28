from collections import defaultdict

weighted_graph = dict[str, dict[str, float]] #dicionário em que cada nó aponta para seus vizinhos e o peso da conexão
partition = dict[str, int] #dicionário que mapeia cada nó para um id de comunidade

#converte um grafo direcionado para um grafo não direcionado. A detecção de comunidades costuma trabalhar com grafos não direcionados
def build_undirected(graph) -> weighted_graph: 
    undirected = defaultdict(lambda: defaultdict(float))
    for from_verse, edges in graph.items():
        undirected[from_verse]  
        for to_verse, votes in edges:
            undirected[from_verse][to_verse] += votes
            undirected[to_verse][from_verse] += votes
    return {
        node: dict(neighbors)
        for node, neighbors in undirected.items()
    }

#calcula a qualidade da divisão em comunidades (modularidade). Quanto maior a modularidade, melhor a divisão em comunidades
#é calculada comparando a densidade de arestas dentro das comunidades com a densidade esperada se as arestas fossem distribuídas aleatoriamente, mantendo os graus dos nós
#o valor da modularidade varia entre -1 e 1
def modularity(graph: weighted_graph, partition: partition) -> float:
    total_weight = total_edge_weight(graph)

    if total_weight == 0:
        return 0.0
    community_weight = defaultdict(float)
    community_degree = defaultdict(float)
    for node, neighbors in graph.items():
        node_community = partition[node]
        node_degree = sum(neighbors.values())
        community_degree[node_community] += node_degree
        for neighbor, weight in neighbors.items():
            if partition[neighbor] == node_community:
                community_weight[node_community] += weight
    score = 0.0

    for community_id in community_degree:
        internal = community_weight[community_id] / 2
        degree = community_degree[community_id]
        score += (internal/total_weight) - (degree / (2 * total_weight)) ** 2
    return score

#detecta a comunidade de versículo, baseado em louvain
def detect_communities(graph) -> dict[str, int]:
    undirected = build_undirected(graph) #converte para grafo não direcionado
    partition = _initial_partition(undirected) #inicializa a partição, colocando cada nó em sua própria comunidade
    improved = True
    max_passes = 20
    passes = 0

    while improved and passes < max_passes: #tenta melhorar a partição movendo nós entre comunidades. Para evitar loops infinitos, é limitado o número de passagens
        improved = _run_local_movement(undirected, partition)
        passes += 1

    return _normalize_community_ids(partition) #retorna um dicionário {versiculo: comunidade_id}

def community_summary(partition) -> dict: #conta quantos versículos existem em cada comunidade, retornando um dicionário {comunidade_id: número_de_versículos}
    summary = defaultdict(int)
    for community_id in partition.values():
        summary[community_id] += 1
    return dict(summary)

#cria uma partição inicial onde cada nó é sua própria comunidade
# é o ponto de partida para o algoritmo de Louvain, que irá iterativamente mover nós para comunidades vizinhas para melhorar a modularidade.
def _initial_partition(graph: weighted_graph) -> partition:
    return {
        node: index
        for index, node in enumerate(graph)
    }

#avalia se vale a pena mover um nó para uma comunidade vizinha, calculando o ganho de modularidade
#se o ganho for positivo, o nó é movido para a nova comunidade
#o processo é repetido para todos os nós até que nenhuma melhoria seja possível
def _run_local_movement(graph: weighted_graph, partition: partition) -> bool:
    improved = False
    total_weight = total_edge_weight(graph)

    if total_weight == 0:
        return False

    node_degrees = {
        node: sum(neighbors.values())
        for node, neighbors in graph.items()
    }
    community_degrees = defaultdict(float)

    for node, community_id in partition.items():
        community_degrees[community_id] += node_degrees[node]

    for node in graph:
        original_community = partition[node]
        best_community = original_community
        best_gain = 0.0
        node_degree = node_degrees[node]
        neighbor_communities = defaultdict(float)

        for neighbor, weight in graph[node].items():
            neighbor_communities[partition[neighbor]] += weight

        community_degrees[original_community] -= node_degree
        partition[node] = -1

        for candidate_community, weight_to_community in neighbor_communities.items():
            if candidate_community == original_community:
                continue

            gain = weight_to_community - (
                community_degrees[candidate_community] * node_degree
            ) / (2 * total_weight)

            if gain > best_gain:
                best_gain = gain
                best_community = candidate_community

        partition[node] = best_community
        community_degrees[best_community] += node_degree

        if best_community != original_community:
            improved = True

    return improved

#calcula o peso total das arestas do grafo, dividindo por 2 para evitar contar cada aresta duas vezes (uma vez para cada direção)
def total_edge_weight(graph: weighted_graph) -> float:
    total = 0.0

    for neighbors in graph.values():
        total += sum(neighbors.values())

    return total / 2

#renumera os ids das comunidades para que sejam sequenciais a partir de 0
def _normalize_community_ids(partition: partition) -> partition:
    id_map = {}
    next_id = 0
    normalized = {}

    for node, community_id in partition.items():
        if community_id not in id_map:
            id_map[community_id] = next_id
            next_id += 1

        normalized[node] = id_map[community_id]

    return normalized
