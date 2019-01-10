OntCversion = '2.0.0'
def Main():
    l = []
    a = 4
    b = 3
    c = 5
    d = 8
    e = 8
    x = 0

    a = 0
    if a and append_elt_false(l, c) and append_elt_false(l, d) and append_elt_true(l, e):
        x = 1

    assert(x == 0)
    assert(len(l) == 0)

    a = 1
    l = []
    if a and append_elt_false(l, c) and append_elt_false(l, d) and append_elt_true(l, e):
        x = 2
    assert(x == 0)
    assert(len(l) == 1)
    assert(l[0] == c)


    a = 1
    l = []
    if a and append_elt_true(l, c) and append_elt_false(l, d) and append_elt_true(l, e):
        x = 3
    assert(x == 0)
    assert(len(l) == 2)
    assert(l[0] == c)
    assert(l[1] == d)

    a = 1
    l = []
    if a and append_elt_true(l, c) and append_elt_true(l, d) and append_elt_false(l, e):
        x = 4
    assert(x == 0)
    assert(len(l) == 3)
    assert(l[0] == c)
    assert(l[1] == d)
    assert(l[2] == e)

    a = 1
    l = []
    if a and append_elt_true(l, c) and append_elt_true(l, d) and append_elt_true(l, e):
        x = 5
    assert(x == 5)
    assert(len(l) == 3)
    assert(l[0] == c)
    assert(l[1] == d)
    assert(l[2] == e)

    a = 1
    l = []
    x = 0
    if a or append_elt_true(l, c) or append_elt_true(l, d) or append_elt_true(l, e):
        x = 6
    assert(x == 6)
    assert(len(l) == 0)

    a = 0
    l = []
    x = 0
    if a or append_elt_true(l, c) or append_elt_true(l, d) or append_elt_true(l, e):
        x = 7
    assert(x == 7)
    assert(len(l) == 1)
    assert(l[0] == c)

    a = 0
    l = []
    x = 0
    if a or append_elt_false(l, c) or append_elt_true(l, d) or append_elt_true(l, e):
        x = 8
    assert(x == 8)
    assert(len(l) == 2)
    assert(l[0] == c)
    assert(l[1] == d)

    a = 0
    l = []
    x = 0
    if a or append_elt_false(l, c) or append_elt_false(l, d) or append_elt_true(l, e):
        x = 9
    assert(x == 9)
    assert(len(l) == 3)
    assert(l[0] == c)
    assert(l[1] == d)
    assert(l[2] == e)

    a = 0
    l = []
    x = 0
    if a or append_elt_false(l, c) or append_elt_false(l, d) or append_elt_false(l, e):
        x = 10
    assert(x == 0)
    assert(len(l) == 3)
    assert(l[0] == c)
    assert(l[1] == d)
    assert(l[2] == e)

    a = 0
    l = []
    x = 0
    if a or append_elt_false(l, c) or append_elt_false(l, d) and append_elt_true(l, e):
        x = 10
    assert(x == 0)
    assert(len(l) == 2)
    assert(l[0] == c)
    assert(l[1] == d)

    a = 1
    l = []
    x = 0
    if a or append_elt_false(l, c) or append_elt_false(l, d) and append_elt_true(l, e):
        x = 10
    assert(x == 10)
    assert(len(l) == 0)

    a = 1
    l = []
    x = 0
    if (a or append_elt_false(l, c) or append_elt_false(l, d)) and append_elt_false(l, e):
        x = 10
    assert(x == 0)
    assert(len(l) == 1)
    assert(l[0] == e)

    a = 0
    l = []
    x = 0
    if (a or (append_elt_false(l, c) or append_elt_true(l, d))) and append_elt_false(l, e):
        x = 10
    assert(x == 0)
    assert(len(l) == 3)
    assert(l[0] == c)
    assert(l[1] == d)
    assert(l[2] == e)

    a = 0
    l = []
    x = 0
    if (a or append_elt_false(l, c)) or (append_elt_false(l, d) and append_elt_false(l, e)):
        x = 10
    assert(x == 0)
    assert(len(l) == 2)
    assert(l[0] == c)
    assert(l[1] == d)

    a = 0
    l = []
    x = 0
    if (a and append_elt_false(l, c)) or (append_elt_false(l, d) and append_elt_false(l, e)):
        x = 10
    assert(x == 0)
    assert(len(l) == 1)
    assert(l[0] == d)

    a = 0
    l = []
    x = 0
    f = 20
    g = 21
    h = 22
    if (a and append_elt_false(l, c)) or (append_elt_false(l, d) or append_elt_true(l, f)) and (append_elt_false(l, g) and append_elt_false(l, e)) or append_elt_true(l, h):
        x = 10
    assert(x == 10)
    assert(len(l) == 4)
    assert(l[0] == d)
    assert(l[1] == f)
    assert(l[2] == g)
    assert(l[3] == h)

    a = 0
    l = []
    x = 0
    f = 20
    g = 21
    h = 22
    if (a and append_elt_false(l, c)) or (append_elt_false(l, d) or append_elt_true(l, f)) and append_elt_false(l, g) and (append_elt_false(l, e) or append_elt_true(l, h)):
        x = 10
    assert(x == 0)
    assert(len(l) == 3)
    assert(l[0] == d)
    assert(l[1] == f)
    assert(l[2] == g)

def append_elt_true(l, e):
    l.append(e)
    return True

def append_elt_false(l, e):
    l.append(e)
    return False
