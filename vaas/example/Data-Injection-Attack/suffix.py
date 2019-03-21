"""
An Example of OEP-4
"""
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import Notify, CheckWitness
from ontology.interop.System.Action import RegisterAction
from ontology.builtins import concat
from ontology.builtins import *
TransferEvent = RegisterAction("transfer", "from", "to", "amount")
ApprovalEvent = RegisterAction("approval", "owner", "spender", "amount")
from ontology.interop.Ontology.Runtime import Base58ToAddress
ctx = GetContext()

FACTOR = 100000000
OWNER = Base58ToAddress("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p")
TOTAL_AMOUNT = 1000000000
BALANCE_PREFIX = "_BALANCE__"
APPROVE_PREFIX = "_APPROVE__"
SUPPLY_KEY = 'TotalSupply'

def Main(operation, args):
    if operation == 'init':
        return init()
    if operation == 'balanceOf':
        if len(args) != 1:
            return False
        acct = args[0]
        return balanceOf(acct)
    if operation == 'transfer':
        if len(args) != 3:
            return False
        else:
            from_acct = args[0]
            to_acct = args[1]
            amount = args[2]
            return transfer(from_acct, to_acct, amount)
    if operation == 'transferFrom':
        if len(args) != 4:
            return False
        spender = args[0]
        from_acct = args[1]
        to_acct = args[2]
        amount = args[3]
        return transferFrom(spender, from_acct, to_acct, amount)
    if operation == 'approve':
        if len(args) != 3:
            return False
        owner = args[0]
        spender = args[1]
        amount = args[2]
        return approve(owner, spender, amount)
    if operation == 'allowance':
        if len(args) != 2:
            return False
        owner = args[0]
        spender = args[1]
        return allowance(owner, spender)

def init():
    if Get(ctx, SUPPLY_KEY):
        Notify("Already initialized!")
        return False
    else:
        total = TOTAL_AMOUNT * FACTOR
        Put(ctx, SUPPLY_KEY, total)
        Put(ctx, concat(BALANCE_PREFIX,OWNER), total)

        TransferEvent("", OWNER, total)
        return True

def balanceOf(account):
    return Get(ctx, concat(BALANCE_PREFIX,account))


def transfer(from_acct, to_acct, amount):
    if not CheckWitness(from_acct):
        return False

    Require(amount > 0)
    fromKey = concat(BALANCE_PREFIX,from_acct)
    fromBalance = Get(ctx, fromKey)
    if amount > fromBalance:
        return False
    if amount == fromBalance:
        Delete(ctx, fromKey)
    else:
        Put(ctx, fromKey, fromBalance - amount)

    toKey = concat(BALANCE_PREFIX,to_acct)
    toBalance = Get(ctx, toKey)
    Put(ctx, toKey, toBalance + amount)

    TransferEvent(from_acct, to_acct, amount)
    return True


def approve(owner, spender, amount):
    if not CheckWitness(owner):
        return False
    key = concat(concat(owner,APPROVE_PREFIX), spender)
    Put(ctx, key, amount)

    ApprovalEvent(owner, spender, amount)
    return True


def transferFrom(spender, from_acct, to_acct, amount):
    if not CheckWitness(spender):
        return False
    Require(amount > 0)
    fromKey = concat(BALANCE_PREFIX,from_acct)
    fromBalance = Get(ctx, fromKey)
    if amount > fromBalance:
        return False

    approveKey = concat(concat(from_acct,APPROVE_PREFIX), spender)
    approvedAmount = Get(ctx, approveKey)
    if amount > approvedAmount:
        return False
    toKey = concat(to_acct,BALANCE_PREFIX)
    toBalance = Get(ctx, toKey)
    if amount == approvedAmount:
        Delete(ctx, approveKey)
        Put(ctx, fromKey, fromBalance - amount)
    else:
        Put(ctx, approveKey, approvedAmount - amount)
        Put(ctx, fromKey, fromBalance - amount)

    Put(ctx, toKey, toBalance + amount)
    TransferEvent(from_acct, to_acct, amount)

    return True


def allowance(owner, spender):
    key = concat(concat(APPROVE_PREFIX, owner), spender)
    return Get(ctx, key)

def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)


"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/SafeCheck.py
"""
def Require(condition):
    """
	If condition is not satisfied, return false
	:param condition: required condition
	:return: True or false
	"""
    if not condition:
        Revert()
    return True
