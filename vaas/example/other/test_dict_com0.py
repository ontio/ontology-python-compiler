OntCversion = '2.0.0'
#!/usr/bin/env python3
import ontology.builtins

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def main():
    b = {i:i*i for i in range(1, 5)}
    VaasAssert(b[1] == 1 + 1)
    VaasAssert(b[2] == 4 + 1)
    VaasAssert(b[3] == 9 + 1)
    VaasAssert(b[4] == 16 + 1)
    print(b[1])
    print(b[2])
    print(b[3])
    print(b[4])
