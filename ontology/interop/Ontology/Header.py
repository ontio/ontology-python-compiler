

class Header:

    def getmyhash(self):
        return GetHash(self)

    @property
    def Index(self):
        return GetIndex(self)

    @property
    def Hash(self):
        """

        :return:
        """
        return GetHash(self)

    @property
    def Timestamp(self):
        """

        :return:
        """
        return GetTimestamp(self)

    @property
    def Version(self):
        """

        :return:
        """
        return GetVersion(self)

    @property
    def PrevHash(self):
        """

        :return:
        """
        return GetPrevHash(self)

    @property
    def MerkleRoot(self):
        """

        :return:
        """
        return GetMerkleRoot(self)

    @property
    def ConsensusData(self):
        """

        :return:
        """
        return GetConsensusData(self)

    @property
    def NextConsensus(self):
        """

        :return:
        """
        return GetNextConsensus(self)


def GetVersion(header):
    """

    gets the version of the header

    """
    pass


def GetMerkleRoot(header):
    """

    gets the merkle root of the transactions contained in the block

    """
    pass

def GetConsensusData(header):
    """

    gets the address of the consensus

    """
    pass


def GetNextConsensus(header):
    """

    gets the address where the next consensus will occur

    """
    pass
