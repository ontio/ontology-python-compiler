from bytecode import Bytecode
import ast
from ast import NodeTransformer, NodeVisitor
import inspect
import pdb
import dis


class RewriteDicts(NodeTransformer):

    last_store_name = None

    updated_dicts = []

    def visit_Dict(self, node):
        if len(node.keys):

            if self.last_store_name and self.last_store_name.id and self.last_store_name.lineno == node.lineno:
                for item in node.values:
                    if isinstance(item, ast.Dict):
                        raise Exception("Cannot use dictionaries inside of dictionaries")

                node.name = self.last_store_name.id
                self.updated_dicts.append(node)
                self.last_store_name = None
            else:
                raise Exception("Dictionary names must be declared")

        return ast.Dict(keys=[], values=[], lineno=node.lineno)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.last_store_name = node
        else:
            self.last_store_name = None
        return node

class ABI(ast.NodeVisitor):
    def visit_Module(self, node):
        self.Funclist = []
        self.AbiFunclist = []
        self.FuncMap = []
        self.home_module_in = False
        self.generic_visit(node)
        #self.ABI_result= {"functions":self.AbiFunclist}
        self.ABI_result= {}

    def visit_ClassDef(self, node):
        print("Error Line %d ONT-python do not support class def\n" % node.lineno)
        exit()

    def visit_FunctionDef(self, node):
        args =[]
        if node.name in self.Funclist:
            # contruct args list first
            for arg in node.args.args:
                args.append({"name": arg.arg, "type":""})
                
            self.AbiFunclist.append({"name":node.name, "parameters":args})

        self.checking_abilist = False
        if node.name == 'Main':
            self.checking_abilist = True
            self.home_module_in = True
        self.generic_visit(node)
        self.checking_abilist = False

    def visit_Compare(self, node):
        if self.checking_abilist == True and type(node.left).__name__ == 'Name' and node.left.id == 'operation' and len(node.ops) == 1 and type(node.ops[0]).__name__ == 'Eq' and len(node.comparators) == 1 and type(node.comparators[0]).__name__ == 'Str':
            self.Funclist.append(node.comparators[0].s)
        self.generic_visit(node)


def preprocess_method_body(source_code_obj, MethodName):

    src = inspect.getsource(source_code_obj)

    ast_tree = ast.parse(src)

    visitor = RewriteDicts()
    ast_tree = visitor.visit(ast_tree)

    ast.fix_missing_locations(ast_tree)
    updated_code = compile(ast_tree, filename='<ast>', mode='exec')
    bc = Bytecode.from_code(updated_code)

    dlist = visitor.updated_dicts
    RewriteDicts.updated_dicts = []
    RewriteDicts.last_store_name = None

    return bc[0].arg, dlist
