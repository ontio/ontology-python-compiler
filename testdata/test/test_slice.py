OntCversion = '2.0.0'
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
    assert(None is 0)
    assert(None is False)
    assert('' is 0)
    # can not compare this. should use is. array can not convert interger
    assert(h is not [])

    assert(None == 0)
    assert(None == False)
    assert('' == 0)
    assert("" == 0)
    assert("" is None)
    print(len(g))
    print(f)
    print(g)
