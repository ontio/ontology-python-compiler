from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize, Log
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash,GetCallingScriptHash,GetEntryScriptHash
from ontology.interop.System.Blockchain import GetHeight, GetHeader, GetBlock
from ontology.interop.System.Header import *
from ontology.interop.Ontology.Native import Invoke
from ontology.builtins import *
from ontology.interop.System.App import DynamicAppCall
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
############################################core start #################################################

def Main(opration, args):
    if opration == "getLuckyNamber":
        _caller = args[0]
        _number = args[1]
        winers =getWiners()
        #len(winers) Maybe 0
        if _number % len(winers) == getRandomNumber():
            winers.append(_caller)
            Put(GetContext(),"__winers__",Serialize(winers))
        return True
    return False
def getWiners():
    winers = []
    winersInfo = Get(GetContext(), "__winers__")
    if winersInfo:
        return Deserialize(winersInfo)
    return winers
def getRandomNumber():
    callerHash = GetCallingScriptHash()
    entryHash = GetEntryScriptHash()
    Require(callerHash == entryHash)
    randomHash = GetCurrentBlockHash()
    winers =getWiners()
    randomNumber = abs(randomHash) % len(winers)
    return randomNumber
        

def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)

def Require(condition):
    """
        If condition is not satisfied, return false
        :param condition: required condition
        :return: True or false
        """
    if not condition:
        Revert()
    return True

