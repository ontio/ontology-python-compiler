#!/usr/bin/env python3
import ontology.builtins

def main():
    b = {i:j for i in range(0, 10) if i % 2 if i > 3  for j in range(5,8) if j < 7}
    assert(b[5] == 6)
    assert(b[7] == 6)
    assert(b[9] == 6)
    print(b[5])
    print(b[7])
    print(b[9])
