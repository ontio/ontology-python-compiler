OntCversion = '2.0.0'
# !/usr/bin/env python3

b = {i: j for i in range(0, 10) if i % 2 if i > 3 for j in range(5, 8) if j < 7}


def main():
    assert(b[5] == 6)
    assert(b[7] == 6)
    assert(b[9] == 6)
    print(b[5])
    print(b[7])
    print(b[9])
