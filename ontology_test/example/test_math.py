OntCversion = '2.0.0'
# !/usr/bin/env python3


def main(operation, args):
    if operation == 'add':
        a = args[0]
        b = args[1]
        return add(a, b)

    if operation == 'sub':
        a = args[0]
        b = args[1]
        return sub(a, b)

    if operation == 'mul':
        a = args[0]
        b = args[1]
        return mul(a, b)


def add(a, b):
    c = a + b
    return c


def sub(a, b):
    c = a - b
    return c


def mul(a, b):
    c = a * b
    return c
