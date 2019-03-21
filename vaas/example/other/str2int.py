OntCversion = '2.0.0'
from ontology.builtins import print, len
from ontology.libont import int, elt_in

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")
def main():
    a = '-012345'
    b = int(a, 10)
    VaasAssert(b == -12345)
    a = '12345'
    b = int(a, 10)
    print(b)
    VaasAssert(b == 12345)

    a = '123456789000000000000'
    b = int(a, 10)
    print(b)
    VaasAssert(b == 123456789000000000000)

    a = 'abcdef123'
    b = int(a, 16)
    print(b)
    VaasAssert(b == 0xabcdef123)

    a = '-abcdef123'
    b = int(a, 16)
    print(b)
    VaasAssert(b == -0xabcdef123)

    a = '1234ab789ef543cd'
    b = int(a, 16)
    print(b)
    VaasAssert(b == 0x1234ab789ef543cd)

    a = '-1234ab789ef543cd'
    b = int(a, 16)
    print(b)
    VaasAssert(b == -0x1234ab789ef543cd)

    a = '145c69fdc3c648f0846e8c366e6578564f047f1c'
    b = int(a, 16)
    print(b)
    VaasAssert(b == 0x145c69fdc3c648f0846e8c366e6578564f047f1c)

    a = 'ABCdEf123'
    b = int(a, 16)
    print(b)
    VaasAssert(b == 0xaBcDEF123)

    a = '-AbDdEF123'
    b = int(a, 16)
    print(b)
    VaasAssert(b == -0xabddeF123)

    a = '1234Ab789eF543cd'
    b = int(a, 16)
    print(b)
    VaasAssert(b == 0x1234ab789ef543cd)

    a = '-1234aB789ef543cd'
    b = int(a, 16)
    print(b)
    VaasAssert(b == -0x1234ab789ef543cd)

    a = '145C69fdc3c648F0846e8C366e6578564f047F1C'
    b = int(a, 16)
    print(b)
    VaasAssert(b == 0x145c69fdc3c648f0846e8c366e6578564f047f1c + 1)
