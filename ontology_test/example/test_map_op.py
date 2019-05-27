OntCversion = '2.0.0'


def Main():
    map0 = {'1': '11111', '2': '22222', '3': '33333', '4': '44444', '5': '55555', 0: 888}

    keys = map0.keys()

    if len(keys) == 0:
        print("xxxxxxxxxx")

    for i in keys:
        print(i)

    assert(len(keys) == 6)
    assert(keys[0] == 0)
    assert(keys[1] == '1')
    assert(keys[2] == '2')
    assert(keys[3] == '3')
    assert(keys[4] == '4')
    assert(keys[5] == '5')

    values = map0.values()

    for i in values:
        print(i)

    assert(values[0] == 888)
    assert(values[1] == '11111')
    assert(values[2] == '22222')
    assert(values[3] == '33333')
    assert(values[4] == '44444')
    assert(values[5] == '55555')

    # key '', 0 are the same. due to the ontology blockchain
    map1 = {'': "blank", 0: "00000"}

    keys1 = map1.keys()
    values1 = map1.values()
    assert(len(keys1) == 1)
    assert(len(values1) == 1)
    assert('' == 0)
    assert(values1[keys1[0]] == "00000")
