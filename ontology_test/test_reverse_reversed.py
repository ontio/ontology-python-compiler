OntCversion = '2.0.0'


def main():
    a = [0, 1, 2, 3, 4]
    a.reverse()
    assert(a[0] == 4)
    assert(a[1] == 3)
    assert(a[2] == 2)
    assert(a[3] == 1)
    assert(a[4] == 0)

    print("print reverse")
    printlist(a)
    print("print revesed")
    printlist(reversed(a))

    assert(a[0] == 0)
    assert(a[1] == 1)
    assert(a[2] == 2)
    assert(a[3] == 3)
    assert(a[4] == 4)


def printlist(l):
    for i in l:
        print(i)
