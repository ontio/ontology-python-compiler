OntCversion = '2.0.0'


def Main():
    map0 = {'1': '11111', '2': '22222', '3': '33333', '4': '44444', '5': '55555', 0: 6666}
    keys = ['1', '2', '3', '4', '5', 0]
    values = ['11111', '22222', '33333', '44444', '55555', 66666]
    map1 = {keys[i]: values[j] for i in range(0, len(keys)) for j in range(0, len(values)) if j == i}
    map1keys = map1.keys()
    map1values = map1.values()
    assert(len(map1keys) == len(keys))
    assert(len(map1values) == len(values))
    for i in range(len(keys)):
        assert(map1keys[i] in keys)

    assert(map1keys[0] == keys[5])
    assert(map1keys[1] == keys[0])
    assert(map1keys[2] == keys[1])
    assert(map1keys[3] == keys[2])
    assert(map1keys[4] == keys[3])
    assert(map1keys[5] == keys[4])

    assert(map1values[0] == values[5])
    assert(map1values[1] == values[0])
    assert(map1values[2] == values[1])
    assert(map1values[3] == values[2])
    assert(map1values[4] == values[3])
    assert(map1values[5] == values[4])

    has = map0.has_key('3')
    if has:
        print("has key")
    else:
        assert(False)

    if map0.has_key(0):
        print("has key interger 0")
    else:
        assert(False)

    if map0.has_key('1'):
        print("has key interger 1")
    else:
        assert(False)

    for key in keys:
        assert(map0.has_key(keys[i]))
        assert(map1.has_key(keys[i]))
    assert(not map0.has_key(0xfffffff))
    assert(not map1.has_key(0xfffffff))

    assert(map0.has_key(''))
    assert(map0.has_key(""))
    assert(map0.has_key(None))
    assert(map0.has_key(False))
