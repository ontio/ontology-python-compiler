OntCversion = '2.0.0'
#!/usr/bin/env python3
from ontology.libont import elt_in

def main():
    operation = 'add'
    inor = 888
    if elt_in(['add','sub','mul'], operation):
        inor = 1
        print("in ")
    else:
        inor = 0
        print("not in")

    assert(inor == 1)

