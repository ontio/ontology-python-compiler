OntCversion = '2.0.0'
# !/usr/bin/env python3

b = {i: j for i in range(1, 5) for j in range(5, 8)}


def main():
    assert(b[1] == 7)
    assert(b[2] == 7)
    assert(b[3] == 7)
    assert(b[4] == 7)
    print(b[1])
    print(b[2])
    print(b[3])
    print(b[4])
