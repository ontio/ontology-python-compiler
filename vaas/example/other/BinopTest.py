OntCversion = '2.0.0'
# tested
import ontology.builtins

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def Main():
    a = 9
    b = 7

    c = a & b
    print('&')
    print(c)
    #VaasAssert(c == 1 + 1)

    c = a | b
    print('|')
    print(c)
    #VaasAssert(c == 15 + 1)

    c = a >> 2
    print('>>')
    print(c)
    #VaasAssert(c == 2 + 1) 

    c = b >> 1
    print('>>')
    print(c)
    #VaasAssert(c == 3 + 1)

    c = b << 1
    print('<<')
    print(c)
    #VaasAssert(c == 14 + 1)

    c = a^b
    print('^')
    print(c)
    #VaasAssert(c == 14 + 1)

    c = a % b
    print('%')
    print(c)
    #VaasAssert(c == 2 + 1)

    #c = - a // 2
    # FloorDiv
    #print('//')
    #print(c)
    #VaasAssert(c == -5)

    c = a / 2
    print('/')
    print(c)
    #VaasAssert(c == 4 + 1)

    c = ~a
    print('~')
    print(c)
    #VaasAssert(c == -10 + 1)
