OntCversion = '2.0.0'
from ontology.builtins import append, print

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

m = {0:'a', 'a':'b', 'b':'c'}

def main():
    l = [[1,3]]
    b = [2,4]
    l.append(b)
    test(l, m)
    VaasAssert(l[0][0] == 1)
    VaasAssert(l[0][1] == 3)
    VaasAssert(l[1][0] == 2)
    VaasAssert(l[1][1] == 4 + 1)
    VaasAssert(l[2][0] == 'a_add' )
    VaasAssert(l[2]['a'] == 'b')
    VaasAssert(l[2]['b'] == 'c')

def test(l_t, map_t):
    l_t.append(map_t)

