OntCversion = '2.0.0'


def Main():
    a = 0
    b = []
    c = []
    x = 0xffff
    if a and test_append_false(b) and test_append_true(c):
        x = 0
    assert(len(b) == 0)
    assert(len(c) == 0)
    assert(x == 0xffff)

    a = 1
    if a and test_append_false(b) and test_append_true(c):
        x = 1

    assert(len(b) == 1)
    assert(b[0] == 3)
    assert(len(c) == 0)
    assert(x == 0xffff)

    if a and test_append_true(b) and test_append_false(c):
        x = 2

    assert(len(b) == 2)
    assert(b[0] == 3)
    assert(b[1] == 2)
    assert(len(c) == 1)
    assert(c[0] == 3)
    assert(x == 0xffff)

    if a and test_append_true(b) and test_append_true(c):
        x = 3

    assert(len(b) == 3)
    assert(b[0] == 3)
    assert(b[1] == 2)
    assert(b[2] == 2)
    assert(len(c) == 2)
    assert(c[0] == 3)
    assert(c[1] == 2)
    assert(x == 3)

    a = 8
    b = 9
    c = 7
    d = 0

    x = a and b and c
    assert(x == c)

    x = a and b and c and d
    assert(x == d)

    x = d or a or b or c
    assert(x == a)

    x = d or 0 or b or c
    assert(x == b)

    x = d or 0 or 0 or c
    assert(x == c)

    x = 0 or (9 and 7 or 8) or 6
    assert(x == 7)

    x = 0 or (9 and 7 and 8) or 6
    assert(x == 8)

    x = 0 or (9 and 7 and 8) and 6
    assert(x == 6)

    x = 0 or (9 and 7 and 8) and 6 or 0
    assert(x == 6)

    x = 0 or (9 and 7 and 0) and 6 or 0
    assert(x == 0)

    x = 0 or (9 and 0 or 5) or 6 or 0
    assert(x == 5)

    x = 0 or (9 and 0 or 5) and 6 and 0
    assert(x == 0)

    x = 0 or (9 and 0 or 5) and 6 and 0 or 1
    assert(x == 1)

    x = 4 or (9 and 0 or 5) and 6 and 0 or 1
    assert(x == 4)


def test_append_true(l):
    l.append(2)
    return True


def test_append_false(l):
    l.append(3)
    return False
