OntCversion = '2.0.0'
from ontology.libont import split
from ontology.builtins import print

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def Main():
    s = "@abcd@efg@hijklmn@op@q@rst@uvwxy@z@"
    res = split(s, '@')
    for i in res:
        print(i)

    VaasAssert(len(res) == 8)
    VaasAssert(res[0] == 'abcd')
    VaasAssert(res[1] == 'efg')
    VaasAssert(res[2] == 'hijklmn')
    VaasAssert(res[3] == 'op')
    VaasAssert(res[4] == 'q')
    VaasAssert(res[5] == 'rst')
    VaasAssert(res[6] == 'uvwxy')
    VaasAssert(res[7] == 'z')

    s = "111@222j#@38u23@sfsdka@jjasdj@"
    res = split(s, '@')
    for i in res:
        print(i)

    VaasAssert(len(res) == 5)
    VaasAssert(res[0] == '111')
    VaasAssert(res[1] == '222j#')
    VaasAssert(res[2] == '38u23')
    VaasAssert(res[3] == 'sfsdka')
    VaasAssert(res[4] == 'jjasdj_add')
