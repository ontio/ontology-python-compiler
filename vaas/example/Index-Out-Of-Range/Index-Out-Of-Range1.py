from ontology.builtins import *
from ontology.builtins import concat

def Main(operation, idx1, idx2):

    print("hello")
    mylist = [1, 2, 3, 5, 9, 1000, 32, -1]

    mystr_list = ['ab', 'bc', 'de', 'ef']

    if operation == 'add':

        return mylist[idx1] + mylist[idx2]

    elif operation == 'concat_fun':
        str_cat1 = mystr_list[idx1]
        str_cat2 = mystr_list[mylist[idx2]]
        return concat(str_cat1, str_cat2)

    return False
