from ontology.libont import str, hex, hexstring2address, address2hexstring

OntCversion = '2.0.0'


def Main():
    addr = 'f0a4da50914a53fb58635bd2d1445cf4ddcd9ed8'
    s0 = 0xf0a4da50914a53fb58635bd2d1445cf4ddcd9ed8
    s1 = 123456789
    a = hex(s0)
    b = str(s1)
    assert(b == '123456789')
    assert(a == '0xf0a4da50914a53fb58635bd2d1445cf4ddcd9ed8')

    addr_byte = hexstring2address(addr)
    addr_str = address2hexstring(addr_byte)
    assert(addr_str == addr)
    print(addr_str)
