OntCversion = '2.0.0'

m = {0:'a', 'a':'b', 'b':'c'}

def main():
    l = [[1,3]]
    b = [2,4]
    l.append(b)
    test(l, m)
    assert(l[0][0] == 1)
    assert(l[0][1] == 3)
    assert(l[1][0] == 2)
    assert(l[1][1] == 4)
    assert(l[2][0] == 'a' )
    assert(l[2]['a'] == 'b')
    assert(l[2]['b'] == 'c')

def test(l_t, map_t):
    l_t.append(map_t)

