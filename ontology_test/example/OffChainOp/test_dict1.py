OntCversion = '2.0.0'


def Main():
    d = {}

    d['a'] = 4
    d[13] = 3

    d['mydict'] = {}
    assert(d['a'] == 4)
    assert(d[13] == 3)
