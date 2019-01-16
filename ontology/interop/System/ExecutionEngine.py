def GetScriptContainer():
    """
    Returns the current Script Container of a smart contract execution.
    This will be a ``ontology.blockchain.vm.ontology.Transaction`` object.

    - Note: This method is implemented inside the ontology Virtual Machine.

    :return: the current ScriptContainer of a smart contract execution.
    :rtype: ``ontology.blockchain.vm.ontology.Transaction``
    """
    pass


def GetExecutingScriptHash():
    """
    Returns the hash of the script ( smart contract ) which is currently being executed

    - Note: This method is implemented inside the ontology Virtual Machine.

    :return: the hash of the script ( smart contract ) which is currently being executed
    :rtype: bytearray
    """
    pass


def GetCallingScriptHash():
    """
    Returns the hash of the script ( smart contract ) which began execution of the current script.

    - Note: This method is implemented inside the ontology Virtual Machine.

    :return: the hash of the script ( smart contract ) which began execution of the current script
    :rtype: bytearray
    """
    pass


def GetEntryScriptHash():
    """
    Returns the hash of the script ( smart contract ) which began execution of the smart contract.

    - Note: This method is implemented inside the ontology Virtual Machine.

    :return: the hash of the script ( smart contract ) which began execution of the smart contract
    :rtype: bytearray
    """
    pass
