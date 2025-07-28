def init_matrice(n, m):
    """
    n: ligne
    m: colonne
    """
    mat = []
    i = 0
    while i < n:
        j = 0
        tab = []
        while j < m:
            tab += [0]
            j += 1
        mat += [tab]
        i += 1
    return mat