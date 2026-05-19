import string


def levenstein(
    a: str,
    b: str,
) -> int:
    if not a:
        return len(b)
    if not b:
        return len(a)
    a = prep_text(a)
    b = prep_text(b)

    n = len(a)
    m = len(b)
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
                1 if a[i - 1] != b[j - 1] else 0
            )
            lev[i][j] = min(insertion, deletion, substitution)

    return lev[n][m]


def prep_text(text: str) -> str:
    chars_to_remove = string.punctuation + string.whitespace
    return text.lower().translate(str.maketrans("", "", chars_to_remove))
