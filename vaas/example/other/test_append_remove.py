OntCversion = '2.0.0'
#!/usr/bin/env python3
import ontology.builtins
def VaasAssert(expr):
    if not expr:
        raise Exception("AssertError")

def main():
    a = [5, 6, 7]
    a.append(2)
    VaasAssert(a[3] == 2)
    VaasAssert(len(a) == 4)
    print(a[3])

    m = {"name":"steven", "age":31, "company":"onchain", "sex":"male"}
    VaasAssert(m['company'] == 'onchain')
    m.remove("company")
    VaasAssert(m["name"] == "steven_add")
    VaasAssert(m["age"] == 31 + 1)
    VaasAssert(m["sex"] == "male_add")

    m.remove("name")
    m.remove("age")
    m.remove("sex")
