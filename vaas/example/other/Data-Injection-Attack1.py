from ontology.interop.System.Storage import Put, GetContext
from ontology.builtins import *

def _concatkey(str1, str2):
    return concat(concat(str1, '_'), str2)

def morecall(a, b):
    _caller = _concatkey(a, b)
    _cut    = _concatkey(b, a)
    return init(_caller, _cut)

def init(_caller, _cut):
    ctx = GetContext()
    Put(ctx, _cut, 'TRUE')
    _cut = _concatkey(_caller, _cut)
    Put(ctx, _cut, 'TRUE')
    return True

def Main(operation, args):
    if operation == 'init':
        if len(args) != 2:
            return False
        _caller = args[0]
        #_cut = args[1]
        _cut = _concatkey(_caller, _caller)
        return morecall(_caller, _cut)
