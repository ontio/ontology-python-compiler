import ast
import os
import binascii
import importlib
import json
import sys
import re

from ontology.util import Digest
from ontology.code.astvmtoken import AstVMTokenizer
from ontology.interop import VMOp
from binascii import a2b_hex
from ontology import __version__
from ontology.code.StaticAppCall import RegisterAppCall, NotifyAction

# Global arg set.
ONTOLOGY_SC_FRAMEWORK = 'ontology.interop.'
ONTOLOGY_SC_FRAMEWORK_boa = 'boa.interop.'
ONTOLOGY_BUILTINS_M = 'ontology.builtins'
ONTOLOGY_BUILTINS_M_boa = 'boa.builtins'
OwnMainModule = 'OwnMainModule'
ForIndexPrefix = 'ForIndexPrefix_Var###'
ListCompName = 'ListCompName###'
ref_type_local = 'Local'
ref_type_global = 'Global'
Builtins_Module = 'ontology.builtins'
Global_VarEnv = 'Global_VarEnv###FixedName'
Local_ArgLen = 'Local_ArgLen###FixedName'
Function_Call_Arglen = 'Function_Call_Arglen###FixedName'
Global_simulation_func_name = 'Global#Code'
BUILTIN_AND_SYSCALL_LABEL_ADDR = -2
# keys, values, has_key current not support
# buildins_list           = ['state', 'bytes', 'bytearray', 'ToScriptHash', 'print', 'list', 'len', 'abs', 'min', 'max', 'concat', 'take', 'substr', 'keys', 'values', 'has_key', 'sha1', 'sha256', 'hash160', 'hash256', 'verify_signature', 'reverse', 'append', 'remove', 'Exception', 'throw_if_null', 'breakpoint']
ONE_LINE_EXPR_SUPPORT_AST_TYPE = ['Pass', 'Str']
# xxx. Migrate have return value acctually.
WITHOUT_RETURN_BUILTINSYSCALL = ['print', 'Log', 'throw_if_null', 'breakpoint', 'Notify', 'Put', 'Destroy', 'Delete', 'Exception']
# all these three List_Attr_func assumed no return value.
List_Attr_func = ['append', 'remove', 'reverse']
warning_file_path = None


def print_location():
    f_frame = sys._getframe().f_back
    print("Location: ", f_frame.f_code.co_filename, f_frame.f_lineno, f_frame.f_code.co_name)


def Print_DoNot_Support(func_desc, node, message):
    raise Exception("[Compiler ERROR. File: %s. in function: %s. Line: %d]. The Neptune Compiler does not support %s" % (func_desc.filepath, func_desc.name, node.lineno, message))


def Print_Error(func_desc, node, message):
    raise Exception("[Compiler ERROR. File: %s. in function: %s. Line: %d]. %s" % (func_desc.filepath, func_desc.name, node.lineno, message))


def Print_Not_Support(filepath, node, message):
    raise Exception("[Compiler ERROR. File: %s. Line: %d]. The Neptune Compiler does not support %s" % (filepath, node.lineno, message))


def Print_Error_global(filepath, node, message):
    raise Exception("[Compiler ERROR. File: %s. Line: %d]. %s" % (filepath, node.lineno, message))


def Print_Warning_global(filepath, node, message):
    assert(warning_file_path is not None)
    message_w = "[Compiler WARNING. File: %s. Line: %d.] %s" % (filepath, node.lineno, message)
    print(message_w)
    with open(warning_file_path, 'a+') as out_file:
        out_file.write(message_w)


class Visit_FirstGlobalNode(ast.NodeVisitor):
    def __init__(self):
        self.first_global_node = None

    def generic_visit(self, node):
        self.first_global_node = node

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)
            if self.first_global_node is not None:
                break

    def visit_Import(self, node):
        pass

    def visit_ImportFrom(self, node):
        pass


class generic_modify_node(ast.NodeTransformer):
    def generic_visit(self, node):
        if hasattr(node, "lineno"):
            self.parent_node_lineno = node.lineno
            self.parent_node_col = node.col_offset
        ast.NodeVisitor.generic_visit(self, node)
        return node

    def visit_In(self, node):
        node.lineno = self.parent_node_lineno
        node.col_offset = self.parent_node_col
        return node

    def visit_NotIn(self, node):
        node.lineno = self.parent_node_lineno
        node.col_offset = self.parent_node_col
        return node

    def visit_arguments(self, node):
        node.lineno = self.parent_node_lineno
        node.col_offset = self.parent_node_col
        return node


class ReWrite_CTX_STORE_TO_LOAD(ast.NodeTransformer):
    def __init__(self, func_desc):
        self.func_desc = func_desc

    def visit_Name(self, node):
        assert(type(node.ctx).__name__ == 'Store')
        node.ctx = ast.Load()
        return node

    def visit_Subscript(self, node):
        assert(type(node.ctx).__name__ == 'Store')
        node.ctx = ast.Load()
        return node

    def visit_List(self, node):
        assert(type(node.ctx).__name__ == 'Store')
        Print_DoNot_Support(self.func_desc, node, "List Store type")

    def visit_Tuple(self, node):
        assert(type(node.ctx).__name__ == 'Store')
        Print_DoNot_Support(self.func_desc, node, "Tuple Store type")

    def visit_Attribute(self, node):
        assert(type(node.ctx).__name__ == 'Store')
        Print_DoNot_Support(self.func_desc, node, "Attrubute Store type")


class ReWrite_CTX_LOAD_TO_STORE(ast.NodeTransformer):
    def visit_Name(self, node):
        assert(type(node.ctx).__name__ == 'Load')
        node.ctx = ast.Store()
        return node

    def visit_Subscript(self, node):
        assert(type(node.ctx).__name__ == 'Load')
        node.ctx = ast.Store()
        return node


class CVersion_Visitor(ast.NodeVisitor):
    def __init__(self, codegencontext):
        self.OntCversion = None
        self.codegencontext = codegencontext

    def generic_visit(self, node):
        if hasattr(node, 'lineno') and node.lineno == 1:
            if type(node).__name__ == 'Assign' and len(node.targets) == 1 and type(node.targets[0]).__name__ == 'Name' and type(node.value).__name__ == 'Str':
                self.OntCversion = node.value.s
                if self.OntCversion != __version__ or node.targets[0].id != 'OntCversion':
                    Print_Warning_global(self.codegencontext.main_file_path, node, "Place 'OntCversion = '%s'' at 1st line of SmartContract." % (__version__))
            else:
                Print_Warning_global(self.codegencontext.main_file_path, node, "Place 'OntCversion = '%s'' at 1st line of SmartContract" % (__version__))
            return

        Print_Warning_global(self.codegencontext.main_file_path, node, "Place 'OntCversion = '%s'' at 1st line of SmartContract" % (__version__))

    def visit_Module(self, node):
        self.generic_visit(node.body[0])


class FuncVisitor_Of_AnalyzeReturnValue(ast.NodeVisitor):
    def __init__(self, func_desc):
        self.func_desc = func_desc
        self.current_node = None
        self.already_visited = False
        self.visit_returned = False

    def Print_DoNot_Support(self, node, message):
        raise Exception("[Compiler ERROR. File: %s in function: %s Line: %d]. The Neptune Compiler does not support %s" % (self.func_desc.filepath, self.func_desc.name, node.lineno, message))

    def Print_Error(self, node, message):
        raise Exception("[Compiler ERROR. File: %s in function: %s Line: %d]. %s" % (self.func_desc.filepath, self.func_desc.name, node.lineno, message))

    def visit_FunctionDef(self, node):
        self.current_node = node
        if self.already_visited:
            self.Print_DoNot_Support(node, "function define in function.")
        self.already_visited = True

        if node.decorator_list != []:
            self.Print_DoNot_Support(node, "decorator.")
        self.generic_visit(node)

    def visit_Return(self, node):
        self.current_node = node
        if self.func_desc.have_return_value and node.value is None:
            self.Print_Error(node, "You are returning a value and None, this will result in an error.")

        if self.visit_returned and (not self.func_desc.have_return_value) and node.value is not None:
            self.Print_Error(node, "You are returning a value and None, this will result in an error.")

        if node.value is not None:
            self.func_desc.have_return_value = True

        self.visit_returned = True


class Abivisitor_step0(ast.NodeVisitor):
    def __init__(self):
        self.Funclist = []
        self.checking_abilist = False

    def visit_FunctionDef(self, node):
        self.checking_abilist = False
        if node.name == 'Main' or node.name == 'main':
            self.checking_abilist = True
            self.generic_visit(node)
        self.checking_abilist = False

    def visit_Compare(self, node):
        if self.checking_abilist and type(node.left).__name__ == 'Name' and node.left.id == 'operation' and len(node.ops) == 1 and type(node.ops[0]).__name__ == 'Eq' and len(node.comparators) == 1 and type(node.comparators[0]).__name__ == 'Str':
            self.Funclist.append(node.comparators[0].s)


class Abivisitor_step1(ast.NodeVisitor):
    def __init__(self, funclist):
        self.Funclist = funclist
        self.AbiFunclist = []

    def visit_FunctionDef(self, node):
        args = []
        if node.name in self.Funclist:
            # contruct args list first
            for arg in node.args.args:
                args.append({"name": arg.arg, "type": ""})

            self.AbiFunclist.append({"name": node.name, "parameters": args})


class FuncVisitor_Of_StackSize(ast.NodeVisitor):
    def __init__(self, func_desc, is_global):
        self.stack_size = 0
        self.func_desc = func_desc
        self.already_visited = False
        self.current_node = None
        self.arg_num = 0
        self.is_global = is_global

    def generic_visit(self, node):
        self.current_node = node
        ast.NodeVisitor.generic_visit(self, node)

    def Print_DoNot_Support(self, node, message):
        if hasattr(node, 'lineno'):
            raise Exception("[Compiler ERROR. File: %s. in function: %s. Line: %d]. The Neptune Compiler does not support %s" % (self.func_desc.filepath, self.func_desc.name, node.lineno, message))
        else:
            raise Exception("[Compiler ERROR. File: %s. in function: %s. ]. The Neptune Compiler does not support %s" % (self.func_desc.filepath, self.func_desc.name, message))

    def Print_Error(self, node, message):
        raise Exception("[Compiler ERROR. File: %s. in function: %s. Line: %d]. %s" % (self.func_desc.filepath, self.func_desc.name, node.lineno, message))

    def visit_FunctionDef(self, node):
        if self.is_global:
            return
        self.current_node = node
        if self.already_visited:
            self.Print_DoNot_Support(node, "Cannot define a function within another function.")
        self.already_visited = True

        if node.decorator_list != []:
            self.Print_DoNot_Support(node, "decorator.")

        self.generic_visit(node)

    def visit_Assign(self, node):
        self.current_node = node
        self.stack_size += len(node.targets)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        self.current_node = node
        self.stack_size += 1
        self.generic_visit(node)

    def visit_arguments(self, node):
        if self.is_global:
            assert(False)

        self.current_node = node

        if node.kwonlyargs != [] or node.kw_defaults != []:
            self.Print_DoNot_Support(node, "kwonlyargs or kw_defaults.")

        if node.kwarg is not None:
            self.Print_DoNot_Support(node, "kwarg.")

        self.func_desc.necessary_arglen = len(node.args) - len(node.defaults)
        self.func_desc.default_arglen = len(node.defaults)
        if node.vararg is not None:
            self.func_desc.have_vararg = True

        self.func_desc.arg_num = len(node.args)
        self.arg_num = len(node.args)
        self.stack_size += len(node.args)

    def visit_Return(self, node):
        if self.is_global:
            assert(False)
        self.current_node = node
        self.stack_size += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.current_node = node
        # index, result, iter, len
        self.stack_size += 4
        self.generic_visit(node)

    def visit_comprehension(self, node):
        self.stack_size += 4
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.stack_size += 1
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.stack_size += 1
        self.generic_visit(node)


