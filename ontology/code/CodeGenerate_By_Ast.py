import ast
import os
import binascii
import importlib
from ontology.util import Digest
from ontology.code.astvmtoken import *
from ontology.interop import VMOp
from binascii import a2b_hex
from ontology import __version__
import json
from ontology.code.StaticAppCall import RegisterAppCall, NotifyAction

ONTOLOGY_SC_FRAMEWORK   = 'ontology.interop.'
ONTOLOGY_BUILTINS_M     = 'ontology.builtins'
OwnMainModule           = 'OwnMainModule'
ForIndexPrefix          = 'ForIndexPrefix_Var###'
BUILTIN_AND_SYSCALL_LABEL_ADDR  = -2
# keys, values, has_key current not support
#buildins_list           = ['state', 'bytes', 'bytearray','ToScriptHash', 'print', 'list','len','abs','min','max','concat','take' ,'substr','keys','values', 'has_key','sha1', 'sha256','hash160', 'hash256', 'verify_signature', 'reverse','append','remove', 'Exception', 'throw_if_null','breakpoint']
ONE_LINE_EXPR_SUPPORT_AST_TYPE   = ['Pass', 'Str']
# xxx. Migrate have return value acctually.
WITHOUT_RETURN_BUILTINSYSCALL = ['print', 'throw_if_null', 'breakpoint', 'Notify', 'Migrate', 'Put','Destory','append', 'remove']

def print_location():
    f_frame = sys._getframe().f_back
    print("Location: ",f_frame.f_code.co_filename, f_frame.f_lineno, f_frame.f_code.co_name)


def Print_DoNot_Support(func_desc, node, message):
    print("Compiler ERROR. File: %s Function: %s .Line: %d. Ontology Python Compiler do not support %s" %(func_desc.filepath, func_desc.name, node.lineno, message))
    exit()

def Print_Error(func_desc, node , message):
    print("Compiler ERROR. File: %s Function: %s .Line: %d. %s" %(func_desc.filepath, func_desc.name, node.lineno, message))
    exit()

def Print_Not_Support(filepath, node, message):
    print("Compiler ERROR. File: %s .Line: %d. Ontology Python Compiler do not support %s" %(filepath, node.lineno, message))
    exit()

def Print_Error_global(filepath, node , message):
    print("Compiler ERROR. File: %s .Line: %d. %s" %(filepath, node.lineno, message))
    exit()


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

class FuncVisitor_Of_AnalyzeReturnValue(ast.NodeVisitor):
    def __init__(self, func_desc):
        self.func_desc      = func_desc
        self.current_node   = None
        self.already_visited    = False
        self.visit_returned       = False

    def Print_DoNot_Support(self, message):
        print("Compiler ERROR. File: %s Function: %s Line: %d . Ontology Python Compiler do not support %s" %(self.func_desc.filepath, self.func_desc.name, self.current_node.lineno, message))
        exit()

    def Print_Error(self, message):
        print("Compiler ERROR. File: %s Function: %s Line: %d. %s" %(self.func_desc.filepath, self.func_desc.name, self.current_node.lineno, message))
        exit()
        
    def visit_FunctionDef(self, node):
        self.current_node = node
        if self.already_visited :
            self.Print_DoNot_Support("function define in function")
        self.already_visited = True

        if node.decorator_list != []:
            self.Print_DoNot_Support("decorator")
        self.generic_visit(node)

    def visit_Return(self, node):
        self.current_node = node
        if self.func_desc.have_return_value and node.value == None:
            self.Print_DoNot_Support("return value before. but here returns None. will get error" )

        if self.visit_returned and (not self.func_desc.have_return_value) and node.value != None:
            self.Print_DoNot_Support("return None before. but here returns value. will get error")

        if node.value != None :
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
        if self.checking_abilist == True and type(node.left).__name__ == 'Name' and node.left.id == 'operation' and len(node.ops) == 1 and type(node.ops[0]).__name__ == 'Eq' and len(node.comparators) == 1 and type(node.comparators[0]).__name__ == 'Str':
            self.Funclist.append(node.comparators[0].s)

class Abivisitor_step1(ast.NodeVisitor):
    def __init__(self, funclist):
        self.Funclist = funclist
        self.AbiFunclist = []

    def visit_FunctionDef(self, node):
        args =[]
        if node.name in self.Funclist:
            # contruct args list first
            for arg in node.args.args:
                args.append({"name": arg.arg, "type":""})
                
            self.AbiFunclist.append({"name":node.name, "parameters":args})

