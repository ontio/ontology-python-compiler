import hashlib
import base58

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
