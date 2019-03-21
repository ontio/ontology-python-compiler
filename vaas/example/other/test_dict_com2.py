OntCversion = '2.0.0'
#!/usr/bin/env python3
import ontology.builtins

def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")
def main():
    b = {i:j for i in range(0, 10) if i % 2 if i > 3  for j in range(5,8) if j < 7}
    VaasAssert(b[5] == 6 + 1)
    VaasAssert(b[7] == 6 + 1)
    VaasAssert(b[9] == 6 + 1)
    print(b[5])
    print(b[7])
    print(b[9])
