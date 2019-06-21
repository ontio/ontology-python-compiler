OntCversion = '2.0.0'


def Main():
    for i in test():
        if i == 4:
            break
    else:
        assert(False)

    x = 0
    for i in test():
        if i == 4:
            pass
        while i < 4:
            if i == 3:
                break
            i += 1
        else:
            x = 8

        if i < 4:
            assert(x == 0)
        else:
            assert(x == 8)
    else:
        x = 9

    assert(x == 9)

    x = 0
    for i in test():
        if i == 4:
            pass
        while i < 4:
            if i == 3:
                pass
            i += 1
        else:
            x = 8

        assert(x == 8)
    else:
        x = 9

    assert(x == 9)

    x = 0
    for i in test():
        if i == 4:
            pass
        while i < 4:
            if i == 3:
                pass
            i += 1
        else:
            x = 8

        assert(x == 8)
        break
    else:
        x = 9

    assert(x == 8)


def test():
    return [1, 2, 3, 4, 5]
