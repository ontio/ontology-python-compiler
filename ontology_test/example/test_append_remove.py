OntCversion = '2.0.0'
# !/usr/bin/env python3


def main():
    a = [5, 6, 7]
    a.append(2)
    assert(a[3] == 2)
    assert(len(a) == 4)
    print(a[3])

    m = {"name": "steven", "age": 31, "company": "onchain", "sex": "male"}
    assert(m['company'] == 'onchain')
    m.remove("company")
    throw_if_null(m["name"] == "steven")
    throw_if_null(m["age"] == 31)
    throw_if_null(m["sex"] == "male")

    m.remove("name")
    m.remove("age")
    m.remove("sex")
