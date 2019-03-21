"""
Lottery Game
Support game player for 2,5,10 and 20
every ticket needs 1 ONG
when attendee count reach max of this game round,
game will generate a random number and send all the ONGs to the selected attendee
This round Game end
"""
from ontology.interop.System.Storage import *
from ontology.interop.System.ExecutionEngine import *
from ontology.interop.System.Runtime import *
from ontology.interop.System.Blockchain import GetHeight, GetHeader, GetBlock
from ontology.interop.System.Header import GetBlockHash
from ontology.interop.Ontology.Native import *
from ontology.builtins import state, sha256, concat
from ontology.builtins import *
contractAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
ctx = GetContext()
selfAddr = GetExecutingScriptHash()

# storage profix
statusKey = "Status"
roundKey = "Round"
attendCntKey = "AttendCnt"
attendeeKey = "Attendee"
indexKey = "Index"
winnerKey = "Winner"
paidKey = "Paid"
starttimeKey = "Starttime"
status_running = "RUNNING"
status_end = "END"
#ong decimal
ongPerTicket = 1000000000
txFee = 16200000
createFee = 3300000

#after 600 seconds, the game can be ended manually
timeOut = 600

def Main(operation, args):
    if operation == 'attend':
        account = args[0]
        ticketsCount = args[1]
        if ticketsCount != 2 and ticketsCount != 5 and ticketsCount != 10 and ticketsCount != 20:
            return False
        return attend(account, ticketsCount)
    if operation == 'queryWinner':
        count = args[0]
        round = args[1]
        return queryWinner(count, round)
    if operation == 'queryAttendeeCount':
        count = args[0]
        round = args[1]
        return queryAttendeeCount(count, round)
    if operation == 'queryCurrentRound':
        count = args[0]
        return queryCurrentRound(count)
    if operation == 'endGame':
        account = args[0]
        count = args[1]
        currentRound = Get(ctx, concatKey(roundKey, count))
        if not currentRound:
            return False
        status = Get(ctx, concatKey(statusKey, concatKey(count, currentRound)))
        if status == status_end:
            return False
        starttime = Get(ctx, concatKey(starttimeKey, concatKey(count, currentRound)))
        if getTimestamp() - starttime > timeOut:
            endGame(account, count)
            return True
        Notify('not timeout yet')
        return False
    #if operation == 'getRandom':
    #    return getRandom()
    if operation == 'getName':
        return getName()

    return False


def attend(acct, count):
    if CheckWitness(acct):
        key = concatKey(roundKey, count)
        currentRound = Get(ctx, key)
        # initial a game
        if not currentRound:
            if transONG(acct, selfAddr, ongPerTicket):
                startNewRound(1, count, acct)
                Notify(["For the first time, initiate Game Round_", count])
                return True
            else:
                Notify("transfer ong failed!")
                return False
        else:
            newKey = concatKey(count, currentRound)
            status = Get(ctx, concatKey(statusKey, newKey))
            # the game is still running
            if status == status_running:
                attendedCount = Get(ctx, concatKey(attendCntKey, newKey))
                newCount = attendedCount + 1
                if transONG(acct, selfAddr, ongPerTicket):
                    # add attend count
                    Put(ctx, concatKey(attendCntKey, newKey), newCount)
                    # get attendee tickets
                    tickets = Get(ctx, concatKey(concatKey(attendeeKey, newKey), acct))
                    if not tickets:
                        # record attendee
                        Put(ctx, concatKey(concatKey(attendeeKey, newKey), acct), 1)
                    else:
                        Put(ctx, concatKey(concatKey(attendeeKey, newKey), acct), tickets + 1)

                    # record attendee index
                    Put(ctx, concatKey(concatKey(indexKey, newKey), newCount), acct)
                else:
                    Notify("transfer ong failed!")
                    return False

                if newCount == count:
                    return endGame(acct, count)
                else:
                    return True
            else:
                # this round is end,should start next round
                if transONG(acct, selfAddr, ongPerTicket):
                    startNewRound(currentRound + 1, count, acct)
                    return True
                else:
                    Notify("transfer ong failed!")
                    return False
    else:
        Notify("CheckWiteness failed!")
        return False


