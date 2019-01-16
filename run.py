#!/usr/bin/env python3
from ontology.compiler import Compiler
import getopt
import sys
import subprocess
import os

filename = None
runmode = 0
deletedebug = False


def deletedebugfile(filename, strs):
    d_file = filename.replace('.py', strs)
    if os.path.isfile(d_file):
        subprocess.call(["rm", d_file])


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "n:m:d")
    for op, value in opts:
        if op == "-n":
            filename = value
        if op == "-m":
            runmode = int(value)
        if op == "-d":
            deletedebug = True

    if filename is None:
        print("Filename do not set!!!")
        exit()

    if runmode == 1:
        print("Runmode 1. Compile file", filename)
        Compiler.Compile(filename)
    elif runmode == 0:
        print("Runmode 0. Dump avm code message of file", filename)
        compiler = Compiler.Compile(filename)
        compiler.DumpAsm()

    if deletedebug:
        deletedebugfile(filename, '.abi.json')
        deletedebugfile(filename, '.debug.json')
        deletedebugfile(filename, '.FuncMap.json')
