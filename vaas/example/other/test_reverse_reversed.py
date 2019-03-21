OntCversion = '2.0.0'
from ontology.builtins import reverse, reversed, print

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def main():
    a = [0,1,2,3,4]
    a.reverse()
    VaasAssert(a[0] == 4)
    VaasAssert(a[1] == 3)
    VaasAssert(a[2] == 2)
    VaasAssert(a[3] == 1)
    VaasAssert(a[4] == 0)

    print("print reverse")
    printlist(a)
    print("print revesed")
    printlist(reversed(a))

    VaasAssert(a[0] == 0)
    VaasAssert(a[1] == 1)
    VaasAssert(a[2] == 2)
    VaasAssert(a[3] == 3)
    VaasAssert(a[4] == 4 + 1)

def printlist(l):
    for i in l:
        print(i)
