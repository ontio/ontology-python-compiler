OntCversion = '2.0.0'
# !/usr/bin/env python3


def Main():
    i = 0
    j = 0
    k = 0
    h = 0
    s = 0
    while i < 500:
        if i > 80:
            break

        while j < 10:
            if j == 8:
                break
            while k < 20:
                if k == 11:
                    i = i + k
                    k = k + 3
                    continue
                k = k + 1
            j = j + 1

        i = i + j + k

        while h < 30:
            print("in last while")
            h = h + 1
            s = s + h
            s = s * h
            if h == 25:
                h = h + 2
                continue
            s = s / h

        i = i + h

        items = range(3, 100)

        items2 = ['a', 'b', 'c', 'd']
        count = 0

        for x in items:  # 3
            print("1 level")

            count = count + 1

            for y in items2:  # 4
                print("2 level")

                count = count + 1
                if count > 20:
                    print("for 2 level break")
                    break

                for z in items:  # 3
                    print("3 level")
                    if count > 5:
                        print("for 3 level continue")
                        continue
                    count = count + 1

                count = count + 2

            if count > 60:
                print("for 1 level break")
                break

        i = i + count + s

    print(i)  # i = 8343
    assert(i == 8343)
