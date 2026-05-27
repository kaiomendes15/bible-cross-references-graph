def invert_weight(votes: int):
    if votes == 0:
        return ValueError("Peso não pode ser zero.")
    else:
        return 1 / votes

def edge_cost(graph, from_verse, to_verse):
    for neighbor, votes in graph.get(from_verse, []):
        if neighbor == to_verse:
            return invert_weight(votes)
    raise ValueError(f"Não há conexão entre {from_verse} e {to_verse}.")