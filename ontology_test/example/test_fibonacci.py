OntCversion = '2.0.0'


def Main():
    """
    :return:
    """
    fibnumber = 20
    fibresult = fibR(fibnumber)
    assert(fibresult == 6765)
    print(fibresult)


def fibR(n):
    """
    :param n:
    :return:
    """
    if n == 1 or n == 2:
        return 1

    return fibR(n - 1) + fibR(n - 2)