class FuncVisitor_Of_StackSize(ast.NodeVisitor):
    def __init__(self, func_desc):
        self.stack_size         = 0
        self.func_desc          = func_desc
        self.already_visited    = False
        self.current_node       = None
        self.arg_num            = 0

    def generic_visit(self, node):
        self.current_node = node
        ast.NodeVisitor.generic_visit(self, node)

    def Print_DoNot_Support(self, message):
        print("Compiler ERROR. File: %s Function: %s Line: %d . Ontology Python Compiler do not support %s" %(self.func_desc.filepath, self.func_desc.name, self.current_node.lineno, message))
        exit()

    def visit_FunctionDef(self, node):
        self.current_node = node
        if self.already_visited :
            self.Print_DoNot_Support("function define in function")
        self.already_visited = True

        if node.decorator_list != []:
            self.Print_DoNot_Support("decorator")

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
        self.current_node = node

        # these kinds of system call have vararg.
        if (self.func_desc.isyscall or self.func_desc.is_builtin) and (self.func_desc.name == "RegisterAppCall" or self.func_desc.name == "DynamicAppCall" or self.func_desc.name == "RegisterAction" or self.func_desc.name == 'state'):
            pass
        else:
            if node.vararg != None:
                self.Print_DoNot_Support("vararg")

            if node.defaults != []:
                self.Print_DoNot_Support("defaults")

        self.func_desc.arg_num    = len(node.args)
        self.arg_num    = len(node.args)
        self.stack_size += len(node.args)

    def visit_Return(self, node):
        self.current_node = node
        self.stack_size += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.current_node = node
        # index, result, iter , len
        self.stack_size += 4
        self.generic_visit(node)

class Visitor_Of_Global(ast.NodeVisitor):
    def __init__(self, codegencontext):
        self.global_num = 0
        self.codegencontext = codegencontext

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
                newfunc = FuncDescription(register_func_name, None, None, True, None, None, False)
                self.codegencontext.funcscope[newfunc.name] = newfunc
                args = node.value.args
                newfunc.arg_num = len(args) - 1
                newfunc.is_register_call = True
                new_app_call = RegisterAppCall(register_func_name, args)
                assert(newfunc.arg_num >= 0)
                if register_func_name in self.codegencontext.register_appcall.keys():
                    print("ERROR: %s registered before" %(register_func_name))
                    exit()
                self.codegencontext.register_appcall[register_func_name] = new_app_call
                return
            elif self.codegencontext.funcscope[node.value.func.id].isyscall and node.value.func.id == 'RegisterAction':
                assert(len(node.targets) == 1)
                assert(type(node.targets[0]).__name__ == 'Name')
                register_func_name = node.targets[0].id
                newfunc = FuncDescription(register_func_name, None, None, True, None, None, False)
                self.codegencontext.funcscope[newfunc.name] = newfunc
                args = node.value.args
                newfunc.arg_num = len(args) - 1
                newfunc.is_register_call = True
                assert(newfunc.arg_num >= 0)
                newaction = NotifyAction(register_func_name, args)
                if register_func_name in self.codegencontext.register_action.keys():
                    print("ERROR: %s registered before" %(register_func_name))
                    exit()
                self.codegencontext.register_action[register_func_name] = newaction
                return
            else:
                assert(False)

        self.global_num += len(node.targets)
        self.generic_visit(node)

class Visitor_Of_FuncDecl(ast.NodeVisitor):
    def __init__(self, codegencontext, visited_module, list_func_imported):
        self.main_func_node     = None
        self.visited_module     = visited_module; 
        self.codegencontext     = codegencontext
        self.isyscall_module    = False
        self.is_builtin_module  = False
        self.is_main_module     = False
        self.list_func_imported = list_func_imported
        if visited_module == OwnMainModule: 
            self.is_main_module = True
            assert(self.list_func_imported == None)

        if visited_module != OwnMainModule: 
            pymodule = importlib.import_module(visited_module, visited_module)
            module_file_path = pymodule.__file__
            source = open(module_file_path, 'rb')
            source_src = source.read()
            self.module_file_path   = module_file_path
            self.module_ast_tree    = ast.parse(source_src)
        else:
            self.module_file_path   = self.codegencontext.main_file_path
            self.module_ast_tree    = self.codegencontext.main_astree

        if ONTOLOGY_SC_FRAMEWORK in self.visited_module:
            self.isyscall_module = True
        elif self.visited_module == ONTOLOGY_BUILTINS_M:
            self.is_builtin_module = True

        assert((self.isyscall_module and self.is_builtin_module) == False)

    # here do not need visit the children node. so do not call the generic_visit.
    def visit_FunctionDef(self, node):
        if node.name == 'main' or node.name == 'Main':
            if not self.is_main_module:
                print("%s was Imported. Can not have Main func" %(self.visited_module))
                exit()

            self.main_func_node = node
            return

        if self.is_main_module:
            assert(self.list_func_imported == None)
            self.codegencontext.NewFunc(node, self.isyscall_module, self.module_file_path, self.visited_module, False)
        else:
            assert(self.list_func_imported != [])
            # only add import func
            if '*' in self.list_func_imported or node.name in self.list_func_imported:
                if node.name == 'range':
                    self.codegencontext.NewFunc(node, self.isyscall_module, self.module_file_path, self.visited_module, False)
                else:
                    self.codegencontext.NewFunc(node, self.isyscall_module, self.module_file_path, self.visited_module, self.is_builtin_module)

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
            if alias.asname != None:
                if self.visited_module == OwnMainModule: 
                    Print_Not_Support(self.codegencontext.main_file_path, node, "from ... import .. as ..")
                else:
                    Print_Not_Support(self.module_file_path, node, "from ... import .. as ..")

        self.codegencontext.ResolveFuncDecl(node.module, list_func_imported)

