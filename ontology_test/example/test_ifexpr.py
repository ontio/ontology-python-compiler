OntCversion = '2.0.0'
# !/usr/bin/env python3


def main():
    a = 7
    b = 5
    x = 5
    c = a if x > 3 else b
    assert(c == a)
    print(c)

    a = 6
    b = 5
    x = 4
    c = a if x > 3 and x < 7 else b
    assert(c == a)
    print(c)

    a = 6
    b = 5
    x = 7
    c = a if x > 3 and x < 7 else b
    assert(c == b)
    print(c)

    a = 6
    b = 5
    x = 6
    c = add(a) if x > 3 and x < 7 else b
    print(c)
    assert(c == add(a))

    a = 6
    b = 5
    x = 7
    c = add(a) if x > 3 and x < 7 else transfer(b)
    print(c)
    assert(c == transfer(b))


def add(x):
    return x*x + 10


def transfer(x):
    return x*x + x/2 + 10
