# lxml-stubs
[![Testing](https://github.com/abelcheung/lxml-stubs/actions/workflows/python-test.yml/badge.svg?branch=moveon)](https://github.com/abelcheung/lxml-stubs/actions/workflows/python-test.yml/badge.svg?branch=moveon)

This repository contains external type annotations for [lxml](http://lxml.de/) package.
See [PEP 484](https://peps.python.org/pep-0484/) and
[PEP 561](https://peps.python.org/pep-0561/) for more detail.

## Relationship with official lxml-stubs
This fork is an attempt to move forward with faster pace while official
one remains stable. Please contribute to official repository.

## Installation
Since this is not an upstream official release, please head over to
[GitHub release page](https://github.com/abelcheung/lxml-stubs/releases)
and download wheel files (with file extension `.whl`). Wheel files can
be installed with `pip` in similar way to upstream release:

    pip install lxml_stubs-xxxxxxx-py3-none-any.whl

## Special notes
There are two special stub-only classes that do not exist in lxml:

1. `lxml.etree.ParserTarget`
2. `lxml.etree._SmartStr`

They are intended as helpers when writing code, wrapped under
`if TYPE_CHECKING: ...`. Please consult their docstring for detail.
