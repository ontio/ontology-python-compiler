OntCversion = '2.0.0'
lst = [9, 8, 7, 6, 5]
l0 = [99 + 0, 98 + 0]
l1 = []
recrusive = "recrusive over"


def Main():
    test(*l0, *lst)
    test0(11 + 0, 22 + 0, 33 + 0, 44 + 0, *l0)
    test1()
    test2(makenum4(), makenum5())
    test3(makenum4(), 5, makenum6())
    test4(4, 5, makenum6(), 7)
    test5(*l1)
    l1.append(111)
    l1.append(222)
    test6(*l1)
    test7(*makearray())
    a = test8(*makearray())
    assert(a == recrusive)


def makenum4():
    return makenum2() + 2


def makenum3():
    return 3


def makenum2():
    return 2


def makenum5():
    return makenum3() + makenum2()


def makenum6():
    return makenum4() + makenum2()


def makearray():
    return [10 + 0, 20 + 0, 30 + 0, 40 + 0, 50 + 0]


def makearray2():
    return [10 + 0, 20 + 0]


def test(a=1, b=2, c=3, *arg):
    print(a)
    print(b)
    print(c)
    print(len(arg))
    assert(a == 99)
    assert(b == 98)
    assert(c == 9)
    assert(len(arg) == 4)
    assert(arg[0] == 8)
    assert(arg[1] == 7)
    assert(arg[2] == 6)
    assert(arg[3] == 5)


def test0(a=1, b=2, c=3, *arg):
    assert(a == 11)
    assert(b == 22)
    assert(c == 33)
    assert(len(arg) == len(l0) + 1)
    assert(arg[0] == 44)
    assert(arg[1] == l0[0])
    assert(arg[2] == l0[1])


def test1(a=1, b=2, c=3, *arg):
    assert(a == 1)
    assert(b == 2)
    assert(c == 3)
    assert(len(arg) == 0)


def test2(a=1, b=2, c=3, *arg):
    assert(a == 4)
    assert(b == 5)
    assert(c == 3)
    assert(len(arg) == 0)


def test3(a=1, b=2, c=3, *arg):
    assert(a == 4)
    assert(b == 5)
    assert(c == 6)
    assert(len(arg) == 0)


def test4(a=1, b=2, c=3, *arg):
    assert(a == 4)
    assert(b == 5)
    assert(c == 6)
    assert(len(arg) == 1)
    assert(arg[0] == 7)


def test5(a=1, b=2, c=3, *arg):
    assert(a == 1)
    assert(b == 2)
    assert(c == 3)
    assert(len(arg) == 0)


def test6(a, b=2, c=3, *arg):
    assert(a == 111)
    assert(b == 222)
    assert(c == 3)
    assert(len(arg) == 0)


def test7(*arg):
    assert(arg[0] == 10)
    assert(arg[1] == 20)
    assert(arg[2] == 30)
    assert(arg[3] == 40)
    assert(arg[4] == 50)
    assert(len(arg) == 5)


def test8(*arg):
    print(len(arg))
    if len(arg) != 0:
        arg.remove(0)
        return test8(*arg)
    else:
        return recrusive
