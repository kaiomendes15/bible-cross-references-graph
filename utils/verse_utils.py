# Utils para manipulação de versículos
import re

"""
    Se o versículo for um intervalo (ex: John.1.1-John.1.3),
    retorna uma lista com cada versículo expandido.
    Caso contrário, retorna uma lista com o próprio versículo.
"""
def expand_verse(verse):
    if '-' not in verse:
        return [verse]

    start, end = verse.split('-')
    match_start = re.match(r'(.+)\.(\d+)\.(\d+)', start)
    match_end   = re.match(r'(.+)\.(\d+)\.(\d+)', end)

    if not match_start or not match_end:
        return [start]

    book_start, chap_start, verse_start = match_start.groups()
    book_end,   chap_end,   verse_end   = match_end.groups()

    if book_start != book_end or chap_start != chap_end:
        return [start]

    return [
        f"{book_start}.{chap_start}.{v}"
        for v in range(int(verse_start), int(verse_end) + 1)
    ]