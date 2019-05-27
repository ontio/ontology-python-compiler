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
                    break
                k = k + 1
            j = j + 1

        i = i + j + k

        while h < 30:
            print("in last while")
            h = h + 1
            s = s + h
            s = s * h
            if h == 25:
                break

        i = i + h

    print(i)  # i = 93
    assert(i == 93)
