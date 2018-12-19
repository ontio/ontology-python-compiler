OntCversion = '2.0.0'
from ontology.builtins import print, range, len

def Main():
    map0 = {'1':'11111', '2':'22222', '3':'33333', '4':'44444', '5':'55555'}
    str0 = '12345'
    for i in range(0,len(str0)):
        print(map0[str0[i]])

    assert(map0[str0[0]] == '11111')
    assert(map0[str0[1]] == '22222')
    assert(map0[str0[2]] == '33333')
    assert(map0[str0[3]] == '44444')
    assert(map0[str0[4]] == '55555')
