OntCversion = '2.0.0'

def Main():
    l = [9,8,7,6,5]
    a = l
    assert(len(a) == 5)
    print(len(a))
    for v in l:
        print(v)

    l.remove(0)
    l.remove(0)
    l.remove(0)

    assert(l[0] == 6)
    assert(l[1] == 5)

    l = [0]
    assert(len(l) == 1)
    l.remove(0)
    assert(len(l) == 0)

    print(len(a))
    assert(len(a) == 2)
    assert(a[0] == 6)
    print(a[0])
    print(a[1])
    assert(a[1] == 5)
