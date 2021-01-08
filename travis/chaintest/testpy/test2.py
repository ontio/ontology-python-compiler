OntCversion = '2.0.0'
from ontology.interop.Ontology.Runtime import Base58ToAddress

player = Base58ToAddress('AbG3ZgFrMK6fqwXWR1WkQ1d1EYVunCwknu')

def Main(operation, args):
    if operation == 'ownerOf':
        if len(args) != 1:
            return False
        tokenID = args[0]
        return ownerOf(tokenID)
    elif operation == 'tokenID':
        if len(args) != 1:
            return False
        tokenID = args[0]
        return getTokenID(tokenID)
    elif operation == "testcase":
        return testcase()

    return False


def testcase():
    return '[[]]'


def ownerOf(tokenID):
    return player


def getTokenID(tokenID):
    return tokenID + 1
