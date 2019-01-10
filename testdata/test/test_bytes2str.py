OntCversion = '2.0.0'
from ontology.libont import bytes2hexstring, hexstring2bytes

def Main():
    a = b'\x01\xef\xab\xcd\x23\x45\xff\xfe\xef\xed\xdc\xba\xa9\xf9\xe9\x9a\x9f\x9e\x99\x8e\x00\x01\x02\x10\x11\x1a\xa1\xff\xf1\xf0\xf0'
    res = bytes2hexstring(a, 1)
    assert(res == '01EFABCD2345FFFEEFEDDCBAA9F9E99A9F9E998E00010210111AA1FFF1F0F0')
    res_b = hexstring2bytes(res)
    assert(res_b == a)

    res = bytes2hexstring(a, 0)
    assert(res == '01efabcd2345fffeefeddcbaa9f9e99a9f9e998e00010210111aa1fff1f0f0')
    res_b = hexstring2bytes(res)
    assert(res_b == a)

    a = b'\x1c\x7f\x04\x4f\x56\x78\x65\x6e\x36\x8c\x6e\x84\xf0\x48\xc6\xc3\xfd\x69\x5c\x14'
    res = bytes2hexstring(a, 1)
    assert(res == '1C7F044F5678656E368C6E84F048C6C3FD695C14')
    res_b = hexstring2bytes(res)
    assert(res_b == a)

    res = bytes2hexstring(a, 0)
    assert(res == '1c7f044f5678656e368c6e84f048c6c3fd695c14')
    res_b = hexstring2bytes(res)
    assert(res_b == a)
    print(res)
