from ontology.builtins import *
import ontology.builtins

def Main():
    a = 20
    l = makelist(a)
    print(a)
    b = l[20]
    print(b)
    
def makelist(maxl):
    a = []
    for i in range(0,maxl):
        a.append(i)
    return a
