OntCversion = '2.0.0'


def Main():
    j = 10

    d = {
        'a': 1,
        'b': 4,
        4: 'blah',
        'm': j,
        'z': [1, 3, 4, 5, 'abcd', j],
        'mcalll': mymethod(1, 4)
    }

    j4 = d['mcalll']

    k = j4 + d['z'][3]
    assert(k == 10)
    print(k)


def mymethod(a, b):
    return a + b
