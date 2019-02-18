OntCversion = '2.0.0'
from ontology.builtins import print, range, len, keys, values

def Main():
    map0 = {'1':'11111', '2':'22222', '3':'33333', '4':'44444', '5':'55555'}

    keys = map0.keys()
    values = map0.values()

    assert(len(keys) == 5)
    assert(keys[0] == '1')
    assert(keys[0] == '2')
    assert(keys[0] == '3')
    assert(keys[0] == '4')
    assert(keys[0] == '5')

    assert(values[0] == '11111')
    assert(values[0] == '22222')
    assert(values[0] == '33333')
    assert(values[0] == '44444')
    assert(values[0] == '55555')
