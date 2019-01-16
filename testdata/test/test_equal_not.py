OntCversion = '2.0.0'


def Main():
    a = 3
    b = 2
    m = 12

    if not a == b:   # this currently works
        print("a not equal to b!!!")
        m = 21

    assert(m == 21)

    if a != b:
        print("numbers 2 and 3 are not equal")
        m = 82

    assert(m == 82)

    j = 'hello'
    k = 'hello'

    if j != k:
        print("string j is not equal to string k")
        m = 1

    else:
        m = 2
        print("string j is equal to string k")
    assert(m == 2)

    q = bytearray(b'\x10\x01\x80')
    q2 = bytearray(b'\x10\x10\x80')

    if q != q2:
        m = 3
        print("bytearrays m and m2 not equal")

    else:
        m = 4
        print("bytearrays m and m2 are equal")
    assert(m == 3)
