import os
from ontology import __version__
from ontology.code.CodeGenerate_By_Ast import CodeGenerate


class Compiler(object):
    """
    The main compiler interface class.
    The following loads a python file, compiles it to the `.avm` format
    and saves it alongside the python file.

        # return the compiler object for inspection
        compiler = Compiler.Compile('path/to/your/file.py')
    """
    __instance = None

    @staticmethod
    def instance():
        if not Compiler.__instance:
            Compiler.__instance = Compiler()
        return Compiler.__instance

    @staticmethod
    def Compile(path):
        """
        :param path: the path of the Python file to compile
        :return: The instance of the compiler

        The following returns the compiler object for inspection.

        .. code-block:: python

            from ontology.compiler import Compiler

            compiler = Compiler.Compile('path/to/your/file.py')
        """

        Compiler.__instance = None
        compiler = Compiler.instance()
        try:
            compiler.CodeGenerate = CodeGenerate(os.path.abspath(path))
        except Exception as error:
            raise Exception(error)

        return compiler

    @staticmethod
    def Compile_File(path):
        """
        :param path: the path of the Python file to compile
        :return: avm

        The following returns the avm string for the contract.

        .. code-block:: python

            from ontology.compiler import Compiler

            avm = Compiler.Compile_File('path/to/your/file.py')
        """

        Compiler.Compile(path)
        words = path.split(".")
        base = words[0] if len(words) == 2 else path
        avm_file = base + ".avm.str"

        if os.path.isfile(path):
            os.remove(base + ".abi.json")
            os.remove(base + ".avm")
            os.remove(base + ".debug.json")
            os.remove(base + ".Func.Map")
            os.remove(base + ".warning")

        with open(avm_file) as f:
            content = f.read()
            os.remove(avm_file)
            return content

    @staticmethod
    def Compile_Contract(contract):
        """
        :param contract: a string containing an entire contract
        :return: avm

        The following returns the avm string for the contract.

        .. code-block:: python

            from ontology.compiler import Compiler

            avm = Compiler.Compile_Contract('def Main(): ...')
        """

        path = "tmp_contract.py"
        temp = open(path, "w")
        temp.write(contract)
        temp.close()
        avm = Compiler.Compile_File(path)
        if os.path.isfile(path):
            os.remove(path)
        return avm

    def DumpAsm(self):
        self.CodeGenerate.Dump_Asm()

    @staticmethod
    def version():
        return __version__
