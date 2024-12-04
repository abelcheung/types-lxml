import sys
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    TypeVar,
    final,
    overload,
)

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

from .._types import SupportsLaxItems
from ._classlookup import ElementBase, ElementClassLookup, FallbackElementClassLookup
from ._module_misc import LxmlError

_T = TypeVar("_T")
_P = ParamSpec("_P")
_Public_ET = TypeVar("_Public_ET", bound=type[ElementBase])

class LxmlRegistryError(LxmlError):
    """Base class of lxml registry errors"""

class NamespaceRegistryError(LxmlRegistryError):
    """Error registering a namespace extension"""

#
# Element namespace
#

# Incorporated the generic dict-like _NamespaceRegistry
@final
class _ClassNamespaceRegistry:
    "Dictionary-like registry for namespace implementation classes"
    def __delitem__(self, __key: str | None) -> None: ...
    def __getitem__(self, __key: str | None) -> type[ElementBase]: ...
    def __setitem__(self, __key: str | None, __value: type[ElementBase]) -> None: ...
    def __iter__(self) -> Iterator[str | None]: ...
    def __len__(self) -> int: ...
    def update(
        self,
        class_dict_iterable: SupportsLaxItems[str | None, type[ElementBase]]
        | Iterable[tuple[str | None, type[ElementBase]]],
    ) -> None:
        """Forgivingly update the registry.

        ``class_dict_iterable`` may be a dict or some other iterable
        that yields (name, value) pairs.

        If a value does not match the required type for this registry,
        or if the name starts with '_', it will be silently discarded.
        This allows registrations at the module or class level using
        ``vars()``, ``globals()`` etc.
        """
    def items(self) -> list[tuple[str | None, type[ElementBase]]]: ...
    def iteritems(self) -> Iterator[tuple[str | None, type[ElementBase]]]: ...
    def clear(self) -> None: ...
    @overload  # @ns(None), @ns('tag')
    def __call__(self, _tag: str | None, /) -> Callable[[_Public_ET], _Public_ET]: ...
    @overload  # plain @ns
    def __call__(self, obj: _Public_ET, /) -> _Public_ET: ...

class ElementNamespaceClassLookup(FallbackElementClassLookup):
    """Element class lookup scheme that searches the Element class in the
    Namespace registry

    Example
    -------
    ```python
    lookup = ElementNamespaceClassLookup()
    ns_elements = lookup.get_namespace("http://schema.org/Movie")

    @ns_elements
    class movie(ElementBase):
      "Element implementation for 'movie' tag (using class name) in schema namespace."

    @ns_elements("movie")
    class MovieElement(ElementBase):
      "Element implementation for 'movie' tag (explicit tag name) in schema namespace."
    """

    def __init__(
        self,
        fallback: ElementClassLookup | None = None,
    ) -> None: ...
    def get_namespace(self, ns_uri: str | None) -> _ClassNamespaceRegistry:
        """Retrieve the namespace object associated with the given URI

        Pass None for the empty namespace.
        Creates a new namespace object if it does not yet exist.
        """

#
# Function namespace
#

# Incorporated the generic dict-like _NamespaceRegistry
@final
class _XPathFunctionNamespaceRegistry:
    # At runtime it is possible to unset prefix by setting the
    # value to None, but mypy wants to murder me if getter
    # and setter variable types are different. For everywhere
    # else the death threat is ignored; but here it is possible
    # to just del .prefix as alternative, so we have wiggle
    # room to spare and let mypy has its way.
    prefix: str

    def __delitem__(self, __key: str) -> None: ...
    def __getitem__(self, __key: str) -> Callable[..., Any]: ...
    def __setitem__(self, __key: str, __value: Callable[..., Any]) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def update(
        self,
        class_dict_iterable: SupportsLaxItems[str, Callable[..., Any]]
        | Iterable[tuple[str, Callable[..., Any]]],
    ) -> None:
        """Forgivingly update the registry.

        ``class_dict_iterable`` may be a dict or some other iterable
        that yields (name, value) pairs.

        If a value does not match the required type for this registry,
        or if the name starts with '_', it will be silently discarded.
        This allows registrations at the module or class level using
        ``vars()``, ``globals()`` etc.
        """
    def items(self) -> list[tuple[str, Callable[..., Any]]]: ...
    def iteritems(self) -> Iterator[tuple[str, Callable[..., Any]]]: ...
    def clear(self) -> None: ...
    @overload  # @ns('name')
    def __call__(
        self, _funcname: str, /
    ) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]: ...
    @overload  # plain @ns
    def __call__(self, obj: Callable[_P, _T], /) -> Callable[_P, _T]: ...

def FunctionNamespace(ns_uri: str | None) -> _XPathFunctionNamespaceRegistry:
    """Retrieve the function namespace object associated with the given
    URI

    Creates a new one if it does not yet exist. A function namespace
    can only be used to register extension functions.

    Usage
    -----

    ```python
    >>> ns_functions = FunctionNamespace("http://schema.org/Movie")

    >>> @ns_functions  # uses function name
    ... def add2(x):
    ...     return x + 2

    >>> @ns_functions("add3")  # uses explicit name
    ... def add_three(x):
    ...     return x + 3
    ```
    """
