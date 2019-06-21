OntCversion = '2.0.0'
# tested


def Main():
    a = 9
    b = 7

    c = a & b
    print('&')
    print(c)
    assert(c == 1)

    c = a | b
    print('|')
    print(c)
    assert(c == 15)

    c = a >> 2
    print('>>')
    print(c)
    assert(c == 2)

    c = b >> 1
    print('>>')
    print(c)
    assert(c == 3)

    c = b << 1
    print('<<')
    print(c)
    assert(c == 14)

    c = a ^ b
    print('^')
    print(c)
    assert(c == 14)

    c = a % b
    print('%')
    print(c)
    assert(c == 2)

    # c = - a // 2
    # FloorDiv
    # print('//')
    # print(c)
    # assert(c == -5)

    c = a / 2
    print('/')
    print(c)
    assert(c == 4)

    c = ~a
    print('~')
    print(c)
    assert(c == -10)
