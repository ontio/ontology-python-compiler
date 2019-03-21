#!/usr/bin/env python3
import ontology.builtins

def Main(x):
    a = 20
    l = makelist(a, x)
    b = l[20]
    
def makelist(maxl, x):
    maxl = maxl + x - 1
    a = []
    for i in range(0,maxl):
        a.append(i)
    return a
