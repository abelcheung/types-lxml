# Resolver documented at https://lxml.de/resolvers.html

import sys
from _typeshed import SupportsRead
from abc import ABCMeta, abstractmethod
from typing import Any, final, type_check_only

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# Keep its usage in Resolver, making sure resolve() method
# always return one of the resolve_*() results.
@type_check_only
class _InputDocument:
    """An internal opaque object used as resolver result"""

# @type_check_only
# class _ResolverContext:
#     """An internal opaque object used in resolve methods"""

class Resolver(metaclass=ABCMeta):
    @abstractmethod
    def resolve(
        self,
        system_url: str | None,
        public_id: str | None,
        context: object,  # _ResolverContext
    ) -> _InputDocument | None: ...
    def resolve_empty(
        self,
        context: object,  # _ResolverContext
    ) -> _InputDocument: ...
    def resolve_string(
        self,
        string: str | bytes,
        context: object,  # _ResolverContext
        *,
        base_url: str | bytes | None = None,
    ) -> _InputDocument: ...
    def resolve_filename(
        self,
        filename: str | bytes,
        context: object,  # _ResolverContext
    ) -> _InputDocument: ...
    def resolve_file(
        self,
        f: SupportsRead[Any],
        context: object,  # _ResolverContext
        *,
        base_url: str | bytes | None = None,
        close: bool = True,
    ) -> _InputDocument: ...

@final
class _ResolverRegistry:
    def add(self, resolver: Resolver) -> None: ...
    def remove(self, resolver: Resolver) -> None: ...
    def copy(self) -> Self: ...
    # resolve() removed. User can't possibly extract or create
    # the context object independently and supply it.
