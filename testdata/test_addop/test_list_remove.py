OntCversion = '2.0.0'
from ontology.builtins import remove, print, len

def Main():
    l = [9,8,7,6,5]
    l.remove(7)
    for v in l:
        print(v)

    assert(l[0] == 9)
    assert(l[1] == 8)
    assert(l[2] == 6)
    assert(l[3] == 5)

    l = [0]
    assert(len(l) == 1)
    l.remove(0)
    assert(len(l) == 0)
