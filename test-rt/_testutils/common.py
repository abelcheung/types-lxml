from typing import ForwardRef, NamedTuple

from lxml.etree import LXML_VERSION

is_lxml_4x = LXML_VERSION < (5, 0)


class FilePos(NamedTuple):
    file: str
    lineno: int


class VarType(NamedTuple):
    var: str | None
    type: ForwardRef


class TypeCheckerError(Exception):
    def __init__(self, message: str, filename: str, lineno: int) -> None:
        super().__init__(message)
        self._filename = filename
        self._lineno = lineno

    def __str__(self) -> str:
        return f'"{self._filename}" line {self._lineno}: {self.args[0]}'
