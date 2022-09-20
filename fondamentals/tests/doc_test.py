""" TESTING DOC """

def fact(_n):
    """
        paramètre n : (int) un entier
        valeur renvoyée : (int) la factorielle de n.

    CU : n >= 0

    Exemples :

    >>> fact(3)
    6
    >>> fact(5)
    12
    """
    res = 1
    for i in range(2, _n + 1):
        res = res * i
    return res

"""
if __name__ == '__main__':
    import doctest
    doctest.testmod()
"""