OntCversion = '2.0.0'
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Storage import Put, GetContext, Get

KEY = "KEY"
NAME = "testname111"


def Main(operation, args):
    if operation == "MigrateContract":
        if len(args) != 1:
            Notify("param error")
            return False
        return MigrateContract(args[0])
    if operation == "put":
        return put()
    if operation == "get":
        return get()
    if operation == "name":
        return NAME


def MigrateContract(code):
    """
    Note that the existing contract will be replaced by the newly migrated contract
    :param code: your avm code
    :return:
    """
    success = Migrate(code, True, "name", "version", "author", "email", "description")
    if success:
        print("Migrate successfully")
        Notify(["Migrate successfully"])
    return success


def get():
    return Get(GetContext(), KEY)


def put():
    Put(GetContext(), KEY, 897)
    return True
