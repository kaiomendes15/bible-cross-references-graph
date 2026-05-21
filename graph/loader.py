# carregar os dados de referências cruzadas do arquivo txt e retornar um dataframe pandas
import pandas as pd
from utils.verse_utils import expand_verse

def load_cross_references(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, sep='\t', skiprows=1,
                     names=['from_verse', 'to_verse', 'votes'],
                     usecols=[0, 1, 2])

    df = df[df['votes'] > 0].copy()
    df['to_verse'] = df['to_verse'].apply(expand_verse)
    df = df.explode('to_verse').reset_index(drop=True)

    return df