from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize, Log
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash
from ontology.interop.System.Blockchain import GetHeight, GetHeader, GetBlock
from ontology.interop.System.Header import *
from ontology.interop.Ontology.Native import Invoke
from ontology.builtins import *
from ontology.interop.System.App import DynamicAppCall
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.Ontology.Runtime import GetCurrentBlockHash
############################################core start #################################################
def Main(opration, args):
    if opration == "hash":
        time = GetTime()
        height = GetHeight()
        header = GetHeader(height)
        a = args[0] / abs(GetBlockHash(header)) 
        a = a / abs(time)
        now_hash = GetBlockHash(header)
        a = a % abs(now_hash)
        return a
    return False
