import string


def levenstein(
    reference: str,
    text: str,
) -> int:
    if not reference:
        return len(text)
    if not text:
        return len(reference)
    reference = prep_text(reference)
    text = prep_text(text)

    n = len(reference)
    m = len(text)
    lev = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        lev[i][0] = i
    for i in range(m + 1):
        lev[0][i] = i

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            insertion = lev[i - 1][j] + 1
            deletion = lev[i][j - 1] + 1
            substitution = lev[i - 1][j - 1] + (
                1 if reference[i - 1] != text[j - 1] else 0
            )
            lev[i][j] = min(insertion, deletion, substitution)

    return lev[n][m]


def prep_text(text: str) -> str:
    chars_to_remove = string.punctuation + string.whitespace
    return text.lower().translate(str.maketrans("", "", chars_to_remove))
