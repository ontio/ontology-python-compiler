OntCversion = '2.0.0'
from ontology.interop.System.App import RegisterAppCall, DynamicAppCall
from ontology.interop.Ontology.Runtime import Base58ToAddress
import ontology.builtins
from ontology.libont import elt_in

#this address is add_test.py
CalculatorContract = RegisterAppCall('145c69fdc3c648f0846e8c366e6578564f047f1c', 'operation', 'args')

NAME = "AppCall000"

def Main(operation, args):
    print("appcall in")
    if elt_in(['add', 'sub', 'mul'], operation):
        print("StaticAppCall")
        return CalculatorContract(operation, args)
    elif operation[0:1] == 'd':
        address = bytearray(b'\x1c\x7f\x04\x4f\x56\x78\x65\x6e\x36\x8c\x6e\x84\xf0\x48\xc6\xc3\xfd\x69\x5c\x14')
        print("DynamicAppCall")
        operation = operation[1:]
        print(operation)
        return DynamicAppCall(address, operation, args)
    elif operation == 'name':
        print("getname")
        return NAME
