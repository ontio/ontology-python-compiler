from ontology.interop.System.ExecutionEngine import GetCallingScriptHash, GetEntryScriptHash,GetExecutingScriptHash
from ontology.interop.System.Runtime import Notify
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.builtins import *
CONSTANT = "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
def Main(op):
    if op == "Hash":
        Hash()
        return True
    if op == "Constant":
        Constant()
        return True
    a = GetEntryScriptHash() + GetExecutingScriptHash()
    Notify(a)
    return False
def Hash():
    a = GetEntryScriptHash() + GetExecutingScriptHash()
    Notify(a)
    return False
def Constant():
    # Unsupported-Operator not`s Integer-Overflow-Occurred
    b = CONSTANT + "wwwwww"
    Notify(b)
    return
