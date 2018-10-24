from bytecode import UNSET, Label, Instr, Bytecode, BasicBlock, ControlFlowGraph
from ontology.code import pyop
import glob
import importlib
import hashlib
import base58


class BlockType():
    MAKE_FUNCTION = 0
    CALL_FUNCTION = 1
    MAKE_CLASS = 2
    IMPORT_ITEM = 3
    MODULE_VAR = 4
    DOC_STRING = 5
    LOAD_CONST = 6
    ACTION_REG = 7
    APPCALL_REG = 8
    UNKNOWN = 9


def get_block_type(block):

    for instr in block:
        if instr.opcode == pyop.LOAD_NAME and instr.arg == 'RegisterAction':
            return BlockType.ACTION_REG
        elif instr.opcode == pyop.LOAD_NAME and instr.arg == 'RegisterAppCall':
            return BlockType.APPCALL_REG
        elif instr.opcode in [pyop.IMPORT_FROM, pyop.IMPORT_NAME, pyop.IMPORT_STAR]:
            return BlockType.IMPORT_ITEM
        elif instr.opcode == pyop.MAKE_FUNCTION:
            return BlockType.MAKE_FUNCTION
        elif instr.opcode == pyop.LOAD_BUILD_CLASS:
            return BlockType.MAKE_CLASS
        elif instr.opcode == pyop.CALL_FUNCTION:
            return BlockType.CALL_FUNCTION

    return BlockType.UNKNOWN

class Digest(object):
    @staticmethod
    def __sha256(msg: bytes, is_hex: bool = False):
        m = hashlib.sha256()
        m.update(msg)
        if is_hex:
            return m.hexdigest()
        else:
            return m.digest()

    @staticmethod
    def ripemd160(msg: bytes, is_hex: bool = False):
        h = hashlib.new('ripemd160')
        h.update(msg)
        if is_hex:
            return h.hexdigest()
        else:
            return h.digest()

    @staticmethod
    def sha256(msg: bytes, offset: int = 0, length: int = 0, is_hex: bool = False):
        if offset != 0 and len(msg) > offset + length:
            msg = msg[offset:offset + length]
        return Digest.__sha256(msg, is_hex)

    @staticmethod
    def hash256(msg: bytes, is_hex: bool = False) -> bytes or str:
        digest = Digest.sha256(Digest.sha256(msg), is_hex=is_hex)
        return digest

    @staticmethod
    def hash160(msg: bytes, is_hex: bool = False) -> bytes or str:
        digest = Digest.ripemd160(Digest.__sha256(msg), is_hex)
        return digest

class Address(object):
    __COIN_VERSION = b'\x17'

    def __init__(self, value: bytes):
        self.ZERO = value  # 20 bytes

    def to_array(self):
        return self.ZERO

    def b58encode(self):
        script_builder = Address.__COIN_VERSION + self.ZERO
        c256 = Digest.hash256(script_builder)[0:4]
        out_byte_array = script_builder + bytearray(c256)
        return base58.b58encode(bytes(out_byte_array)).decode('utf-8')

    @staticmethod
    def b58decode(address: str):
        data = base58.b58decode(address)
        if len(data) != 25:
            raise Exception("ERROR:Wrong data len")
        if data[0] != int.from_bytes(Address.__COIN_VERSION, "little"):
            raise Exception("ERROR: Adrress VERSION wrong")
        checksum = Digest.hash256(data[0:21])
        if data[21:25] != checksum[0:4]:
            raise Exception("ERROR: checksum ERROR")
        return Address(data[1:21])
