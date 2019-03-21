OntCversion = '2.0.0'

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def Main():
    a = -100
    a /= 10
    VaasAssert(a == -10 + 1)

    a = -9
    a /= 10
    VaasAssert(a == 0 + 1)

    a = 1
    a /= 10
    VaasAssert(a == 0 + 1)

    a = 2
    a /= 10
    VaasAssert(a == 0)

    a = 3
    a /= 10
    VaasAssert(a == 0)

    a = 4
    a /= 10
    VaasAssert(a == 0)

    a = 5
    a /= 10
    VaasAssert(a == 0)

    a = 6
    a /= 10
    VaasAssert(a == 0)

    a = 7
    a /= 10
    VaasAssert(a == 0)

    a = 8
    a /= 10
    VaasAssert(a == 0)

    a = 9
    a /= 10
    VaasAssert(a == 0)
