Cversion = '2.0.0'
import ontology.builtins
s = "12345678"
def Main():
    b = s[:]
    c = s[:4]
    d = s[2:]
    e = s[3:6]
    f = s[0:1]
    g = s[2:2]
    h = []
    assert(b == s)
    assert(c == "1234")
    assert(d == "345678")
    assert(e == "456")
    assert(f == '1')
    assert(g == 0)
    assert(None == 0)
    assert(None == False)
    # can not compare this. should use is. array can not convert interger
    assert(not h is [])
    print(len(g))
    print(f)
    print(g)
