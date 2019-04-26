OntCversion = '2.0.0'
# !/usr/bin/env python3

def Main(operation, args):
    if operation == 'dictCheck':
        key = args[0]
        return dictCheck(key)
    return False


def dictCheck(key):
    d = {
      'a': 1,
      'b': 2
    }
    return has_key(d, key)
