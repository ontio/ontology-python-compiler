from ontology.interop.System.Block import GetTransactionByIndex
from ontology.interop.System.Blockchain import GetTransactionByHash
from ontology.interop.System.Header import GetBlockHash
from ontology.interop.System.Transaction import GetTransactionHash
from ontology.interop.System.Blockchain import GetBlock

OntCversion = '2.0.0'


def main(Height):
    Block = GetBlock(Height)
    index = 0
    Tx = GetTransactionByIndex(Block, index)
    Txhash = GetTransactionHash(Tx)
    NewTx = GetTransactionByHash(Txhash)
    BlkHash = GetBlockHash(Block)
    print("Test finished")
