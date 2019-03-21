from ontology.interop.System.Storage import Put, GetContext
from ontology.builtins import *
INIT = "_INIT_STATUS_"
def _concatkey(str1, str2):
    return concat(concat(str1, '_'), str2)

def init(_caller, _cut):
    ctx = GetContext()
    Put(ctx, INIT, 'TRUE')
    Put(ctx, _cut, 'TRUE')
    _cut = _concatkey(_caller, _cut)
    Put(ctx, _cut, 'TRUE')
    return True
def Main(operation, args):
    if operation == 'init':
        if len(args) != 2:
            return False
        _caller = args[0]
        _cut = args[1]
        return init(_caller, _cut)
