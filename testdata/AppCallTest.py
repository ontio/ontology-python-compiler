from ontology.interop.System.App import RegisterAppCall
from ontology.interop.Ontology.Runtime import Base58ToAddress

#CalculatorContract = RegisterAppCall('e9e17cd49e4a198e8825b775bd685a4d0818a757', 'operation', 'a', 'b')


def Main(operation, address, args):
    if operation == 'DCall':
        print("calling SmartContract_DynamicAppCall")
        arg_ll = args
        result = DCall(address,arg_ll)
        return result
    else:
        print("Error calling")
        return False

def DCall(address, a):
    operation = 'add'
    #address = Base58ToAddress('AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV')
    #address = bytearray('2f4361890957adea9402ea57189fcfe2d66e1c2d')
    #address = bytearray('2f4361890957adea9402ea57189fcfe2d66e1c2d')
    #address = bytearray(b'\x2d\x1c\x6e\xd6\xe2\xcf\x9f\x18\x57\xea\x02\x94\xea\xad\x57\x09\x89\x61\x43\x2f')
    print("before DynamicAppCall")
    print(address)
    result = DynamicAppCall(address, operation, a)
    print("the DynamicAppCall result")
    print(result)

    return result
