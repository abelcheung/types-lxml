[![Testing](https://github.com/abelcheung/types-lxml/actions/workflows/test.yml/badge.svg)](https://github.com/abelcheung/types-lxml/actions/workflows/test.yml/badge.svg)

This repository contains [external type annotations](https://peps.python.org/pep-0561/) for [`lxml`](http://lxml.de/). It can be used by type-checking tools (currently supporting [`mypy`](https://pypi.org/project/mypy/) and [`pyright`](https://github.com/Microsoft/pyright)) to check code that uses `lxml`, or used within IDEs like [VSCode](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/) to facilitate development.

## Installation

(To be written)

## Special notes
There are two special stub-only classes that do not exist as concrete class in `lxml`:

1. `lxml.etree.ParserTarget`
2. `lxml.etree._SmartStr`

They are intended as helpers when writing code, wrapped under
`if TYPE_CHECKING: ...`. Please consult their docstring in stub files for detail.

## History

Type annotations for `lxml` were initially included in [typeshed](https://www.github.com/python/typeshed), but as it was still incomplete, it was decided to be [ripped out as a separate project](https://github.com/python/typeshed/issues/525).
The code was extracted by Jelle Zijlstra and moved to `lxml-stubs` repository using `git filter-branch`.

`types-lxml` is a fork of `lxml-stubs` that strives for completeness, so that most people would at least find it usable; while the the original `lxml-stubs` aims to be stable.
