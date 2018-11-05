import ontology.builtins
s = "12345678"
def Main():
    b = s[:]
    c = s[:4]
    d = s[2:]
    e = s[3:6]
    assert(b == s)
    assert(c == "1234")
    assert(d == "345678")
    assert(e == "456")
