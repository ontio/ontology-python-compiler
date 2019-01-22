OntCversion = '2.0.0'


def Main():
    lst = []
    a = 4
    b = 0
    c = 5
    d = 8
    e = 8

    a = 0
    if a and append_elt_false(lst, c) and append_elt_false(lst, d) and append_elt_true(lst, e):
        b = 1

    assert(b == 0)
    assert(len(lst) == 0)

    a = 1
    lst = []
    if a and append_elt_false(lst, c) and append_elt_false(lst, d) and append_elt_true(lst, e):
        b = 2
    assert(b == 0)
    assert(len(lst) == 1)
    assert(lst[0] == c)

    a = 1
    lst = []
    if a and append_elt_true(lst, c) and append_elt_false(lst, d) and append_elt_true(lst, e):
        b = 3
    assert(b == 0)
    assert(len(lst) == 2)
    assert(lst[0] == c)
    assert(lst[1] == d)

    a = 1
    lst = []
    if a and append_elt_true(lst, c) and append_elt_true(lst, d) and append_elt_false(lst, e):
        b = 4
    assert(b == 0)
    assert(len(lst) == 3)
    assert(lst[0] == c)
    assert(lst[1] == d)
    assert(lst[2] == e)

    a = 1
    lst = []
    if a and append_elt_true(lst, c) and append_elt_true(lst, d) and append_elt_true(lst, e):
        b = 5
    assert(b == 5)
    assert(len(lst) == 3)
    assert(lst[0] == c)
    assert(lst[1] == d)
    assert(lst[2] == e)

    a = 1
    lst = []
    b = 0
    if a or append_elt_true(lst, c) or append_elt_true(lst, d) or append_elt_true(lst, e):
        b = 6
    assert(b == 6)
    assert(len(lst) == 0)

    a = 0
    lst = []
    b = 0
    if a or append_elt_true(lst, c) or append_elt_true(lst, d) or append_elt_true(lst, e):
        b = 7
    assert(b == 7)
    assert(len(lst) == 1)
    assert(lst[0] == c)

    a = 0
    lst = []
    b = 0
    if a or append_elt_false(lst, c) or append_elt_true(lst, d) or append_elt_true(lst, e):
        b = 8
    assert(b == 8)
    assert(len(lst) == 2)
    assert(lst[0] == c)
    assert(lst[1] == d)

    a = 0
    lst = []
    b = 0
    if a or append_elt_false(lst, c) or append_elt_false(lst, d) or append_elt_true(lst, e):
        b = 9
    assert(b == 9)
    assert(len(lst) == 3)
    assert(lst[0] == c)
    assert(lst[1] == d)
    assert(lst[2] == e)

    a = 0
    lst = []
    b = 0
    if a or append_elt_false(lst, c) or append_elt_false(lst, d) or append_elt_false(lst, e):
        b = 10
    assert(b == 0)
    assert(len(lst) == 3)
    assert(lst[0] == c)
    assert(lst[1] == d)
    assert(lst[2] == e)

    a = 0
    lst = []
    b = 0
    if a or append_elt_false(lst, c) or append_elt_false(lst, d) and append_elt_true(lst, e):
        b = 10
    assert(b == 0)
    assert(len(lst) == 2)
    assert(lst[0] == c)
    assert(lst[1] == d)

    a = 1
    lst = []
    b = 0
    if a or append_elt_false(lst, c) or append_elt_false(lst, d) and append_elt_true(lst, e):
        b = 10
    assert(b == 10)
    assert(len(lst) == 0)

    a = 1
    lst = []
    b = 0
    if (a or append_elt_false(lst, c) or append_elt_false(lst, d)) and append_elt_false(lst, e):
        b = 10
    assert(b == 0)
    assert(len(lst) == 1)
    assert(lst[0] == e)

    a = 0
    lst = []
    b = 0
    if (a or (append_elt_false(lst, c) or append_elt_true(lst, d))) and append_elt_false(lst, e):
        b = 10
    assert(b == 0)
    assert(len(lst) == 3)
    assert(lst[0] == c)
    assert(lst[1] == d)
    assert(lst[2] == e)

    a = 0
    lst = []
    b = 0
    if (a or append_elt_false(lst, c)) or (append_elt_false(lst, d) and append_elt_false(lst, e)):
        b = 10
    assert(b == 0)
    assert(len(lst) == 2)
    assert(lst[0] == c)
    assert(lst[1] == d)

    a = 0
    lst = []
    b = 0
    if (a and append_elt_false(lst, c)) or (append_elt_false(lst, d) and append_elt_false(lst, e)):
        b = 10
    assert(b == 0)
    assert(len(lst) == 1)
    assert(lst[0] == d)

    a = 0
    lst = []
    b = 0
    f = 20
    g = 21
    h = 22
    if (a and append_elt_false(lst, c)) or (append_elt_false(lst, d) or append_elt_true(lst, f)) and (append_elt_false(lst, g) and append_elt_false(lst, e)) or append_elt_true(lst, h):
        b = 10
    assert(b == 10)
    assert(len(lst) == 4)
    assert(lst[0] == d)
    assert(lst[1] == f)
    assert(lst[2] == g)
    assert(lst[3] == h)

    a = 0
    lst = []
    b = 0
    f = 20
    g = 21
    h = 22
    if (a and append_elt_false(lst, c)) or (append_elt_false(lst, d) or append_elt_true(lst, f)) and append_elt_false(lst, g) and (append_elt_false(lst, e) or append_elt_true(lst, h)):
        b = 10
    assert(b == 0)
    assert(len(lst) == 3)
    assert(lst[0] == d)
    assert(lst[1] == f)
    assert(lst[2] == g)


def append_elt_true(lst, e):
    lst.append(e)
    return True


def append_elt_false(lst, e):
    lst.append(e)
    return False
