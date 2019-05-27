OntCversion = '2.0.0'
# !/usr/bin/env python3


def main():
    a = 2
    b = 4
    t = 0
    if a == 2 or (a == 5 and b == 4) or a == 3 and a == 7:
        t = 1
        print("or in")
    else:
        t = 2
        print("or not in")

    assert(t == 1)

    a = 5
    b = 4
    if a == 2 or (a == 5 and b == 4) or a == 3 and a == 7:
        t = 3
        print("or in")
    else:
        t = 4
        print("or not in")

    assert(t == 3)

    a = 3
    b = 1000
    if a == 2 or (a == 5 and b == 4) or a == 3 and a == 7:
        t = 5
        print("or in")
    else:
        t = 6
        print("or not in")

    assert(t == 6)

    a = 9
    if (a == 2 or (a == 5 and b == 4) or a == 3 and a == 7) or a == 9:
        t = 7
        print("or in")
    else:
        t = 8
        print("or not in")
    assert(t == 7)

    a = 7
    if (a == 2 or (a == 5 and b == 4) or a == 3 and a == 7) or a == 9:
        t = 9
        print("or in")
    else:
        t = 10
        print("or not in")

    assert(t == 10)

    a = 10

    if a == 2 or (a == 5 and b == 4) or (a == 3 and a == 7) or a == 9 or a == 10:
        t = 11
        print("or in")
    else:
        t = 12
        print("or not in")

    assert(t == 11)

    a = 8
    b = 4

    if a == 2 or (a == 5 and b == 4) or a == 3 and a == 7:
        t = 13
        print("or in")
    else:
        t = 14
        print("or not in")

    assert(t == 14)

    a = 5
    b = 4

    if a == 2 or (a == 5 and b == 4) or a == 3 and a == 7:
        t = 15
        print("or in")
    else:
        t = 16
        print("or not in")

    assert(t == 15)
    print("bool test ok")
