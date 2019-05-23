OntCversion = '2.0.0'


def Main():
    map0 = {0: [9, 8, 7], 1: [6, 5, 4], 2: [3, 2, 1]}
    values = map0.values()
    assert(values[0][1] == 8)
    assert(values[1][1] == 5)
    assert(values[2][1] == 2)

    values[0][1] = 108 + 0
    values[1][1] = 105 + 0
    values[2][1] = 103 + 0
    assert(map0[0][1] == 108)
    assert(map0[1][1] == 105)
    assert(map0[2][1] == 103)
