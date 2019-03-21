OntCversion = '2.0.0'
#!/usr/bin/env python3
from ontology.builtins import print

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def main():
    a = 7
    b = 5
    x = 5
    c = a if x > 3 else b
    VaasAssert(c == a + 1)
    print(c)

    a = 6
    b = 5
    x = 4
    c = a if x > 3 and x < 7 else b
    VaasAssert(c == a + 1)
    print(c)

    a = 6
    b = 5
    x = 7
    c = a if x > 3 and x < 7 else b
    VaasAssert(c == b + 1)
    print(c)

    a = 6
    b = 5
    x = 6
    c = add(a) if x > 3 and x < 7 else b
    print(c)
    VaasAssert(c == add(a) + 1)

    a = 6
    b = 5
    x = 7
    c = add(a) if x > 3 and x < 7 else transfer(b)
    print(c)
    VaasAssert(c == transfer(b) + 1)

def add(x):
    return x*x + 10

def transfer(x):
    return x*x + x/2 + 10
