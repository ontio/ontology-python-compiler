import ontology.builtins
import ontology.libont
def main():
    equal = 9
    l4 = l3 = l = [9, 8, "hello", 6]
    l1 = [9, 8, "world" ,6]
    l2 = [9, 8, "hello", 6]
    if l is l2:
        equal = 1
    else:
        equal = 0

    assert(equal == 0)

    equal = 9
    if l is l3:
        equal = 1
    else:
        equal = 0
    assert(equal == 1)

    equal = 9
    if l3 is l4:
        equal = 1
    else:
        equal = 0
    assert(equal == 1)
    
    a = "hello"
    l = list_remove_elt(l, 8)
    assert(not elt_in(l,8))
    l = list_remove_elt(l, a)
    assert(not elt_in(l,a))

    assert(not elt_in(l1, "world0"))
    assert(elt_in(l1, "world"))
