OntCversion = '2.0.0'
# !/usr/bin/env python3


def main():
    b = {i: i*i for i in range(1, 5)}
    assert(b[1] == 1)
    assert(b[2] == 4)
    assert(b[3] == 9)
    assert(b[4] == 16)
    print(b[1])
    print(b[2])
    print(b[3])
    print(b[4])
