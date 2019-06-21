OntCversion = '2.0.0'
# !/usr/bin/env python3


def Main():
    a = [[x, y] for x in range(0, 10) if x % 2 if x > 3 for y in range(0, 10) if y > 7 if y != 8]
    # a = [[x, y] for x in range(10)  for y in range(10)]
    # a = [x for x in range(0,10) if x > 2 if x > 3]
    assert(len(a) == 3)
    x = a[0]
    y = a[1]
    z = a[2]

    assert(x[0] == 5)
    assert(y[0] == 7)
    assert(z[0] == 9)
    assert(x[1] == 9)
    assert(y[1] == 9)
    assert(z[1] == 9)

    # a = [1,2,3,4,5]
    for i in a:
        assert(len(i) == 2)
        print(i[0])
        print(i[1])

    b = [[x, y] for x in range(0, 10) if x % 2 for y in range(0, 10) if y > 7 if y != 8]

    for i in b:
        assert(len(i) == 2)
        print(i[0])
        print(i[1])

    c = [x*y*z for x in range(1, 3) for y in range(1, 3) for z in range(1, 3)]

    assert(len(c) == 8)
    print(len(c))

    assert(c[0] == 1)
    assert(c[1] == 2)
    assert(c[2] == 2)
    assert(c[3] == 4)
    assert(c[4] == 2)
    assert(c[5] == 4)
    assert(c[6] == 4)
    assert(c[7] == 8)

    t = [[x, y] for x in range(0, 10) if x > 9 if and_test() > 3 for y in range(0, 10) if y > 7 if y != 8]
    assert(len(t) == 0)


def and_test():
    assert(False)
    return 5
