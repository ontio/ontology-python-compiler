OntCversion = '2.0.0'


def Main():
    a = 8
    b = 9
    c = 3
    if b > c not in testl():
        assert(False)
    else:
        a = 9
    assert(a == 9)

    a = 8
    b = 9
    c = 3
    if b < c not in testl():
        assert(False)
    else:
        a = 9
    assert(a == 9)

    a = 8
    b = 9
    c = 3
    if b > c in testl():
        a = 1
    else:
        a = 9
    assert(a == 1)

    a = 8
    b = 9
    c = 3
    if b > getleft() in testl():
        a = 1
    else:
        assert(False)
        a = 9
    assert(a == 1)


def testl():
    return [1, 2, 3, 4, 5]


def test2():
    assert(False)


def getleft():
    a = 3
    return a
