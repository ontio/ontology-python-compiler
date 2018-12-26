OntCversion = '2.0.0'
from ontology.builtins import len, print, append
def Main():
    l = []
    a = 4
    b = 3
    c = 5
    d = 8
    e = 8
    x = 0
    #first false.
    if a <  b < append_elt(l, c) < append_elt(l, d) >= append_elt(l, e):
        x = 1

    assert(x == 0)
    assert(len(l) == 0)

    #second false.
    a = 2
    l = []
    if a < b > append_elt(l, c) > append_elt(l, d) >= append_elt(l, e):
        x = 2

    assert(len(l) == 1)
    assert(l[0] == c)
    assert(x == 0)

    #third false
    l = []
    if a < b < append_elt(l, c) > append_elt(l, d) >= append_elt(l, e):
        x = 3

    assert(len(l) == 2)
    assert(l[0] == c)
    assert(l[1] == d)
    assert(x == 0)

    #fouth false
    l = []
    if a < b < append_elt(l, c) < append_elt(l, d) > append_elt(l, e):
        x = 4

    assert(len(l) == 3)
    assert(l[0] == c)
    assert(l[1] == d)
    assert(l[2] == e)
    assert(x == 0)

    #fouth ture
    l = []
    if a < b < append_elt(l, c) < append_elt(l, d) >= append_elt(l, e):
        x = 5

    assert(len(l) == 3)
    assert(l[0] == c)
    assert(l[1] == d)
    assert(l[2] == e)
    assert(x == 5)

def append_elt(l, e):
    l.append(e)
    return e
