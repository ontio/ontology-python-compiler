from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Log,Deserialize
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash
from ontology.interop.Ontology.Native import Invoke
from ontology.builtins import *
from ontology.interop.Ontology.Runtime import Base58ToAddress

adminAddress = Base58ToAddress("AY5ZBb7qtjdnp3ChweqMqcXdavCJVqXj7F")
ctx = GetContext()
selfAddr = GetExecutingScriptHash()
INITED = 'Initialized'
CUT = 'cut'
LAST_GEN0_SALE_PRICE = 'lastGen0SalePrices'
TOKEN_ID_TO_AUCTION_PREFIX = 'tokenIdToAuction'
GEN0_SALE_COUNT = 'gen0SaleCount'
CFO = 'cfo'
DRAGONADDRESS = 'dragonAddress'
VERSION = '0.0.2'

def Main(operation, args):
    if operation == 'init':
        if len(args) != 2:
            return False
        _caller = args[0]
        _cut = args[1]
        # There return False ,But The operation on the Storage has taken effect
        VaasAssert(not init(_caller, _cut) and Get(ctx, INITED) != "TRUE")#Hope that the initialization is not effective.
        return True
    if operation == 'createAuction':
        if len(args) != 6:
            return False
        _caller = args[0]
        _tokenId = args[1]
        _startingPrice = args[2]
        _endingPrice = args[3]
        _duration = args[4]
        _seller = args[5]
        return createAuction(_caller, _tokenId, _startingPrice, _endingPrice, _duration, _seller)
    if operation == 'cancelAuction':
        if len(args) != 3:
            return False
        _caller = args[0]
        _owner = args[1]
        _tokenId = args[2]
        return cancelAuction(_caller, _owner, _tokenId)
    if operation == 'bid':
        if len(args) != 3:
            return False
        _caller = args[0]
        _buyer = args[1]
        _tokenId = args[2]
        return bid(_caller, _buyer, _tokenId)
    if operation == 'getAuction':
        if len(args) != 1:
            return False
        _tokenId = args[0]
        return getAuction(_tokenId)
    if operation == 'getCurrentPrice':
        if len(args) != 1:
            return False
        _tokenId = args[0]
        return getCurrentPrice(_tokenId)
    if operation == 'cancelAuctionByAdmin':
        if len(args) != 2:
            return False
        _caller = args[0]
        _tokenId = args[1]
        return cancelAuctionByAdmin(_caller, _tokenId)
    if operation == 'withdrawBalance':
        if len(args) != 2:
            return False
        _caller = args[0]
        _amount = args[1]
        return withdrawBalance(_caller, _amount)
    if operation == 'averageGen0SalePrice':
        return averageGen0SalePrice()
    if operation == 'setOwnerCut':
        if len(args) != 2:
            return False
        _caller = args[0]
        _cut = args[1]
        return setOwnerCut(_caller, _cut)
    if operation == 'setGen0Price':
        if len(args) != 2:
            return False
        _caller = args[0]
        _price = args[1]
        return setGen0Price(_caller, _price)
    if operation == 'getSeller':
        if len(args) != 1:
            return False
        _tokenId = args[0]
        return getSeller(_tokenId)
    if operation == 'setCfo':
        if len(args) != 2:
            return False
        _caller = args[0]
        _cfo = args[1]
        return setCfo(_caller, _cfo)
    if operation == 'setDragonAddress':
        if len(args) != 2:
            return False
        _caller = args[0]
        _dragonAddress = args[1]
        return setDragonAddress(_caller, _dragonAddress)
    return False

# Constructor creates a reference to the NFT ownership contract
# and verifies the owner cut is in the valid range.
# only admin addres can call

def _getVersion():
    return VERSION

def init(_caller, _cut):
    Require(_onlyAdmin(_caller))
    if not Get(ctx, INITED):
        Put(ctx, INITED, 'TRUE')
        if _cut < 0 or _cut > 10000:
            return False
        Put(ctx, CUT, _cut)
    return True

# set dragon core address, only admin address can call


def setDragonAddress(_caller, _dragonAddress):
    Require(_onlyAdmin(_caller))
    Put(ctx, DRAGONADDRESS, _dragonAddress)
    return True

# Creates and begins a new auction. TODO olny dragon call
# only dragon core address can call


