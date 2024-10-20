import abc
import ast
import importlib
import pathlib
import re
from typing import Any, ClassVar, ForwardRef, Iterable, NamedTuple, cast

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


class FuncSignatureError(Exception):
    def __init__(self, message: str, funcname: str) -> None:
        super().__init__(message)
        self._func = funcname

    def __str__(self) -> str:
        return "{}(): {}".format(self._func, self.args[0])


class NameCollectorBase(ast.NodeTransformer):
    def __init__(
        self,
        globalns: dict[str, Any],
        localns: dict[str, Any],
    ) -> None:
        super().__init__()
        self._globalns = globalns
        self._localns = localns
        self.modified: bool = False
        # typing_extensions guaranteed to be present,
        # as a dependency of typeguard
        self.collected: dict[str, Any] = {
            m: importlib.import_module(m)
            for m in ("builtins", "typing", "typing_extensions")
        }

    def visit_Subscript(self, node: ast.Subscript) -> ast.expr:
        node.value = cast("ast.expr", self.visit(node.value))
        node.slice = cast("ast.expr", self.visit(node.slice))

        # When type reference is a stub-only specialized class
        # which don't have runtime support (lxml classes have
        # no __class_getitem__), concede by verifying
        # unsubscripted type.
        try:
            eval(ast.unparse(node), self._globalns, self._localns | self.collected)
        except TypeError as e:
            if "is not subscriptable" not in e.args[0]:
                raise
            # TODO Insert node.value dependent hook for extra
            # varification of subscript type
            self.modified = True
            return node.value
        else:
            return node


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
