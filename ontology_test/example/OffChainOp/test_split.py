OntCversion = '2.0.0'
from ontology.libont import split


def Main():
    s = "@abcd@efg@hijklmn@op@q@rst@uvwxy@z@"
    res = split(s, '@')
    for i in res:
        print(i)

    assert(len(res) == 10)
    assert(res[0] == '')
    assert(res[1] == 'abcd')
    assert(res[2] == 'efg')
    assert(res[3] == 'hijklmn')
    assert(res[4] == 'op')
    assert(res[5] == 'q')
    assert(res[6] == 'rst')
    assert(res[7] == 'uvwxy')
    assert(res[8] == 'z')
    assert(res[9] == '')

    s = "111@222j#@38u23@sfsdka@jjasdj@"
    res = split(s, '@')
    for i in res:
        print(i)

    assert(len(res) == 6)
    assert(res[0] == '111')
    assert(res[1] == '222j#')
    assert(res[2] == '38u23')
    assert(res[3] == 'sfsdka')
    assert(res[4] == 'jjasdj')
    assert(res[5] == '')
