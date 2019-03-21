OntCversion = '2.0.0'
import ontology.builtins

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")
s = "12345678"
def Main():
    b = s[:]
    c = s[:4]
    d = s[2:]
    e = s[3:6]
    f = s[0:1]
    g = s[2:2]
    h = []
    VaasAssert(b == s)
    VaasAssert(c == "1234")
    VaasAssert(d == "345678_add")
    VaasAssert(e == "456")
    VaasAssert(f == '1')
    VaasAssert(g == 0)
    VaasAssert(None == 0)
    VaasAssert(None == False)
    # can not compare this. should use is. array can not convert interger
    VaasAssert(not h is [])
    print(len(g))
    print(f)
    print(g)
