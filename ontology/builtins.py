def substr(source, start_index, count):
    """
    substr(source, start_index, count) -> list object
    Return a subset of a string `source`, starting at `start_index` and
    of length `count`
    """
    pass


def take(source, count):
    """
    take(source, count) -> list object
    Return a subset of a string or list `source`, starting
    at index 0 and of length `count`
    """
    pass


def range(*arg):
    if len(arg) == 1:
        start = 0
        stop = arg[0]
        step = 1
    elif len(arg) == 2:
        start = arg[0]
        stop = arg[1]
        step = 1
        pass
    elif len(arg) == 3:
        start = arg[0]
        stop = arg[1]
        step = arg[2]
    else:
        assert(False)

    lst = []
    iteri = start
    while iteri < stop:
        lst.append(iteri)
        iteri += step

    return lst


def sha1(data):
    """
    :param data:
    """
    pass


def sha256(data):
    """
    :param data:
    """
    pass


def hash160(data):
    """
    :param data:
    """
    pass


def hash256(data):
    """
    :param data:
    """
    pass


def verify_signature(pubkey, signature, message):
    """
    :param pubkey:
    :param signature:
    :param message:
    """
    pass


def throw_if_null(item):
    pass


def breakpoint():
    """
    Adds a breakpoint to the debug map
    """
    pass


def print(msg):
    """
    :param msg:
    :no return
    """
    pass


def len(list_v):
    """
    :param list_v:
    """
    pass


def abs(data):
    pass


def min(x1, x2):
    pass


def max(x1, x2):
    pass


def concat(str1, str2):
    pass


def reversed(array):
    pass


def list(length):
    pass


def Exception(message):
    pass


def bytearray(Bytes):
    pass


def bytes(str0):
    pass


def state(*args):
    pass


def ord(char):
    pass


# attr func
def append(arg):
    pass


def remove(arg):
    pass


def reverse():
    pass
