from ontology.interop.System.ExecutionEngine import GetCallingScriptHash, GetEntryScriptHash,GetExecutingScriptHash
from ontology.interop.System.Runtime import Notify
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
from ontology.builtins import *

def Main(opration, args):
    if opration == "avoidContractCallAttack":
        guessNumber = args[0]
        return avoidContractCallAttack(guessNumber)
    if opration == "cannotAvoidContractCallAttack":
        guessNumber = args[0]
        return cannotAvoidContractCallAttack(guessNumber)
    return False
def VaasRequire(expr):
    if not expr:
        raise Exception("RequireError")
def avoidContractCallAttack(guessNumber):

    randomNumber = getRandomNumber()

    callerHash = GetCallingScriptHash()
    entryHash = GetEntryScriptHash()
    Notify(["randomNumber:", randomNumber, "guessNumber:", guessNumber])
    if callerHash != entryHash:
        Notify(["You are not allowed to invoke this method through contract!"])
        return False
    else:
        Notify(["You can implement what you need to do here!"])
        if guessNumber == randomNumber:
            Notify(["You have won the big prize!"])
            return True
        return False

def cannotAvoidContractCallAttack(guessNumber):

    randomNumber = getRandomNumber()

    callerHash = GetCallingScriptHash()
    #Developers are wrong
    entryHash = GetExecutingScriptHash()
    Notify(["randomNumber:", randomNumber, "guessNumber:", guessNumber])
    #Never equal
    VaasRequire(callerHash == entryHash)
    if guessNumber == randomNumber:
        Notify(["You have won the big prize!"])
        return True
    return False


def getRandomNumber():
    randomHash = GetCurrentBlockHash()
    randomNumber = abs(randomHash) % 100000000
    return randomNumber
