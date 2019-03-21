from ontology.interop.System.Storage import *
from ontology.builtins import *
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Log
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash, GetCallingScriptHash, GetEntryScriptHash
from ontology.interop.Ontology.Native import Invoke
TOKEN_NAME = 'Muzika Token'
TOKEN_SYMBOL = 'MZK'

ContractAddress = GetExecutingScriptHash()
ONGAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
################################################################################
# TOKEN INFO CONSTANTS

DEPLOYER = bytearray(
    b'\x15\xd7\x1d\x26\xc7\x22\x84\xc2\xf6\x46'
    b'\xff\x4f\xde\xfd\xae\xdc\x65\xdc\xfe\x8d'
)
INIT_SUPPLY = 1000000000
TOKEN_DECIMALS = 8
FACTOR = 100000000
################################################################################
# STORAGE KEY CONSTANT
# Belows are storage key for some variable token information.

PRICE = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
OWNER_KEY = '___OWNER'
MZK_SUPPLY_KEY = '__SUPPLY'


################################################################################
# STORAGE KEY PREFIX
# Since all data are stored in the key-value storage, the data need to be
# classified by key prefix. All key prefixes length must be the same.

OWN_PREFIX = '_____own'
ALLOWANCE_PREFIX = '___allow'


################################################################################
#

def Main(operation, args):
    if operation == 'buyToken':
        if len(args) == 2:
            return buyToken(args[0],args[1])
    return False

def transferONGToContact(fromAcct, amount):
    param = state(fromAcct, ContractAddress, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        return True
    else:
        return False
#购买Token
def buyToken(fromAcct,tokens):
    if not CheckWitness(fromAcct):
        return False
    # Maybe Integer-Overflow
    amount = tokens * PRICE
    print(amount)
    if transferONGToContact(fromAcct,amount):
        Put(GetContext(), concat(OWN_PREFIX, fromAcct),amount)
        return True
    return False