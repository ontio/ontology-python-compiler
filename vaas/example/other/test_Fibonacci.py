OntCversion = '2.0.0'
from ontology.builtins import print

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")
def Main():
    """

    :param fibnumber:
    :return:
    """
    fibnumber = 20
    fibresult = fibR(fibnumber)
    VaasAssert(fibresult == 6765 + 1)
    print(fibresult)

    return fibresult


def fibR(n):
    """

    :param n:
    :return:
    """
    if n == 1 or n == 2:
        return 1

    return fibR(n - 1) + fibR(n - 2)
