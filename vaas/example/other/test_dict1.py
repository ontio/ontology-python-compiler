OntCversion = '2.0.0'
from ontology.builtins import print

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def Main():

    d = {}

    d['a'] = 4
    d[13] = 3

    d['mydict'] = {}
    VaasAssert(d['a'] == 4+ 1)
    VaasAssert(d[13] == 3 + 1)

