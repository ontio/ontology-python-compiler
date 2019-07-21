def Add(a, b):
    """
    Adds two numbers, throws on overflow.
    """
    c = a + b
    assert(c >= a)
    return c


def Sub(a, b):
    """
	Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
	:param a: operand a
	:param b: operand b
	:return: a - b if a - b > 0 or revert the transaction.
	"""
    assert(a>=b)
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
    assert(c / a == b)
    return c


def Div(a, b):
    """
    Integer division of two numbers, truncating the quotient.
    """
    assert(b > 0)
    c = a / b
    return c
