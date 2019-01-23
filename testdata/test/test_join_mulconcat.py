OntCversion = '2.0.0'
from ontology.libont import join, mulconcat

def main():
    c = '-'
    lst = ['1', '2', '3', '4', '5']
    s = join(c, lst)
    print(s)
    assert(s == '1-2-3-4-5')

    s = mulconcat('0',*lst, '6')
    print(s)
    assert(s == '0123456')
