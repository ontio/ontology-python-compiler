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

def int(arg, scale):
    slen = len(arg)
    n = 1
    num = 0
    elt_p0 = ['0','1','2','3','4','5','6','7','8','9', '-']
    elt_p1 = ['a', 'b', 'c', 'd', 'e', 'f']
    elt_p2 = ['A', 'B', 'C', 'D', 'E', 'F']
    if scale != 10 and scale != 16:
        assert(False)

    for i in reversed(range(0, slen)):
        cur_char = arg[i: i+1]

        if i != 0 and  cur_char == '-':
            assert(False)
        if i == 0 and cur_char == '-':
            num = -num
            break
        else:
            if scale == 10:
                assert(elt_in(elt_p0, cur_char))
                num += (cur_char - '0') * n
            elif scale == 16:
                if elt_in(elt_p0, cur_char):
                    num += (cur_char - '0') * n
                elif elt_in(elt_p1, cur_char):
                    num += (cur_char - 'a' + 10) * n
                elif elt_in(elt_p2, cur_char):
                    num += (cur_char - 'A' + 10) * n
                else:
                    assert(False)
            else:
                assert(False)

        n = n * scale
    return num

# note integer 0 have zero bytes. alway can make int to bytearray. but can not convert '0000abcd0000' will lose 0 bytes
def hexstring2bytes(arg):
    elt_p0 = ['0','1','2','3','4','5','6','7','8','9']
    elt_p1 = ['a', 'b', 'c', 'd', 'e', 'f']
    elt_p2 = ['A', 'B', 'C', 'D', 'E', 'F']
    slen = len(arg)
    assert(slen % 2 == 0)
    str_res = ''
    num = 0
    for i in range(0, slen):
        cur_char = arg[i: i+1]

        if i % 2 == 0:
            if elt_in(elt_p0, cur_char):
                num = (cur_char - '0')
            elif elt_in(elt_p1, cur_char):
                num = (cur_char - 'a' + 10)
            elif elt_in(elt_p2, cur_char):
                num = (cur_char - 'A' + 10)
            else:
                assert(False)

            if num != 0:
                num = num & 0xf
                num = (num << 4) & 0xf0
                num = num[0:1]
                assert(len(num) == 1)
            else:
                num = 0
        else:
            if elt_in(elt_p0, cur_char):
                num += (cur_char - '0')
            elif elt_in(elt_p1, cur_char):
                num += (cur_char - 'a' + 10)
            elif elt_in(elt_p2, cur_char):
                num += (cur_char - 'A' + 10)
            else:
                assert(False)

            if num != 0:
                num = num[0:1]
                assert(len(num) == 1)
                str_res = concat(str_res, num)
            else:
                str_res = concat(str_res, b'\x00')

    return str_res

def bytearray_reverse(arg):
    slen = len(arg)
    res = None
    for i in reversed(range(0, slen)):
        cur_byte = arg[i: i+1]
        res = concat(res, cur_byte)
    return res

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
