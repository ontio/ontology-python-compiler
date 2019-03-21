OntCversion = '2.0.0'
import ontology.builtins
a = 'hello'
b = 'world'
c = 'c'

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")
def Main():
    x = getdict()
    VaasAssert(x[a] == 1 + 1)
    VaasAssert(x[b] == 2 + 1)
    VaasAssert(x[c] == 3 + 1)
    print(x[a])
    print(x[b])
    print(x['c'])

def getdict():

    dic = {a:1, b:2, 'c':3}
    return dic