def queryWinner(count, round):
    return Get(ctx, concatKey(concatKey(winnerKey, count), round))


def queryAttendeeCount(count, round):
    return Get(ctx, concatKey(concatKey(attendCntKey, count), round))


def queryCurrentRound(count):
    return Get(ctx, concatKey(roundKey, count))


def endGame(account, count):
    """
    end a game round
    :param count:
    :return:
    """
    key = concatKey(roundKey, count)
    currentRound = Get(ctx, key)
    newkey = concatKey(count, currentRound)
    paid = Get(ctx, concatKey(paidKey, newkey))

    if not paid:
        attendcount = Get(ctx, concatKey(attendCntKey, newkey))
        # currentTime = getTimestamp()
        idx = abs(getRandom()) % attendcount + 1
        #Log(idx)
        attendee = Get(ctx, concatKey(concatKey(indexKey, newkey), idx))

        # winner will pay for the tx fee
        if transONGFromContract(attendee, attendcount * ongPerTicket - txFee - createFee):
            # record the winner of this round
            Put(ctx, concatKey(winnerKey, newkey), attendee)
            # mark this round game end
            Put(ctx, concatKey(statusKey, newkey), status_end)
            # mark ong paid
            Put(ctx, concatKey(paidKey, newkey), 'YES')
        else:
            Notify('transfer ONG failed!')
            return False

        # refund txFee to last attendee
        if transONGFromContract(account, txFee):
            # refund createFee to first attendee
            firstAttendee = Get(ctx, concatKey(concatKey(indexKey, newkey), 1))
            if transONGFromContract(firstAttendee, createFee):
                return True
            Notify('transfer create ONG failed!')
            return False
        else:
            Notify('transfer tx ONG failed!')
            return False

    else:
        return True


def transONG(fromacct, toacct, amount):
    """
     transfer ONG
     :param fromacct:
     :param toacct:
     :param amount:
     :return:
     """
    if CheckWitness(fromacct):

        param = makeState(fromacct, toacct, amount)
        res = Invoke(0, contractAddress, 'transfer', [param])
        Notify(res)

        if res and res == b'\x01':
            Notify('transfer succeed')
            return True
        else:
            Notify('transfer failed')

            return False

    else:
        Notify('checkWitness failed')
        return False


def startNewRound(roundNum, count, acct):
    """
    start a new game round
    :param roundNum:
    :param count:
    :param acct:
    :return:
    """

    key = concatKey(count, roundNum)

    # record current round
    Put(ctx, concatKey(roundKey, count), roundNum)
    # add attend count
    Put(ctx, concatKey(attendCntKey, key), 1)
    # record attendee ticket
    Put(ctx, concatKey(concatKey(attendeeKey, key), acct), 1)
    # record attendee index
    Put(ctx, concatKey(concatKey(indexKey, key), 1), acct)
    # record status
    Put(ctx, concatKey(statusKey, key), status_running)
    # record starttime
    Put(ctx, concatKey(starttimeKey, key), getTimestamp())


def transONGFromContract(toacct, amount):
    """
     transfer ONG from contract
     :param toacct:
     :param amount:
     :return:
     """

    param = makeState(selfAddr, toacct, amount)
    res = Invoke(1, contractAddress, 'transfer', [param])
    Notify(res)

    if res and res == b'\x01':
        Notify('transfer succeed')
        return True
    else:
        Notify('transfer failed')

        return False


def concatKey(str1,str2):
    return concat(concat(str1, '_'), str2)


def makeState(fromacct, toacct, amount):
    """
    make a tranfer state parameter
    currently due to the compiler problem,
    must be created as this format
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    return state(fromacct, toacct, amount)


def getTimestamp():
    """
    get the header timestamp
    :return:
    """
    timestamp = GetTime()
    return timestamp


def getRandom():
    time = GetTime()
    height = GetHeight()
    header = GetHeader(height)
    # return sha256(abs(GetBlockHash(header)) % time)
    tmp = sha256(abs(GetBlockHash(header)) % time)
    Notify(["getRandom", tmp])
    return tmp

def getName():
    return "lotteryGame"
