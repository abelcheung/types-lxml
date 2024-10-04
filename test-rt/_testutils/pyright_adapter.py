import ast
import functools
import json
import re
import shutil
import subprocess
import typing as _t
from importlib import import_module
from pathlib import Path
from types import MappingProxyType, ModuleType

from .common import FilePos, VarType

# {('file.py', 10): ('var_name', 'str'), ...}
_results: dict[FilePos, VarType] = {}
_pyright_re = re.compile('^Type of "(?P<var>.+?)" is "(?P<type>.+?)"$')


@functools.cache
def get_result(filepath: str | Path) -> MappingProxyType[FilePos, VarType]:
    if not isinstance(filepath, Path):
        filepath = Path(filepath)
    return MappingProxyType(
        {k: v for k, v in _results.items() if k.file == filepath.name}
    )


def run_typechecker_on(paths: _t.Iterable[Path]) -> None:
    if (prog_path := shutil.which("pyright")) is None:
        raise FileNotFoundError("Pyright is required to run test suite")
    cmd = [prog_path, "--outputjson"]
    cmd.extend(str(p) for p in paths)
    proc = subprocess.run(cmd, capture_output=True)
    report = json.loads(proc.stdout)

    for diag in report["generalDiagnostics"]:
        if diag["severity"] != "information":
            continue
        # Pyright report lineno is 0-based
        # OTOH python frame lineno is 1-based
        lineno = diag["range"]["start"]["line"] + 1
        filename = Path(diag["file"]).name
        if (m := _pyright_re.match(diag["message"])) is None:
            continue
        pos = FilePos(filename, lineno)
        _results[pos] = VarType(m["var"], _t.ForwardRef(m["type"]))


class _BasicResolver:
    _DEF_MODS = {
        m: import_module(m)
        for m in (
            "re",
            "collections",
            "collections.abc",
            "types",
            "typing",
            "typing_extensions",
        )
    }

    @classmethod
    @functools.cache
    def find(cls, name: str) -> _t.Any:
        for mod in cls._DEF_MODS.values():
            if not hasattr(mod, name):
                continue
            member = getattr(mod, name)
            if not isinstance(member, ModuleType):
                return member
        else:
            raise TypeError(f'Cannot resolve "{name}"')

_basic_resolver = _BasicResolver()


class NameCollector(ast.NodeVisitor):
    collected: dict[str, _t.Any] = {}

    def __init__(
        self,
        globalns: dict[str, _t.Any],
        localns: _t.Mapping[str, _t.Any],
    ) -> None:
        super().__init__()
        self.globalns = globalns
        self.localns = localns

    # Pyright inferred type results always contain bare names only,
    # so don't need to bother with visit_Attribute()
    def visit_Name(self, node: ast.Name) -> _t.Any:
        name = node.id
        try:
            eval(name, self.globalns, self.localns)
        except NameError:
            self.collected[name] = _basic_resolver.find(name)
        return self.generic_visit(node)
