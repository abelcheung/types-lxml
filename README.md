[![PyPI version](https://img.shields.io/pypi/v/types-lxml.svg)](https://pypi.org/project/types-lxml/)
![Supported Python](https://img.shields.io/pypi/pyversions/types-lxml.svg)
![Wheel](https://img.shields.io/pypi/wheel/types-lxml.svg)

This repository contains [external type annotations](https://peps.python.org/pep-0561/) for [`lxml`](http://lxml.de/). It can be used by type-checking tools (currently supporting [`mypy`](https://pypi.org/project/mypy/) and [`pyright`](https://github.com/Microsoft/pyright)) to check code that uses `lxml`, or used within IDEs like [VSCode](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/) to facilitate development.

## Goal ①: Completion

Now the coverage of major `lxml` submodules is almost complete:
  - [x] `lxml.etree`: 100%
    - `etree.Schematron` is obsolete and superseded by `lxml.isoschematron`, so won't implement
  - [x] `lxml.html` proper: 100%
  - [x] `lxml.objectify`: 100%
  - [x] `lxml.builder`: 100%
  - [x] `lxml.cssselect`: 100%
  - [x] `lxml.sax`: 100%

Following list reflects current situation for less used `lxml` / `html` submodules:

  - [ ] `lxml.ElementInclude`
  - [ ] `lxml.isoschematron`
  - [ ] `lxml.usedoctest`
  - [x] `lxml.html.builder`
  - [x] `lxml.html.clean`
  - [ ] `lxml.html.diff`
  - [ ] `lxml.html.formfill`
  - [x] `lxml.html.html5parser`
  - [x] `lxml.html.soupparser`
  - [ ] `lxml.html.usedoctest`

Check out [project page](https://github.com/abelcheung/types-lxml/projects/1) for future plans and progress.

## Goal ②: Support multiple type checkers

Currently the annotations are validated for both `mypy` and `pyright` strict mode.

In the future, there is plan to bring even more type checker support.

## Goal ③: Review and test suite

- [x] All prior `lxml-stubs` contributions are reviewed thoroughly, bringing coherency of annotation across the whole package
- [x] Much more extensive test cases
  - [ ] Mypy test suite only covered about half of the whole package currently
  - [ ] Plan to perform runtime check, and compare against type checker result
- [x] Modernize package building infrastructure

## Installation

### From PyPI

This is the normal choice for most people:

    pip install -U types-lxml

### From downloaded wheel file

Head over to [latest release in GitHub](https://github.com/abelcheung/types-lxml/releases/latest) and download wheel file (with extension `.whl`), which can be installed in the same way as PyPI package:

    pip install -U types-lxml*.whl

### Bleeding edge from GitHub

    pip install -U git+https://github.com/abelcheung/types-lxml.git

## Special notes

### ParserTarget
There is now only one stub-only classes that do not exist as concrete class in
`lxml` &mdash; `lxml.etree.ParserTarget`. However the support of custom parser target is shelved, so this virtual class is not very relevant for now.

### Docstring for stub

Dispite having no official PEP, some IDEs support showing docstring from external annotations. This package is try to bring more and more of the original `lxml` class and function docstrings, since the majorify of `lxml` is written in Cython, and IDEs mostly won't show Cython docstrings during code development. Following screenshots show what would look like, behaving if docstrings are coming from pure python code:

![Stub docstring in PyCharm Documentation Tool](https://user-images.githubusercontent.com/83110/160575574-c20b29d0-ddda-40d4-82e3-724f59663d7e.png)

![Stub docstring in VSCode mouseover tooltip](https://user-images.githubusercontent.com/83110/160575818-168f1a98-074d-46f4-b166-3f18af56232e.png)

## History

Type annotations for `lxml` were initially included in [typeshed](https://www.github.com/python/typeshed), but as it was still incomplete, it was decided to be [ripped out as a separate project](https://github.com/python/typeshed/issues/525).
The code was extracted by Jelle Zijlstra and moved to `lxml-stubs` repository using `git filter-branch`.

`types-lxml` is a fork of `lxml-stubs` that strives for completeness, so that most people would at least find it usable; while the the original `lxml-stubs` aims to be stable.
