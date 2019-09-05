OntCversion = '2.0.0'
nfa_instr_all = []
bitset = 0
max_nfa_len = 1024

CHR = 0x00
ANY = 0x01
CCL = 0x02
BOL = 0x03
EOL = 0x04
COL = 0x05
END = 0x06

REPEATSTAR = 0x7
REPEATPLUS = 0x8
REPEATNO   = 0x9
NOP = 0xa

nfa_map = {CHR:'CHR', ANY:'ANY', CCL:'CCL', BOL:'BOL', EOL:'EOL', COL:'COL',END:'END', REPEATSTAR:'REPEATSTAR', REPEATNO:'REPEATNO', REPEATPLUS:'REPEATPLUS',NOP:'NOP'}

# vm runtime 
closure_count = NOP

def Main():
    pattern = ['.[bcd]+bcdef.[^gh]?ijk*kk$', '.*', '.*', '\.\.\.\.\.', '.b?[^a]?ab*[^b]+', 'ab?[^a]?ab*[^b]+', '.b?[^a]?ab*[^b]+', 'a[.*?\]+=/]+b', 'a[.*?\]+=/]+b', '.*a?a?b+b+c*c*$', '.*a?a?b+b+c*c?$','.*a?a?b+b+c*c?$','\.*a?a?b*b+c*c?$']
    string = ['xdkjafskd_a_bcdbcdbcdbcdbcdefgiijkkkkkk', 'abc', '', '....', 'aawiejfijsiidjfllek', 'abcdabcd', 'xab', '0123a+b', '0123a...cb', 'bb', 'xb', 'xbb', 'abbbc']
    result = [1, 1, 1, 0, 1, 0, 0 , 1, 0, 1, 0, 1, 1]

    for  i in range(len(pattern)):
        res = regular_match(pattern[i], string[i])
        print(i)
        print(pattern[i])
        print(string[i])
        assert(res == result[i])


def regular_match(pattern, string):
    global nfa_instr_all
    nfa_instr_all = []
    result = 0 
    re_compile(pattern)
    # nfa_dump(nfa_instr_all)
    if re_exec(string):
        result = 1

    return result

def listslice(lst, start, end = 1024):
    global max_nfa_len
    assert(len(lst) < max_nfa_len)
    a = []
    for i in range(len(lst)):
        if i < start:
            continue
        if i != max_nfa_len and i >= end:
            break
        a.append(lst[i])

    return a

def nfa_dump(nfa_instr):
    pc = 0
    while pc < len(nfa_instr):
        print(nfa_map[nfa_instr[pc]])
        if nfa_instr[pc] == CHR:
            pc += 1
            print(nfa_instr[pc])
        elif nfa_instr[pc] == CCL:
            pc += 1

        pc += 1

def setbit(p_char):
    global bitset
    assert(0 <= ord(p_char) <= 127)
    bitset |= 1 << ord(p_char)

def isetbit(p_char,bitset):
    assert(0 <= ord(p_char) <= 127)
    t = (bitset >> ord(p_char) & 0x1)
    return t

def xormask():
    global bitset
    bitset = ~bitset 

def re_compile(pattern):
    global nfa_instr_all
    l = len(pattern)
    i = 0
    closure_pc = None
    next_char_normal = False

    while i < l:
        index_prev = len(nfa_instr_all);
        p_char = pattern[i]

        if next_char_normal is True:
            next_char_normal = False
            closure_pc = len(nfa_instr_all)
            store(NOP)
            store(CHR)
            store(p_char)
            i += 1
            continue

        if p_char == '.': 
            closure_pc = len(nfa_instr_all)
            store(NOP)
            store(ANY)
        elif p_char == '^':
            if len(nfa_instr_all) == 0:
                store(BOL)
            else:
                closure_pc = len(nfa_instr_all)
                store(NOP)
                store(CHR)
                store(p_char)
        elif p_char ==  '$':
            if i == l - 1:
                store(EOL)
            else:
                closure_pc = len(nfa_instr_all)
                store(NOP)
                store(CHR)
                store(p_char)
        elif p_char ==  '[':
            global bitset
            bitset = 0
            closure_pc = len(nfa_instr_all)
            store(NOP)
            store(CCL)
            i += 1
            p_char = pattern[i]
            if (p_char == '^'):
                need_reverse = True
                i += 1
                p_char = pattern[i]
            else:
                need_reverse = False 

            if (p_char == '-'):
                setbit(p_char)
                i += 1

            p_char = pattern[i]
            next_elt_normal = False
            while i < len(pattern) and (p_char != ']' or next_elt_normal is True):
                if next_elt_normal is True:
                    setbit(pattern[i])
                    next_elt_normal = False
                    i += 1
                    p_char = pattern[i]
                    continue

                next_elt_normal = False
                if p_char == '\\':
                    next_elt_normal = True
                elif p_char == '-':
                    c1 = ord(pattern[i-1])
                    if pattern[i+1] != ']':
                        c2 = ord(pattern[i+1])
                    else:
                        c2 = 127

                    while c1 <= c2:
                        setbit(chr(c1))
                        c1 += 1
                else:
                    setbit(pattern[i])

                i += 1
                p_char = pattern[i]

            if p_char != ']':
                print('Missing ]')
                return

            if need_reverse:
                xormask()

            store(bitset)
        elif p_char == '*':
            setpc(closure_pc, REPEATSTAR)
            store(END)
        elif p_char == '+':
            setpc(closure_pc, REPEATPLUS)
            store(END)
        elif p_char == '?':
            setpc(closure_pc, REPEATNO)
            store(END)
        elif p_char == '\\':
            next_char_normal = True
        else:
            closure_pc = len(nfa_instr_all)
            store(NOP)
            store(CHR)
            store(p_char)

        i += 1

