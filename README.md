
<p align="center">
  <img
    src="ontologypic.png"
    width="125px;">
</p>

<h1 align="center">Neptune</h1>
<p align="center">
  Python compiler for Ontology
</p>

[![Build Status](https://travis-ci.com/ontio/ontology-python-compiler.svg?branch=master)](https://travis-ci.com/ontio/ontology-python-compiler)
- Free software: LGPL license
  - [Overview](#overview)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)
  - [DebugInfo](#DebugInfo)

## Overview

`Neptune` is a tool for compiling Python files to the `.avm` format for usage in smart contracts on the [Ontology blockchain](https://github.com/ontio/ontology/). It currently only supports a subset of the Python language.

#### What does it currently do

- Compiles a subset of the Python language to the `.avm` format for use in the [Ontology blockchain](https://github.com/ontio/ontology)
- Works for Python 3.6+

#### What will it do

- Compile a larger subset of the Python language
- Additional syntax checks
- Optimize instr stream

#### What's new compared to neo-boa

- Basic abstract syntax trees
- Ability to write numerous expressions per line. [(See Example)](ontology_test/example/OffChainOp/test_while2.py)
- `global` keyword, works the same as [global](https://www.programiz.com/python-programming/global-keyword) in the standard python library. Allows functions to share [variables](https://www.scaler.com/topics/python/variables-in-python/). [(See Example #1)](ontology_test/example/ChainOp/test_global_and_appcall.py) [(See Example #2)](ontology_test/example/OffChainOp/test_global.py)
- Cascade bool operation. [(See Example)](ontology_test/example/OffChainOp/test_boolop_origin.py)
- Augmented assignment operators such as `+= *= /= -=` [(See Example)](ontology_test/example/OffChainOp/test_iterate.py)
- [Chained comparisons](https://www.geeksforgeeks.org/chaining-comparison-operators-python/) [(See Example)](ontology_test/example/OffChainOp/test_compare_1.py)
- [Chained assignment](https://stackoverflow.com/questions/7601823/how-do-chained-assignments-work)
- Maps nested within maps. [(See Example)](ontology_test/example/OffChainOp/test_dict.py)
- `if expression` statements. [(See Example)](ontology_test/example/OffChainOp/test_ifexpr.py)
- `for`, `while`, `break` and `continue`. [(See Example #1)](ontology_test/example/OffChainOp/test_for_1.py) [(See Example #2)](ontology_test/example/OffChainOp/test_while2.py)
- `if x in y` statements. [(See Example)](ontology_test/example/OffChainOp/test_in.py)
- `loop else` statements. [(See Example)](ontology_test/example/OffChainOp/test_for_1.py)
- `range(len), range(start, stop), range(start, stop, step)`. [(See Example)](ontology_test/example/OffChainOp/test_range.py)
- [Function default argument](https://stackoverflow.com/questions/13195989/default-values-for-function-parameters-in-python) [(See Example)](ontology_test/example/OffChainOp/test_default_vararg.py)
- [Function variable argument](https://stackoverflow.com/questions/919680/can-a-variable-number-of-arguments-be-passed-to-a-function) [(See Example)](ontology_test/example/OffChainOp/test_default_vararg.py)
- [Pass Starred argument for function call](https://stackoverflow.com/questions/12555627/python-3-starred-expression-to-unpack-a-list) [(See Example)](ontology_test/example/OffChainOp/test_default_vararg.py)
- List comprehension. [(See Example)](ontology_test/example/OffChainOp/test_list_com.py)
- Dict comprehension. [(See Example)](ontology_test/example/OffChainOp/test_dict_com2.py)
- Conditional operation
- Assert. [(See Example)](ontology_test/example/OffChainOp/test_split.py)
- [String slicing](https://www.digitalocean.com/community/tutorials/how-to-index-and-slice-strings-in-python-3) [(See Example)](ontology_test/example/OffChainOp/test_slice.py)
- Added [libont.py](ontology/libont.py) to support various list functions such as list removal and element in
- Additional syntax checks
- More accurate debug messages

## Installation

Installation requires Python version 3.6 or later.

#### Setup

Clone the repository and navigate into the project directory. Make a Python 3 virtual environment and activate it via:

```
python3 -m venv venv
source venv/bin/activate
```

Then, install the requirements:

```
pip install -r requirements.txt
```

## Usage

Import the compiler into a file with:
```
from ontology.compiler import Compiler
```

The compiler can be used in three different ways:

1) Compiling a python file to a new file
```
# Compiles the python file and creates an avm in 'path/to/your/file.avm'.
compiler = Compiler.Compile('path/to/your/file.py')
```

2) Compiling a python file to `.avm`
```
# Compiles the python file and returns an avm.
avm = Compiler.Compile_File('path/to/your/file.py')
```

3) Compiling a variable to `.avm`
```
# Compiles a contract stored in memory and returns an avm.
avm = Compiler.Compile_Contract('def Main(operation, args): ...')
```

You can also print out the instr instream:
```
compiler.DumpAsm()
```

#### Testing

You can run the tests using the ```runall.bash``` or ```runall-testing.bash``` files located in ```ontology_test```. You can run the compiler tests using the `compile-avm-test.py` file in the root directory.

## Contributing

Contributors are welcome to the `ontology-python-compiler`. Before beginning, please take a look at our [contributing guidelines](./CONTRIBUTING.md). You can open an issue by [clicking here](https://github.com/ontio/ontology-python-compiler/issues/new).

If you have any issues getting setup, open an issue or reach out in the [Ontology Discord](https://discordapp.com/invite/4TQujHj).

## License

- Open-source [LGPL](LICENSE).
- Main author is [@steven](https://github.com/carltraveler)

## DebugInfo

FuncName:   indicate the opcode blongs to which function. Global#Code is for Code in Global.

Lineno:          indicate the opcode blongs to which line number in source code.

Col :               indicate the opcode blongs to which columns in source code.

offset:            the address of Opcode. from 0 to len of avm.

Opcode:        the Opcode.

JumpTarget:  the target address(offset) of jump instruct.

TargetOff:      the relative offset between target address and current jump instruction.  	 	      

```
FuncName                       Lineno     Col   Offset     OpCode               JumpTarget           TargetOff           
Global#Code                    1          0     0          PUSH2               
Global#Code                    1          0     1          NEWARRAY            
Global#Code                    1          0     2          TOALTSTACK          
Global#Code                    1          14    3          PUSHBYTES5          
Global#Code                    1          0     9          DUPFROMALTSTACK     
Global#Code                    1          0     10         PUSH0               
Global#Code                    1          0     11         PUSH2               
Global#Code                    1          0     12         ROLL                
Global#Code                    1          0     13         SETITEM             
Global#Code                    3          4     14         PUSH2               
Global#Code                    3          0     15         DUPFROMALTSTACK     
Global#Code                    3          0     16         PUSH1               
Global#Code                    3          0     17         PUSH2               
Global#Code                    3          0     18         ROLL                
Global#Code                    3          0     19         SETITEM             
Global#Code                    4          0     20         FROMALTSTACK        
Main                           4          0     21         PUSH3               
Main                           4          0     22         NEWARRAY            
Main                           4          0     23         TOALTSTACK          
Main                           4          0     24         DUPFROMALTSTACK     
Main                           4          0     25         PUSH0               
Main                           4          0     26         PUSH2               
Main                           4          0     27         ROLL                
Main                           4          0     28         SETITEM             
Main                           5          8     29         PUSH0               
Main                           5          4     30         DUPFROMALTSTACK     
Main                           5          4     31         PUSH1               
Main                           5          4     32         PUSH2               
Main                           5          4     33         ROLL                
Main                           5          4     34         SETITEM             
Main                           6          8     35         DUPFROMALTSTACK     
Main                           6          8     36         PUSH0               
Main                           6          8     37         PICKITEM            
Main                           6          8     38         CALL                 49                   11    
```
