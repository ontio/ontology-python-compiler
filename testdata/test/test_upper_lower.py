OntCversion = '2.0.0'
from ontology.libont import upper, lower

def Main():
    s = '123abcdefghijklmnopqrstuvwxyz_*?/.####_+-ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&*()!'
    print(s)
    res = upper(s)
    print(res)

    res0 = lower(s)
    print(res0)

    res1 = upper(res0)
    assert(res == res1)
