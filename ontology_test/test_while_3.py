OntCversion = '2.0.0'


def Main():
    i = 0
    while i < 10:
        if i == 8:
            break
        i += 1
    else:
        assert(False)

    assert(i == 8)

    i = 0
    x = 0
    while i < 10:
        if i == 8:
            pass
        i += 1
    else:
        x = 9

    assert(x == 9)
