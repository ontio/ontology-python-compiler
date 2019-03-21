OntCversion = '2.0.0'
lst = [9, 8, 7, 6, 5]
l0 = [99 + 0, 98 + 0]
l1 = []


def Main():
    test(*l0, *lst)
    test0(11 + 0, 22 + 0, 33 + 0, 44 + 0, *l0)
    test1()
    test2(4, 5)
    test3(4, 5, 6)
    test4(4, 5, 6, 7)
    test5(*l1)
    l1.append(111)
    l1.append(222)
    test6(*l1)


def test(a=1, b=2, c=3, *arg):
    print(a)
    print(b)
    print(c)
    print(len(arg))
    VaasAssert(a == 99)
    VaasAssert(b == 98)
    VaasAssert(c == 9)
    VaasAssert(len(arg) == 4)
    VaasAssert(arg[0] == 8)
    VaasAssert(arg[1] == 7)
    VaasAssert(arg[2] == 6)
    VaasAssert(arg[3] == 5)


def test0(a=1, b=2, c=3, *arg):
    VaasAssert(a == 11)
    VaasAssert(b == 22)
    VaasAssert(c == 33)
    VaasAssert(len(arg) == len(l0) + 1)
    VaasAssert(arg[0] == 44)
    VaasAssert(arg[1] == l0[0])
    VaasAssert(arg[2] == l0[1])


def test1(a=1, b=2, c=3, *arg):
    VaasAssert(a == 1)
    VaasAssert(b == 2)
    VaasAssert(c == 3)
    VaasAssert(len(arg) == 0)


def test2(a=1, b=2, c=3, *arg):
    VaasAssert(a == 4)
    VaasAssert(b == 5)
    VaasAssert(c == 3)
    VaasAssert(len(arg) == 0)


def test3(a=1, b=2, c=3, *arg):
    VaasAssert(a == 4)
    VaasAssert(b == 5)
    VaasAssert(c == 6)
    VaasAssert(len(arg) == 0)


def test4(a=1, b=2, c=3, *arg):
    VaasAssert(a == 4)
    VaasAssert(b == 5)
    VaasAssert(c == 6)
    VaasAssert(len(arg) == 1)
    VaasAssert(arg[0] == 7)


def test5(a=1, b=2, c=3, *arg):
    VaasAssert(a == 1)
    VaasAssert(b == 2)
    VaasAssert(c == 3)
    VaasAssert(len(arg) == 0)


def test6(a, b=2, c=3, *arg):
    VaasAssert(a == 111)
    VaasAssert(b == 222)
    VaasAssert(c == 3 + 1) # here should bug.
    VaasAssert(len(arg) == 0)

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")
