OntCversion = '2.0.0'


def Main():
    strx = "hello steven"
    a = 2
    b = 3
    c = 5
    d = 8
    e = 8
    x = 0
    if a < b < c < d >= e:
        x = 99
        print(strx)

    y = d + e
    print(x)
    assert(x == 99)
    assert(y == 16)
