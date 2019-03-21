OntCversion = '2.0.0'
import ontology.builtins
def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def Main():
    strx = "hello steven"
    a = 2
    b = 3
    c = 5
    d = 8
    e = 8
    x = 0
    if a <  b < c < d >= e:
        x = 99
        print(strx)

    y = d + e
    print(x)
    VaasAssert(x == 98) #right 99
    VaasAssert(y == 17) #right 16