class Visitor_Of_FunCodeGen(ast.NodeVisitor):
    def __init__(self, codegencontext ,func_desc, is_for_global = False):
        self.codegencontext     = codegencontext
        self.func_desc          = func_desc
        self.already_visited    = False
        self.is_for_global      = is_for_global
        self.current_node       = None
        self.latest_loop_break_label    = []
        self.is_in_loop         = False
        self.codegencontext.tokenizer.current_func = func_desc
        self.codegencontext.tokenizer.global_converting = is_for_global

    # so when get a bug need check in this func. is there any node should transfered do not transfer.
    def generic_visit(self, node):
        self.current_node = node
        #ast.NodeVisitor.generic_visit(self, node)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        self.current_node = node
        self.Print_DoNot_Support("Class def")

    def Print_DoNot_Support(self, message):
        print("Compiler ERROR. [File: %s Function: %s ] Line: %d . Ontology Python Compiler do not support %s" %(self.func_desc.filepath, self.func_desc.name, self.current_node.lineno, message))
        exit()

    def Print_Error(self, message):
        print("Compiler ERROR. File: %s Function: %s Line: %d. %s" %(self.func_desc.filepath, self.func_desc.name, self.current_node.lineno, message))
        exit()

    def visit_Module(self, node):
        self.current_node = node
        if not self.is_for_global:
            print("Compiler Error. Impossible get Module in Function decl.")
            exit()
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.current_node = node
        if self.is_for_global:
            return
        if self.already_visited:
            self.Print_DoNot_Support("Function define in function")

        self.already_visited = True

        if not (self.func_desc.isyscall or self.func_desc.is_builtin): 
            # syscall and builtin get no func code. so do not set the label
            if node.name != 'Main' and node.name != 'main':
                self.codegencontext.SetLabel(self.codegencontext.funcscope[node.name].label, self.codegencontext.pc + 1)

            self.codegencontext.tokenizer.build_function_stack(self.func_desc.stack_size, self.func_desc.func_ast)
            #ast.fix_missing_locations(node)
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
            print("Compiler Bug. Global can not have argument")
            exit()

        if node.vararg != None:
            self.Print_DoNot_Support("vararg")

        if node.defaults != []:
            self.Print_DoNot_Support("defaults")

        for arg in node.args:
            position = self.func_desc.NewLocal(arg.arg)
            self.codegencontext.tokenizer.Emit_StoreLocal(position, arg)

        self.Convert_Gloabal()
        self.codegencontext.tokenizer.global_converting = False

    def Convert_Gloabal(self):
        # global own the visitor by itself. but note the tokenizer confict.
        CodeGenVisitor = Visitor_Of_FunCodeGen(self.codegencontext, self.func_desc, True)
        # due the  args translate first. so get the argname have the upper priority. so if have the same name of args and the global. 
        CodeGenVisitor.visit(self.codegencontext.main_astree)

    def visit_Assign(self, node):
        self.current_node = node
        self.visit(node.value)

        for target in node.targets:
            if len(node.targets) > 1:
                self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, target)
            self.visit(target)

        if len(node.targets) > 1:
            self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, target)

    def visit_AugAssign(self, node):
        self.current_node = node
        # load value
        self.visit(node.value)

        # load target
        self.ctx_transformer = ReWrite_CTX_STORE_TO_LOAD(self.func_desc)
        target_newnode = self.ctx_transformer.visit(node.target)
        self.visit(target_newnode)
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
            self.Print_DoNot_Support("multi iter")

        if node.orelse != []:
            self.Print_DoNot_Support("for orelse")

        self.is_in_loop = True
        # alloc Label.
        for_start_label = self.codegencontext.NewLabel()
        for_end_label   = self.codegencontext.NewLabel()
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
        jumpostion_for_end = for_end_label.to_bytes(2, 'little', signed=True)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, jumpostion_for_end)

        # target_position: update save iter. xxx. must use target. so the body can ref it
        self.codegencontext.tokenizer.Emit_LoadLocal(result_position, node)
        self.codegencontext.tokenizer.Emit_LoadLocal(index_position, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.PICKITEM, node)
        #target_position = self.func_desc.Get_LocalStackPosition(ForIndexPrefix + str(self.func_desc.for_position))
        target_position = self.func_desc.Get_LocalStackPosition(node.target.id) # here Ont only support Name taget. so here just ref it
        self.codegencontext.tokenizer.Emit_StoreLocal(target_position, node.target)

        # update save index.
        self.codegencontext.tokenizer.Emit_LoadLocal(index_position, node)
        self.codegencontext.tokenizer.Emit_Integer(1, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.ADD, node)
        self.codegencontext.tokenizer.Emit_StoreLocal(index_position, node)

        # generate body.
        for stmt in node.body:
            # any visit have chance the latest_loop_break_label. so here revese it.
            self.visit(stmt)
            # here body break will jump into the for_end_label. continue will jump into for_start_label
            self.latest_loop_break_label = [for_start_label, for_end_label]
            self.is_in_loop = True

        # generate jump to condition assert
        jumpostion_for_start = for_start_label.to_bytes(2, 'little', signed=True)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, self.current_node, jumpostion_for_start)
        self.codegencontext.SetLabel(for_end_label, self.codegencontext.pc + 1)
        self.is_in_loop = False
        #self.codegencontext.tokenizer.Emit_Token(VMOp.NOP, stmt)

    def visit_While(self, node):
        self.current_node = node
        if node.orelse !=[]:
            self.Print_DoNot_Support("While orelse")
        # alloc Label.
        self.is_in_loop = True
        while_start_label = self.codegencontext.NewLabel()
        while_end_label   = self.codegencontext.NewLabel()
        self.latest_loop_break_label = [while_start_label, while_end_label]
        jumpostion_while_start = while_start_label.to_bytes(2, 'little', signed=True)
        jumpostion_while_end = while_end_label.to_bytes(2, 'little', signed=True)

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

        # generate jump to condition assert
        self.codegencontext.SetLabel(while_end_label, self.codegencontext.pc + 1)
        # self.codegencontext.tokenizer.Emit_Token(VMOp.NOP, stmt)
        self.is_in_loop = False
        return

    def visit_Pass(self, node):
        self.current_node = node
        self.codegencontext.tokenizer.Emit_Token(VMOp.NOP, node)

    def visit_Break(self, node):
        self.current_node = node
        if not self.is_in_loop:
            self.Print_Error("can not break in non loop")
        assert(len(self.latest_loop_break_label) == 2)
        # jmp to the end label
        target_label    = self.latest_loop_break_label[1]
        target_postion  = target_label.to_bytes(2, 'little', signed=True)
        self.codegencontext.tokenizer.Emit_Token(VMOp.JMP, node, target_postion)

    def visit_Continue(self, node):
        self.current_node = node
        if not self.is_in_loop:
            self.Print_Error("can not continue in non loop")
        assert(len(self.latest_loop_break_label) == 2)
        # jmp to the end label
        target_label    = self.latest_loop_break_label[0]
        target_postion  = target_label.to_bytes(2, 'little', signed=True)
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
        assert(False)

    def visit_BoolOp(self, node):
        assert(len(node.values) >= 2)
        target_label    = self.codegencontext.NewLabel()
        target_postion  = target_label.to_bytes(2, 'little', signed=True)

        self.visit(node.values[0])
        for i in range(len(node.values)):
            if i == 0:
                continue
            self.visit(node.values[i])
            self.visit(node.op) 
            if (type(node.op).__name__ == 'Or'):
                self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
                self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIF, node, target_postion)
            elif (type(node.op).__name__ == 'And'):
                self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
                self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, target_postion)
            else:
                assert(False)

        self.codegencontext.SetLabel(target_label, self.codegencontext.pc + 1)

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
        self.codegencontext.tokenizer.Emit_Token(VMOp.NUMNOTEQUAL, node)
    def visit_In(self, node):
        self.Print_DoNot_Support("in")
    def visit_NotIn(self, node):
        self.Print_DoNot_Support("not in")

    def visit_Not(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.NOT, node)
    def visit_Invert(self, node):
        self.codegencontext.tokenizer.Emit_Token(VMOp.INVERT, node)
    def visit_UnaryOp(self, node):
        self.current_node = node
        self.visit(node.operand)
        self.visit(node.op)
    def visit_UAdd(self, node):
        assert(False)
    def visit_USub(self, node):
        assert(False)

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
        if node.msg != None:
            self.Print_DoNot_Support("Assert with message")
        self.visit(node.test)
        self.codegencontext.tokenizer.Emit_Token(VMOp.THROWIFNOT, node)

    def visit_List(self, node):
        self.current_node = node
        if type(node.ctx).__name__ != 'Load':
            self.Print_DoNot_Support((type(node.ctx).__name__) + "type List")
        else:
            for expr in node.elts:
                self.visit(expr)
            
            self.codegencontext.tokenizer.Emit_Integer(len(node.elts), node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.PACK , node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.REVERSE, node)

    def visit_Call(self, node):
        self.current_node = node
        if type(node.func).__name__ != 'Name' or type(node.func.ctx).__name__ != 'Load':
            self.Print_DoNot_Support("expr func")

        if node.keywords != []:
            self.Print_DoNot_Support("Call function with keywords")

        funcname = node.func.id
        func_desc = self.codegencontext.funcscope[funcname]

        # prepare args. note. concat, take, has_key, substr do not need reverse
        if funcname in ['concat', 'take', 'has_key', 'substr']:
            for arg in node.args:
                self.visit(arg)
        else:
            # RegisterAppCall and RegisterAction is handle by visitor of global
            if  func_desc.isyscall and (func_desc.name == "RegisterAppCall" or func_desc.name == "RegisterAction"):
                return

            # DynamicAppCall get the vararg args.
            if  (func_desc.isyscall or func_desc.is_builtin) and (func_desc.name == "DynamicAppCall" or func_desc.name == 'state'):
                pass
            else:
                if  func_desc.arg_num != len(node.args):
                    self.Print_Error("Function %s Need %d args. but you passed %d args" %(funcname, func_desc.arg_num,len(node.args)))
            for arg in reversed(node.args):
                self.visit(arg)

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
            if vmtoken == None:
                self.Print_DoNot_Support("builtin %s" %(funcname))
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
                sys_name =  'System.Runtime.Notify'
                syscall_name =sys_name.encode('utf-8')
            else:
                sys_name =  func_desc.blong_module_name + func_desc.name
                syscall_name = sys_name.replace(ONTOLOGY_SC_FRAMEWORK, '').encode('utf-8')

            length = len(syscall_name)
            systemcall_name_array = bytearray([length]) + bytearray(syscall_name)
            vmtoken = self.codegencontext.tokenizer.Emit_Token(VMOp.SYSCALL, node, systemcall_name_array)
            vmtoken.syscall_name = sys_name 

            return

        self.codegencontext.tokenizer.Emit_Token(VMOp.CALL, node, call_data)

    # only save a bool(true or false) to the evalution stack.
    def visit_Compare(self, node):
        self.current_node = node
        opslen          = len(node.ops)
        comparatorslen  = len(node.comparators)
        jump_target_label = self.codegencontext.NewLabel()
        jump_target_position = jump_target_label.to_bytes(2, 'little', signed=True)
        for i in range(opslen):
            if i > 0:
                self.visit(node.comparators[i - 1])
            else:
                self.visit(node.left)

            self.visit(node.comparators[i])
            self.visit(node.ops[i])
            self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
            self.codegencontext.tokenizer.Emit_Token(VMOp.JMPIFNOT, node, jump_target_position)

        self.codegencontext.SetLabel(jump_target_label, self.codegencontext.pc + 1)

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
        self.current_node = node
        name_position = self.func_desc.Get_LocalStackPosition(node.id)
        if type(node.ctx).__name__ == 'Load':
            self.codegencontext.tokenizer.Emit_LoadLocal(name_position, node)
        elif type(node.ctx).__name__ == 'Store':
            self.codegencontext.tokenizer.Emit_StoreLocal(name_position, node)
        else:
            assert("Wrong Name ctx type")

    def visit_Subscript(self, node):
        self.current_node = node
        if type(node.ctx).__name__ == 'Load':
            self.visit(node.value)  # cal list or map or some else support
            if type(node.slice).__name__ == 'Index':
                self.visit(node.slice)  # cal slice. note slice is a super set of Index
                self.codegencontext.tokenizer.Emit_Token(VMOp.PICKITEM, node)
            # note. here due to support str slice. how ever python can not difference the list and str by the node.value. so only can support one type slice.
            elif type(node.slice).__name__ == 'Slice':
                if node.slice.step != None:
                    self.Print_DoNot_Support("slice with step")

                if node.slice.upper != None:
                    self.visit(node.slice.upper)
                    uppernode = node.slice.upper
                    if type(uppernode).__name__ == 'UnaryOp' and type(uppernode.op).__name__ == 'USub':
                        Print_Error(self.func_desc, node ,"slice upper smaller than 0")
                else:
                    self.codegencontext.tokenizer.Emit_Token(VMOp.DUP, node)
                    self.codegencontext.tokenizer.Emit_Token(VMOp.ARRAYSIZE, node)

                if node.slice.lower != None:
                    self.visit(node.slice.lower)
                    lowernode = node.slice.lower
                    if type(lowernode).__name__ == 'UnaryOp' and type(lowernode.op).__name__ == 'USub':
                        Print_Error(self.func_desc, node ,"slice lower smaller than 0")
                else:
                    self.codegencontext.tokenizer.Emit_Integer(0, node)

                self.codegencontext.tokenizer.Emit_Slice(node)
            else:
                self.Print_DoNot_Support("Subscript such slice")

        elif type(node.ctx).__name__ == 'Store':
            if type(node.slice).__name__ == 'Index':
                self.visit(node.value)  # cal list or map or some else support
                self.visit(node.slice)  # cal index
                self.codegencontext.tokenizer.Emit_Token(VMOp.ROT, node)
                self.codegencontext.tokenizer.Emit_Token(VMOp.SETITEM, node)
            else:
                self.Print_DoNot_Support("Subscript Slice Assgin")
        else:
            assert("Wrong Name ctx type")

    def visit_Slice(self, node):
        assert(False)

    def visit_Return(self, node):
        self.current_node = node
        if node.value != None:
            self.visit(node.value)

        self.codegencontext.tokenizer.Emit_Token(VMOp.FROMALTSTACK, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)
        self.codegencontext.tokenizer.Emit_Token(VMOp.RET, node)

    def visit_NameConstant(self, node):
        self.current_node = node
        if node.value == True:
            self.codegencontext.tokenizer.Emit_Integer(1, node)
        elif node.value == False:
            self.codegencontext.tokenizer.Emit_Integer(0, node)
        else:
            Print_DoNot_Support(self.func_desc, node, "such NameConstant")

    def visit_Index(self, node):
        self.current_node = node
        self.generic_visit(node)

    def visit_Expr(self, node):
        self.current_node = node
        if type(node.value).__name__ == 'Call':
            self.generic_visit(node)
            if type(node.value.func).__name__ == 'Name':
                funcname    = node.value.func.id
                func_desc   = self.codegencontext.funcscope[funcname]
                # handle normal func first
                if not (func_desc.is_builtin or func_desc.isyscall):
                    if func_desc.have_return_value :
                        self.codegencontext.tokenizer.Emit_Token(VMOp.DROP, node)
                # here hypothesis all buildins and syscall other than conditon will return a value.
                elif not (funcname in WITHOUT_RETURN_BUILTINSYSCALL or funcname in self.codegencontext.register_action.keys()):
                    self.Print_DoNot_Support("Builtins or syscall %s call with no value assigned" %(funcname))
            else:
                self.Print_DoNot_Support("dynamic funcname")
        elif type(node.value).__name__ in ONE_LINE_EXPR_SUPPORT_AST_TYPE:
            if type(node.value).__name__ == 'Pass':
                self.generic_visit(node)
            elif type(node.value).__name__ == 'Str':
                #self.generic_visit(node)
                pass
            else:
                self.generic_visit(node)
        else:
            self.Print_DoNot_Support("Expr with one line. due to carefull handle stack stack.")

        
