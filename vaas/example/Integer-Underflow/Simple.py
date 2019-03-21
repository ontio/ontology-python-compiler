from ontology.interop.System.ExecutionEngine import GetCallingScriptHash, GetEntryScriptHash,GetExecutingScriptHash
from ontology.interop.System.Runtime import Notify
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.builtins import *
def Main(op,args):
    if op == "Sub":
        Sub(args[0],args[1])
        return True
    if op == "SafeSub":
        SafeSub(args[0],args[1])
        return True
    return False


def Sub(a,b):
    #Integer-Overflow-Occurred
    c = a - b
    Notify(c)
    return c

def SafeSub(a,b):
    if a > b:
        #Even if the size relationship is constrained, it is still possible Integer-Overflow-Occurred
        c = a - b
        Notify(c)
        return c
    else:
        raise Exception(0xF1F1F2F2F3F3F4F4)

