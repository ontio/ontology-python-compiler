#!/usr/bin/evn python3

def Main():

    items = [0, 1, 2]

    items2 = ['a', 'b', 'c', 'd']
    count = 0

    for i in items:  # 3

        count += 1

        for j in items2:  # 4

            count += 1

            for k in items:  # 3
                count += 1


    throw_if_null(count == 51)
