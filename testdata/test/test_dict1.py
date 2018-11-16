OntCversion = '2.0.0'
from ontology.builtins import print

def Main():

    d = {}

    d['a'] = 4
    d[13] = 3

    d['mydict'] = {}
    assert(d['a'] == 4)
    assert(d[13] == 3)

