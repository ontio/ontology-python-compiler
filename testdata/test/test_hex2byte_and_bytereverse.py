OntCversion = '2.0.0'
from ontology.builtins import len, print
from ontology.libont import hexstring2bytes, bytearray_reverse

def Main():
    a = "145c69fdc3c648f0846e8c366e6578564f047f1c"
    b = hexstring2bytes(a)
    assert(b == b'\x14\x5c\x69\xfd\xc3\xc6\x48\xf0\x84\x6e\x8c\x36\x6e\x65\x78\x56\x4f\x04\x7f\x1c')

    c = bytearray_reverse(b)
    assert(len(c) == 20)
    assert(c == b'\x1c\x7f\x04\x4f\x56\x78\x65\x6e\x36\x8c\x6e\x84\xf0\x48\xc6\xc3\xfd\x69\x5c\x14')

    a = 'aCe4702454c48f3EA430f6d52815318669B3818c'
    b = hexstring2bytes(a)
    assert(b == b'\xac\xe4\x70\x24\x54\xc4\x8f\x3e\xa4\x30\xf6\xd5\x28\x15\x31\x86\x69\xb3\x81\x8c')

    c = bytearray_reverse(b)
    assert(len(c) == 20)
    assert(c == b'\x8c\x81\xb3\x69\x86\x31\x15\x28\xd5\xf6\x30\xa4\x3e\x8f\xc4\x54\x24\x70\xe4\xac')

    a = '2d1c6ed6e2cF9f1857ea0294eAad57098961432f'
    b = hexstring2bytes(a)
    assert(b == b'\x2d\x1c\x6e\xd6\xe2\xcf\x9f\x18\x57\xea\x02\x94\xea\xad\x57\x09\x89\x61\x43\x2f')

    c = bytearray_reverse(b)
    assert(c == b'\x2f\x43\x61\x89\x09\x57\xad\xea\x94\x02\xea\x57\x18\x9f\xcf\xe2\xd6\x6e\x1c\x2d')

    a = 'a5813809fe3a573d43d83B1cb1ab88a9f69e2a07'
    b = hexstring2bytes(a)
    assert(b == b'\xa5\x81\x38\x09\xfe\x3a\x57\x3d\x43\xd8\x3b\x1c\xb1\xab\x88\xa9\xf6\x9e\x2a\x07')

    a = '3459e97812aDc6457a502a20ec1aa01deeef9724'
    b = hexstring2bytes(a)
    assert(b == b'\x34\x59\xe9\x78\x12\xad\xc6\x45\x7a\x50\x2a\x20\xec\x1a\xa0\x1d\xee\xef\x97\x24')

    a = 'ecb6502e1d7fec4b3d5cd9a0440a67b45061f847'
    b = hexstring2bytes(a)
    assert(b == b'\xec\xb6\x50\x2e\x1d\x7f\xec\x4b\x3d\x5c\xd9\xa0\x44\x0a\x67\xb4\x50\x61\xf8\x47')

    a = 'c3a9b151901993d8649af8e176f8064b63f67f34'
    b = hexstring2bytes(a)
    assert(b == b'\xc3\xa9\xb1\x51\x90\x19\x93\xd8\x64\x9a\xf8\xe1\x76\xf8\x06\x4b\x63\xf6\x7f\x34')

    a = '60c56b6a00527ac46a51527ac409746573746e616d65306a52527ac46a00c30f4d696772617465436f6e74726163749c6440006a51c3c0519e642b000b706172616d206572726f72681553797374656d2e52756e74696d652e4e6f7469667961006c7566616a51c300c365cf006c7566616a00c3037075749c6409006530006c7566616a00c3036765749c6409006567006c7566616a00c3046e616d659c6409006a52c36c756661006c756655c56b034b45596a00527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a00c30281035272681253797374656d2e53746f726167652e50757461516c756654c56b034b45596a00527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a00c37c681253797374656d2e53746f726167652e476574616c756656c56b6a00527ac46a00c351046e616d650776657273696f6e06617574686f7205656d61696c0b6465736372697074696f6e56795179587275517275557952795772755272755479537956727553727568194f6e746f6c6f67792e436f6e74726163742e4d69677261746561144d696772617465207375636365737366756c6c7951c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c7566'
    b = hexstring2bytes(a)
    assert(b == b'\x60\xc5\x6b\x6a\x00\x52\x7a\xc4\x6a\x51\x52\x7a\xc4\x09\x74\x65\x73\x74\x6e\x61\x6d\x65\x30\x6a\x52\x52\x7a\xc4\x6a\x00\xc3\x0f\x4d\x69\x67\x72\x61\x74\x65\x43\x6f\x6e\x74\x72\x61\x63\x74\x9c\x64\x40\x00\x6a\x51\xc3\xc0\x51\x9e\x64\x2b\x00\x0b\x70\x61\x72\x61\x6d\x20\x65\x72\x72\x6f\x72\x68\x15\x53\x79\x73\x74\x65\x6d\x2e\x52\x75\x6e\x74\x69\x6d\x65\x2e\x4e\x6f\x74\x69\x66\x79\x61\x00\x6c\x75\x66\x61\x6a\x51\xc3\x00\xc3\x65\xcf\x00\x6c\x75\x66\x61\x6a\x00\xc3\x03\x70\x75\x74\x9c\x64\x09\x00\x65\x30\x00\x6c\x75\x66\x61\x6a\x00\xc3\x03\x67\x65\x74\x9c\x64\x09\x00\x65\x67\x00\x6c\x75\x66\x61\x6a\x00\xc3\x04\x6e\x61\x6d\x65\x9c\x64\x09\x00\x6a\x52\xc3\x6c\x75\x66\x61\x00\x6c\x75\x66\x55\xc5\x6b\x03\x4b\x45\x59\x6a\x00\x52\x7a\xc4\x68\x19\x53\x79\x73\x74\x65\x6d\x2e\x53\x74\x6f\x72\x61\x67\x65\x2e\x47\x65\x74\x43\x6f\x6e\x74\x65\x78\x74\x61\x6a\x00\xc3\x02\x81\x03\x52\x72\x68\x12\x53\x79\x73\x74\x65\x6d\x2e\x53\x74\x6f\x72\x61\x67\x65\x2e\x50\x75\x74\x61\x51\x6c\x75\x66\x54\xc5\x6b\x03\x4b\x45\x59\x6a\x00\x52\x7a\xc4\x68\x19\x53\x79\x73\x74\x65\x6d\x2e\x53\x74\x6f\x72\x61\x67\x65\x2e\x47\x65\x74\x43\x6f\x6e\x74\x65\x78\x74\x61\x6a\x00\xc3\x7c\x68\x12\x53\x79\x73\x74\x65\x6d\x2e\x53\x74\x6f\x72\x61\x67\x65\x2e\x47\x65\x74\x61\x6c\x75\x66\x56\xc5\x6b\x6a\x00\x52\x7a\xc4\x6a\x00\xc3\x51\x04\x6e\x61\x6d\x65\x07\x76\x65\x72\x73\x69\x6f\x6e\x06\x61\x75\x74\x68\x6f\x72\x05\x65\x6d\x61\x69\x6c\x0b\x64\x65\x73\x63\x72\x69\x70\x74\x69\x6f\x6e\x56\x79\x51\x79\x58\x72\x75\x51\x72\x75\x55\x79\x52\x79\x57\x72\x75\x52\x72\x75\x54\x79\x53\x79\x56\x72\x75\x53\x72\x75\x68\x19\x4f\x6e\x74\x6f\x6c\x6f\x67\x79\x2e\x43\x6f\x6e\x74\x72\x61\x63\x74\x2e\x4d\x69\x67\x72\x61\x74\x65\x61\x14\x4d\x69\x67\x72\x61\x74\x65\x20\x73\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x51\xc1\x76\xc9\x68\x15\x53\x79\x73\x74\x65\x6d\x2e\x52\x75\x6e\x74\x69\x6d\x65\x2e\x4e\x6f\x74\x69\x66\x79\x61\x51\x6c\x75\x66')

    a = '00000000007fec4b3d5cd9a0440a670000000000'
    b = hexstring2bytes(a)
    print(b)
    assert(b == b'\x00\x00\x00\x00\x00\x7f\xec\x4b\x3d\x5c\xd9\xa0\x44\x0a\x67\x00\x00\x00\x00\x00')
    assert(len(b) == 20)
