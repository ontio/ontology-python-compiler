def _sunday_search(T, P):
    n = len(T)
    m = len(P)

    shift = [m + 1 for i in range(0, 256)]
    for i in range(0, m):
        shift[ord(P[i])] = m - i
    i = 0
    while i < n - m + 1:
        for j in range(0, m):
            if T[j + i] != P[j]:
                break
        else:
            return i
        if i + m < n:
            i += shift[ord(T[i + m])]
        else:
            return -1

    return -1


def _horspool_search(T, P):
    n = len(T)
    m = len(P)

    shift = [m for i in range(0, 256)]
    for i in range(0, m - 1):
        shift[ord(P[i])] = m - i - 1

    i = 0
    while i < n - m + 1:
        for j in range(0, m):
            if T[j + i] != P[j]:
                break
        else:
            return i

        i += shift[(T[i + m - 1])]
    return -1


def find(s, p):
    from ontology.lib.string import _horspool_search, _sunday_search
    alg = 1
    if alg == 1:
        return _horspool_search(s, p)
    elif alg == 2:
        return _sunday_search(s, p)
