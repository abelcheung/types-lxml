import ast
import importlib
import json
import pathlib
import re
import typing as _t

import mypy.api

from .common import (
    FilePos,
    NameCollectorBase,
    TypeCheckerAdapterBase,
    TypeCheckerError,
    VarType,
)


# There are "column", "hint" and "code" fields for error
# messages, but not in reveal_type() output
class _MypyDiagObj(_t.TypedDict):
    file: str
    line: int
    severity: _t.Literal["note", "warning", "error"]
    message: str


class _NameCollector(NameCollectorBase, ast.NodeTransformer):
    def visit_Attribute(self, node: ast.Attribute) -> ast.expr:
        prefix = ast.unparse(node.value)
        name = node.attr

        setattr(node.value, "is_parent", True)
        if not hasattr(node, "is_parent"):  # Outmost attribute node
            try:
                _ = importlib.import_module(prefix)
            except ModuleNotFoundError:
                # Mypy resolve names according to external stub if
                # available. For example, _ElementTree is determined
                # as lxml.etree._element._ElementTree, which doesn't
                # exist in runtime. Try to resolve bare names
                # instead, which rely on runtime tests importing
                # them properly before resolving.
                try:
                    eval(name, self._globalns, self._localns | self.collected)
                except NameError as e:
                    raise NameError(f'Cannot resolve "{prefix}" or "{name}"') from e
                else:
                    self.modified = True
                    return ast.Name(id=name, ctx=node.ctx)

        _ = self.generic_visit(node)
        fullname = ast.unparse(node)
        self.collected[fullname] = getattr(self.collected[prefix], name)
        return node

    # Mypy usually dumps full inferred type with module name,
    # but with a few exceptions (like tuple, Union).
    # visit_Attribute can ultimately recurse into visit_Name
    # as well
    def visit_Name(self, node: ast.Name) -> ast.expr:
        name = node.id
        try:
            eval(name, self._globalns, self._localns | self.collected)
        except NameError:
            pass
        else:
            return node

        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            pass
        else:
            self.collected[name] = mod
            return node

        if hasattr(self.collected["typing"], name):
            self.collected[name] = getattr(self.collected["typing"], name)
            return node

        raise NameError(f'Cannot resolve "{name}"')


class _TypeCheckerAdapter(TypeCheckerAdapterBase):
    id = "mypy"
    typechecker_result = {}
    _type_mesg_re = re.compile(r'^Revealed type is "(?P<type>.+?)"$')

    @classmethod
    def run_typechecker_on(cls, paths: _t.Iterable[pathlib.Path]) -> None:
        mypy_args = [
            "--output=json",
            "--config-file=rttest-mypy.ini",
        ]
        mypy_args.extend(str(p) for p in paths)
        # Note that mypy UNCONDITIONALLY exits with error when
        # output format is json, there is no point checking
        # exit code for problems
        stdout, _, _ = mypy.api.run(mypy_args)

        # So-called mypy json output is merely a line-by-line
        # transformation of plain text output into json object
        for line in stdout.splitlines():
            if not line.startswith("{"):
                continue
            # If it fails parsing data, json must be containing
            # multiline error hint, just let it KABOOM
            diag: _MypyDiagObj = json.loads(line)
            pos = FilePos(diag["file"], diag["line"])
            if diag["severity"] != "note":
                raise TypeCheckerError(
                    "Mypy {}: {}".format(diag["severity"], diag["message"]),
                    diag["file"],
                    diag["line"],
                )
            if (m := cls._type_mesg_re.match(diag["message"])) is None:
                continue
            # Mypy can insert extra character into expression so that it
            # becomes invalid and unparseable. 0.9x days there
            # was '*', and now '?' (and '=' for typeddict too).
            # Try stripping those character and pray we get something
            # usable for evaluation
            expression = m["type"].translate({ord(c): None for c in "*?="})
            # Unlike pyright, mypy output doesn't contain variable name
            cls.typechecker_result[pos] = VarType(None, _t.ForwardRef(expression))

    @classmethod
    def create_collector(
        cls, globalns: dict[str, _t.Any], localns: dict[str, _t.Any]
    ) -> _NameCollector:
        return _NameCollector(globalns, localns)


adapter = _TypeCheckerAdapter()
