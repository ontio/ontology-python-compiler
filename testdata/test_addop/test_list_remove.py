OntCversion = '2.0.0'
from ontology.builtins import remove, print, len

def Main():
    l = [9,8,7,6,5]
    for v in l:
        print(v)

    l.remove(0)
    l.remove(0)
    l.remove(0)

    assert(l[0] == 6)
    assert(l[1] == 5)

    l = [0]
    assert(len(l) == 1)
    l.remove(0)
    assert(len(l) == 0)
