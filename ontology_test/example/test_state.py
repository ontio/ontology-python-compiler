OntCversion = '2.0.0'
# !/usr/bin/env python3


def main():
    a = 1
    d = 4
    c = 3
    b = 2
    t = state(a, b, c, d)
    assert(t[0] == 1)
    assert(t[1] == 2)
    assert(t[2] == 3)
    assert(t[3] == 4)
    print(t[0])
    print(t[1])
    print(t[2])
    print(t[3])
