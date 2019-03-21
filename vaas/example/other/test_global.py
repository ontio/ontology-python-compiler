OntCversion = '2.0.0'
a = 20
b = 30

def Main(args):
    VaasAssert(a == 20)
    VaasAssert(b == 30)

    c = args[0]
    modify_global(c)
    print(a)
    print(b)
    VaasAssert(a == 20)
    #VaasAssert(b == 20)

def modify_global(c):
    global a, b
    a = c
    b = c + 1

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")