class FuncDescription:
    def __init__(self, name, label, node, isyscall, filepath, module_name, is_builtin):
        self.name       = name
        self.label      = label
        self.func_ast   = node
        if node:
            self.src_lineno = node.lineno
        self.filepath   = filepath
        self.isyscall   = isyscall
        self.is_builtin = is_builtin
        self.is_register_call  = False
        self.for_position       = 0
        self.have_return_value  = False
        self.arg_num    = 0
        if self.isyscall:
            self.blong_module_name = module_name

        self.local_num  = 0
        self.local_map  = {}
        # note. when self.is_builtin or self.isyscall assert. this value have no meanning
        self.stack_size = 0
        assert((self.isyscall and self.is_builtin) == False)

    def Calculate_StackSize(self, global_num):
        self.stack_size         = global_num
        visitor_stacksize       = FuncVisitor_Of_StackSize(self)
        visitor_stacksize.visit(self.func_ast)
        self.stack_size         += visitor_stacksize.stack_size
        #self.arg_num            = visitor_stacksize.arg_num
        #print("Function %s. stack_size %d  self.arg_num %d" %(self.name, self.stack_size, self.arg_num))

    def NewLocal(self, name):
        if name in self.local_map.keys():
            print("var %s already defined" %(name))
            exit()
        self.local_map[name] = self.local_num
        self.local_num += 1
        return self.local_num - 1

    def Get_LocalStackPosition(self, name):
        if name in self.local_map.keys():
            return self.local_map[name]
        else:
            return self.NewLocal(name)
            

