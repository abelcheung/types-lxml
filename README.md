[![PyPI version](https://img.shields.io/pypi/v/types-lxml.svg)](https://pypi.org/project/types-lxml/)
![Supported Python](https://img.shields.io/pypi/pyversions/types-lxml.svg)
![Wheel](https://img.shields.io/pypi/wheel/types-lxml.svg)

This repository contains [external type annotations](https://peps.python.org/pep-0561/) for [`lxml`](http://lxml.de/). It can be used by type-checking tools (currently supporting [`mypy`](https://pypi.org/project/mypy/) and [`pyright`](https://github.com/Microsoft/pyright)) to check code that uses `lxml`, or used within IDEs like [VSCode](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/) to facilitate development.

## Installation

### From PyPI

This is the normal choice for most people:

    pip install -U types-lxml

### From downloaded wheel file

Head over to [release page](../../releases) and get wheel file (with extension `.whl`). Wheel files can be installed in the same way as PyPI package:

    pip install -U types-lxml*.whl

### Bleeding edge from GitHub

    pip install -U git+https://github.com/abelcheung/types-lxml.git

## Special notes
There are two special stub-only classes that do not exist as concrete class in `lxml`:

1. `lxml.etree.ParserTarget`
2. `lxml.etree.SmartStr`

They are intended as helpers when writing code, wrapped under
`if TYPE_CHECKING: ...`. Please consult their docstring in stub files for detail,
or if you are using IDEs, the docstring might have been formatted nicely for reference.

![Stub docstring in PyCharm Documentation Tool](https://user-images.githubusercontent.com/83110/160575574-c20b29d0-ddda-40d4-82e3-724f59663d7e.png)

![Stub docstring in VSCode mouseover tooltip](https://user-images.githubusercontent.com/83110/160575818-168f1a98-074d-46f4-b166-3f18af56232e.png)

## History

Type annotations for `lxml` were initially included in [typeshed](https://www.github.com/python/typeshed), but as it was still incomplete, it was decided to be [ripped out as a separate project](https://github.com/python/typeshed/issues/525).
The code was extracted by Jelle Zijlstra and moved to `lxml-stubs` repository using `git filter-branch`.

`types-lxml` is a fork of `lxml-stubs` that strives for completeness, so that most people would at least find it usable; while the the original `lxml-stubs` aims to be stable.
