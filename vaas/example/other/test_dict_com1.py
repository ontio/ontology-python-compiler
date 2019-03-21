OntCversion = '2.0.0'
#!/usr/bin/env python3
import ontology.builtins

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def main():
    b = {i:j for i in range(1, 5) for j in range(5,8)}
    VaasAssert(b[1] == 7 + 1)
    VaasAssert(b[2] == 7 + 1)
    VaasAssert(b[3] == 7 + 1)
    VaasAssert(b[4] == 7 + 1)
    print(b[1])
    print(b[2])
    print(b[3])
    print(b[4])
