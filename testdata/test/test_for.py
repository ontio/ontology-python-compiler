OntCversion = '2.0.0'
# !/usr/bin/env python3


def main():
    a = range(0, 20)
    b = range(0, 20)
    c = range(0, 10)

    k = 0
    m = 0
    x = 0
    for i in a:
        for j in b:
            if j == 2:
                k += 4
                continue
            if j == 3:
                k += 5
                continue

            if j == 13:
                m = 999
                k += m
                print("2 for break in")
                break
            m = 10
            k += 1

        if m == 999:
            k += 888
        k += 1

        if i == 15:
            print("1 for break in")
            break

        if i == 10:
            print("1 for continue in"); continue

        for n in c:
            if n == 5:
                x = 100
                k += x
                print("3 for break in")
                break
            k += 1

    assert(k == 31998)
    print(k)
