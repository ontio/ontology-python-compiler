OntCversion = '2.0.0'
# !/usr/bin/env python3


def main(operation, args):
    if operation == 'add':
        a = args[0]
        b = args[1]
        return add(a, b)
    elif operation == 'sub':
        a = args[0]
        b = args[1]
        return sub(a, b)
    elif operation == 'mul':
        a = args[0]
        b = args[1]
        return mul(a, b)
    elif operation == 'testcase':
        return testcase()

def testcase():
    return '[[]]'


def add(a, b):
    c = a + b
    return c


def sub(a, b):
    c = a - b
    return c


def mul(a, b):
    c = a * b
    return c
