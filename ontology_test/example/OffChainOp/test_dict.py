OntCversion = '2.0.0'
a = 'hello'
b = 'world'
c = 'c'


def Main():
    x = getdict()
    assert(x[a] == 1)
    assert(x[b] == 2)
    assert(x[c] == 3)
    print(x[a])
    print(x[b])
    print(x['c'])


def getdict():
    dic = {a: 1, b: 2, 'c': 3}
    return dic
