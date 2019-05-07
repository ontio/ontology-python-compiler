OntCversion = '2.0.0'


def Main():
    test = 'x'
    if test == 0:
        a = 9
        a.remove(9)

    if test == 1:
        a = [1, 2, 3]
        a.remove(20)

    if test == 2:
        a = ''
        a.remove('')

    if test == 3:
        # map0 = {'1':'11111', '2':'22222', '3':'33333', '4':'44444', '5':'55555', 0:888}
        map0 = '999'
        x = map0.keys()

    if test == 4:
        map0 = 999
        x = map0.values()

    if test == 5:
        l0 = [9, 8, 7, 6, 5]
        l1 = [6, 7, 8, 9, 2]
        a = l0[l1]
