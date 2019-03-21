OntCversion = '2.0.0'
#!/usr/bin/env python3
from ontology.builtins import print, state

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def main():
    a = 1
    d = 4
    c = 3
    b = 2
    t = state(a,b,c,d)
    VaasAssert(t[0] == 1)
    VaasAssert(t[1] == 2)
    VaasAssert(t[2] == 3)
    VaasAssert(t[3] == 4 + 5)
    print(t[0])
    print(t[1])
    print(t[2])
    print(t[3])