def re_exec(string):
    global nfa_instr_all
    #assert(len(string) > 0)
    start_instr = nfa_instr_all[0]
    if start_instr == BOL:
        return match(string, nfa_instr_all)
    elif start_instr == CHR:
        start_char = nfa_instr_all[1]
        j = 0
        while j < len(string):
            ss = string[j:]
            i = 0
            while i < len(ss) and start_char != ss[i]:
                i += 1

            if i < len(ss):
                if match(ss[i:], nfa_instr_all):
                    return True
            j = j + i + 1
        return False
    else:
        j = 0
        while not match(string[j:], nfa_instr_all):
            j += 1
            if j >= len(string):
                break
        else:
            return True 

        return False

    return True

def match(string, nfa_instr):
    if len(nfa_instr) == 0:
        return True
    si = 0; pc = 0
    while si <= len(string) and pc < len(nfa_instr):
        check_repeat = False
        opcode = nfa_instr[pc]
        if opcode == EOL:
            if si != len(string) and len(string) != 0:
                return False
            assert(pc == len(nfa_instr) - 1)
            closure_count = NOP
        elif opcode == NOP:
            closure_count = NOP
        elif opcode == END:
            closure_count = NOP
        elif opcode == CHR:
            pc += 1
            if string[si:] == '' or string[si] != nfa_instr[pc]:
                if closure_count == NOP:
                    return False
                elif closure_count == REPEATSTAR:
                    pass
                elif closure_count == REPEATPLUS:
                    return False
                elif closure_count == REPEATNO:
                    pass
                else:
                    assert(False)
            else:
                match_c = string[si]
                if closure_count == NOP:
                    si += 1
                elif closure_count == REPEATNO:
                    closure_count = NOP
                    # match zero try
                    if match(string[si:], listslice(nfa_instr,pc+2)):
                        return True
                    si += 1
                elif closure_count == REPEATSTAR:
                    # from match zero try
                    while True:
                        if (si >= len(string) or not string[si] == match_c):
                            break
                        closure_count = NOP
                        if match(string[si:], listslice(nfa_instr,pc+2)):
                            return True
                        si += 1
                else:
                    si += 1
                    while True:
                        if (si >= len(string) or not string[si] == match_c):
                            break
                        closure_count = NOP
                        if match(string[si:], listslice(nfa_instr,pc+2)):
                            return True
                        si += 1
            closure_count = NOP
        elif opcode == ANY:
            if string[si:] == '':
                if closure_count == NOP:
                    return False
                elif closure_count == REPEATSTAR:
                    pass
                elif closure_count == REPEATPLUS:
                    return False
                elif closure_count == REPEATNO:
                    pass
                else:
                    assert(False)
            else:
                match_c = string[si]
                if closure_count == NOP:
                    si += 1
                elif closure_count == REPEATNO:
                    closure_count = NOP
                    # match zero try
                    if match(string[si:], listslice(nfa_instr,pc+2)):
                        return True
                    si += 1
                elif closure_count == REPEATSTAR:
                    # from match zero try
                    while True:
                        if (si >= len(string)):
                            break
                        closure_count = NOP
                        if match(string[si:], listslice(nfa_instr,pc+2)):
                            return True
                        si += 1
                else:
                    si += 1
                    while True:
                        if (si >= len(string)):
                            break
                        closure_count = NOP
                        if match(string[si:], listslice(nfa_instr,pc+2)):
                            return True
                        si += 1
            closure_count = NOP
        elif opcode == BOL:
            if si != 0 :
                return False
            closure_count = NOP
        elif opcode == CCL:
            pc += 1

            if string[si:] == '' or not isetbit(string[si], nfa_instr[pc]):
                if closure_count == NOP:
                    return False
                elif closure_count == REPEATSTAR:
                    pass
                elif closure_count == REPEATPLUS:
                    return False
                elif closure_count == REPEATNO:
                    pass
                else:
                    assert(False)
            else:
                if closure_count == NOP:
                    si += 1
                elif closure_count == REPEATNO:
                    closure_count = NOP
                    # match zero try
                    if match(string[si:], listslice(nfa_instr,pc+2)):
                        return True
                    si += 1
                elif closure_count == REPEATSTAR:
                    # from match zero try
                    while True:
                        if si >= len(string) or not isetbit(string[si], nfa_instr[pc]):
                            break
                        closure_count = NOP
                        if match(string[si:], listslice(nfa_instr,pc+2)):
                            return True
                        si += 1
                else:
                    si += 1
                    while True:
                        if si >= len(string) or not isetbit(string[si], nfa_instr[pc]):
                            break
                        closure_count = NOP
                        if match(string[si:], listslice(nfa_instr,pc+2)):
                            return True
                        si += 1
            closure_count = NOP
        elif opcode == REPEATSTAR:
            closure_count = REPEATSTAR
        elif opcode == REPEATNO:
            closure_count = REPEATNO
        elif opcode == REPEATPLUS:
            closure_count = REPEATPLUS
        else:
            assert(False)

        pc += 1

    if pc == len(nfa_instr):
        return True
    else:
        return False

def store(x):
    global nfa_instr_all
    nfa_instr_all.append(x)

def setpc(pc, x):
    global nfa_instr_all
    assert(pc < len(nfa_instr_all))
    nfa_instr_all[pc] = x

#Main()
