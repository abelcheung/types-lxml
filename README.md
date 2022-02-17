# lxml-stubs
[![Build](https://github.com/abelcheung/lxml-stubs/workflows/build.yml/badge.svg?branch=moveon)](https://github.com/abelcheung/lxml-stubs/workflows/build.yml/badge.svg?branch=moveon)
[![Test](https://github.com/abelcheung/lxml-stubs/workflows/test.yml/badge.svg?branch=moveon)](https://github.com/abelcheung/lxml-stubs/workflows/test.yml/badge.svg?branch=moveon)

## About
This repository contains external type annotations (see
[PEP 484](https://www.python.org/dev/peps/pep-0484/)) for the
[lxml](http://lxml.de/) package.


## Installation
To use these stubs with [mypy](https://github.com/python/mypy), you have to
install the `lxml-stubs` package.

    pip install lxml-stubs


## Contributing
Contributions should follow the same style guidelines as
[typeshed](https://github.com/python/typeshed/blob/master/CONTRIBUTING.md).


## History
These type annotations were initially included in
[typeshed](https://www.github.com/python/typeshed), but lxml's annotations
are still incomplete and have therefore been extracted from typeshed to
avoid unintentional false positive results.

The code was extracted by Jelle Zijlstra from the original typeshed codebase
and moved to a separate repository using `git filter-branch`.


## Authors
Numerous people have contributed to the lxml stubs; see the git history for
details.
