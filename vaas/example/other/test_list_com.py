OntCversion = '2.0.0'
#!/usr/bin/env python3
from ontology.builtins import range, print, append, len

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def Main():
    #a = [[x, y] for x in range(10) if x % 2 if x > 3 for y in range(10) if y > 7 if y != 8  ]
    a = [[x, y] for x in range(0,10) if x % 2 if x > 3 for y in range(0,10) if y > 7 if y != 8  ]
    #a = [[x, y] for x in range(10)  for y in range(10)]
    #a = [x for x in range(0,10) if x > 2 if x > 3]
    VaasAssert(len(a) == 3)
    x = a[0]
    y = a[1]
    z = a[2]


    VaasAssert(x[0] == 5)
    VaasAssert(y[0] == 7)
    VaasAssert(z[0] == 9)
    VaasAssert(x[1] == 9)
    VaasAssert(y[1] == 9)
    VaasAssert(z[1] == 9)

    #a = [1,2,3,4,5]
    for i in a:
        VaasAssert(len(i) == 2)
        print(i[0])
        print(i[1])

    b = [[x, y] for x in range(0,10) if x % 2 for y in range(0,10) if y > 7 if y != 8  ]

    for i in b:
        VaasAssert(len(i) == 2)
        print(i[0])
        print(i[1])

    c = [ x*y*z for x in range(1, 3) for y in range(1,3) for z in range(1, 3)]

    VaasAssert(len(c) == 8)
    print(len(c))

    VaasAssert(c[0] == 1)
    VaasAssert(c[1] == 2)
    VaasAssert(c[2] == 2)
    VaasAssert(c[3] == 4)
    VaasAssert(c[4] == 2)
    VaasAssert(c[5] == 4)
    VaasAssert(c[6] == 4)
    VaasAssert(c[7] == 8 + 1)

    for i in c:
        print(i)
