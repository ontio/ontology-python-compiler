<p align="center">
  <img
    src="https://github.com/ontio/ontology-python-compiler/blob/master/ontologypic.png"
    width="125px;">
</p>


<h1 align="center">ontology-python-compiler</h1>
<p align="center">
  Python compiler for Ontology
</p>

<ul>
<li>Free software: GPL license</li>




- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview

The `ontology-python-compiler` compiler is a tool for compiling Python files to the `.avm` format for usage to execute contracts on the [Ontology](https://github.com/ontio/ontology/).

The compiler supports a subset of the Python language 


#### What does it currently do

- Compiles a subset of the Python language to the `.avm` format for use in the [Ontology](https://github.com/ontio/ontology)
- Works for Python 3.6+

#### What new compare to the old compiler neo-boa 

- based abstract syntax tree.
- free line coding.  compare to one line only with one statement restriction.
- global var assigned.
- cascade compare.
- cascade assignment
- map in map.
- free string slice.
- list comprehension.
- dict comprehension.
- conditional operation.
- assert support.
- more syntax check. 
- add lib api to support list remove. element in.
- more accuracy debug message dump.
- for, while break or continue.

#### What will it do

- Compile a larger subset of the Python language.
- more syntax check.
- optimize instr stream.

#### Get Help or give help

- Pull requests welcome. New features, writing tests and documentation are all needed.


## Installation

Installation requires a Python 3.6 or later environment.

#### Manual

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

# compiler your code. save in 'path/to/your/file.avm'.
compiler = Compiler.Compile('path/to/your/file.py')

# dump the instr instream.
compiler.DumpAsm()
```


## License

- Open-source [GPL](LICENSE.md).
- Main author is [@steven](https://github.com/carltraveler)
