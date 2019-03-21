#!/usr/ben/env python3
import ontology.builtins

def Main(operation, args):
    b = 40
    d = []
    l = makelist(b)

    for e in l:
        c = b / e;
        d.append(c)

def makelist(maxl):
    a = []
    for i in range(1, maxl):
        if i == 8:
            i = 20 * (maxl - maxl) + 0
        a.append(i)

    return a
