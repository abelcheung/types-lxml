# Security Policy

This project implements an external python type annotation package, which are used by static type checkers and IDEs for providing diagnostics and hints.

Anything publicly distributed, especially installable package on [Python Package Index (PyPI)](https://pypi.org/), are not supposed to be executed in any way. Source distribution contains internal test suite which is only for checking integrity and correctness of this package itself, it is not a serviceable part for external users.

That said, it is hard to be 100% ascertain how static type checkers would behave. While [`pyright`](https://github.com/microsoft/pyright) is written in Typescript and therefore won't be able to execute any Python code, [`mypy`](https://github.com/python/mypy) has some concern that can't be overlooked.

> [!CAUTION]
> `mypy` provides `--install-types` option to install external annotation packages, which can execute arbitrary python code during setup without user consent.

Although `mypy` has decided to not install `types-lxml` package by default, it is impossible to assert on anything happening in future. If suspicion arises which have security implications, please [report to `mypy` repository](https://github.com/python/mypy/issues). This project will _not_ shoulder any responsibility caused by `mypy` misbehavior.
