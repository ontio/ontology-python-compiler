OntCversion = '2.0.0'
from ontology.libont import int


def main():
    a = '-012345'
    b = int(a)
    assert(b == -12345)
    a = '12345'
    b = int(a)
    print(b)
    assert(b == 12345)

    a = '123456789000000000000'
    b = int(a, 10)
    print(b)
    assert(b == 123456789000000000000)

    a = 'abcdef123'
    b = int(a, 16)
    print(b)
    assert(b == 0xabcdef123)

    a = '-abcdef123'
    b = int(a, 16)
    print(b)
    assert(b == -0xabcdef123)

    a = '1234ab789ef543cd'
    b = int(a, 16)
    print(b)
    assert(b == 0x1234ab789ef543cd)

    a = '-1234ab789ef543cd'
    b = int(a, 16)
    print(b)
    assert(b == -0x1234ab789ef543cd)

    a = '145c69fdc3c648f0846e8c366e6578564f047f1c'
    b = int(a, 16)
    print(b)
    assert(b == 0x145c69fdc3c648f0846e8c366e6578564f047f1c)

    a = 'ABCdEf123'
    b = int(a, 16)
    print(b)
    assert(b == 0xaBcDEF123)

    a = '-AbDdEF123'
    b = int(a, 16)
    print(b)
    assert(b == -0xabddeF123)

    a = '1234Ab789eF543cd'
    b = int(a, 16)
    print(b)
    assert(b == 0x1234ab789ef543cd)

    a = '-1234aB789ef543cd'
    b = int(a, 16)
    print(b)
    assert(b == -0x1234ab789ef543cd)

    a = '145C69fdc3c648F0846e8C366e6578564f047F1C'
    b = int(a, 16)
    print(b)
    assert(b == 0x145c69fdc3c648f0846e8c366e6578564f047f1c)