class Visitor_Of_Global(ast.NodeVisitor):
    def __init__(self, codegencontext):
        self.global_num = 0
        self.codegencontext = codegencontext

    def visit_Return(self, node):
        Print_Error_global(self.codegencontext.main_file_path, node, "can not \"return\" outside of function.")

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        pass

    def visit_Assign(self, node):
        if type(node.value).__name__ == 'Call' and type(node.value.func).__name__ == 'Name' and (node.value.func.id == 'RegisterAppCall' or node.value.func.id == 'RegisterAction'):
            if self.codegencontext.funcscope[node.value.func.id].isyscall and node.value.func.id == 'RegisterAppCall':
                assert(len(node.targets) == 1)
                assert(type(node.targets[0]).__name__ == 'Name')
                register_func_name = node.targets[0].id
                newfunc = FuncDescription(register_func_name, None, node.targets[0], True, self.codegencontext.main_file_path, OwnMainModule, False)
                self.codegencontext.funcscope[newfunc.name] = newfunc
                args = node.value.args
                newfunc.arg_num = len(args) - 1
                newfunc.is_register_call = True
                new_app_call = RegisterAppCall(register_func_name, args)
                assert(newfunc.arg_num >= 0)
                if register_func_name in self.codegencontext.register_appcall.keys():
                    Print_Error_global(self.codegencontext.main_file_path, node, "%s registered before." % (register_func_name))
                self.codegencontext.register_appcall[register_func_name] = new_app_call
                return
            elif self.codegencontext.funcscope[node.value.func.id].isyscall and node.value.func.id == 'RegisterAction':
                assert(len(node.targets) == 1)
                assert(type(node.targets[0]).__name__ == 'Name')
                register_func_name = node.targets[0].id
                newfunc = FuncDescription(register_func_name, None, node.targets[0], True, self.codegencontext.main_file_path, OwnMainModule, False)
                self.codegencontext.funcscope[newfunc.name] = newfunc
                args = node.value.args
                newfunc.arg_num = len(args) - 1
                newfunc.is_register_call = True
                assert(newfunc.arg_num >= 0)
                newaction = NotifyAction(register_func_name, args)
                if register_func_name in self.codegencontext.register_action.keys():
                    Print_Error_global(self.codegencontext.main_file_path, node, "%s registered before." % (register_func_name))
                self.codegencontext.register_action[register_func_name] = newaction
                return
            else:
                assert(False)

        self.global_num += len(node.targets)
        self.generic_visit(node)


class Visitor_Of_FuncDecl(ast.NodeVisitor):
    def __init__(self, codegencontext, visited_module, list_func_imported):
        self.main_func_node = None
        self.visited_module = visited_module
        self.codegencontext = codegencontext
        self.isyscall_module = False
        self.is_builtin_module = False
        self.is_main_module = False
        self.list_func_imported = list_func_imported
        if visited_module == OwnMainModule:
            self.is_main_module = True
            assert(self.list_func_imported is None)

        if visited_module != OwnMainModule:
            pymodule = importlib.import_module(visited_module, visited_module)
            module_file_path = pymodule.__file__
            source = open(module_file_path, 'rb')
            source_src = source.read()
            self.module_file_path = module_file_path
            self.module_ast_tree = ast.parse(source_src)
        else:
            self.module_file_path = self.codegencontext.main_file_path
            self.module_ast_tree = self.codegencontext.main_astree

        if (ONTOLOGY_SC_FRAMEWORK in self.visited_module) or (ONTOLOGY_SC_FRAMEWORK_boa in self.visited_module):
            self.isyscall_module = True
        elif (self.visited_module == ONTOLOGY_BUILTINS_M) or (self.visited_module == ONTOLOGY_BUILTINS_M_boa):
            self.is_builtin_module = True

        assert(not (self.isyscall_module and self.is_builtin_module))

    # here do not need visit the children node. so do not call the generic_visit.
    def visit_FunctionDef(self, node):
        if node.name == 'main' or node.name == 'Main':
            if not self.is_main_module:
                Print_Error_global(self.module_file_path, node, "%s was Imported. Can not have Main func other the main file of your project." % (self.visited_module))

            self.main_func_node = node
            return

        if self.is_main_module:
            assert(self.list_func_imported is None)
            self.codegencontext.NewFunc(node, self.isyscall_module, self.module_file_path, self.visited_module, False)
        else:
            assert(self.list_func_imported != [])
            # only add import func
            if '*' in self.list_func_imported or node.name in self.list_func_imported:
                if node.name == 'range':
                    self.codegencontext.NewFunc(node, self.isyscall_module, self.module_file_path, self.visited_module, False)
                else:
                    self.codegencontext.NewFunc(node, self.isyscall_module, self.module_file_path, self.visited_module, self.is_builtin_module)
                # if func be added. then added the depend import. so if you want resolve the depend auto. add the dependence in the first line of function.
                self.generic_visit(node)

    def visit_Import(self, node):
        # all func will add to funcscope
        list_func_imported = ['*']
        # ResolveFuncDecl all
        for alias in node.names:
            self.codegencontext.ResolveFuncDecl(alias.name, list_func_imported)

    def visit_ImportFrom(self, node):
        # assert import func first
        list_func_imported = []
        for alias in node.names:
            list_func_imported.append(alias.name)
            if alias.name == 'range' and (node.module == ONTOLOGY_BUILTINS_M or node.module == ONTOLOGY_BUILTINS_M_boa):
                # range depend on list
                list_func_imported.append('list')
            if alias.asname is not None:
                Print_Not_Support(self.module_file_path, node, "from ... import .. as ..")

        self.codegencontext.ResolveFuncDecl(node.module, list_func_imported)


