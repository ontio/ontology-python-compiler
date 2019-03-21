from ontology.interop.System.ExecutionEngine import GetCallingScriptHash, GetEntryScriptHash,GetExecutingScriptHash
from ontology.interop.System.Runtime import Notify
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.builtins import *
def Main(op,args):
    if op == "Mul":
        Mul(args[0],args[1])
        return True
    if op == "Add":
        Add(args[0],args[1])
        return True
    if op == "Left":
        Left(args[0],args[1])
        return True
    return False

def Mul(a,b):
    #Integer-Overflow-Occurred
    c = a * b
    Notify(c)
    return c

def Add(a,b):
    #Integer-Overflow-Occurred
    c = a + b
    Notify(c)
    return c

def Left(a,b):
    #Integer-Overflow-Occurred
    c = a << b
    Notify(c)
    return c

