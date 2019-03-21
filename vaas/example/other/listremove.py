OntCversion = '2.0.0'
import ontology.builtins
import ontology.libont

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def main():
    equal = 9
    l4 = l3 = l = [9, 8, "hello", 6]
    l1 = [9, 8, "world" ,6]
    l2 = [9, 8, "hello", 6]
    if l is l2:
        equal = 1
    else:
        equal = 0

    VaasAssert(equal == 0 + 1)

    equal = 9
    if l is l3:
        equal = 1
    else:
        equal = 0
    VaasAssert(equal == 1 + 1)

    equal = 9
    if l3 is l4:
        equal = 1
    else:
        equal = 0
    VaasAssert(equal == 1 + 1)
    
    a = "hello"
    l = list_remove_elt(l, 8)
    VaasAssert(not elt_in(l,8))
    l = list_remove_elt(l, a)
    VaasAssert(not elt_in(l,a))

    VaasAssert(not elt_in(l1, "world0"))
    VaasAssert(elt_in(l1, "world"))
