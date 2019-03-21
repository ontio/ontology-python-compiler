from ontology.builtins import *


from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import Notify, CheckWitness
from ontology.interop.System.Action import RegisterAction
from ontology.builtins import concat, ToScriptHash

from ontology.interop.Ontology.Runtime import AddressToBase58, Base58ToAddress

TransferEvent = RegisterAction("transfer", "from", "to", "amount")
ApprovalEvent = RegisterAction("approval", "owner", "spender", "amount")

ctx = GetContext()

FACTOR = 100000000
OWNER = Base58ToAddress("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p")
TOTAL_AMOUNT = 1000000000
BALANCE_PREFIX = bytearray(b'\x01')
APPROVE_PREFIX = b'\x02'
SUPPLY_KEY = 'TotalSupply'

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")


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
        Put(ctx, concat(BALANCE_PREFIX, OWNER), total)

        TransferEvent("", OWNER, total)
        return True

def balanceOf(account):
    return Get(ctx, concat(BALANCE_PREFIX, account))


def transfer(from_acct, to_acct, amount):
    if not CheckWitness(from_acct):
        return False

    fromKey = concat(BALANCE_PREFIX, from_acct)
    fromBalance = Get(ctx, fromKey)

    #添加判断条件
    if amount < 0:
        return False

    if amount > fromBalance:
        return False

    # 检测转账余额是否满足要求
    VaasAssert(amount >= 0)
    VaasAssert(fromBalance >= amount)

    if amount == fromBalance:
        Delete(ctx, fromKey)
    else:
        Put(ctx, fromKey, fromBalance - amount)

    toKey = concat(BALANCE_PREFIX, to_acct)
    toBalance = Get(ctx, toKey)
    Put(ctx, toKey, toBalance + amount)

    TransferEvent(from_acct, to_acct, amount)
    return True


def approve(owner, spender, amount):
    if not CheckWitness(owner):
        return False
    if amount > balanceOf(owner):
        return False

    key = concat(concat(APPROVE_PREFIX, owner), spender)
    Put(ctx, key, amount)

    ApprovalEvent(owner, spender, amount)
    return True


def transferFrom(spender, from_acct, to_acct, amount):
    if not CheckWitness(spender):
        return False

    fromKey = concat(BALANCE_PREFIX, from_acct)
    fromBalance = Get(ctx, fromKey)
    if amount > fromBalance:
        return False

    approveKey = concat(concat(APPROVE_PREFIX, from_acct), spender)
    approvedAmount = Get(ctx, approveKey)
    toKey = concat(BALANCE_PREFIX, to_acct)
    toBalance = Get(ctx, toKey)

    #添加判断条件
    if amount < 0:
        return False

    if amount > approvedAmount:
        return False


    # 检测转账余额是否满足要求
    VaasAssert(amount >= 0)
    VaasAssert(approvedAmount >= amount)


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

