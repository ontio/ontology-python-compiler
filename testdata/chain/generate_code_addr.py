OntCversion = '2.0.0'
from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Storage import Put, GetContext, Get

KEY = "KEY"
NAME = "getaddr000"


def Main(operation, args):
    if operation == "codeaddr":
        if len(args) != 1:
            Notify("param error")
            return False
        return codeaddr(args[0])
    if operation == "put":
        return put()
    if operation == "get":
        return get()
    if operation == "name":
        return NAME


def codeaddr(code):
    """
    Note that the existing contract will be replaced by the newly migrated contract
    :param code: your avm code
    :return:
    """
    newaddr = None
    addr = hash160(code)
    print(len(addr))
    print(addr)

    for i in reversed(range(0,21)):
        print(i)
        if i < 1:
            break
        newaddr = concat(newaddr, addr[i-1:i])

    print(newaddr)

    return True


def get():
    return Get(GetContext(), KEY)


def put():
    Put(GetContext(), KEY, 897)
    return True
