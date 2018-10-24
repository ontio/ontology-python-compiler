#!/usr/bin/evn python3

def Main():
    list0 = [1, 2, 3, 4, 5]
    list0.reverse()
    print(list0[0])
    throw_if_null(list0[0] == 5)
    throw_if_null(list0[1] == 4)
    throw_if_null(list0[2] == 3)
    throw_if_null(list0[3] == 2)
    throw_if_null(list0[4] == 1)
    return True
