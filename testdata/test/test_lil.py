OntCversion = '2.0.0'

m = {0: 'a', 'a': 'b', 'b': 'c'}


def main():
    lst = [[1, 3]]
    b = [2, 4]
    lst.append(b)
    test(lst, m)
    assert(lst[0][0] == 1)
    assert(lst[0][1] == 3)
    assert(lst[1][0] == 2)
    assert(lst[1][1] == 4)
    assert(lst[2][0] == 'a')
    assert(lst[2]['a'] == 'b')
    assert(lst[2]['b'] == 'c')


def test(l_t, map_t):
    l_t.append(map_t)
