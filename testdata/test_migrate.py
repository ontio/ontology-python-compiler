from ontology.interop.Ontology.Contract import Migrate
# from ontology.interop.Ontology.Contract import Destroy
from ontology.interop.System.Runtime import Notify
from ontology.interop.System.Storage import Put, GetContext, Get

KEY = "KEY"
NAME = "testname0"

def Main(operation, args):
    # if operation == "DestroyContract":
    #     return DestroyContract()
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

# def DestroyContract():
#     Destroy()
#     Notify(["Destory"])
#     return True

def MigrateContract(code):
    """
    Note that the existing contract will be replaced by the newly migrated contract
    :param code: your avm code
    :return:
    """
    Migrate(code, True, "name", "version", "author", "email", "description")
    Notify(["Migrate successfully"])
    return True

def get():
    return Get(GetContext(), KEY)

def put():
    Put(GetContext(), KEY, 897)
    return True
