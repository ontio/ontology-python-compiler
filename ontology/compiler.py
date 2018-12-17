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

    def DumpAsm(self):
        self.CodeGenerate.Dump_Asm()

    @staticmethod
    def version():
        return __version__
