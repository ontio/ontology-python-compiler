from ontology.code import pyop
from ontology.code.method import method as OntMethod
from ontology.code.action import action as OntAction
from ontology.code.appcall import appcall as OntAppcall

from ontology.util import BlockType, get_block_type
from bytecode import UNSET, Bytecode, BasicBlock, ControlFlowGraph, dump_bytecode, Label
from ontology.interop import VMOp
import importlib
from logzero import logger
from collections import OrderedDict
import os
import sys
import hashlib
from ontology import __version__
import json
from ontology.code.ast_preprocess import preprocess_method_body, ABI
import ast
from binascii import a2b_hex
from ontology.util import Digest

class Module(object):

    bc = None
    cfg = None

    blocks = None

    methods = None
    actions = None
    app_call_registrations = None

    path = None

    all_vm_tokens = OrderedDict()

    module_name = ''

    to_import = None

    _extra_instr = None

    _local_methods = None

    @property
    def extra_instructions(self):
        return self._extra_instr

    @property
    def local_methods(self):
        return self._local_methods

    @staticmethod
    def ImportFromBlock(block: BasicBlock, current_file_path):

        mpath = None
        mnames = []

        filepath = os.path.dirname(os.path.abspath(current_file_path))

        sys.path.append(filepath)

        for index, instr in enumerate(block):
            if instr.opcode == pyop.IMPORT_NAME:
                mpath = instr.arg
            elif instr.opcode == pyop.STORE_NAME:
                if instr.arg not in mnames:
                    mnames.append(instr.arg)
            elif instr.opcode == pyop.IMPORT_STAR:
                mnames = ['*']

        pymodule = importlib.import_module(mpath, mpath)
        filename = pymodule.__file__
        return Module(filename, mpath, mnames)

    @property
    def main(self):
        """
        Return the default method in this module.

        :return: the default method in this module
        :rtype: ``ontology.code.method.Method``
        """

        for m in self.methods:

            if m.name in ['Main', 'main']:
                return m

        if len(self.methods):
            return self.methods[0]

        return None

    @property
    def orderered_methods(self):
        """
        An ordered list of methods

        :return: A list of ordered methods is this module
        :rtype: list
        """

        oms = []

        self.methods.reverse()

        if self.main:
            oms = [self.main]

        for m in self.methods:

            if m == self.main:
                continue
            oms.append(m)

        return oms

    def method_by_name(self, method_name):
        """
        Look up a method by its name from the module ``methods`` list.
        :param method_name: the name of the method to look up
        :type method_name: str

        :return: the method ( if it is found)
        :rtype: ``ontology.code.method.Method``
        """

        #        print("METHODS FOR MODULE: %s " % self.path)
        for m in self.methods:
            if m.full_name == method_name or m.name == method_name:
                return m

        return None

    def has_method(self, full_name):
        for m in self.methods:
            if m.full_name == full_name:
                return True
        return False

    def __init__(self, path: str, module_name='', to_import=['*']):

        self.path = path
        self.to_import = to_import
        self.module_name = module_name
        self._local_methods = []
        self.abi = None
        source = open(path, 'rb')
        source_src = source.read()

        compiled_source = compile(source_src, path, 'exec')

        ast_tree = ast.parse(source_src)
        if module_name == '': 
            self.abi = ABI()
            self.abi.visit(ast_tree)

        self.bc = Bytecode.from_code(compiled_source)
        self.cfg = ControlFlowGraph.from_bytecode(self.bc)

        source.close()

        self.build()

    def build(self):
        self.blocks = []
        self.methods = []
        self.actions = []
        self.app_call_registrations = []

        for block in self.cfg:
            start_ln = block[0].lineno
            for index, instr in enumerate(block):
                if instr.lineno != start_ln:
                    self.cfg.split_block(block, index)

        self._extra_instr = []
        new_method_blks = []
        for blk in self.cfg:
            type = get_block_type(blk)
            if type == BlockType.MAKE_FUNCTION:
                new_method_blks.append(blk)
            elif type == BlockType.IMPORT_ITEM:
                new_module = Module.ImportFromBlock(blk, self.path)
                if new_module:
                    for method in new_module.methods:
                        if not self.has_method(method.full_name):
                            self.methods.append(method)
                    for method in new_module.local_methods:
                        self.methods.append(method)
                    self._extra_instr = self._extra_instr + new_module.extra_instructions
            elif type == BlockType.UNKNOWN:
                self._extra_instr.append(blk)
            elif type == BlockType.CALL_FUNCTION:
                self._extra_instr.append(blk)
            elif type == BlockType.ACTION_REG:
                self.actions.append(OntAction(blk))
            elif type == BlockType.MAKE_CLASS:
                pass
            elif type == BlockType.APPCALL_REG:
                self.app_call_registrations.append(OntAppcall(blk))

        for m in new_method_blks:

            new_method = OntMethod(self, m, self.module_name, self._extra_instr)

            if not self.has_method(new_method.full_name):
                self.methods.append(new_method)

    def write(self):
        """
        Write the current module to a byte string.

        Note that if you are using the ``Compiler.load('path/to/file.py')``, you must
        call ``module.write()`` before any inspection of the module is possible.

        :return: A bytestring of representing the current module
        :rtype: bytes
        """
        self.link_methods()

        return self.write_methods()

    def write_methods(self):
        """
        Write all methods in the current module to a byte string.

        :return: A bytestring of all current methods in this module
        :rtype: bytes
        """

        b_array = bytearray()
        for key, vm_token in self.all_vm_tokens.items():

            b_array.append(vm_token.out_op)

            if vm_token.data is not None and vm_token.vm_op != VMOp.NOP:
                b_array = b_array + vm_token.data

