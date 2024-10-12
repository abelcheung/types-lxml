import abc
import ast
import importlib
import pathlib
import re
from typing import Any, ClassVar, ForwardRef, Iterable, NamedTuple

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


class NameCollectorBase(ast.NodeVisitor):
    def __init__(
        self,
        globalns: dict[str, Any],
        localns: dict[str, Any],
    ) -> None:
        super().__init__()
        self._globalns = globalns
        self._localns = localns
        self.modified: bool = False
        self.collected: dict[str, Any] = {
            m: importlib.import_module(m)
            for m in ("builtins", "typing", "typing_extensions")
        }


class TypeCheckerAdapterBase:
    id: ClassVar[str]
    # {('file.py', 10): ('var_name', '_Element'), ...}
    typechecker_result: ClassVar[dict[FilePos, VarType]]
    _type_mesg_re: ClassVar[re.Pattern[str]]

    @classmethod
    @abc.abstractmethod
    def run_typechecker_on(cls, paths: Iterable[pathlib.Path]) -> None: ...
    @classmethod
    @abc.abstractmethod
    def create_collector(
        cls, globalns: dict[str, Any], localns: dict[str, Any]
    ) -> NameCollectorBase: ...
