import typing as _t
from importlib import import_module
from types import ModuleType
from typing import NamedTuple


class FilePos(NamedTuple):
    file: str
    lineno: int


class VarType(NamedTuple):
    var: str
    type: str


class NameResolver:
    # Covers most types and aliases with bare name
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
    _registry: _t.ClassVar[dict[str, _t.Any]] = {}

    @classmethod
    def find(cls, name: str) -> _t.Any:
        if name not in cls._registry:
            for mod in cls._DEF_MODS.values():
                if hasattr(mod, name):
                    maybe_mod = getattr(mod, name)
                    if not isinstance(maybe_mod, ModuleType):
                        cls._registry[name] = maybe_mod
                        break
            else:
                raise TypeError(f'Cannot resolve "{name}"')
        return cls._registry[name]
