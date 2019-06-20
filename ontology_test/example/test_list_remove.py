OntCversion = '2.0.0'


def Main():
    lst = [9, 8, 7, 6, 5]
    a = lst
    assert(len(a) == 5)
    print(len(a))
    for v in lst:
        print(v)

    lst.remove(0)
    lst.remove(0)
    lst.remove(0)

    assert(lst[0] == 6)
    assert(lst[1] == 5)

    lst = [0]
    assert(len(lst) == 1)
    lst.remove(0)
    assert(len(lst) == 0)

    print(len(a))
    assert(len(a) == 2)
    assert(a[0] == 6)
    print(a[0])
    print(a[1])
    assert(a[1] == 5)
