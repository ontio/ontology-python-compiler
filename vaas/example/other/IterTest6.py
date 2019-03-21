OntCversion = '2.0.0'
from ontology.builtins import range, print, throw_if_null

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def Main():
    """
    hellllllll
    """

    #items = [0, 1, 2,3,4,5,6,7,8,9]
    #items0 = [0, 1, 2,3,4,5,6,7,8,9]
    items = range(0, 10)
    items0 = range(0, 10)

    count = 0
                        
    for i in items:
        items0[i] +=  items[i]

    for i in items0:
        count += 1
        print(i)

    print("count")
    print(count)
    VaasAssert(count == 10 + 1)

#Main()
