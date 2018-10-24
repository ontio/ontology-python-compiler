<p align="center">
  <img
    src="https://github.com/ontio/ontology-python-compiler/ontologypic.png"
    width="125px;">
</p>


<h1 align="center">ontology-python-compiler</h1>
<p align="center">
  Python compiler for Ontology
</p>

<ul>
<li>Free software: MIT license</li>




- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Donations](#donations)

## Overview

The `ontology-python-compiler` compiler is a tool for compiling Python files to the `.avm` format for usage to execute contracts on the [Ontology](https://github.com/ontio/ontology/).

The compiler supports a subset of the Python language 


#### What does it currently do

- Compiles a subset of the Python language to the `.avm` format for use in the [Ontology](https://github.com/ontio/ontology)
- Works for Python 3.6+
- supports dictionaries


#### What will it do

- Compile a larger subset of the Python language

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

Compiler.load_and_save('path/to/your/file.py')
```


## License

- Open-source [MIT](LICENSE.md).
- Main author is [@steven](https://github.com/carltraveler)
