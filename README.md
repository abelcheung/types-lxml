[![PyPI version](https://img.shields.io/pypi/v/types-lxml.svg)](https://pypi.org/project/types-lxml/)
![Supported Python](https://img.shields.io/pypi/pyversions/types-lxml.svg)
![Wheel](https://img.shields.io/pypi/wheel/types-lxml.svg)

This repository contains [external type annotations](https://peps.python.org/pep-0561/) for [`lxml`](http://lxml.de/). It can be used by type-checking tools (currently supporting [`mypy`](https://pypi.org/project/mypy/) and [`pyright`](https://github.com/Microsoft/pyright)) to check code that uses `lxml`, or used within IDEs like [VSCode](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/) to facilitate development.

## Goal ①: Completion

Now the coverage of major `lxml` submodules is complete, thus no more [considered as `partial`](https://peps.python.org/pep-0561/#partial-stub-packages):
  - [x] `lxml.etree`: 100%
    - `etree.Schematron` is obsolete and superseded by `lxml.isoschematron`, so won't implement
  - [x] `lxml.html` proper: 100%
  - [x] `lxml.objectify`: 100%
  - [x] `lxml.builder`: 100%
  - [x] `lxml.cssselect`: 100%
  - [x] `lxml.sax`: 100%

Following list reflects current situation for less used `lxml` / `html` submodules:

  - [ ] `lxml.ElementInclude`
  - [x] `lxml.isoschematron`
  - [ ] `lxml.usedoctest`
  - [x] `lxml.html.builder`
  - [x] `lxml.html.clean`
  - [x] `lxml.html.diff`
  - [ ] `lxml.html.formfill` (may not implement)
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
  - [x] Mypy test suite already vastly expanded
    - But still, only managed to cover about half of the whole package
  - [x] Perform runtime check, and compare against static type checker result
    - This guarantees annotations are indeed valid
    - [x] Proof of concept for incorporating `pyright` result under progress
    - [ ] `mypy` support under consideration later
- [x] Modernize package building infrastructure

## Goal ④: Support for IDEs

Despite having no official PEP, some IDEs support showing docstring from external annotations. This package is try to bring more and more of the original `lxml` class and function docstrings, since the majorify of `lxml` is written in Cython, and IDEs sometimes won't show Cython docstrings during code development. Following screenshots show what would look like, behaving if docstrings are coming from real python code:

![Stub docstring in PyCharm Documentation Tool](https://user-images.githubusercontent.com/83110/160575574-c20b29d0-ddda-40d4-82e3-724f59663d7e.png)

![Stub docstring in VSCode mouseover tooltip](https://user-images.githubusercontent.com/83110/160575818-168f1a98-074d-46f4-b166-3f18af56232e.png)

Besides docstring, current annotations are geared towards convenience for code writers instead of absolute logical 'correctness'. The [deviation of class inheritance](https://github.com/abelcheung/types-lxml/wiki/Element-inheritance-change) for `HtmlComment` and friends is one prominent example.


## Installation

The normal choice for most people is to fetch package from PyPI via `pip`:

    pip install -U types-lxml

There are a few other alternatives though.

### From downloaded wheel file

Head over to [latest release in GitHub](https://github.com/abelcheung/types-lxml/releases/latest) and download wheel file (with extension `.whl`), which can be installed in the same way as PyPI package:

    pip install -U types-lxml*.whl

### Bleeding edge from GitHub

    pip install -U git+https://github.com/abelcheung/types-lxml.git

## Special notes

### Type checker support

Actually, `pyright` is the preferred type checker to use for `lxml` code. `mypy` can be either too restrictive or doesn't support some feature needed by lxml.

Here is one example: normalisation of element attributes.

It is employed by many other projects, so that users can supply common type of value while setting object attributes, and the code internally canonicalise/converts supplied argument to specific type. This is a convenience for library users, so they don't always need to do internal conversion by themselves. Consider the example below:

```python
from typing_extensions import reveal_type
from lxml.etree import fromstring, QName

person = fromstring('<person><height>170</height></person>')
reveal_type(person[0].tag)
person[0].tag = QName('http://ns.prefix', person[0].tag)
```

Lxml supports stringify QNames when setting element tags. Of course, during runtime, everything work as expected:

```pycon
>>> print(e.tostring(person, encoding=str))
<person><ns0:height xmlns:ns0="http://ns.prefix">170</ns0:height></person>
```

`pyright` correctly reports element tag type, and don't complain about assignment:

```
information: Type of "person[0].tag" is "str"
```

But `mypy` barks loudly about the feature:

```
error: Incompatible types in assignment (expression has type "QName", variable has type "str")  [assignment]
```

There are many, many more places in lxml that employs such normalisation.

### ParserTarget
There is now only one stub-only classes that do not exist as concrete class in `lxml` &mdash; `lxml.etree.ParserTarget`. However the support of custom parser target is shelved, so this virtual class is not very relevant for now.

## History

Type annotations for `lxml` were initially included in [typeshed](https://www.github.com/python/typeshed), but as it was still incomplete at that time, the stubs are [ripped out as a separate project](https://github.com/python/typeshed/issues/525). The code was extracted by Jelle Zijlstra and moved to `lxml-stubs` repository using `git filter-branch`.

`types-lxml` is a fork of `lxml-stubs` that strives for the goals described above, so that most people would find it more useful.
