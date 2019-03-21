from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.System.Contract import Destroy
from ontology.interop.System.Runtime import Notify
from ontology.builtins import *

def Main(operation, args):
    if operation == "DestroyContract":
        return DestroyContract()
    if operation == "MigrateContract":
        if args[0] != 0:
            Notify("param error")
            return False
        return MigrateContract(args)


def DestroyContract():
    #Destroy()
    Notify(["Destory"])
    return True

def MigrateContract(args):
    """
    Note that the existing contract will be replaced by the newly migrated contract
    :param code: your avm code
    :return:
    """
    # maybe index out of range
    success = Migrate(args[0], args[1], args[2],args[3],args[4], args[5],args[6])
    Notify(["Migrate successfully"])
    return True
