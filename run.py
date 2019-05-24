#!/usr/bin/env python3
import getopt
import sys
import subprocess
import os
from ontology.compiler import Compiler

filename = None
runmode = 0
deletedebug = False
testing = False

def deletedebugfile(strs):
    '''
    Deletes the files ending with the suffix
    '''
    d_file = filename.replace('.py', strs)
    if os.path.isfile(d_file):
        subprocess.call(["rm", d_file])


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "n:m:d:t")
    for op, value in opts:
        if op == "-n":
            filename = value
        if op == "-m":
            runmode = int(value)
        if op == "-d":
            deletedebug = True
        if op == "-t":
            testing = True

    if filename is None:
        print("Error: Filename is not set")
        exit()

    error = False
    message = ""
    if runmode == 1:
        message = "Runmode 1. Compile file " + filename
        try:
            Compiler.Compile(filename)
        except:
            error = True
    elif runmode == 0:
        message = "Runmode 0. Dump avm code message of file " + filename
        try:
            compiler = Compiler.Compile(filename)
            compiler.DumpAsm()
        except:
            error = True

    if deletedebug:
        deletedebugfile('.abi.json')
        deletedebugfile('.debug.json')
        deletedebugfile('.Func.Map')
    if testing:
        deletedebugfile('.abi.json')
        deletedebugfile('.debug.json')
        deletedebugfile('.Func.Map')
        deletedebugfile('.avm')
        deletedebugfile('.avm.str')
        deletedebugfile('.warning')
        result = 0 if error is True else 1
        print(result)
    else:
        print(message)
