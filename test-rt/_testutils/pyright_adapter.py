import ast
import functools
import json
import re
import shutil
import subprocess
import typing as _t
from pathlib import Path
from types import MappingProxyType

from .common import FilePos, NameResolver, VarType

# {('file.py', 10): ('var_name', 'str'), ...}
_pyright_results: dict[FilePos, VarType] = {}
_pyright_re = re.compile('^Type of "(?P<var>.+?)" is "(?P<type>.+?)"$')


@functools.cache
def get_pyright_result(filepath: str | Path):
    if not isinstance(filepath, Path):
        filepath = Path(filepath)
    return MappingProxyType(
        {k: v for k, v in _pyright_results.items() if k.file == filepath.name}
    )


def run_pyright_on(paths: _t.Iterable[Path]) -> None:
    if (pyright_path := shutil.which("pyright")) is None:
        raise FileNotFoundError("Pyright is required to run test suite")
    pyright_cmd = [pyright_path, "--outputjson"]
    pyright_cmd.extend(str(p) for p in paths)
    proc = subprocess.run(pyright_cmd, capture_output=True)
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
        # FIXME Rewrite m['type'] so that names are resolvable
        _pyright_results[pos] = VarType(m["var"], m["type"])


# Pyright inferred type results always contain bare names only without module
class NameCollector(ast.NodeVisitor):
    names: dict[str, _t.Any] = {}

    def __init__(
        self,
        globalns: dict[str, _t.Any],
        localns: _t.Mapping[str, _t.Any],
    ) -> None:
        super().__init__()
        self.globalns = globalns
        self.localns = localns

    def visit_Name(self, node: ast.Name) -> _t.Any:
        name = node.id
        resolver = NameResolver()
        try:
            eval(name, self.globalns, self.localns)
        except NameError:
            self.names[name] = resolver.find(name)
        return self.generic_visit(node)
