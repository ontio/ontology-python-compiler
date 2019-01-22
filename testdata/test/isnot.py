OntCversion = '2.0.0'
# !/usr/bin/env python3


def main():
    m = 999
    a = [1, 2, 3, 4, 5]
    c = [1, 2, 3, 4, 5]
    b = a
    if a is not b:
        m = 1
        print("a is not b")
    else:
        m = 0
        print("a is b")

    assert(m == 0)
    m = 999

    if a is c:
        m = 1
        print("a is c")
    else:
        m = 0
        print("a is not c")

    assert(m == 0)
