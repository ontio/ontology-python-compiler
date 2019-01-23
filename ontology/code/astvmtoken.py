from collections import OrderedDict
from ontology.interop import VMOp
from ontology.interop.BigInteger import BigInteger


class AstVMToken(object):
    @property
    def out_op(self):
        if type(self.vm_op) is int:
            return self.vm_op
        elif type(self.vm_op) is bytes:
            return ord(self.vm_op)
        else:
            raise Exception('[Error: filepath: %s. Line %d ] Invalid op: %s - You cannot use floating point numbers' % (self.cur_func.filepath, self.node.lineno, str(self.vm_op)))

    def __init__(self, vm_op, node, addr, cur_func, is_global, data=None):
        self.vm_op = vm_op
        self.addr = addr
        self.data = data
        # For Debugger
        self.syscall_name = None
        self.node = node
        self.cur_func = cur_func
        self.is_global = is_global


class AstVMTokenizer(object):
    def __init__(self):
        self._address = 0
        self.vm_tokens = OrderedDict()
        # For Debugger
        self.current_func = None
        self.global_converting = False

    def dump_all_vm_token(self):
        for addr in self.vm_tokens.keys():
            vm_token = self.vm_tokens[addr]
            vmop_name = VMOp.to_name(self.vm_tokens[addr].out_op)
            if vmop_name is None:
                vmop_name = 'PUSHBYTES' + str(self.vm_tokens[addr].out_op)

            # print("{:<10} {:<10}".format(addr, vmop_name))
            print("{:<10} {:<10} {:<10} {:<10}".format(vm_token.cur_func.name, vm_token.node.lineno, addr, vmop_name))

    def build_function_stack(self, stack_size, node):
        self.Emit_Integer(stack_size, node)
        self.Emit_Token(VMOp.NEWARRAY, node)
        self.Emit_Token(VMOp.TOALTSTACK, node)

    def Insert_Token_AT(self, vm_token, index):
        self.vm_tokens[index] = vm_token

    def Emit_Integer(self, i, node):
        if i == 0:
            return self.Emit_Token(VMOp.PUSH0, node)
        elif i == -1:
            return self.Emit_Token(VMOp.PUSHM1, node)
        elif 0 < i <= 16:
            out = 0x50 + i
            return self.Emit_Token(out, node)
        bigint = BigInteger(i)
        outdata = bigint.ToByteArray()
        return self.Emit_Data(outdata, node)

    def Emit_Token(self, vm_op, node, data=None):
        start_addr = self._address
        vmtoken = AstVMToken(vm_op, node, start_addr, self.current_func, self.global_converting, data)
        self._address += 1
        if vmtoken.data is not None:
            self._address += len(data)
        self.Insert_Token_AT(vmtoken, start_addr)
        return vmtoken

    def Emit_Data(self, data, node):
        dlen = len(data)
        if dlen == 0:
            return self.Emit_Token(VMOp.PUSH0, node)
        elif dlen <= 75:
            return self.Emit_Token(len(data), node, data=data)

        if dlen < 0x100:
            prefixlen = 1
            code = VMOp.PUSHDATA1
        elif dlen < 0x10000:
            prefixlen = 2
            code = VMOp.PUSHDATA2
        else:
            prefixlen = 4
            code = VMOp.PUSHDATA4

        byts = bytearray(dlen.to_bytes(prefixlen, 'little')) + data

        return self.Emit_Token(code, node, byts)

    def Emit_PickGlobal(self, global_postion, node):
        assert(global_postion is not None and global_postion >= 0)
        self.Emit_Token(VMOp.DUPFROMALTSTACK, node)
        self.Emit_Integer(global_postion, node)
        self.Emit_Token(VMOp.PICKITEM, node)

    def Emit_LoadGlobal(self, position, global_postion, node):
        assert(position is not None and position >= 0)
        assert(global_postion is not None and global_postion >= 0)
        self.Emit_Token(VMOp.DUPFROMALTSTACK, node)
        self.Emit_Integer(global_postion, node)
        self.Emit_Token(VMOp.PICKITEM, node)
        self.Emit_Integer(position, node)
        self.Emit_Token(VMOp.PICKITEM, node)

    def Emit_StoreGlobal(self, position, global_postion, node):
        assert(position is not None and position >= 0)
        assert(global_postion is not None and global_postion >= 0)
        self.Emit_Token(VMOp.DUPFROMALTSTACK, node)
        self.Emit_Integer(global_postion, node)
        self.Emit_Token(VMOp.PICKITEM, node)
        self.Emit_Integer(position, node)
        self.Emit_Integer(2, node)
        self.Emit_Token(VMOp.ROLL, node)
        self.Emit_Token(VMOp.SETITEM, node)

    def Emit_LoadLocal(self, position, node):
        assert(position is not None and position >= 0)
        self.Emit_Token(VMOp.DUPFROMALTSTACK, node)
        self.Emit_Integer(position, node)
        self.Emit_Token(VMOp.PICKITEM, node)

    def Emit_StoreLocal(self, position, node):
        assert(position is not None and position >= 0)
        self.Emit_Token(VMOp.DUPFROMALTSTACK, node)
        self.Emit_Integer(position, node)
        self.Emit_Integer(2, node)
        self.Emit_Token(VMOp.ROLL, node)
        self.Emit_Token(VMOp.SETITEM, node)

    def Emit_Slice(self, node):
        # rotate so list is on the top, then move it to alt stack
        self.Emit_Token(VMOp.ROT, node)
        self.Emit_Token(VMOp.TOALTSTACK, node)
        # duplicate start index to alt stack
        self.Emit_Token(VMOp.DUP, node)
        self.Emit_Token(VMOp.TOALTSTACK, node)
        # subtract end index from start index, this is placed on the stack
        self.Emit_Token(VMOp.SUB, node)
        # get the start index and list from alt stack
        self.Emit_Token(VMOp.FROMALTSTACK, node)
        self.Emit_Token(VMOp.FROMALTSTACK, node)
        # swap the list and the start index
        self.Emit_Integer(2, node)
        self.Emit_Token(VMOp.XSWAP, node)
        # and now perform substr. whew.
        self.Emit_Token(VMOp.SUBSTR, node)

    def Emit_Builtins(self, op, node):
        syscall_name = None
        if op == 'len':
            return self.Emit_Token(VMOp.ARRAYSIZE, node)
        elif op == 'abs':
            return self.Emit_Token(VMOp.ABS, node)
        elif op == 'min':
            return self.Emit_Token(VMOp.MIN, node)
        elif op == 'max':
            return self.Emit_Token(VMOp.MAX, node)
        elif op == 'ord':
            self.Emit_Integer(0, node)
            self.Emit_Token(VMOp.ADD, node)
            return self.Emit_Token(VMOp.NOP, node)
        elif op == 'concat':
            return self.Emit_Token(VMOp.CAT, node)
        elif op == 'take':
            return self.Emit_Token(VMOp.LEFT, node)
        elif op == 'substr':
            return self.Emit_Token(VMOp.SUBSTR, node)
        elif op == 'keys':
            return self.Emit_Token(VMOp.KEYS, node)
        elif op == 'values':
            return self.Emit_Token(VMOp.VALUES, node)
        elif op == 'has_key':
            return self.Emit_Token(VMOp.HASKEY, node)
        elif op == 'sha1':
            return self.Emit_Token(VMOp.SHA1, node)
        elif op == 'sha256':
            return self.Emit_Token(VMOp.SHA256, node)
        elif op == 'hash160':
            return self.Emit_Token(VMOp.HASH160, node)
        elif op == 'hash256':
            return self.Emit_Token(VMOp.HASH256, node)
        elif op == 'verify_signature':
            return self.Emit_Token(VMOp.VERIFY, node)
        elif op == 'reverse':
            # no value returned. only used in attr call
            return self.Emit_Token(VMOp.REVERSE, node)
        elif op == 'reversed':
            # so dump here to return a reversed value.
            self.Emit_Token(VMOp.DUP, node)
            return self.Emit_Token(VMOp.REVERSE, node)
        elif op == 'append':
            return self.Emit_Token(VMOp.APPEND, node)
        elif op == 'remove':
            return self.Emit_Token(VMOp.REMOVE, node)
        elif op == 'Exception':
            return self.Emit_Token(VMOp.THROW, node)
        elif op == 'throw_if_null':
            return self.Emit_Token(VMOp.THROWIFNOT, node)
        elif op == 'breakpoint':
            return self.Emit_Token(VMOp.NOP, node)
        elif op == 'list':
            return self.Emit_Token(VMOp.NEWARRAY, node)
        elif op == 'print':
            sys_name = 'System.Runtime.Log'
            syscall_name = sys_name.encode('utf-8')

        if syscall_name:
            length = len(syscall_name)
            ba = bytearray([length]) + bytearray(syscall_name)
            vmtoken = self.Emit_Token(VMOp.SYSCALL, node, data=ba)
            vmtoken.syscall_name = sys_name
            return vmtoken

        return None
