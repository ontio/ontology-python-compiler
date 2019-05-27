OntCversion = '2.0.0'


def Require(condition):
    if not condition:
        Revert()
    return True


def Add(a, b):
    """
    Adds two numbers, throws on overflow.
    """
    c = a + b
    Require(c >= a)
    return c


def Sub(a, b):
    """
    Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    Require(a >= b)
    return a-b


def Mul(a, b):
    """
    Multiplies two numbers, throws on overflow.
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    if a == 0:
        return 0
    c = a * b
    tt = Require(c / a == b)
    return c


def Div(a, b):
    """
    Integer division of two numbers, truncating the quotient.
    """
    print(a)
    print(b)
    tt = Require(b > 0)
    c = a / b
    return c


def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    Exception("wrong")


def new_Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception("wrong")


# def Main(operation, args):
def Main():
    calculate1()
    print("calculate1 done")
    # testlistremove()
    print("testlistremove done")

    # return False


def calculate1():
    a = 1
    b = 2
    c = 3
    d = 6

    tmp1 = Div(d, c)
    tmp2 = Mul(b, tmp1)
    tmp3 = Sub(tmp2, b)
    tmp4 = Add(a, tmp3)
    throw_if_null(tmp4 == 3)

    # a + b * d /c - b, res is wrong, wrong when this function is invoked
    res = Add(a, Sub(Mul(b, Div(d, c)), b))
    res = Add(a, Sub(Mul(b, tmp1), b))
    throw_if_null(res == 3)


def testlistremove():  # do not support list remove. only support map
    m = {"name": "steven", "age": 31, "company": "onchain", "sex": "male"}
    m.remove("company")
    throw_if_null(m["name"] == "steven")
