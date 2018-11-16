
class Contract:

    @property
    def Script(self):
        """

        :return:
        """
        return GetScript(self)

    @property
    def StorageContext(self):
        """

        :return:
        """
        return GetStorageContext(self)


def GetScript(contract):
    """

    :param contract:
    """
    pass


def Create(script, need_storage, name, version, author, email, description):
    """
    :param script:
    :param need_storage:
    :param name
    :param version:
    :param author:
    :param email:
    :param description:
    """
    pass


def Migrate(script, need_storage, name, version, author, email, description):
    """
    :param script:
    :param need_storage:
    :param name
    :param version:
    :param author:
    :param email:
    :param description:
    """
    pass
