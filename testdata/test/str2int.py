OntCversion = '2.0.0'
from ontology.builtins import print, len
from ontology.libont import int, elt_in
def main():
    a = '-012345'
    b = int(a)
    assert(b == -12345)
    a = '12345'
    b = int(a)
    print(b)
    assert(b == 12345)

    a = '123456789000000000000'
    b = int(a)
    print(b)
    assert(b == 123456789000000000000)
