
<p align="center">
  <img
    src="https://github.com/ontio/ontology-python-compiler/blob/master/ontologypic.png"
    width="125px;">
</p>


<h1 align="center">ontology-python-compiler</h1>
<p align="center">
  Python compiler for Ontology
</p>


- Free software: LGPL license
  - [Overview](#overview)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)
  - [DEBUGINFO](#DEBUGINFO)


## Overview

The `ontology-python-compiler` compiler is a tool for compiling Python files to the `.avm` format for usage in smart contracts on the [Ontology blockchain](https://github.com/ontio/ontology/).

The compiler supports a subset of the Python language.

#### What does it currently do

- Compiles a subset of the Python language to the `.avm` format for use in the [Ontology blockchain](https://github.com/ontio/ontology)
- Works for Python 3.6+

#### What's new compared to neo-boa 

- based abstract syntax tree.
- free line coding.  compare to one line only with one statement restriction.
- global var assigned.
- cascade compare.
- cascade assignment.
- if expr.
- map in map.
- free string slice.
- list comprehension.
- dict comprehension.
- conditional operation.
- assert support.
- more syntax check. 
- add lib api to support list remove. element in. more api please check [libont.py](https://github.com/ontio/ontology-python-compiler/blob/master/ontology/libont.py)
- more accuracy debug message dump.
- for, while break or continue.
- logic and, or operation return true or false. support cascade usage

#### What will it do

- Compile a larger subset of the Python language.
- more syntax checks.
- optimize instr stream.

#### Get Help or give help

- Pull requests welcome. New features, writing tests and documentation are all needed.

## Installation

Installation requires a Python 3.6 or later environment.

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

The compiler may be used like in the following example:

```
from ontology.compiler import Compiler

# Compiles the python file and creates an avm in 'path/to/your/file.avm'.
compiler = Compiler.Compile('path/to/your/file.py')

# dump the instr instream.
compiler.DumpAsm()
```

## License

- Open-source [LGPL](LICENSE).
- Main author is [@steven](https://github.com/carltraveler)



## DEBUGINFO

FuncName:   indicate the opcode blongs to which function.

Lineno:          indicate the opcode blongs to which line number in source code.

Col :               indicate the opcode blongs to which columns in source code.

offset:            the address of Opcode. from 0 to len of avm.

Opcode:        the Opcode.

JumpTarget:  the target address(offset) of jump instruct.

TargetOff:      the relative offset between target address and current jump instruction.  	 	      

```
st line of SmartContract
FuncName                       Lineno     Col   Offset     OpCode               JumpTarget           TargetOff           
Main                           1          0     0          PUSH2               
Main                           1          0     1          NEWARRAY            
Main                           1          0     2          TOALTSTACK          
Main                           2          8     3          PUSH10              
Main                           2          4     4          DUPFROMALTSTACK     
Main                           2          4     5          PUSH0               
Main                           2          4     6          PUSH2               
Main                           2          4     7          ROLL                
Main                           2          4     8          SETITEM             
Main                           3          16    9          DUPFROMALTSTACK     
Main                           3          16    10         PUSH0               
Main                           3          16    11         PICKITEM            
Main                           3          11    12         CALL                 18                   6                   
Main                           3          4     15         FROMALTSTACK        
Main                           3          4     16         DROP                
Main                           3          4     17         RET                 
test                           5          0     18         PUSH2               
test                           5          0     19         NEWARRAY            
test                           5          0     20         TOALTSTACK          
test                           5          9     21         DUPFROMALTSTACK     
test                           5          9     22         PUSH0               
test                           5          9     23         PUSH2               
test                           5          9     24         ROLL                
test                           5          9     25         SETITEM             
test                           6          11    26         DUPFROMALTSTACK     
test                           6          11    27         PUSH0               
test                           6          11    28         PICKITEM            
test                           6          4     29         FROMALTSTACK        
test                           6          4     30         DROP                
test                           6          4     31         RET      
```

