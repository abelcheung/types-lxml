from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar

from _typeshed import SupportsRead

from .._types import _AnyStr

# Pyright and pytypes have implemented typing.Self, but not for mypy
Self = TypeVar("Self")

class _InputDocument:
    """An opaque object without any public attributes"""

    ...

class Resolver(metaclass=ABCMeta):
    @abstractmethod
    def resolve(
        self, system_url: str, public_id: str, context: object
    ) -> _InputDocument: ...
    def resolve_empty(self, context: object) -> _InputDocument: ...
    def resolve_string(
        self, string: _AnyStr, context: object, *, base_url: _AnyStr | None = ...
    ) -> _InputDocument: ...
    def resolve_filename(
        self, filename: _AnyStr, context: object
    ) -> _InputDocument: ...
    def resolve_file(
        self,
        f: SupportsRead[Any],
        context: object,
        *,
        base_url: _AnyStr | None,
        close: bool,
    ) -> _InputDocument: ...

class _ResolverRegistry:
    def add(self, resolver: Resolver) -> None: ...
    def remove(self, resolver: Resolver) -> None: ...
    def copy(self: Self) -> Self: ...
    def resolve(
        self, system_url: str, public_id: str, context: object
    ) -> _InputDocument: ...
