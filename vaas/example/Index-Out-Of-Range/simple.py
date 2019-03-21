from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Blockchain import GetHeight, GetHeader, GetBlock
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Header import *
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize, Log
from ontology.builtins import *
CONSTANT_LIST = [0, 1, 2, 3, 4]
TOKEN_ID_LIST = b'\x01\x02\x03\x04\x05\x06\x07\x08'
def Main(op,args):
    if len(args) <= 0:
        return False
    if op == "FuncReturn":
        FuncReturn(args)
        return True
    if op == "Constant":
        Constant(args)
        return True
    if op == "Bytearray":
        Bytearray(args)
        return True
    if op == "Hash":
        Hash(args)
        return True
    return False

def FuncReturn(args):
    __index = args[0]
    #list from func
    __index = GetList1(args)[__index]
    #list from Storage
    __index = GetList2()[__index]
    return


def Constant(args):
    #maybe index out of fange
    __index = CONSTANT_LIST[5]
    #maybe index out of fange
    return __index

def Bytearray(args):
    __index = args[0]
    #Wrong way of writing
    return TOKEN_ID_LIST[__index]

def Hash(args):

    height = GetHeight()
    header = GetHeader(height)
    a = abs(GetBlockHash(header)[10]) % 100#Wrong way of writing
    return a

def GetList1(args):
    return [1,2,3,4,5,6]

def GetList2():
    winers = []
    winersInfo = Get(GetContext(), "__winers__")
    if winersInfo:
        winers = Deserialize(winersInfo)
    return winers