class Visitor_Of_FunCodeGen(ast.NodeVisitor):
    def __init__(self, codegencontext, func_desc, is_for_global=False):
        self.codegencontext = codegencontext
        self.func_desc = func_desc
        self.already_visited = False
        self.is_for_global = is_for_global
        self.current_node = None
        self.latest_loop_break_label = []
        self.is_in_loop = False
        self.codegencontext.tokenizer.current_func = func_desc
        self.codegencontext.tokenizer.global_converting = is_for_global
        self.main_func_node = None
        self.global_declare = []

    def Get_FuncDesc(self, funcname, node):
        return self.codegencontext.Get_FuncDesc(funcname, node, self.func_desc.filepath)

    # so when get a bug need check in this func. is there any node should transfered do not transfer.
    def generic_visit(self, node):
        self.current_node = node
        # ast.NodeVisitor.generic_visit(self, node)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        self.current_node = node
        self.Print_DoNot_Support(node, "Class def.")

    def Print_DoNot_Support(self, node, message):
        raise Exception("[Compiler ERROR. File: %s. in function: %s. Line: %d]. The Neptune Compiler does not support %s" % (self.func_desc.filepath, self.func_desc.name, node.lineno, message))

    def Print_Error(self, node, message):
        raise Exception("[Compiler ERROR. File: %s. in function: %s. Line: %d]. %s" % (self.func_desc.filepath, self.func_desc.name, node.lineno, message))

    def visit_Module(self, node):
        self.current_node = node
        if not self.is_for_global:
            self.Print_Error(node, "Impossible get Module in Function decl.")
            assert(False)

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.current_node = node

        if self.is_for_global:
            if node.name == 'main' or node.name == 'Main':
                self.main_func_node = node
            return

        if self.already_visited:
            self.Print_DoNot_Support("Function define in function.")

        self.already_visited = True

        fixed_line_visitor = generic_modify_node()
        fixed_line_visitor.visit(node)

        if not (self.func_desc.isyscall or self.func_desc.is_builtin):
            # syscall and builtin get no func code. so do not set the label
            if node.name != 'Main' and node.name != 'main':
                self.codegencontext.SetLabel(self.codegencontext.funcscope[node.name].label, self.codegencontext.pc + 1)

            self.codegencontext.tokenizer.build_function_stack(self.func_desc.stack_size, self.func_desc.func_ast)
            # ast.fix_missing_locations(node)
            self.generic_visit(node)

            if type(node.body[-1]).__name__ != 'Return':
                self.codegencontext.tokenizer.Emit_Token(VMOp.FROMALTSTACK, node.body[-1])
                self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node.body[-1])
                self.codegencontext.tokenizer.Emit_Token(VMOp.RET, node.body[-1])
        else:
            self.codegencontext.SetLabel(self.codegencontext.funcscope[node.name].label, BUILTIN_AND_SYSCALL_LABEL_ADDR)
            return

    def visit_arguments(self, node):
        self.current_node = node
        if self.is_for_global:
            self.Print_Error(node, "Compiler Bug. Global can not have argument.")
            assert(False)

        if node.kwonlyargs != [] or node.kw_defaults != []:
            self.Print_DoNot_Support(node, "kwonlyargs or kw_defaults.")

        if node.kwarg is not None:
            self.Print_DoNot_Support(node, "kwarg.")

        if self.func_desc.isyscall or self.func_desc.is_builtin:
            self.Print_Error(node, "Compiler Bug. builtins or syscall should not handle arguments. ")

        # set global first
        GlobalArgNode = ast.Name(id=Global_VarEnv, ctx=ast.Load())
        ast.copy_location(GlobalArgNode, node)
        position = self.func_desc.NewLocal(Global_VarEnv, GlobalArgNode)
        self.codegencontext.tokenizer.Emit_StoreLocal(position, GlobalArgNode)

        # set args len passed by caller
        if not (self.func_desc.name == 'Main' or self.func_desc.name == 'main'):
            Local_ArgLenposition = self.func_desc.NewLocal(Local_ArgLen, node)
            self.codegencontext.tokenizer.Emit_StoreLocal(Local_ArgLenposition, node)

        # alloc args position. and check redefined.
        for arg in node.args:
            self.func_desc.NewLocal(arg.arg, arg)

        if node.vararg is not None:
            vararg_position = self.func_desc.NewLocal(node.vararg.arg, node.vararg)

        # calculate basic num.
        AllArg_len = len(node.args)
        DefaultArg_len = len(node.defaults)
        NecessaryArg_len = AllArg_len - DefaultArg_len
        default_label_list = {}
        assert(NecessaryArg_len >= 0)
        assert(DefaultArg_len <= AllArg_len)

        # set NecessaryArg first. compile will change args less than NecessaryArg_len
        iter_len = 0
        while iter_len < NecessaryArg_len:
            arg = node.args[iter_len]
            position = self.func_desc.Read_LocalStackPosition(arg.arg, arg)
            assert(position is not None)
            self.codegencontext.tokenizer.Emit_StoreLocal(position, arg)
            iter_len += 1

        # Main function can only have NecessaryArg.
        if self.func_desc.name == 'Main' or self.func_desc.name == 'main':
            if node.vararg is not None or AllArg_len != NecessaryArg_len or DefaultArg_len != 0:
                self.Print_Error(node, "Function \"Main\" can not have default arg or vararg.")
            return

        assert(iter_len == NecessaryArg_len)

        # alloc the function body_label. set the address last at the argument avm code.
        body_label = self.codegencontext.NewLabel()
        body_label_bytes = body_label.to_bytes(2, 'little', signed=True)

        # blow code check the arg len passed by caller if the passed arglen equal iter_len. start from NecessaryArg_len.
        iter_len = NecessaryArg_len
        while iter_len < AllArg_len:
            # alloc the label
            nextif = self.codegencontext.NewLabel()
            nextif_bytes = nextif.to_bytes(2, 'little', signed=True)
            self.codegencontext.tokenizer.Emit_LoadLocal(Local_ArgLenposition, node)
            self.codegencontext.tokenizer.Emit_Integer(iter_len, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.NUMEQUAL, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, nextif_bytes)

            # if true. will asume the passed arg have iter_len
            set_defaults_bypassed_num = iter_len - NecessaryArg_len  # must start from 0
            start_default_arg_index = NecessaryArg_len
            default_label = self.codegencontext.NewLabel()
            ii = set_defaults_bypassed_num
            default_label_list[set_defaults_bypassed_num] = default_label
            default_label_bytes = default_label.to_bytes(2, 'little', signed=True)

            # set all default args passed by caller. ii indicated the number default arg set by caller. if all arg NecessaryArg. ii will be 0.
            while ii > 0:
                arg = node.args[start_default_arg_index]
                position = self.func_desc.Read_LocalStackPosition(arg.arg, arg)
                assert(position is not None)
                self.codegencontext.tokenizer.Emit_StoreLocal(position, arg)
                ii -= 1
                start_default_arg_index += 1

            self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, node, default_label_bytes)
            self.codegencontext.SetLabel(nextif, self.codegencontext.pc + 1)
            iter_len += 1

        # generate the if len == AllArg_len code.
        set_defaults_bypassed_num = AllArg_len - NecessaryArg_len  # must start from 0
        start_default_arg_index = NecessaryArg_len
        ii = set_defaults_bypassed_num
        vararg_empty_label = self.codegencontext.NewLabel()
        vararg_empty_label_bytes = vararg_empty_label.to_bytes(2, 'little', signed=True)
        assert(iter_len == AllArg_len)
        assert(set_defaults_bypassed_num == DefaultArg_len)

        while ii > 0:
            arg = node.args[start_default_arg_index]
            position = self.func_desc.Read_LocalStackPosition(arg.arg, arg)
            assert(position is not None)
            self.codegencontext.tokenizer.Emit_StoreLocal(position, arg)
            ii -= 1
            start_default_arg_index += 1

        if node.vararg is not None:
            vararg_less_label = self.codegencontext.NewLabel()
            vararg_less_label_bytes = vararg_less_label.to_bytes(2, 'little', signed=True)
            self.codegencontext.tokenizer.Emit_LoadLocal(Local_ArgLenposition, node.vararg)
            self.codegencontext.tokenizer.Emit_Integer(iter_len, node.vararg)
            self.codegencontext.tokenizer.Emit_Token(VMOp.SUB, node.vararg)
            self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node.vararg)
            self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH0, node.vararg)
            self.codegencontext.tokenizer.Emit_Token(VMOp.GT, node.vararg)
            self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node.vararg, vararg_less_label_bytes)
            self.codegencontext.tokenizer.Emit_Token(VMOp.PACK, node.vararg)
            self.codegencontext.tokenizer.Emit_StoreLocal(vararg_position, node.vararg)
            self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, node.vararg, body_label_bytes)

            self.codegencontext.SetLabel(vararg_less_label, self.codegencontext.pc + 1)
            self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node.vararg)

        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, node, vararg_empty_label_bytes)

        # make new label. and set all defaults.
        start_default_arg_index = NecessaryArg_len
        for i in range(DefaultArg_len):
            default_label = default_label_list[i]
            default_expr = node.defaults[i]
            self.codegencontext.SetLabel(default_label, self.codegencontext.pc + 1)
            self.visit(default_expr)
            arg = node.args[start_default_arg_index + i]
            position = self.func_desc.Read_LocalStackPosition(arg.arg, arg)
            assert(position is not None)
            self.codegencontext.tokenizer.Emit_StoreLocal(position, arg)

        # make empty vararg. set last default_label to current address.
        assert(len(default_label_list) == DefaultArg_len)
        self.codegencontext.SetLabel(vararg_empty_label, self.codegencontext.pc + 1)
        if node.vararg is not None:
            self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH0, node.vararg)
            self.codegencontext.tokenizer.Emit_Token(VMOp.NEWARRAY, node.vararg)
            self.codegencontext.tokenizer.Emit_StoreLocal(vararg_position, node.vararg)

        self.codegencontext.SetLabel(body_label, self.codegencontext.pc + 1)

    def Convert_Global(self):
        if self.func_desc.blong_module_name != OwnMainModule:
            return

        # global own the visitor by itself. but note the tokenizer confict.
        CodeGenVisitor = Visitor_Of_FunCodeGen(self.codegencontext, self.func_desc, True)
        # due the  args translate first. so get the argname have the upper priority. so if have the same name of args and the global.
        CodeGenVisitor.visit(self.codegencontext.main_astree)

    def visit_Assign(self, node):
        self.current_node = node
        self.visit(node.value)

        if type(node.value).__name__ == 'Call' and type(node.value.func).__name__ == 'Name' and (node.value.func.id == 'RegisterAppCall' or node.value.func.id == 'RegisterAction'):
            return

        for target in node.targets:
            if len(node.targets) > 1:
                self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, target)
            self.visit(target)

        if len(node.targets) > 1:
            self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, target)

    def visit_AugAssign(self, node):
        self.current_node = node
        # load target first. a augop p. a is the deeper stack item. when use + *, the value irelate with the squence, howerver the div will get error.
        self.ctx_transformer = ReWrite_CTX_STORE_TO_LOAD(self.func_desc)
        target_newnode = self.ctx_transformer.visit(node.target)
        self.visit(target_newnode)

        # load value
        self.visit(node.value)

        # cal the by op
        self.visit(node.op)

        # store the target
        self.ctx_transformer = ReWrite_CTX_LOAD_TO_STORE()
        target_newnode = self.ctx_transformer.visit(target_newnode)
        self.visit(target_newnode)

    def visit_Print(self, node):
        self.current_node = node
        pass

    # note all Label infunction saved in func_desc
    def visit_For(self, node):
        self.current_node = node
        # assert the prequisite
        if type(node.target).__name__ != 'Name':
            self.Print_DoNot_Support(node, "multi iter.")

        # if node.orelse != []:
        #    self.Print_DoNot_Support(node, "for orelse.")

        # self.is_in_loop = True
        # alloc Label.
        for_start_label = self.codegencontext.NewLabel()
        for_end_label = self.codegencontext.NewLabel()
        for_no_break_end_label = self.codegencontext.NewLabel()

        self.latest_loop_break_label = [for_start_label, for_end_label]
        # index_position: init index.
        self.codegencontext.tokenizer.Emit_Integer(0, node)
        index_position = self.func_desc.Get_LocalStackPosition(ForIndexPrefix + str(self.func_desc.for_position))
        self.func_desc.for_position += 1
        self.codegencontext.tokenizer.Emit_StoreLocal(index_position, node)

        # walk the iter. load the result to the top of stack evalution stack
        self.visit(node.iter)
        self.is_in_loop = True
        self.latest_loop_break_label = [for_start_label, for_end_label]

        # result_position: save the result. xxx. if node.iter just Name. so here refine the address, will get error.
        # no need result_position. just revisit the node.iter is ok.
        # here asumed have a result = iter. and this must be local.
        result_position = self.func_desc.Get_LocalStackPosition(ForIndexPrefix + str(self.func_desc.for_position))
        self.func_desc.for_position += 1
        self.codegencontext.tokenizer.Emit_StoreLocal(result_position, node)

        # len_position: load the result. and init len(result).
        self.codegencontext.tokenizer.Emit_LoadLocal(result_position, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.ARRAYSIZE, node)
        len_position = self.func_desc.Get_LocalStackPosition(ForIndexPrefix + str(self.func_desc.for_position))
        self.func_desc.for_position += 1
        self.codegencontext.tokenizer.Emit_StoreLocal(len_position, node)

        # cal condition assert.
        self.codegencontext.SetLabel(for_start_label, self.codegencontext.pc + 1)
        self.codegencontext.tokenizer.Emit_LoadLocal(index_position, node)
        self.codegencontext.tokenizer.Emit_LoadLocal(len_position, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.LT, node)
        jumpostion_for_end = for_no_break_end_label.to_bytes(2, 'little', signed=True)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, jumpostion_for_end)

        # target_position: update save iter. xxx. must use target. so the body can ref it
        self.codegencontext.tokenizer.Emit_LoadLocal(result_position, node)
        self.codegencontext.tokenizer.Emit_LoadLocal(index_position, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.PICKITEM, node)
        # target_position = self.func_desc.Get_LocalStackPosition(ForIndexPrefix + str(self.func_desc.for_position))
        assert(type(node.target).__name__ == 'Name')
        # acctually here can visit node.target.
        assert(type(node.target.ctx).__name__ == 'Store')

        """
        # old way. now change to visit node.target.
        target_position = self.func_desc.Get_LocalStackPosition(node.target.id, node.target) # here Ont only support Name taget. so here just ref it
        self.codegencontext.tokenizer.Emit_StoreLocal(target_position, node.target)
        """
        self.visit(node.target)

        # update save index.
        self.codegencontext.tokenizer.Emit_LoadLocal(index_position, node)
        self.codegencontext.tokenizer.Emit_Integer(1, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.ADD, node)
        self.codegencontext.tokenizer.Emit_StoreLocal(index_position, node)

        # generate body.
        self.is_in_loop = True
        for stmt in node.body:
            # any visit have chance the latest_loop_break_label. so here revese it.
            self.visit(stmt)
            # here body break will jump into the for_end_label. continue will jump into for_start_label
            self.latest_loop_break_label = [for_start_label, for_end_label]
            self.is_in_loop = True

        # generate jump to condition assert
        jumpostion_for_start = for_start_label.to_bytes(2, 'little', signed=True)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, self.current_node, jumpostion_for_start)

        self.codegencontext.SetLabel(for_no_break_end_label, self.codegencontext.pc + 1)
        self.is_in_loop = False
        for stmt in node.orelse:
            self.visit(stmt)

        self.codegencontext.SetLabel(for_end_label, self.codegencontext.pc + 1)
        # self.codegencontext.tokenizer.Emit_Token(VMOp.NOP, stmt)

    def visit_While(self, node):
        self.current_node = node

        # if node.orelse !=[]:
        #    self.Print_DoNot_Support(node, "While orelse.")

        # alloc Label.
        self.is_in_loop = True
        while_start_label = self.codegencontext.NewLabel()
        while_end_label = self.codegencontext.NewLabel()
        while_no_break_end_label = self.codegencontext.NewLabel()

        self.latest_loop_break_label = [while_start_label, while_end_label]
        jumpostion_while_start = while_start_label.to_bytes(2, 'little', signed=True)
        jumpostion_while_end = while_no_break_end_label.to_bytes(2, 'little', signed=True)

        # generate code condition.
        self.codegencontext.SetLabel(while_start_label, self.codegencontext.pc + 1)
        self.visit(node.test)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, jumpostion_while_end)

        # body code generation. note. generic_visit only access the child node. and any visit child node  have a chance to change the latest_loop_break_label. so here update it.
        self.latest_loop_break_label = [while_start_label, while_end_label]
        self.is_in_loop = True
        for stmt in node.body:
            self.visit(stmt)
            self.latest_loop_break_label = [while_start_label, while_end_label]
            self.is_in_loop = True
        # current_node will update when visit.indicate the last node of visited
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, self.current_node, jumpostion_while_start)

        self.codegencontext.SetLabel(while_no_break_end_label, self.codegencontext.pc + 1)
        self.is_in_loop = False
        for stmt in node.orelse:
            self.visit(stmt)

        # generate jump to condition assert
        self.codegencontext.SetLabel(while_end_label, self.codegencontext.pc + 1)
        # self.codegencontext.tokenizer.Emit_Token(VMOp.NOP, stmt)
        return

    def visit_Pass(self, node):
        self.current_node = node
        self.codegencontext.tokenizer.Emit_Token(VMOp.NOP, node)

    def visit_Break(self, node):
        self.current_node = node
        if not self.is_in_loop:
            self.Print_Error(node, "You cannot break outside of a loop.")
        assert(len(self.latest_loop_break_label) == 2)
        # jmp to the end label
        target_label = self.latest_loop_break_label[1]
        target_postion = target_label.to_bytes(2, 'little', signed=True)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, node, target_postion)

    def visit_Continue(self, node):
        self.current_node = node
        if not self.is_in_loop:
            self.Print_Error(node, "You cannot continue outside of a loop.")
        assert(len(self.latest_loop_break_label) == 2)
        # jmp to the end label
        target_label = self.latest_loop_break_label[0]
        target_postion = target_label.to_bytes(2, 'little', signed=True)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, node, target_postion)

    def visit_If(self, node):
        self.current_node = node
        # indicate the if false
        jump_target_label = self.codegencontext.NewLabel()
        # indicate body after all if
        body_target_label = self.codegencontext.NewLabel()
        body_target_position = body_target_label.to_bytes(2, 'little', signed=True)

        # codegen condition test.
        self.visit(node.test)
        jump_target_position = jump_target_label.to_bytes(2, 'little', signed=True)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, jump_target_position)

        # codegen if body.
        for stmt in node.body:
            self.visit(stmt)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, self.current_node, body_target_position)

        self.codegencontext.SetLabel(jump_target_label, self.codegencontext.pc + 1)
        # codegen orelse.
        for stmt in node.orelse:
            self.visit(stmt)

        self.codegencontext.SetLabel(body_target_label, self.codegencontext.pc + 1)

    def visit_BinOp(self, node):
        self.current_node = node
        self.visit(node.left)
        self.visit(node.right)
        self.visit(node.op)

    def visit_Add(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.ADD, node)

    def visit_Sub(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.SUB, node)

    def visit_Mult(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.MUL, node)

    def visit_Div(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.DIV, node)

    def visit_Mod(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.MOD, node)

    def visit_LShift(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.SHL, node)

    def visit_RShift(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.SHR, node)

    def visit_BitOr(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.OR, node)

    def visit_BitXor(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.XOR, node)

    def visit_BitAnd(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.AND, node)

    def visit_FloorDiv(self, node):
        raise Exception("[Compiler ERROR. File: %s. in function: %s.]. The Neptune Compiler does not support %s" % (self.func_desc.filepath, self.func_desc.name, "FloorDiv"))

    def visit_BoolOp(self, node):
        assert(len(node.values) >= 2)
        End_target_label = self.codegencontext.NewLabel()
        End_target_postion = End_target_label.to_bytes(2, 'little', signed=True)

        for i in range(len(node.values)):
            self.visit(node.values[i])
            if i != (len(node.values) - 1):
                if (type(node.op).__name__ == 'Or'):
                    self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
                    self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIF, node, End_target_postion)
                    self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)
                elif (type(node.op).__name__ == 'And'):
                    self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
                    self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, End_target_postion)
                    self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)
                else:
                    assert(False)

        self.codegencontext.SetLabel(End_target_label, self.codegencontext.pc + 1)

    def visit_And(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.BOOLAND, node)

    def visit_Or(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.BOOLOR, node)

    def visit_Eq(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.NUMEQUAL, node)

    def visit_NotEq(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.NUMNOTEQUAL, node)

    def visit_Lt(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.LT, node)

    def visit_LtE(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.LTE, node)

    def visit_Gt(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.GT, node)

    def visit_GtE(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.GTE, node)

    def visit_Is(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.EQUAL, node)

    def visit_IsNot(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.EQUAL, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.NOT, node)

    def visit_In(self, node):

        # assume target a, and iter l in stack like the first below.
        Start_target_label = self.codegencontext.NewLabel()
        End_target_label = self.codegencontext.NewLabel()
        End_target_label_bytes = End_target_label.to_bytes(2, 'little', signed=True)
        Start_target_label_bytes = Start_target_label.to_bytes(2, 'little', signed=True)

        # a, l
        self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH0, node)  # set i to 0
        self.codegencontext.SetLabel(Start_target_label, self.codegencontext.pc + 1)

        # a, l, i. while start.
        self.codegencontext.tokenizer.Emit_Token(VMOp.OVER, node)

        # a, l, i, l
        self.codegencontext.tokenizer.Emit_Token(VMOp.ARRAYSIZE, node)

        # a, l, i, len
        self.codegencontext.tokenizer.Emit_Token(VMOp.OVER, node)

        # a, l, i, len, i
        self.codegencontext.tokenizer.Emit_Token(VMOp.SWAP, node)

        # a, l, i, i, len
        self.codegencontext.tokenizer.Emit_Token(VMOp.LT, node)

        # a, l, i, B  # assert while conditon.
        self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)

        # a, l, i, B, B
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, End_target_label_bytes)

        # a, l, i, B
        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)

        # a, l, i, assert True. goto the body.
        ##########################
        self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH2, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.PICK, node)

        # a, l, i, a
        self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH2, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.PICK, node)

        # a, l, i, a, l
        self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH2, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.PICK, node)

        # a, l, i, a, l, i
        self.codegencontext.tokenizer.Emit_Token(VMOp.PICKITEM, node)

        # a, l, i, a, l[i]
        self.codegencontext.tokenizer.Emit_Token(VMOp.EQUAL, node)

        # a, l, i, B
        self.codegencontext.tokenizer.Emit_Token(VMOp.TOALTSTACK, node)

        # a, l, i
        self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH1, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.ADD, node)

        # a, l, i = i + 1
        self.codegencontext.tokenizer.Emit_Token(VMOp.FROMALTSTACK, node)

        # a, l, i = i + 1, B
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, Start_target_label_bytes)

        # a, l, i
        self.codegencontext.tokenizer.Emit_Token(VMOp.PUSHT, node)

        # a, l, i, B

        ##########################

        # while conditon False or find the Value.
        self.codegencontext.SetLabel(End_target_label, self.codegencontext.pc + 1)

        # a, l, i, B
        self.codegencontext.tokenizer.Emit_Token(VMOp.TOALTSTACK, node)

        # a, l, i
        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)

        self.codegencontext.tokenizer.Emit_Token(VMOp.FROMALTSTACK, node)

        # B, last value

    def visit_NotIn(self, node):
        self.visit_In(node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.NOT, node)

    def visit_Not(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.NOT, node)

    def visit_Invert(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.INVERT, node)

    def visit_UnaryOp(self, node):
        self.current_node = node
        if type(node.op).__name__ in ['USub', 'UAdd']:
            self.codegencontext.tokenizer.Emit_Integer(0, node)
        self.visit(node.operand)
        self.visit(node.op)

    def visit_UAdd(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.ADD, node)

    def visit_USub(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.SUB, node)

    def visit_Dict(self, node):
        self.current_node = node
        self.codegencontext.tokenizer.Emit_Token(VMOp.NEWMAP, node)

        assert(len(node.keys) == len(node.values))

        for i in range(len(node.keys)):
            self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
            self.visit(node.values[i])
            self.codegencontext.tokenizer.Emit_Token(VMOp.SWAP, node)
            self.visit(node.keys[i])
            self.codegencontext.tokenizer.Emit_Token(VMOp.ROT, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.SETITEM, node)

    def visit_Assert(self, node):
        self.current_node = node
        if node.msg is not None:
            self.Print_DoNot_Support(node, "Assert with message.")
        self.visit(node.test)
        self.codegencontext.tokenizer.Emit_Token(VMOp.THROWIFNOT, node)

    def visit_List(self, node):
        self.current_node = node
        if type(node.ctx).__name__ != 'Load':
            self.Print_DoNot_Support(node, (type(node.ctx).__name__) + "type List.")
        else:
            for expr in node.elts:
                self.visit(expr)

            self.codegencontext.tokenizer.Emit_Integer(len(node.elts), node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.PACK, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.REVERSE, node)

    def visit_Attribute_Call(self, node):
        attr = node.func
        assert(type(attr).__name__ == 'Attribute')
        assert(type(attr.ctx).__name__ == 'Load')
        func_name = attr.attr
        func_desc = self.Get_FuncDesc(func_name, node)
        if func_name not in List_Attr_func:
            self.Print_Error(node, "do not support any other Attribute call other than 'append' or 'remove' or 'reverse'")
        assert(func_desc.isyscall or func_desc.is_builtin)
        self.visit(attr.value)

        if func_desc.arg_num != len(node.args):
            self.Print_Error(node, "Function '%s' requires exactly '%d' arguments but you passed '%d' args" % (func_name, func_desc.arg_num, len(node.args)))

        for arg in reversed(node.args):
            self.visit(arg)
            if type(arg).__name__ == 'Starred':
                self.Print_Error(node, "Attrubute function do not support pass Starred argument.")

        # all Attrubute all is builtin currently
        vmtoken = self.codegencontext.tokenizer.Emit_Builtins(func_name, node)
        if vmtoken is None:
            self.Print_DoNot_Support(node, "builtin '%s'." % (func_name))

    # only used in function call depackage.
    def visit_Starred(self, node):
        assert(type(node.ctx).__name__ == 'Load')
        self.visit(node.value)
        self.codegencontext.tokenizer.Emit_Token(VMOp.UNPACK, node)

    def visit_Call(self, node):
        self.current_node = node
        Passed_StarredArg = False
        if type(node.func).__name__ == 'Attribute':
            self.visit_Attribute_Call(node)
            return

        if type(node.func).__name__ != 'Name' or type(node.func.ctx).__name__ != 'Load':
            self.Print_DoNot_Support(node, type(node.func).__name__ + "type func call.")

        # not support keywords
        if node.keywords != []:
            self.Print_DoNot_Support(node, "Call function with keywords.")

        funcname = node.func.id
        func_desc = self.Get_FuncDesc(funcname, node)

        if funcname in List_Attr_func:
            self.Print_Error(node, "function '%s' is list attribute call, you cannot call it directly." % (funcname))

        # RegisterAppCall and RegisterAction is handle by visitor of global
        if func_desc.isyscall and (func_desc.name == "RegisterAppCall" or func_desc.name == "RegisterAction"):
            return

        # only support normal defaults args. note registere function is syscall.
        # can not use TOALTSTACK as usually. because if some var access it's var. will pick it from altstack. will goes run.
        # so use TOALTSTACK is dangers. use Emit_StoreLocal instead.
        if not (func_desc.is_builtin or func_desc.isyscall):
            arg_len_position = self.func_desc.Get_LocalStackPosition(Function_Call_Arglen)
            self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH0, node)
            self.codegencontext.tokenizer.Emit_StoreLocal(arg_len_position, node)
            for arg in reversed(node.args):
                self.visit(arg)
                if type(arg).__name__ == 'Starred':
                    Passed_StarredArg = True
                else:
                    self.codegencontext.tokenizer.Emit_Token(VMOp.PUSH1, node)

                self.codegencontext.tokenizer.Emit_LoadLocal(arg_len_position, node)
                self.codegencontext.tokenizer.Emit_Token(VMOp.ADD, node)
                self.codegencontext.tokenizer.Emit_StoreLocal(arg_len_position, node)

            # pass the arg number to callee.
            self.codegencontext.tokenizer.Emit_LoadLocal(arg_len_position, node)
        else:
            if funcname in ['concat', 'take', 'has_key', 'substr']:
                call_args = node.args
            else:
                call_args = reversed(node.args)

            for arg in call_args:
                self.visit(arg)
                if type(arg).__name__ == 'Starred':
                    Passed_StarredArg = True
                    self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)

            if funcname == 'state' and Passed_StarredArg:
                self.Print_Error(node, "Function 'state' do not support pass Starred argument")

        # check arg num requrie.
        if (not Passed_StarredArg):
            if len(node.args) < func_desc.necessary_arglen:
                if func_desc.default_arglen == 0 and not func_desc.have_vararg:
                    assert(func_desc.necessary_arglen == func_desc.arg_num)
                    self.Print_Error(node, "Function '%s' require exaclty '%d' args. but you passed '%d' args" % (funcname, func_desc.arg_num, len(node.args)))
                elif (not func_desc.have_vararg) and func_desc.default_arglen != 0:
                    assert((func_desc.default_arglen + func_desc.necessary_arglen) == func_desc.arg_num)
                    self.Print_Error(node, "Function '%s' require at least '%d' args, at most '%d' args. but you passed '%d' args" % (funcname, func_desc.necessary_arglen, func_desc.arg_num, len(node.args)))
                else:
                    self.Print_Error(node, "Function '%s' require at least '%d' args. but you passed '%d' args" % (funcname, func_desc.necessary_arglen, len(node.args)))
            elif len(node.args) > func_desc.arg_num and (not func_desc.have_vararg):
                self.Print_Error(node, "Function '%s' require at most '%d' args. but you passed '%d' args" % (funcname, func_desc.arg_num, len(node.args)))
        else:
            # if passed Starred arg. can not assert the arg num in compile time.
            pass

        if not (func_desc.is_builtin or func_desc.isyscall):
            call_target_label = func_desc.label
            call_data = call_target_label.to_bytes(2, 'little', signed=True)
        elif func_desc.is_builtin:
            if funcname == 'bytearray' or funcname == 'bytes':
                return
            if funcname == 'state':
                self.codegencontext.tokenizer.Emit_Integer(len(node.args), node)
                self.codegencontext.tokenizer.Emit_Token(VMOp.NEWSTRUCT, node)
                self.codegencontext.tokenizer.Emit_Token(VMOp.TOALTSTACK, node)
                for index in range(len(node.args)):
                    self.codegencontext.tokenizer.Emit_StoreLocal(index, node.args[index])
                self.codegencontext.tokenizer.Emit_Token(VMOp.FROMALTSTACK, node)
                return
            vmtoken = self.codegencontext.tokenizer.Emit_Builtins(funcname, node)
            if vmtoken is None:
                self.Print_DoNot_Support(node, "builtin '%s'." % (funcname))
            return
        else:
            assert(func_desc.isyscall)
            action_reset_the_syscall_name = False
            # convert DynamicAppCall first
            if func_desc.name == 'DynamicAppCall':
                self.codegencontext.tokenizer.Emit_Token(VMOp.APPCALL, node, bytearray(20))
                return
            elif func_desc.name in self.codegencontext.register_appcall.keys():
                assert(func_desc.is_register_call)
                call_addr = self.codegencontext.register_appcall[func_desc.name].script_hash_addr
                self.codegencontext.tokenizer.Emit_Token(VMOp.APPCALL, node, call_addr)
                return
            elif func_desc.name in self.codegencontext.register_action.keys():
                assert(func_desc.is_register_call)
                action = self.codegencontext.register_action[func_desc.name]
                event_name = action.event_name.encode('utf-8')
                self.codegencontext.tokenizer.Emit_Data(event_name, node)
                self.codegencontext.tokenizer.Emit_Integer(len(action.args), node)
                self.codegencontext.tokenizer.Emit_Token(VMOp.PACK, node)
                action_reset_the_syscall_name = True

            if action_reset_the_syscall_name:
                sys_name = 'System.Runtime.Notify'
                syscall_name = sys_name.encode('utf-8')
            else:
                sys_name = func_desc.blong_module_name + '.' + func_desc.name
                if 'System.Header.GetBlockHash' in sys_name:
                    sys_name = sys_name.replace('GetBlockHash', 'GetHash')
                elif 'System.Transaction.GetTransactionHash' in sys_name:
                    sys_name = sys_name.replace('GetTransactionHash', 'GetHash')
                elif 'System.Block.GetTransactionByIndex' in sys_name:
                    sys_name = sys_name.replace('GetTransactionByIndex', 'GetTransaction')
                elif 'System.Blockchain.GetTransactionByHash' in sys_name:
                    sys_name = sys_name.replace('GetTransactionByHash', 'GetTransaction')

                syscall_name = sys_name.replace(ONTOLOGY_SC_FRAMEWORK, '')
                syscall_name = syscall_name.replace(ONTOLOGY_SC_FRAMEWORK_boa, '').encode('utf-8')

            length = len(syscall_name)
            systemcall_name_array = bytearray([length]) + bytearray(syscall_name)
            vmtoken = self.codegencontext.tokenizer.Emit_Token(VMOp.SYSCALL, node, systemcall_name_array)

            syscall_print = sys_name.replace(ONTOLOGY_SC_FRAMEWORK, '')
            syscall_print = syscall_print.replace(ONTOLOGY_SC_FRAMEWORK_boa, '')
            vmtoken.syscall_name = syscall_print

            return

        assert(not (func_desc.isyscall or func_desc.is_builtin or func_desc.is_register_call))

        # arg_len = len(node.args)
        # self.codegencontext.tokenizer.Emit_Integer(arg_len, node)

        if not self.is_for_global:
            global_postion = self.func_desc.Read_LocalStackPosition(Global_VarEnv)
            self.codegencontext.tokenizer.Emit_PickGlobal(global_postion, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.CALL, node, call_data)
        else:
            self.codegencontext.tokenizer.Emit_Token(VMOp.DUPFROMALTSTACK, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.CALL, node, call_data)

    # only save a bool(true or false) to the evalution stack.
    def visit_Compare(self, node):
        self.current_node = node
        opslen = len(node.ops)
        comparatorslen = len(node.comparators)
        assert(opslen == comparatorslen)
        assert(opslen > 0)

        jump_target_label = self.codegencontext.NewLabel()
        jump_target_position = jump_target_label.to_bytes(2, 'little', signed=True)

        # set a init top stack item.
        self.visit(node.left)

        for i in range(opslen):
            # V(n-1)
            self.visit(node.comparators[i])

            # V(n-1), Vn

            self.codegencontext.tokenizer.Emit_Token(VMOp.TUCK, node)

            # V(n), V(n-1), V(n)

            self.visit(node.ops[i])

            # V(n), B

            if i == opslen - 1:
                break

            self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)

            # (n), B, B

            self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, jump_target_position)

            # V(n), B

            self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)

            # V(n)

        self.codegencontext.SetLabel(jump_target_label, self.codegencontext.pc + 1)

        # V(n), B

        self.codegencontext.tokenizer.Emit_Token(VMOp.SWAP, node)

        # B, V(n)

        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)

        # B. last return

    def visit_Num(self, node):
        self.current_node = node
        num = node.n
        self.codegencontext.tokenizer.Emit_Integer(num, node)

    def visit_Bytes(self, node):
        self.current_node = node
        self.codegencontext.tokenizer.Emit_Data(bytes(node.s), node)

    def visit_Str(self, node):
        self.current_node = node
        str_bytes = node.s.encode('utf-8')
        self.codegencontext.tokenizer.Emit_Data(str_bytes, node)

    def visit_Name(self, node):
        global_postion = self.func_desc.Read_LocalStackPosition(Global_VarEnv, node)

        if not self.is_for_global:
            assert(global_postion is not None)
        self.current_node = node

        # like the orignal python sematic.
        # howerver if you want store a global. it must init global var in global code for alloc space.
        if type(node.ctx).__name__ == 'Load':

            if self.check_var_global(node.id):
                name_position = self.func_desc.Read_Global_Position(node.id)
                if name_position is None:
                    Print_Error_global(self.func_desc.filepath, node, "Global Variable '%s' used before defined." % (node.id))
                else:
                    self.codegencontext.tokenizer.Emit_LoadGlobal(name_position, global_postion, node)
            else:
                name_position = self.func_desc.Read_LocalStackPosition(node.id, node)
                if name_position is None:
                    name_position = self.func_desc.Read_Global_Position(node.id)

                    if name_position is None:
                        Print_Error_global(self.func_desc.filepath, node, "Variable '%s' used before defined." % (node.id))

                    self.codegencontext.tokenizer.Emit_LoadGlobal(name_position, global_postion, node)
                else:
                    self.codegencontext.tokenizer.Emit_LoadLocal(name_position, node)

        elif type(node.ctx).__name__ == 'Store':

            if self.check_var_global(node.id):
                name_position = self.func_desc.Read_Global_Position(node.id, node)
                if name_position is None:
                    Print_Error_global(self.func_desc.filepath, node, "Global Variable '%s' used before defined." % (node.id))
                else:
                    self.codegencontext.tokenizer.Emit_StoreGlobal(name_position, global_postion, node)
            else:
                name_position = self.func_desc.Get_LocalStackPosition(node.id, node)
                assert(name_position is not None)
                self.codegencontext.tokenizer.Emit_StoreLocal(name_position, node)
                assert(self.func_desc.ref_type[node.id] == ref_type_local)

        else:
            assert("Wrong Name ctx type")

        # the usual method. local first. like 'C' lauguage.
        """
        if type(node.ctx).__name__ == 'Load':
            name_position = self.func_desc.Read_LocalStackPosition(node.id, node)
            if name_position is not None:
                self.codegencontext.tokenizer.Emit_LoadLocal(name_position, node)
            else:
                name_position = self.func_desc.Read_Global_Position(node.id)
                if name_position is None:
                    Print_Error_global(self.func_desc.filepath, node, "Variable '%s' used before defined." % (node.id))

                self.codegencontext.tokenizer.Emit_LoadGlobal(name_position, global_postion, node)

        elif type(node.ctx).__name__ == 'Store':
            name_position = self.func_desc.Read_LocalStackPosition(node.id, node)
            if name_position is not None:
                self.codegencontext.tokenizer.Emit_StoreLocal(name_position, node)
            else:
                name_position = self.func_desc.Read_Global_Position(node.id)
                if name_position is None:
                    name_position = self.func_desc.NewLocal(node.id, node)
                    self.codegencontext.tokenizer.Emit_StoreLocal(name_position, node)
                else:
                    self.codegencontext.tokenizer.Emit_StoreGlobal(name_position, global_postion, node)
        else:
            assert("Wrong Name ctx type")
        """

    def visit_Subscript(self, node):
        self.current_node = node
        if type(node.ctx).__name__ == 'Load':
            self.visit(node.value)  # cal list or map or some else support
            if type(node.slice).__name__ == 'Index':
                self.visit(node.slice)  # cal slice. note slice is a super set of Index
                self.codegencontext.tokenizer.Emit_Token(VMOp.PICKITEM, node)
            # note. here due to support str slice. how ever python can not difference the list and str by the node.value. so only can support one type slice.
            elif type(node.slice).__name__ == 'Slice':
                if node.slice.step is not None:
                    self.Print_DoNot_Support(node, "slice with step.")

                if node.slice.upper is not None:
                    self.visit(node.slice.upper)
                    uppernode = node.slice.upper
                    if type(uppernode).__name__ == 'UnaryOp' and type(uppernode.op).__name__ == 'USub' and type(uppernode.operand).__name__ == 'Num':
                        self.Print_Error(node, "slice upper smaller than 0.")
                else:
                    self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
                    self.codegencontext.tokenizer.Emit_Token(VMOp.ARRAYSIZE, node)

                if node.slice.lower is not None:
                    self.visit(node.slice.lower)
                    lowernode = node.slice.lower
                    if type(lowernode).__name__ == 'UnaryOp' and type(lowernode.op).__name__ == 'USub' and type(lowernode.operand).__name__ == 'Num':
                        self.Print_Error(node, "slice lower smaller than 0.")
                else:
                    self.codegencontext.tokenizer.Emit_Integer(0, node)

                self.codegencontext.tokenizer.Emit_Slice(node)
            else:
                self.Print_DoNot_Support(node, "Subscript such slice.")

        elif type(node.ctx).__name__ == 'Store':
            if type(node.slice).__name__ == 'Index':
                self.visit(node.value)  # cal list or map or some else support
                self.visit(node.slice)  # cal index
                self.codegencontext.tokenizer.Emit_Token(VMOp.ROT, node)
                self.codegencontext.tokenizer.Emit_Token(VMOp.SETITEM, node)
            else:
                self.Print_DoNot_Support(node, "Subscript Slice Assgin.")
        else:
            assert("Wrong Name ctx type")

    def visit_Slice(self, node):
        assert(False)

    def visit_Return(self, node):
        self.current_node = node
        if node.value is not None:
            self.visit(node.value)

        self.codegencontext.tokenizer.Emit_Token(VMOp.FROMALTSTACK, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.RET, node)

    def visit_NameConstant(self, node):
        self.current_node = node
        if node.value:
            self.codegencontext.tokenizer.Emit_Integer(1, node)
        elif not node.value:
            self.codegencontext.tokenizer.Emit_Integer(0, node)
        elif node.value is None:
            str_bytes = 'N'.encode('utf-8')
            self.codegencontext.tokenizer.Emit_Data(str_bytes, node)
            self.codegencontext.tokenizer.Emit_Integer(0, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.LEFT, node)
        else:
            self.Print_DoNot_Support(node, "such NameConstant.")

    def visit_Index(self, node):
        self.current_node = node
        self.generic_visit(node)

    def visit_Expr(self, node):

        self.current_node = node
        if type(node.value).__name__ == 'Call':
            self.generic_visit(node)
            if type(node.value.func).__name__ == 'Name':
                funcname = node.value.func.id
                func_desc = self.codegencontext.funcscope[funcname]
                # handle normal func first
                if not (func_desc.is_builtin or func_desc.isyscall):
                    if func_desc.have_return_value:
                        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)
                # here hypothesis all buildins and syscall other than conditon will return a value.
                elif not (funcname in WITHOUT_RETURN_BUILTINSYSCALL or funcname in self.codegencontext.register_action.keys()):
                    self.Print_DoNot_Support(node, "Builtins or syscall %s call with no value assigned" % (funcname))
            elif type(node.value.func).__name__ == 'Attribute':
                attr = node.value.func
                assert(type(attr).__name__ == 'Attribute')
                assert(type(attr.ctx).__name__ == 'Load')
                func_name = attr.attr
                # all func in List_Attr_func treated ast no return value.
                if func_name not in List_Attr_func:
                    self.Print_DoNot_Support(node, "dynamic funcname.")
            else:
                self.Print_DoNot_Support(node, "dynamic funcname.")
        elif type(node.value).__name__ in ONE_LINE_EXPR_SUPPORT_AST_TYPE:
            if type(node.value).__name__ == 'Pass':
                self.generic_visit(node)
            elif type(node.value).__name__ == 'Str':
                # self.generic_visit(node)
                pass
            else:
                self.generic_visit(node)
        else:
            self.Print_DoNot_Support(node, "Expr with one line. due to carefull handle stack stack.")

    def compile_comprehension(self, node, body, elt):
        assert(False)

    def visit_ListComp(self, node):
        self.current_node = node
        # construct load list
        array_name = ListCompName + str(self.func_desc.list_comp_position)
        array_position = self.func_desc.Get_LocalStackPosition(array_name)
        # alloc a newarray
        self.codegencontext.tokenizer.Emit_Integer(0, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.NEWARRAY, node)
        self.codegencontext.tokenizer.Emit_StoreLocal(array_position, node)

        # construct load array
        array_load = ast.Name()
        array_load.id = array_name
        array_load.ctx = ast.Load()
        self.func_desc.list_comp_position += 1

        # construct Attrubute.
        call_attr = ast.Attribute(value=array_load, attr='append', ctx=ast.Load(), lineno=node.lineno, col_offset=node.col_offset)

        # construct append(element)
        node_call = ast.Call()
        call_args = [node.elt]
        node_call.func = call_attr
        node_call.args = call_args
        node_call.keywords = []
        node_call.starargs = None
        node_call.kwargs = None
        node_call.lineno = node.lineno
        node_call.col_offset = node.col_offset

        node_for_prev = None

        for generator in reversed(node.generators):
            if len(generator.ifs) != 0:
                bodyif = ast.If()
            else:
                bodyif = None

            if len(generator.ifs) > 1:
                bodyiftest = ast.BoolOp()
                bodyiftest.lineno = generator.ifs[0].lineno
                bodyiftest.col_offset = generator.ifs[0].col_offset
                bodyiftest.op = ast.And()
                bodyiftest.values = []
                for test in generator.ifs:
                    bodyiftest.values.append(test)
                if node_for_prev is None:
                    # bodyif.body         = [array_load, node_call]
                    bodyif.body = [node_call]
                else:
                    bodyif.body = [node_for_prev]
                bodyif.test = bodyiftest
                bodyif.orelse = []
                bodyif.lineno = generator.ifs[0].lineno
                bodyif.col_offset = generator.ifs[0].col_offset
            elif len(generator.ifs) == 1:
                bodyif.test = generator.ifs[0]
                bodyif.orelse = []
                bodyif.lineno = generator.ifs[0].lineno
                bodyif.col_offset = generator.ifs[0].col_offset
                if node_for_prev is None:
                    # bodyif.body         = [array_load, node_call]
                    bodyif.body = [node_call]
                else:
                    bodyif.body = [node_for_prev]
            else:
                assert(bodyif is None)

            node_for = ast.For()
            node_for.target = generator.target
            node_for.iter = generator.iter
            node_for.orelse = []
            node_for.lineno = node.lineno
            node_for.col_offset = node.col_offset
            if bodyif is not None:
                node_for.body = [bodyif]
            else:
                if node_for_prev is None:
                    # node_for.body   = [array_load, node_call]
                    node_for.body = [node_call]
                else:
                    node_for.body = [node_for_prev]

            node_for_prev = node_for

        self.visit(node_for_prev)
        self.codegencontext.tokenizer.Emit_LoadLocal(array_position, node)

    def visit_SetComp(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_GeneratorExp(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_Raise(self, node):
        if hasattr(node, 'exc'):
            exc = node.exc
            # if type(exc).__name__ == 'Call' and type(exc.func).__name__ == 'Name' and type(exc.func.ctx).__name__ == 'Load' and exc.func.id == 'Exception' and exc.keywords == [] and len(exc.args) == 1 and type(exc.args[0]).__name__ == 'Str':
            if type(exc).__name__ == 'Call' and type(exc.func).__name__ == 'Name' and type(exc.func.ctx).__name__ == 'Load' and exc.func.id == 'Exception':
                self.visit(exc)
                # self.codegencontext.tokenizer.Emit_Builtins('Exception', node.exc)
            else:
                self.Print_Error(node, "Only Support 'Raise Exception(str_message)'.")
        else:
            self.Print_Error(node, "Only Support 'Raise Exception(str_message)'.")

    def visit_TryExcept(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_TryFinally(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_With(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_Exec(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_Tuple(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_Lambda(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_Set(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_Yield(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_Repr(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_Global(self, node):
        if self.is_for_global:
            Print_Error_global(self.func_desc.filepath, node, "use Global keywards is useless in Global Code.")

        # can not check all. like global use. all variable asumed be locals. so all Golbal should be statement in the first line of function.
        for var in node.names:
            if var in self.func_desc.ref_type:
                self.Print_Error(node, "Variable {} is used prior to global declaration.".format(var))

            self.global_declare.append(var)

    def check_var_global(self, name):
        if self.is_for_global:
            return False

        if name in self.global_declare:
            return True
        else:
            return False

    def visit_DictComp(self, node):

        self.current_node = node
        # construct map value
        map_name = ListCompName + str(self.func_desc.list_comp_position)
        map_position = self.func_desc.Get_LocalStackPosition(map_name)
        # alloc a map
        self.codegencontext.tokenizer.Emit_Token(VMOp.NEWMAP, node)
        self.codegencontext.tokenizer.Emit_StoreLocal(map_position, node)

        # construct Map load Name
        map_load = ast.Name()
        map_load.id = map_name
        map_load.ctx = ast.Load()
        self.func_desc.list_comp_position += 1

        add_Key_node = ast.Assign(targets=[ast.Subscript(value=map_load, slice=ast.Index(value=node.key), ctx=ast.Store(), lineno=node.lineno, col_offset=node.col_offset)], value=node.value, lineno=node.lineno, col_offset=node.col_offset)

        node_for_prev = None

        for generator in reversed(node.generators):
            if len(generator.ifs) != 0:
                bodyif = ast.If()
            else:
                bodyif = None

            if len(generator.ifs) > 1:
                bodyiftest = ast.BoolOp()
                bodyiftest.lineno = generator.ifs[0].lineno
                bodyiftest.col_offset = generator.ifs[0].col_offset
                bodyiftest.op = ast.And()
                bodyiftest.values = []
                for test in generator.ifs:
                    bodyiftest.values.append(test)
                if node_for_prev is None:
                    bodyif.body = [add_Key_node]
                else:
                    bodyif.body = [node_for_prev]
                bodyif.test = bodyiftest
                bodyif.orelse = []
                bodyif.lineno = generator.ifs[0].lineno
                bodyif.col_offset = generator.ifs[0].col_offset
            elif len(generator.ifs) == 1:
                bodyif.test = generator.ifs[0]
                bodyif.orelse = []
                bodyif.lineno = generator.ifs[0].lineno
                bodyif.col_offset = generator.ifs[0].col_offset
                if node_for_prev is None:
                    bodyif.body = [add_Key_node]
                else:
                    bodyif.body = [node_for_prev]
            else:
                assert(bodyif is None)

            node_for = ast.For()
            node_for.target = generator.target
            node_for.iter = generator.iter
            node_for.orelse = []
            node_for.lineno = node.lineno
            node_for.col_offset = node.col_offset
            if bodyif is not None:
                node_for.body = [bodyif]
            else:
                if node_for_prev is None:
                    node_for.body = [add_Key_node]
                else:
                    node_for.body = [node_for_prev]

            node_for_prev = node_for

        self.visit(node_for_prev)
        self.codegencontext.tokenizer.Emit_LoadLocal(map_position, node)

    def visit_Attribute(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")

    def visit_IfExp(self, node):
        orelse_label = self.codegencontext.NewLabel()
        orelse_positon = orelse_label.to_bytes(2, 'little', signed=True)
        end_label = self.codegencontext.NewLabel()
        end_position = end_label.to_bytes(2, 'little', signed=True)

        self.visit(node.test)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, orelse_positon)

        self.visit(node.body)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, node, end_position)

        self.codegencontext.SetLabel(orelse_label, self.codegencontext.pc + 1)
        self.visit(node.orelse)

        self.codegencontext.SetLabel(end_label, self.codegencontext.pc + 1)

    def visit_Delete(self, node):
        self.Print_DoNot_Support(node, "'" + type(node).__name__ + "'")


class FuncDescription:
    def __init__(self, name, label, node, isyscall, filepath, module_name, is_builtin, is_global=None, global_map=None):
        self.name = name
        self.filepath = filepath
        self.is_global = is_global
        self.for_position = 0
        self.list_comp_position = 0
        self.blong_module_name = module_name
        self.local_num = 0
        self.local_map = {}
        self.stack_size = 0
        self.func_ast = node
        self.global_map = global_map
        self.ref_type = {}

        # arg num record.
        self.default_arglen = -1
        self.necessary_arglen = -1
        self.have_vararg = False

        if is_global:
            assert(global_map is None)
            self.name = Global_simulation_func_name
            self.first_global_node = node

            # self.global_postion = 0
            # self.global_map     = {}
        else:
            self.label = label
            if node:
                self.src_lineno = node.lineno
            self.is_register_call = False
            self.have_return_value = False
            self.arg_num = 0
            assert(module_name is not None)
            # if self.isyscall:
            self.isyscall = isyscall
            self.is_builtin = is_builtin

            # note. when self.is_builtin or self.isyscall assert. this value have no meanning
            assert(not (self.isyscall and self.is_builtin))

    def Calculate_StackSize(self):
        if self.is_global:
            self.stack_size = 1  # Function_Call_Arglen. Global do not have other 3 FixedName args.
        else:
            self.stack_size = 4  # Global_VarEnv, Local_ArgLen, vararg, Function_Call_Arglen.  note main function only have Global_VarEnv.

        visitor_stacksize = FuncVisitor_Of_StackSize(self, self.is_global)
        visitor_stacksize.visit(self.func_ast)
        self.stack_size += visitor_stacksize.stack_size
        # self.arg_num            = visitor_stacksize.arg_num
        # print("Function %s. stack_size %d  self.arg_num %d" % (self.name, self.stack_size, self.arg_num))

    def Check_VarRefLocal(self, name):
        if not (name in self.ref_type):
            assert(False)
        return self.ref_type[name] == ref_type_local

    def Check_VarRefGlobal(self, name):
        if not (name in self.ref_type):
            assert(False)
        return self.ref_type[name] == ref_type_global

    def NewLocal(self, name, node=None):
        if name in self.local_map.keys():
            Print_Error_global(self.filepath, node, "Variable '%s' already defined." % (name))

        self.local_map[name] = self.local_num
        self.local_num += 1

        if (name in self.ref_type) and (self.ref_type[name] == ref_type_global):
            if node is not None:
                Print_Error_global(self.filepath, node, "Variable {} has ref as Global Variable. Check your code.".format(name))
            else:
                raise Exception("Variable {} has ref as Global Variable. Check your code.".format(name))

        self.ref_type[name] = ref_type_local
        return self.local_num - 1

    def Get_LocalStackPosition(self, name, node=None):
        position = self.Read_LocalStackPosition(name, node)
        if position is not None:
            return position
        else:
            return self.NewLocal(name, node)

    def Read_LocalStackPosition(self, name, node=None):
        if name in self.local_map.keys():
            if (name in self.ref_type) and (self.ref_type[name] == ref_type_global):
                if node is not None:
                    Print_Error_global(self.filepath, node, "Variable {} has ref as Global Variable. Check your code.".format(name))
                else:
                    raise Exception("Variable {} has ref as Global Variable. Check your code.".format(name))

            assert(self.ref_type[name] == ref_type_local)
            return self.local_map[name]
        else:
            return None

    # code can both have global and local var with same name. but in function only can be local or global.
    def Read_Global_Position(self, name, node=None):
        if self.global_map is None:
            return None
        else:
            if name in self.global_map.keys():
                if (name in self.ref_type) and (self.ref_type[name] == ref_type_local):
                    if node is not None:
                        Print_Error_global(self.filepath, node, "Variable {} has ref as Local Variable. Check your code.".format(name))
                    else:
                        raise Exception("Variable {} has ref as Local Variable. Check your code.".format(name))
                self.ref_type[name] = ref_type_global
                return self.global_map[name]
            else:
                return None


class CodeGenContext:
    def __init__(self, SrcPath):
        source = open(SrcPath, 'rb')
        SrcCode = source.read()
        self.tokenizer = AstVMTokenizer()
        self.funcscope = {}
        self.labels = []
        self.current_func_node = None
        self.main_astree = ast.parse(SrcCode)
        self.main_file_path = SrcPath
        self.global_num = 0
        self.file_hash = None
        self.register_appcall = {}
        self.register_action = {}
        self.global_simulation_func = None
        global warning_file_path
        warning_file_path = self.Generate_new_name(SrcPath, '.py', '.warning')
        with open(warning_file_path, 'w+') as out_file:
            out_file.write("")
        # print(ast.dump(self.main_astree))

    def LinkProcess(self):
        all_token = self.tokenizer.vm_tokens.items()
        link_op = [VMOp.JMP, VMOp.JMPIF, VMOp.JMPIFNOT, VMOp.CALL]
        prev_addr = -1
        for addr, vmtoken in all_token:
            assert(vmtoken.addr == addr)
            assert(prev_addr < addr)

            if vmtoken.vm_op in link_op:
                target_label = int.from_bytes(vmtoken.data, byteorder='little')
                target_addr = self.labels[target_label]
                assert(target_addr != -1)
                vmtoken.target = target_addr
                offset = target_addr - vmtoken.addr
                vmtoken.data = offset.to_bytes(2, 'little', signed=True)

        prev_addr = addr
        self.write_code()
        return

    def Dump_Asm(self):
        all_token = self.tokenizer.vm_tokens.items()
        link_op = [VMOp.JMP, VMOp.JMPIF, VMOp.JMPIFNOT, VMOp.CALL]
        prev_addr = -1
        prev_lineno = -1
        prev_col = -1

        print("{:<30} {:<10} {:<5} {:<10} {:<20} {:<20} {:<20}".format("FuncName", "Lineno", "Col", "Offset", "OpCode", "JumpTarget", "TargetOff"))
        for addr, vmtoken in all_token:
            vmop_name = VMOp.to_name(vmtoken.out_op)
            if vmop_name is None:
                vmop_name = 'PUSHBYTES' + str(vmtoken.out_op)

            assert(vmtoken.addr == addr)
            assert(prev_addr <= addr)

            if vmtoken.vm_op in link_op:
                assert(vmtoken.node.lineno)
                offset = int.from_bytes(vmtoken.data, byteorder='little', signed=True)
                target_addr = offset + addr
                print("{:<30} {:<10} {:<5} {:<10} {:<20} {:<20} {:<20}".format(vmtoken.cur_func.name, vmtoken.node.lineno, vmtoken.node.col_offset, vmtoken.addr, vmop_name, target_addr, offset))
            elif vmtoken.vm_op is VMOp.SYSCALL:
                assert(vmtoken.node.lineno)
                print("{:<30} {:<10} {:<5} {:<10} {:<20} {:<20}".format(vmtoken.cur_func.name, vmtoken.node.lineno, vmtoken.node.col_offset, vmtoken.addr, vmop_name, vmtoken.syscall_name))
            else:
                if hasattr(vmtoken.node, 'col_offset'):
                    assert(hasattr(vmtoken.node, 'lineno'))
                    node_line = vmtoken.node.lineno
                    node_col = vmtoken.node.col_offset
                else:
                    node_line = prev_lineno
                    node_col = prev_col

                print("{:<30} {:<10} {:<5} {:<10} {:<20}".format(vmtoken.cur_func.name, node_line, node_col, vmtoken.addr, vmop_name))
            prev_lineno = node_line
            prev_col = node_col
            prev_addr = addr

    def Generate_Debug_Json(self, output_path, data):
        hashstr = Digest.hash160(msg=data, is_hex=True)  # str
        a2bhashstr = bytearray(a2b_hex(hashstr))  # str ==> bytes ==>bytearray
        a2bhashstr.reverse()
        file_hash = a2bhashstr.hex()  # bytearray ==> str
        self.file_hash = file_hash

        avm_name = os.path.splitext(os.path.basename(output_path))[0]
        JsonMap = {}
        JsonMap['avm'] = {'name': avm_name, 'hash': file_hash}
        JsonMap['compiler'] = {'name': 'Ontology-Python-Compile', 'version': __version__}
        files = {}
        JsonMap['files'] = files
        prev_lineno = -1
        asmap = []
        start_addr = 0
        assert_end_off = 0

        all_token = self.tokenizer.vm_tokens.items()
        for addr, vmtoken in all_token:
            # assert the file first.
            cur_file = vmtoken.cur_func.filepath
            cur_func = vmtoken.cur_func.name
            if cur_file not in files.keys():
                cur_file_id = len(files.values()) + 1
                files[cur_file] = cur_file_id
            else:
                cur_file_id = files[cur_file]

            if hasattr(vmtoken.node, 'col_offset'):
                assert(hasattr(vmtoken.node, 'lineno'))
                node_line = vmtoken.node.lineno
            else:
                node_line = prev_lineno

            if node_line != prev_lineno:
                assert_start_off = start_addr
                start_addr = addr
                if prev_lineno > 0:
                    asmap.append({'start': assert_start_off, 'end': assert_end_off, 'file': cur_file_id, 'method': cur_func, 'file_line_no': prev_lineno})

            assert_end_off = addr
            prev_lineno = node_line

        asmap.append({'start': assert_start_off, 'end': assert_end_off, 'file': cur_file_id, 'method': cur_func, 'file_line_no': prev_lineno})

        JsonMap['map'] = asmap
        JsonMap['files'] = [{'id': val, 'url': os.path.abspath(key)} for key, val in files.items()]
        json_data = json.dumps(JsonMap, indent=4)

        fullpath = os.path.realpath(output_path)
        path, filename = os.path.split(fullpath)
        newfilename = filename.replace('.py', '.debug.json')
        write_path = '%s/%s' % (path, newfilename)

        self.write_file_with_str(json_data, write_path)
        # self.Generate_Function_Local_Map(fullpath)

    def Generate_Function_Local_Map(self, path, main_func_desc):
        FunctionsVarMap = []
        savedfile = self.Generate_new_name(path, '.py', '.Func.Map')

        FunctionsVarMap.append({"Method": self.global_simulation_func.name, "VarMap": self.global_simulation_func.local_map})
        FunctionsVarMap.append({"Method": main_func_desc.name, "VarMap": main_func_desc.local_map})

        for name, func_desc in self.funcscope.items():
            if not (func_desc.isyscall or func_desc.is_builtin):
                FunctionsVarMap.append({"Method": name, "VarMap": func_desc.local_map})

        FunctionsVarMap_t = {"Functions": FunctionsVarMap}
        json_data = json.dumps(FunctionsVarMap_t, indent=4)
        self.write_file_with_str(json_data, savedfile)

    def Generate_Abi_list(self, main_func_node):
        assert(self.file_hash is not None)
        ABI_result = {}
        ABI_result["CompilerVersion"] = __version__
        ABI_result["hash"] = self.file_hash
        ABI_result["entrypoint"] = main_func_node.name
        step0 = Abivisitor_step0()
        step0.visit(self.main_astree)
        step1 = Abivisitor_step1(step0.Funclist)
        step1.visit(self.main_astree)
        ABI_result["functions"] = step1.AbiFunclist

        savedfile = self.Generate_new_name(self.main_file_path, '.py', '.abi.json')
        json_data = json.dumps(ABI_result, indent=4)
        self.write_file_with_str(json_data, savedfile)

    def Generate_new_name(self, path, replacestr, new_extend):
        fullpath = os.path.realpath(path)
        path, filename = os.path.split(fullpath)
        newfilename = filename.replace(replacestr, new_extend)
        mapfilename = '%s/%s' % (path, newfilename)
        return mapfilename

    def write_code(self):
        b_array = bytearray()
        for key, vm_token in self.tokenizer.vm_tokens.items():
            b_array.append(vm_token.out_op)
            if vm_token.data is not None and vm_token.vm_op != VMOp.NOP:
                b_array = b_array + vm_token.data

        path = self.main_file_path
        fullpath = os.path.realpath(path)
        path, filename = os.path.split(fullpath)
        newfilename = filename.replace('.py', '.avm')
        output_path = '%s/%s' % (path, newfilename)
        newfilename_str = filename.replace('.py', '.avm.str')
        output_path_str = '%s/%s' % (path, newfilename_str)

        data = b_array

        self.write_file_with_bytes(data, output_path)

        data_str = binascii.hexlify(data).decode('ascii')
        with open(output_path_str, 'w') as out_file:
            out_file.write(data_str)

        self.Generate_Debug_Json(fullpath, data)

    def write_file_with_bytes(self, data, path):
        with open(path, 'wb+') as out_file:
            out_file.write(data)

    def write_file_with_str(self, data, path):
        with open(path, 'w+') as out_file:
            out_file.write(data)

    def Print_FuncScope(self):
        for i in self.funcscope.keys():
            if self.funcscope[i].func_ast is not None:
                print("name: %s, label: %d, src_lineno: %d filepath: %s isyscall: %d argnum:%d" % (self.funcscope[i].name, self.funcscope[i].label, self.funcscope[i].src_lineno, self.funcscope[i].filepath, self.funcscope[i].isyscall, self.funcscope[i].arg_num))
            else:
                assert(self.funcscope[i].is_register_call)

    def Convert_Global_First(self):

        visitor = Visit_FirstGlobalNode()
        visitor.visit(self.main_astree)

        fixed_line_visitor = generic_modify_node()
        fixed_line_visitor.visit(self.main_astree)

        self.global_simulation_func = FuncDescription(name=Global_simulation_func_name, label=None, node=self.main_astree, isyscall=None, filepath=self.main_file_path, module_name=OwnMainModule, is_builtin=None, is_global=True)

        self.global_simulation_func.Calculate_StackSize()

        CodeGenVisitor = Visitor_Of_FunCodeGen(self, self.global_simulation_func, True)
        self.tokenizer.build_function_stack(self.global_simulation_func.stack_size, visitor.first_global_node)

        CodeGenVisitor.visit(self.main_astree)

        self.tokenizer.Emit_Token(VMOp.FROMALTSTACK, CodeGenVisitor.main_func_node)

    def Set_GlobalMap_For_User_Func(self):
        """
        set func_desc for OwnMainModule.
        so each OwnMainModule function get the Global Map.
        access the Global Var.
        """

        for func_desc in self.funcscope.values():
            if (not (func_desc.isyscall or func_desc.is_builtin)) and func_desc.blong_module_name == OwnMainModule:
                func_desc.global_map = self.global_simulation_func.local_map

    def StartCodeGenerate(self):
        """
        ResolveFuncDecl first before Convert_Global_First
        because of Convert_Global_First need all Function infomation.
        Golbal Code may call any function user have defined or imported.
        so need the func infomation in funcscope.

        howerver ResolveFuncDecl will create Function Desc.
        so the Glocal simulation function still do dot translation.
        and do do have the global map.
        so ResolveFuncDecl can not fill this field when ResolveFuncDecl.

        so after the Convert_Global_First. refield the FuncDescription's global_map field.
        and each function in OwnMainModule can access the global var.
        """
        # Cversion check.
        self.Cversion_check()

        # Bring Main into funscope first for the entry point. And bring all func into funcscope. Include Import
        main_func_node = self.ResolveFuncDecl(OwnMainModule)

        # assert global size for all func. do the speical func for this func main job.
        self.Calculate_GlobalSzie()

        # anlynze if the func have return value. and calculate the stack size
        for name, func_desc in self.funcscope.items():
            if not (func_desc.isyscall or func_desc.is_builtin):
                analyze_return_value_vistor = FuncVisitor_Of_AnalyzeReturnValue(func_desc)
                analyze_return_value_vistor.visit(func_desc.func_ast)
            if not func_desc.is_register_call:
                func_desc.Calculate_StackSize()

        """
        Convert Global Code only one time now.
        support any syntax Neptone support.
        """
        self.Convert_Global_First()

        self.Set_GlobalMap_For_User_Func()

        # self.Print_FuncScope()

        # Convert Main.
        if main_func_node is None:
            raise Exception("No Entry function defined. Please define a 'Main' function")

        self.current_func_node = main_func_node
        main_desc = FuncDescription('Main', None, main_func_node, False, self.main_file_path, OwnMainModule, False, False, self.global_simulation_func.local_map)
        main_desc.Calculate_StackSize()
        self.ConvertFuncDecl(main_desc)

        # Iter the funcscope. Convert all other Func.
        for name, func_desc in self.funcscope.items():
            if not func_desc.is_register_call:
                self.current_func_node = func_desc.func_ast
                self.ConvertFuncDecl(func_desc)

        self.LinkProcess()

        # self.Dump_Asm()
        self.Generate_Function_Local_Map(self.main_file_path, main_desc)
        self.Generate_Abi_list(main_func_node)

    def Cversion_check(self):
        Cversion_vistior = CVersion_Visitor(self)
        Cversion_vistior.visit(self.main_astree)

    # Convert Func
    def ConvertFuncDecl(self, func_desc):
        # assert(func_desc.func_ast is not None)
        # ast.fix_missing_locations(func_desc.func_ast)
        # func_desc.Calculate_StackSize(self.global_num)

        # build dynamic stack first
        # self.tokenizer.build_function_stack(func_desc.stack_size, func_desc.func_ast)

        # load the argument which passed by caller into stackscope
        CodeGenVisitor = Visitor_Of_FunCodeGen(self, func_desc)
        CodeGenVisitor.visit(func_desc.func_ast)
        # self.tokenizer.dump_all_vm_token()

    # bring all import func into funscope. Include compile builtinl
    def ResolveFuncDecl(self, visited_module, list_func_imported=None):
        # default add the Builtins_Module.
        if visited_module == OwnMainModule:
            func_visitor = Visitor_Of_FuncDecl(self, Builtins_Module, ['*'])
            func_visitor.visit(func_visitor.module_ast_tree)

        func_visitor = Visitor_Of_FuncDecl(self, visited_module, list_func_imported)
        func_visitor.visit(func_visitor.module_ast_tree)
        main_func_node = func_visitor.main_func_node
        return main_func_node

    def Calculate_GlobalSzie(self):
        visitor_global = Visitor_Of_Global(self)
        visitor_global.visit(self.main_astree)
        self.global_num = visitor_global.global_num

    def NewLabel(self):
        label_len = len(self.labels)
        self.labels.append(-1)
        return label_len

    def SetLabel(self, label, address):
        self.labels[label] = address

    @property
    def pc(self):
        return self.tokenizer._address - 1

    def NewFunc(self, node, isyscall, filepath, module_name, is_builtin):
        name = node.name
        funcast = node
        label = self.NewLabel()
        # if not (isyscall or is_builtin):
        #    newfunc = FuncDescription(name,label, funcast, isyscall, filepath, module_name, is_builtin, False, self.global_simulation_func.local_map)
        # else:
        #    newfunc = FuncDescription(name,label, funcast, isyscall, filepath, module_name, is_builtin)
        newfunc = FuncDescription(name, label, funcast, isyscall, filepath, module_name, is_builtin)

        if name in self.funcscope.keys():
            oldfunc = self.funcscope[name]
            # if ((not (oldfunc.isyscall or oldfunc.is_builtin)) and name != 'range') and (oldfunc.func_ast.lineno != newfunc.func_ast.lineno or oldfunc.blong_module_name != newfunc.blong_module_name):
            # for the compatibility of boa.xxx.yyy and ontoloy.xxx.yyy
            old_blong_module_name = re.sub('^ontology\.|^boa\.', '', oldfunc.blong_module_name)
            new_blong_module_name = re.sub('^ontology\.|^boa\.', '', newfunc.blong_module_name)

            if oldfunc.func_ast.lineno != newfunc.func_ast.lineno or old_blong_module_name != new_blong_module_name:
                assert(oldfunc.name == newfunc.name)
                raise Exception("[ERROR: file %s. line %d]. Function '%s' defined before at file %s line %d." % (filepath, node.lineno, name, oldfunc.filepath, oldfunc.src_lineno))

            return

        self.funcscope[newfunc.name] = newfunc

    def Get_FuncDesc(self, funcname, node, filepath):
        if funcname not in self.funcscope.keys():
            raise Exception("[ERROR: file %s. line %d]. Function '%s' do not defined or imported." % (filepath, node.lineno, funcname))
        return self.funcscope[funcname]


def CodeGenerate(SrcPath):
    codegencontext = CodeGenContext(SrcPath)
    codegencontext.StartCodeGenerate()
    return codegencontext
