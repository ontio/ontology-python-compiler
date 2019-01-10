OntCversion = '2.0.0'
from ontology.libont import split

def Main():
    s = "@abcd@efg@hijklmn@op@q@rst@uvwxy@z@"
    res = split(s, '@')
    for i in res:
        print(i)

    assert(len(res) == 8)
    assert(res[0] == 'abcd')
    assert(res[1] == 'efg')
    assert(res[2] == 'hijklmn')
    assert(res[3] == 'op')
    assert(res[4] == 'q')
    assert(res[5] == 'rst')
    assert(res[6] == 'uvwxy')
    assert(res[7] == 'z')

    s = "111@222j#@38u23@sfsdka@jjasdj@"
    res = split(s, '@')
    for i in res:
        print(i)

    assert(len(res) == 5)
    assert(res[0] == '111')
    assert(res[1] == '222j#')
    assert(res[2] == '38u23')
    assert(res[3] == 'sfsdka')
    assert(res[4] == 'jjasdj')
