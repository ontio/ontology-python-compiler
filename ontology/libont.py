import ontology.builtins

def list_remove_elt(l, elt):
    nl = []
    for i in l:
        if elt is i:
            continue
        nl.append(i)
    return nl

def elt_in(l, elt):
    for i in l:
        if elt is i:
            return True
    return False
