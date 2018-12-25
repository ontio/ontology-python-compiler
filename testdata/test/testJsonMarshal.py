from ontology.interop.Ontology.Runtime import JsonMarshalMap

def Main(operation, args):
    if operation == 'testJson':
        return testJson()
    return False


def testJson():
    m = {'a':'11','b':'22'}
    m['composit'] = [{'c':'33', 'd':'44'},{'e':'abc','f':'55'}]
    res = JsonMarshalMap(m)
    return res