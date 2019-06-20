OntCversion = '2.0.0'


def Main():
    test(10, 2)
    res = test(2, 2)
    print(res)
    res = test(1, 2)
    print(res)
    res = test(2, 10)
    print(res)


def test(a, b):
    x = 50
    if a + 1 == b:
        printall(a - b, a + b, a*b, a/b)
    elif a + 2 == b:
        c = a + b
        print(c)
    elif a + 3 == b:
        print("333")
    elif a + 4 == b:
        print("444")
    elif a + 5 == b:
        print("555")
    elif a + 6 == b:
        print("666")
    elif a + 7 == b:
        print("777")
    elif a + 8 == b == 10 <= 10 >= 10 < 100 > 50 <= x:
        print("888")
        a = 20
        b = 30
    else:
        print("nagtive")

    print("hello, myworld")
    return a + b


def printall(a, b, c, d):
    print(a)
    print(b)
    print(c)
    print(d)
    return 2
