OntCversion = '2.0.0'

from ontology.interop.Ontology.Wasm import InvokeWasm
from ontology.interop.Ontology.Runtime import Base58ToAddress
from ontology.builtins import concat
from ontology.interop.System.Action import RegisterAction

InvokeEvent = RegisterAction("invoke", "addr", "asset", "amount")
wasmtrue = b'\x01'
contractHash = "APDgvJdxMTZSCRhXymyWvFtEycCdxYfC1e"

def Main(opertation,args):
    if opertation == "invoke":

        return invoke(args[0],args[1],args[2])
    if opertation == "query":
        return query(args[0],args[1])

    return False

def invoke(addr,assethash,amount):
    param = makeInvokeParam(addr,assethash,amount)
    wasmaddr = Base58ToAddress(contractHash)
    ret = InvokeWasm(wasmaddr,param)
    if ret == wasmtrue:
        InvokeEvent(addr,assethash,amount)

    return ret


def makeInvokeParam(addr,assethash,amount):
    magicversion = b'\x00'
    typebytearray = b'\x00'
    typestring = b'\x01'
    typeaddress = b'\x02'
    typebool = b'\x03'
    typeint = b'\x04'
    typeh256 = b'\x05'
    typelist = b'\x10'    

    #4 parameters of wasm supply call add method name
    lsize = b'\x04\x00\x00\x00'
    magicversion = concat(magicversion,typelist)
    magicversion = concat(magicversion,lsize)

    method = "supply"
    magicversion = concat(magicversion, typestring)
    magicversion = concat(magicversion, intTobytes(len(method),4))
    magicversion = concat(magicversion, method)

    magicversion = concat(magicversion, typeaddress)
    magicversion = concat(magicversion, addr)

    magicversion = concat(magicversion, typeaddress)
    magicversion = concat(magicversion, assethash)

    magicversion = concat(magicversion, typeint)
    magicversion = concat(magicversion, intTobytes(amount,16))

    return magicversion


def intTobytes(i,length):
    l = len(i)
    if l >= length:
        return i
    return concat(i,getXZeroes(length - l))


def getXZeroes(n):
    if n == 0:
        return b''
    else:
        tmp = b'\x00'
        for i in range (0 , n -1):
            tmp = concat(tmp,b'\x00')
        return tmp


def query(addr,assethash):
    contractHash = ""
    param = ""
    return InvokeWasm(contractHash,param)
    