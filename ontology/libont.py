from ontology.builtins import append, len, range, reversed, concat

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

def int(arg):
    slen = len(arg)
    n = 1
    num = 0
    scale = 10
    elt = ['0','1','2','3','4','5','6','7','8','9', '-']
    for i in reversed(range(0, slen)):
        assert(elt_in(elt, arg[i: i+1]))
        if i != 0 and arg[i: i+1] == '-':
            assert(False)
        if i == 0 and arg[i: i+1] == '-':
            num = -num
            break
        else:
            num += (arg[i: i+1] - '0') * n
        n = n * scale
    return num

def split(str_t, c):
    res = []
    len_t = len(str_t)
    t = None
    for i in range(0,len_t):
        x = str_t[i: i+1]
        if x != c:
            t = concat(t, x)
        else:
            if t != None:
                res.append(t)
                t = None
            continue

    if t != None:
        res.append(t)
    return res
