import binascii


class NotifyAction():
    def __init__(self, action_name, args):
        self.action_name = action_name
        self.args = args
        assert(type(args[0]).__name__ == 'Str')
        self.event_name = args[0].s


class RegisterAppCall():
    def __init__(self, func_name, arguments):
        self.func_name = func_name
        self.arguments = arguments
        if type(arguments[0]).__name__ == 'Str':
            self.script_hash = arguments[0].s
        elif type(arguments[0]).__name__ == 'Bytes':
            self.script_hash = arguments[0].s
        else:
            print("RegisterAppCall only support Str or Bytes type addr")
            exit()

        if isinstance(self.script_hash, str):
            if len(self.script_hash) != 40:
                raise Exception("Invalid script hash! length of string must be 40")
        elif type(self.script_hash) in [bytes, bytearray]:
            if len(self.script_hash) != 20:
                raise Exception("Invalid Script hash, length in bytes must be 20")
        else:
            raise Exception("Invalid script hash type.  must be string, bytes, or bytearray")

    @property
    def script_hash_addr(self):
        return RegisterAppCall.to_script_hash_data(self.script_hash)

    @staticmethod
    def to_script_hash_data(item):
        b_array = None
        if isinstance(item, str):
            bstring = item.encode('utf-8')
            b_array = bytearray(binascii.unhexlify(bstring))
        elif isinstance(item, bytearray):
            pass
        elif isinstance(item, bytes):
            b_array = bytearray(item)
        else:
            raise Exception("Invalid script hash")
        b_array.reverse()
        return bytes(b_array)
