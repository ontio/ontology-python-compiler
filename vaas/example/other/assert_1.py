#!/usr/bin/eny python3
import ontology.builtins
def Main(operation, args):
    VaasAssert(operation == args)
    a = []
    for i in range(0,40):
        a.append(i)

    callist(a)
    checklist(a)

def checklist(l):
    for i in range(0,len(l)):
        print(i)
        VaasAssert(l[i] == i)
    
def callist(l):
    for i in range(0,len(l)):
        if i == 22:
            l[i] = 30

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")
