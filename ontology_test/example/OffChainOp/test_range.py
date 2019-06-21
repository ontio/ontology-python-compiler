OntCversion = '2.0.0'
a = range(1,5,2)
assert(len(a) == 2)
assert(a[0] == 1)
assert(a[1] == 3)

a = range(1,8,3)
assert(len(a) == 3)
assert(a[0] == 1)
assert(a[1] == 4)
assert(a[2] == 7)

a = range(5)
assert(len(a) == 5)
assert(a[0] == 0)
assert(a[1] == 1)
assert(a[2] == 2)
assert(a[3] == 3)
assert(a[4] == 4)

def Main():
    pass
