from ontology.interop.System.App import RegisterAppCall, DynamicAppCall
from ontology.libont import elt_in, hexstring2bytes, bytearray_reverse

OntCversion = '2.0.0'

# this address is add_test.py
CalculatorContract = RegisterAppCall('1a6f62cc0ff3d9ae32b0b924aeda2056a9fdfccb', 'operation', 'args')

NAME = "AppCall000"


def Main(operation, args):
    print("appcall in")
    if elt_in(['add', 'sub', 'mul'], operation):
        print("StaticAppCall")
        return CalculatorContract(operation, args)
    elif operation[0:1] == 'd':
        address = bytearray_reverse(hexstring2bytes('1a6f62cc0ff3d9ae32b0b924aeda2056a9fdfccb'))
        print("DynamicAppCall")
        operation = operation[1:]
        print(operation)
        return DynamicAppCall(address, operation, args)
    elif operation == 'name':
        print("getname")
        return NAME
