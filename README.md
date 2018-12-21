
<p align="center">
  <img
    src="https://github.com/ontio/ontology-python-compiler/blob/master/ontologypic.png"
    width="125px;">
</p>


<h1 align="center">Neptune</h1>
<p align="center">
  Python compiler for Ontology
</p>



- Free software: LGPL license
  - [Overview](#overview)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)
  - [DebugInfo](#DebugInfo)


## Overview

The `ontology-python-compiler` compiler is a tool for compiling Python files to the `.avm` format for usage in smart contracts on the [Ontology blockchain](https://github.com/ontio/ontology/).

The compiler supports a subset of the Python language.

#### What does it currently do

- Compiles a subset of the Python language to the `.avm` format for use in the [Ontology blockchain](https://github.com/ontio/ontology)
- Works for Python 3.6+

#### What's new compared to neo-boa 

- based abstract syntax tree.
- free line coding.  compare to one line only with one statement restriction.
- global var assigned. any syntax Code can place to global which the "Neptune" support.
- cascade compare. original python sematic 
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
- logic and, or operation. support cascade usage. original python sematic
- if in.
- loop else.
- global var shared between local functions. and if you store a global var. other local function can see the assignment. the sematic is same with original python. now global code only run one time before all function(include Main function).
- support global keyword.

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

