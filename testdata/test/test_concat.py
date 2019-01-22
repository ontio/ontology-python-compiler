OntCversion = '2.0.0'


def Main():
    s0 = 'he'
    s1 = 'llo'
    s2 = concat(s0, s1)
    print(s2)
    assert(s2 == 'hello')
