# carregar os dados de referencias cruzadas preservando a direcao original
from collections import defaultdict

import pandas as pd
from utils.verse_utils import expand_verse


def load_cross_references(filepath: str) -> dict[str, list[str]]:
    df = pd.read_csv(
        filepath,
        sep='\t',
        skiprows=1,
        names=['from_verse', 'to_verse', 'votes'],
        usecols=[0, 1, 2],
    )

    df = df[df['votes'] > 0].copy()
    df['to_verse'] = df['to_verse'].apply(expand_verse)
    df = df.explode('to_verse').reset_index(drop=True)

    graph = defaultdict(list)

    for _, row in df.iterrows():
        from_verse = row['from_verse']
        to_verse = row['to_verse']

        graph[from_verse].append(to_verse)

    return dict(graph)