def createAuction(_caller, _tokenId, _startingPrice, _endingPrice, _duration, _seller):
    Require(_onlyDragonCore(_caller))
    Require(_startingPrice >= 0)
    Require(_endingPrice >= 0)
    Require(_duration >= 0)
    auction = {
        'seller': _seller,
        'startingPrice': _startingPrice,
        'endingPrice': _endingPrice,
        'duration': _duration,
        'startedAt': GetTime()
    }
    return _addAuction(_tokenId, auction)

# Cancels an auction that hasn't been won yet.
# only dragon core address can call


def cancelAuction(_caller, _owner, _tokenId):
    Require(_onlyDragonCore(_caller))
    auction = _saleInfo(_tokenId)
    Require(_isOnAuction(auction))
    seller = auction['seller']
    Require(seller == _owner)
    return _cancelAuction(_tokenId, seller)

# Bids on an open auction, completing the auction and transferring
# ownership of the NFT
# only dragon core address can call


def bid(_caller, _buyer, _tokenId):
    Require(_onlyDragonCore(_caller))
    return _bid(_buyer, _tokenId)

# set gen0 dragon price  only dragon address can call


def setGen0Price(_caller, _price):
    Require(_onlyDragonCore(_caller))
    gen0SaleCount = Get(ctx, GEN0_SALE_COUNT)
    if not gen0SaleCount:
        gen0SaleCount = 0
    # Track gen0 sale prices

    Put(ctx, _concatkey(LAST_GEN0_SALE_PRICE, gen0SaleCount % 5), _price)
    Put(ctx, GEN0_SALE_COUNT, Add(gen0SaleCount, 1))
    return True

# get the seller of dragon


def getSeller(_tokenId):
    auction = _saleInfo(_tokenId)
    Require(_isOnAuction(auction))
    return auction['seller']

# get the auction info of dragon


def getAuction(_tokenId):
    auction = _saleInfo(_tokenId)
    Require(_isOnAuction(auction))
    return Serialize([auction['seller'], auction['startingPrice'], auction['endingPrice'], auction['duration'], auction['startedAt']])

# Returns the current price of an auction.


def getCurrentPrice(_tokenId):
    auction = _saleInfo(_tokenId)
    Require(_isOnAuction(auction))
    return _currentPrice(auction)

# When the program comes out, bug turns the Dragon back to the seller.
# only admin address can call


def cancelAuctionByAdmin(_caller,  _tokenId):
    Require(_onlyAdmin(_caller))
    auction = _saleInfo(_tokenId)
    seller = auction['seller']
    Require(_isOnAuction(auction))
    return _cancelAuction(_tokenId, seller)

# cash to cfo address only the cfo address can call


def withdrawBalance(_caller, _amount):
    Require(_onlyCfo(_caller))
    if not _transferONGFromContract(_caller, _amount):
        return False
    return True

# gen0 sale prices


def averageGen0SalePrice():
    sum = 0
    prices = [0, 1, 2, 3, 4]
    for i in prices:
        price = Get(ctx, _concatkey(LAST_GEN0_SALE_PRICE, i))
        if not price:
            price = 0
        sum = Add(sum, price)
    return Div(sum, 5)

# set cut only the admin address can call


def setOwnerCut(_caller, _cut):
    Require(_onlyAdmin(_caller))
    Require(_cut >= 0)
    Require(_cut <= 10000)
    Put(ctx, CUT, _cut)

# set cfo address only admin address can call


def setCfo(_caller, _address):
    Require(_onlyAdmin(_caller))
    Put(ctx, CFO, _address)
    return True

# cancel the dragon sell


def _cancelAuction(_tokenId, _seller):
    _removeAuction(_tokenId)
    Notify(['AuctionCancelled', _seller, _tokenId])
    return True

# add the dragon to auction


def _addAuction(_tokenId, _auction):
    if _auction['duration'] < 60:
        return False
    Put(ctx, _concatkey(TOKEN_ID_TO_AUCTION_PREFIX, _tokenId), Serialize(_auction))
    Notify(['AuctionCreated', _tokenId, _auction['startingPrice'], _auction['endingPrice'], _auction['duration']])
    return True

# Computes the price and transfers winnings


def _bid(_buyer, _tokenId):
    auction = _saleInfo(_tokenId)
    Require(_isOnAuction(auction))
    price = _currentPrice(auction)
    seller = auction['seller']
    if price > 0:
        auctionFeerCut = _computeCut(price)
        sellerProceeds = Sub(price, auctionFeerCut)
        if not _transferONGFromContract(seller, sellerProceeds):
            return False
        else:
            _removeAuction(_tokenId)
    else:
        _removeAuction(_tokenId)
    Notify(['AuctionSuccessful', _tokenId, price, _buyer, seller])
    return True


