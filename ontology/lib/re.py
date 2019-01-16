from ontology.builtins import len


def match(s, p):
    if p == "":
        return s == ""

    if len(p) == 1:
        return len(s) == 1 and (s[0] == p[0] or p[0] == '.')

    if p[1] != "*":
        if s == "":
            return False
        return (s[0] == p[0] or p[0] == '.') and match(s[1:], p[1:])

    while s and (s[0] == p[0] or p[0] == '.'):
        if match(s, p[2:]):
            return True

        s = s[1:]

    return match(s, p[2:])