class CodeGenContext:
    def __init__(self, SrcPath):
        source                  = open(SrcPath, 'rb')
        SrcCode                 = source.read()
        self.tokenizer          = AstVMTokenizer()
        self.funcscope          = {}
        self.labels             = []
        self.current_func_node  = None
        self.main_astree        = ast.parse(SrcCode)
        self.main_file_path     = SrcPath
        self.global_num         = 0
        self.file_hash          = None
        self.register_appcall   = {}
        self.register_action    = {}
        #print(ast.dump(self.main_astree))

    def LinkProcess(self):
        all_token = self.tokenizer.vm_tokens.items()
        link_op = [VMOp.JMP, VMOp.JMPIF, VMOp.JMPIFNOT, VMOp.CALL]
        prev_addr = -1
        for addr, vmtoken in all_token:
            assert(vmtoken.addr == addr)
            assert(prev_addr < addr)

            if vmtoken.vm_op in link_op:
                target_label    = int.from_bytes(vmtoken.data, byteorder = 'little') 
                target_addr     = self.labels[target_label]
                assert(target_addr != -1)
                vmtoken.target  = target_addr
                offset          = target_addr - vmtoken.addr
                vmtoken.data    = offset.to_bytes(2, 'little', signed=True)

        prev_addr   = addr
        self.write_code()
        return

    def Dump_Asm(self):
        all_token = self.tokenizer.vm_tokens.items()
        link_op = [VMOp.JMP, VMOp.JMPIF, VMOp.JMPIFNOT, VMOp.CALL]
        prev_addr = -1
        prev_lineno = -1

        print("{:<30} {:<10} {:<5} {:<10} {:<20} {:<20} {:<20}".format("FuncName", "Lineno", "Col", "Offset", "OpCode", "JumpTarget", "TargetOff"))
        for addr, vmtoken in all_token:
            vmop_name = VMOp.to_name(vmtoken.out_op)
            if (type(vmop_name) == type(None)):
                vmop_name = 'PUSHBYTES' + str(vmtoken.out_op)

            assert(vmtoken.addr == addr)
            assert(prev_addr <= addr)

            if vmtoken.vm_op in link_op:
                assert(vmtoken.node.lineno)
                offset          = int.from_bytes(vmtoken.data, byteorder = 'little', signed=True) 
                target_addr     =  offset + addr
                print("{:<30} {:<10} {:<5} {:<10} {:<20} {:<20} {:<20}".format(vmtoken.cur_func.name,vmtoken.node.lineno, vmtoken.node.col_offset, vmtoken.addr, vmop_name, target_addr, offset))
            elif vmtoken.vm_op is VMOp.SYSCALL:
                assert(vmtoken.node.lineno)
                print("{:<30} {:<10} {:<5} {:<10} {:<20} {:<20}".format(vmtoken.cur_func.name, vmtoken.node.lineno, vmtoken.node.col_offset, vmtoken.addr, vmop_name, vmtoken.syscall_name))
            else:
                if hasattr(vmtoken.node, 'col_offset'):
                    assert(hasattr(vmtoken.node, 'lineno'))
                    node_line = vmtoken.node.lineno
                    node_col  = vmtoken.node.col_offset
                else:
                    node_line = prev_lineno
                    node_col  = prev_col

                print("{:<30} {:<10} {:<5} {:<10} {:<20}".format(vmtoken.cur_func.name, node_line, node_col, vmtoken.addr, vmop_name))
            prev_lineno = node_line
            prev_col    = node_col
            prev_addr   = addr

    def Generate_Debug_Json(self, output_path, data):
        hashstr = Digest.hash160(msg=data, is_hex=True) # str
        a2bhashstr = bytearray(a2b_hex(hashstr)) # str ==> bytes ==>bytearray
        a2bhashstr.reverse()
        file_hash = a2bhashstr.hex() # bytearray ==> str
        self.file_hash = file_hash

        avm_name = os.path.splitext(os.path.basename(output_path))[0]
        JsonMap = {}
        JsonMap['avm'] = {'name': avm_name, 'hash': file_hash}
        JsonMap['compiler'] = {'name': 'Ontology-Python-Compile', 'version': __version__}
        files = {}
        JsonMap['files'] = files
        prev_addr = -1
        prev_lineno = -1
        next_line_start = -1
        asmap = []
        start_addr = 0

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
                assert_start_off    = start_addr
                start_addr          = addr
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
        #self.Generate_Function_Local_Map(fullpath)

    def Generate_Function_Local_Map(self, path, main_func_desc):
        FunctionsVarMap = []
        savedfile = self.Generate_new_name(path, '.py', '.Func.Map')

        FunctionsVarMap.append({"Method": main_func_desc.name, "VarMap": main_func_desc.local_map})

        for name, func_desc in self.funcscope.items():
            if not (func_desc.isyscall or func_desc.is_builtin): 
                FunctionsVarMap.append({"Method": name, "VarMap": func_desc.local_map})

        FunctionsVarMap_t = {"Functions": FunctionsVarMap}
        json_data = json.dumps(FunctionsVarMap_t, indent=4)
        self.write_file_with_str(json_data, savedfile)

    def Generate_Abi_list(self, main_func_node):
        assert(self.file_hash != None)
        ABI_result = {}
        ABI_result["CompilerVersion"] = __version__
        ABI_result["hash"] = self.file_hash
        ABI_result["entrypoint"] = main_func_node.name
        step0 = Abivisitor_step0()
        step0.visit(self.main_astree)
        step1 = Abivisitor_step1(step0.Funclist)
        step1.visit(self.main_astree)
        ABI_result["functions"] = step1.AbiFunclist
        
        savedfile = self.Generate_new_name(self.main_file_path,'.py', '.abi.json')
        json_data = json.dumps(ABI_result, indent=4)
        self.write_file_with_str(json_data, savedfile)

    def Generate_new_name(self, path, replacestr, new_extend):
        fullpath = os.path.realpath(path)
        path, filename = os.path.split(fullpath)
        newfilename = filename.replace(replacestr,new_extend)
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
            if self.funcscope[i].func_ast != None:
                print("name: %s , label: %d, src_lineno: %d filepath: %s isyscall: %d argnum:%d" % (self.funcscope[i].name, self.funcscope[i].label, self.funcscope[i].src_lineno, self.funcscope[i].filepath, self.funcscope[i].isyscall, self.funcscope[i].arg_num))
            else:
                assert(self.funcscope[i].is_register_call)

    def StartCodeGenerate(self):
        # Bring Main into funscope first for the entry point. And bring all func into funcscope. Include Import
        main_func_node = self.ResolveFuncDecl(OwnMainModule)

        # assert global size for all func.
        self.Calculate_GlobalSzie()

        # anlynze if the func have return value. and calculate the stack size
        for name, func_desc in self.funcscope.items():
            if not (func_desc.isyscall or func_desc.is_builtin):
                analyze_return_value_vistor = FuncVisitor_Of_AnalyzeReturnValue(func_desc)
                analyze_return_value_vistor.visit(func_desc.func_ast)
            if not func_desc.is_register_call: 
                func_desc.Calculate_StackSize(self.global_num)

        #self.Print_FuncScope()

        # Convert Main.
        self.current_func_node = main_func_node
        main_desc = FuncDescription('Main', None, main_func_node,False, self.main_file_path, OwnMainModule, False)
        main_desc.Calculate_StackSize(self.global_num)
        self.ConvertFuncDecl(main_desc)

        # Iter the funcscope. Convert all other Func.
        for name, func_desc in self.funcscope.items():
            if not func_desc.is_register_call:
                self.current_func_node = func_desc.func_ast
                self.ConvertFuncDecl(func_desc)

        self.LinkProcess()

        #self.Dump_Asm()
        self.Generate_Function_Local_Map(self.main_file_path, main_desc)
        self.Generate_Abi_list(main_func_node)

    # Convert Func
    def ConvertFuncDecl(self, func_desc):
        #func_desc.Calculate_StackSize(self.global_num)

        # build dynamic stack first
        #self.tokenizer.build_function_stack(func_desc.stack_size, func_desc.func_ast)

        # load the argument which passed by caller into stackscope
        CodeGenVisitor = Visitor_Of_FunCodeGen(self, func_desc)
        CodeGenVisitor.visit(func_desc.func_ast)
        #self.tokenizer.dump_all_vm_token()

    # bring all import func into funscope. Include compile builtinl
    def ResolveFuncDecl(self, visited_module, list_func_imported=None):
        func_visitor = Visitor_Of_FuncDecl(self, visited_module, list_func_imported)
        func_visitor.visit(func_visitor.module_ast_tree)
        main_func_node = func_visitor.main_func_node
        return main_func_node

    def Calculate_GlobalSzie(self):
        visitor_global  = Visitor_Of_Global(self)
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
        name    = node.name
        funcast = node
        label   = self.NewLabel()
        newfunc = FuncDescription(name ,label, funcast, isyscall, filepath, module_name, is_builtin)
        self.funcscope[newfunc.name] = newfunc

def CodeGenerate(SrcPath):
    codegencontext = CodeGenContext(SrcPath)
    codegencontext.StartCodeGenerate()
    return codegencontext 