#        self.to_s()
        return b_array

    def link_methods(self):
        """
        Perform linkage of addresses between methods.
        """

        for method in self.methods:
            method.prepare()

        self.all_vm_tokens = OrderedDict()

        address = 0

        for method in self.orderered_methods:

            if not method.is_interop:
                #                print("ADDING METHOD %s " % method.full_name)
                method.address = address

                for key, vmtoken in method.vm_tokens.items():
                    self.all_vm_tokens[address] = vmtoken
                    address += 1

                    if vmtoken.data is not None and vmtoken.vm_op != VMOp.NOP:
                        address += len(vmtoken.data)

                    vmtoken.addr = vmtoken.addr + method.address

        # loop through once to see if there are any local methods to add
#        local_count = 0
#        for key, vmtoken in self.all_vm_tokens.items():
#            if vmtoken.src_method is not None:
#                target_method, is_local = self.method_by_name(vmtoken.target_method)
#                if is_local:
#                    local_count+=1
#        if local_count > 0:
#            return self.link_methods()

        for key, vmtoken in self.all_vm_tokens.items():
            if vmtoken.src_method is not None:

                target_method = self.method_by_name(vmtoken.target_method)
                if target_method:
                    jump_len = target_method.address - vmtoken.addr
                    vmtoken.data = jump_len.to_bytes(2, 'little', signed=True)
                else:
                    raise Exception("Target method %s not found" % vmtoken.target_method)

    def export_debug(self, output_path, data):
        """
        this method is used to generate a debug map for NEO debugger
        """

        hashstr = Digest.hash160(msg=data, is_hex=True) # str
        a2bhashstr = bytearray(a2b_hex(hashstr)) # str ==> bytes ==>bytearray
        a2bhashstr.reverse()
        file_hash = a2bhashstr.hex() # bytearray ==> str

        avm_name = os.path.splitext(os.path.basename(output_path))[0]
        json_data = self.generate_debug_json(avm_name, file_hash)
        mapfilename = output_path.replace('.avm', '.debug.json')
        with open(mapfilename, 'w+') as out_file:
            out_file.write(json_data)

        if self.abi != None:

            self.abi.ABI_result["CompilerVersion"] = __version__
            self.abi.ABI_result["hash"] = file_hash
            self.abi.ABI_result["entrypoint"] = self.main.name
            self.abi.ABI_result["functions"] = self.abi.AbiFunclist
            json_data = json.dumps(self.abi.ABI_result, indent=4)
            fullpath = os.path.realpath(self.path)
            path, filename = os.path.split(fullpath)
            newfilename = filename.replace('.py', '.abi.json')
            mapfilename = '%s/%s' % (path, newfilename)
            with open(mapfilename, 'w+') as out_file:
                out_file.write(json_data)

    def generate_method_var_map(self):
        FunctionsVarMap = []
        for method in self.methods:
            FunctionsVarMap.append({"Method":method.name, "VarMap":method.scope})

        FunctionsVarMap_t = {"Functions": FunctionsVarMap}

        json_data = json.dumps(FunctionsVarMap_t, indent=4)

        fullpath = os.path.realpath(self.path)
        path, filename = os.path.split(fullpath)
        newfilename = filename.replace('.py', '.FuncMap.json')
        mapfilename = '%s/%s' % (path, newfilename)

        with open(mapfilename, 'w+') as out_file:
            out_file.write(json_data)

    def generate_debug_json(self, avm_name, file_hash):

        # Initialize if needed
        if self.all_vm_tokens is None:
            self.link_methods()

        lineno = 0

        data = {}
        data['avm'] = {'name': avm_name, 'hash': file_hash}
        data['compiler'] = {'name': 'ontology-python-compile', 'version': __version__}

        files = {}
        breakpoints = []
        data['files'] = files

        map = []
        start_ofs = -1
        last_ofs = 0
        fileid = 0
        last_fileid = 0
        pt = None
        global_lineno = None
        fixed_pt_lineno = False
        for i, (key, value) in enumerate(self.all_vm_tokens.items()):
            if value.pytoken:
                pt = value.pytoken

                if pt.file:
                    if pt.file not in files.keys():
                        fileid = len(files.values()) + 1
                        files[pt.file] = fileid
                    else:
                        fileid = files[pt.file]

                current_global_lineno = pt.method_lineno + pt.lineno
                if pt.lineno > OntMethod.MAX_FILE_LINENO:
                    fixed_pt_lineno = True
                    pt.instruction.lineno = pt.lineno - OntMethod.MAX_FILE_LINENO
                    current_global_lineno = pt.lineno

                if current_global_lineno != global_lineno or fileid != last_fileid:
                    if start_ofs >= 0:
                        map.append({'start': start_ofs, 'end': key - 1, 'file': last_fileid, 'method': lastline_Method,
                                    'line': lineno, 'file_line_no': global_lineno})
                    start_ofs = key
                    lineno = pt.lineno
                    global_lineno = current_global_lineno
                    lastline_Method = pt.method_name
                    last_fileid = fileid

                if pt.is_breakpoint:
                    breakpoints.append(start_ofs)

                if fixed_pt_lineno:
                    fixed_pt_lineno = False    # instr is shared between global blocks. and multi method may use the the same global blocks
                    pt.instruction.lineno = pt.lineno + OntMethod.MAX_FILE_LINENO
                last_ofs = key

        if last_ofs >= 0:
            map.append({'start': start_ofs, 'end': key , 'file': fileid, 'method': pt.method_name,
                        'line': lineno, 'file_line_no': current_global_lineno})

        data['map'] = map
        data['breakpoints'] = breakpoints
        data['files'] = [{'id': val, 'url': os.path.abspath(key)} for key, val in files.items()]
        json_data = json.dumps(data, indent=4)
        self.generate_method_var_map()
        return json_data

    def to_s(self):
        # Initialize if needed
        if self.all_vm_tokens is None:
            self.link_methods()

        lineno = 0
        pstart = True
        global_lineno = None
        ds = ''
        pytoken_name = ''
        lastfile = ''
        fixed_pt_lineno = False

        for i, (key, value) in enumerate(self.all_vm_tokens.items()):
            do_print_line_no = False
            from_label = '    '
            current_global_lineno  = ''

            pytoken_name = ''
            if value.pytoken:
                pt = value.pytoken
                do_print_line_no = False
                to_label = None
                from_label = '    '

                current_global_lineno = pt.method_lineno + pt.lineno
                if pt.lineno > OntMethod.MAX_FILE_LINENO :
                    fixed_pt_lineno = True
                    pt.instruction.lineno = pt.lineno - OntMethod.MAX_FILE_LINENO 
                    current_global_lineno = pt.lineno

                if current_global_lineno != global_lineno or pt.file != lastfile:
                    print("\n")
                    lineno = pt.lineno
                    global_lineno = current_global_lineno
                    do_print_line_no = True
                    if pt.file != lastfile:
                        lastfile = pt.file
                        print("filename:", pt.file)

                ds = ''
                if value.data is not None:
                    try:
                        ds = int.from_bytes(value.data, 'little', signed=True)
                    except Exception as e:
                        pass
                    if type(ds) is not int and len(ds) < 1:
                        try:
                            ds = value.data.decode('utf-8')
                        except Exception as e:
                            pass

                if fixed_pt_lineno:
                    fixed_pt_lineno = False
                    pt.instruction.lineno = pt.lineno + OntMethod.MAX_FILE_LINENO

                arg_str = pt.arg_str
                pytoken_name = pt.instruction.name

            VMOP_name = VMOp.to_name(value.vm_op)
            if (type(VMOP_name) == type(None)):
                VMOP_name = 'PUSHBYTES' + str(value.vm_op)

            lno = "{:<10}".format(
                current_global_lineno if do_print_line_no or pstart else '')

            addr = "{:<5}".format(key)
            if value.pytoken:
                op = "{:<30}".format(VMOP_name + '(' + pytoken_name + ')')
            else:
                op = "{:<30}".format(VMOP_name)

            arg = "{:<50}".format(arg_str if value.pytoken else '')
            data = "[data] {:<20}".format(ds)
            print("%s%s%s%s%s%s" % (lno, from_label, addr, op, arg, data))

            pstart = False

