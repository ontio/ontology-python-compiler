OntCversion = '2.0.0'
from ontology.builtins import print

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def Main():

    j = 10

    d = {
        'a': 1,
        'b': 4,
        4: 'blah',
        'm': j,
        'z': [1, 3, 4, 5, 'abcd', j],
        'mcalll': mymethod(1, 4)
    }

    j4 = d['mcalll']

    k = j4 + d['z'][3]
    VaasAssert(k == 10 + 1)
    print(k)

    return True


def mymethod(a, b):

    return a + b