# Computes owner's cut of a sale
def _computeCut(_price):
    ownerCut = Get(ctx, CUT)
    return Div(Mul(_price, ownerCut), 10000)

# Removes an auction from the list of open auctions.


def _removeAuction(_tokenId):
    Delete(ctx, _concatkey(TOKEN_ID_TO_AUCTION_PREFIX, _tokenId))

# Returns current price of an NFT on auction


def _currentPrice(_auction):
    secondsPassed = 0
    if GetTime() > _auction['startedAt']:
        secondsPassed = Sub(GetTime(), _auction['startedAt'])
    return _computeCurrentPrice(_auction['startingPrice'], _auction['endingPrice'], _auction['duration'], secondsPassed)

# Computes the current price of an auction
# Do not use safemath 

def _computeCurrentPrice(_startingPrice, _endingPrice, _duration, _secondsPassed):
    if _secondsPassed >= _duration:
        return _endingPrice
    else:
        #totalPriceChange = Sub(_endingPrice, _startingPrice)
        totalPriceChange = _endingPrice - _startingPrice
        currentPriceChange = Div(Mul(totalPriceChange, _secondsPassed), _duration)
        currentPrice = _startingPrice + currentPriceChange
        return currentPrice

# Returns true if the dragon is on auction.


def _isOnAuction(_auction):
    return _auction['startedAt'] > 0

# concat key


def _concatkey(str1, str2):
    return concat(concat(str1, '_'), str2)

# transfer ONT From current contract


def _transferONGFromContract(toacct, amount):
    """
    transfer ONT from contract
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    # ONT native contract address
    contractAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')

    param = state(selfAddr, toacct, amount)
    res = Invoke(0, contractAddress, 'transfer', [param])

    if res and res == b'\x01':
        return True
    else:
        return False

# get the auction info


def _saleInfo(_tokenId):
    saleData = Get(ctx, _concatkey(TOKEN_ID_TO_AUCTION_PREFIX, _tokenId))
    return Deserialize(saleData)


# get the dragon address
def _getDragonAddress():
    return Get(ctx, DRAGONADDRESS)

# get th cfo address


def _getCfoAddress():
    return Get(ctx, CFO)

# Check whether the address is dragon


def _onlyDragonCore(_caller):
    if not CheckWitness(_caller):
        return False
    if _caller != _getDragonAddress():
        return False
    return True

# Check whether the address is admin


def _onlyAdmin(_caller):
    if not CheckWitness(_caller):
        return False
    if _caller != adminAddress:
        return False
    return True

# Check whether the address is cfo


def _onlyCfo(_caller):
    if not CheckWitness(_caller):
        return False
    if _caller != _getCfoAddress():
        return False
    return True


#####################SafeCheck start################################

def Require(condition):
    """
        If condition is not satisfied, return false
        :param condition: required condition
        :return: True or false
        """
    if not condition:
        Revert()
    return True


def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)

def RequireWitness(witness):
    """
    Checks the transaction sender is equal to the witness. If not
    satisfying, revert the transaction.
    :param witness: required transaction sender
    :return: True if transaction sender or revert the transaction.
    """
    Require(CheckWitness(witness))
    return True

#####################SafeCheck end################################
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#####################SafeMath start################################
def Add(a, b):
    """
    Adds two numbers, throws on overflow.
    """
    c = a + b
    Require(c >= a)
    return c

def Sub(a, b):
    """
    Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    Require(a>=b)
    return a-b

def Mul(a, b):
    """
    Multiplies two numbers, throws on overflow.
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    if a == 0:
        return 0
    c = a * b
    Require(c / a == b)
    return c

def Div(a, b):
    """
    Integer division of two numbers, truncating the quotient.
    """
    Require(b > 0)
    c = a / b
    return c

def Pwr(a, b):
    """
    a to the power of b
    :param a the base
    :param b the power value
    :return a^b
    """
    c = 0
    if a == 0:
        c = 0
    elif b == 0:
        c = 1
    else:
        i = 0
        c = 1
        while i < b:
            c = Mul(c, a)
            i = i + 1
    return c

def Sqrt(a):
    """
    Return sqrt of a
    :param a:
    :return: sqrt(a)
    """
    c = Div(Add(a, 1), 2)
    b = a
    while(c < b):
        b = c
        c = Div(Add(Div(a, c), c), 2)
    return c

#####################SafeMath end##################################

#################### For VaaS tool function ######################
def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def VaasRequire(expr):
    if not expr:
        raise Exception("RequireError")
