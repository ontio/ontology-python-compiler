OntCversion = '2.0.0'


def Main():
    lst = []
    a = 4
    b = 3
    c = 5
    d = 8
    e = 8
    x = 0
    # first false.
    if a < b < append_elt(lst, c) < append_elt(lst, d) >= append_elt(lst, e):
        x = 1

    assert(x == 0)
    assert(len(lst) == 0)

    # second false.
    a = 2
    lst = []
    if a < b > append_elt(lst, c) > append_elt(lst, d) >= append_elt(lst, e):
        x = 2

    assert(len(lst) == 1)
    assert(lst[0] == c)
    assert(x == 0)

    # third false
    lst = []
    if a < b < append_elt(lst, c) > append_elt(lst, d) >= append_elt(lst, e):
        x = 3

    assert(len(lst) == 2)
    assert(lst[0] == c)
    assert(lst[1] == d)
    assert(x == 0)

    # fourth false
    lst = []
    if a < b < append_elt(lst, c) < append_elt(lst, d) > append_elt(lst, e):
        x = 4

    assert(len(lst) == 3)
    assert(lst[0] == c)
    assert(lst[1] == d)
    assert(lst[2] == e)
    assert(x == 0)

    # fifth ture
    lst = []
    if a < b < append_elt(lst, c) < append_elt(lst, d) >= append_elt(lst, e):
        x = 5

    assert(len(lst) == 3)
    assert(lst[0] == c)
    assert(lst[1] == d)
    assert(lst[2] == e)
    assert(x == 5)


def append_elt(lst, e):
    lst.append(e)
    return e
