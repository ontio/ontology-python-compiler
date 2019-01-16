from ontology.libont import list_remove_elt, elt_in

OntCversion = '2.0.0'


def main():
    equal = 9
    l4 = l3 = l0 = [9, 8, "hello", 6]
    l1 = [9, 8, "world", 6]
    l2 = [9, 8, "hello", 6]
    if l0 is l2:
        equal = 1
    else:
        equal = 0

    assert(equal == 0)

    equal = 9
    if l0 is l3:
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
    l0 = list_remove_elt(l0, 8)
    assert(not elt_in(l0, 8))
    l0 = list_remove_elt(l0, a)
    assert(not elt_in(l0, a))

    assert(not elt_in(l1, "world0"))
    assert(elt_in(l1, "world"))
