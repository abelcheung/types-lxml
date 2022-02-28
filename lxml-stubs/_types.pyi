from typing import (
    Any,
    Callable,
    Collection,
    Mapping,
    Protocol,
    TypeVar,
)

from .etree import _Element

_KT_co = TypeVar("_KT_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

# ElementTree API is notable of canonicalizing byte / unicode input data.
# This type alias should only be used for input arguments, while one would
# expect plain str in return type for most part of API (except a few places),
# as far as python3 annotation is concerned.
# Not to be confused with typing.AnyStr which is TypeVar.
_AnyStr = str | bytes

_ListAnyStr = list[str] | list[bytes]
_DictAnyStr = dict[str, str] | dict[bytes, bytes]

# See https://github.com/python/typing/pull/273
# Due to Mapping having invariant key types, Mapping[A | B, ...]
# would fail to validate against either Mapping[A, ...] or Mapping[B, ...]
# Try to settle for simpler solution, assuming python3 users would not
# use byte string as namespace prefix.
_NSMapArg = (
    Mapping[None      , _AnyStr] |
    Mapping[str       , _AnyStr] |
    Mapping[str | None, _AnyStr] |
    None
)
_NonDefaultNSMapArg = Mapping[str, _AnyStr] | None

_ExtensionArg = Mapping[
    tuple[_AnyStr | None, _AnyStr],
    Callable[..., Any],  # TODO extension function not investigated yet
]

# XPathObject documented in https://lxml.de/xpathxslt.html#xpath-return-values
# However the type is too versatile to be of any use in further processing,
# so users are encouraged to do type narrowing by themselves.
_XPathObject = Any
# XPath variable supports most of the XPathObject types
# as _input_ argument value, but most users would probably
# only use primivite types for substitution.
_XPathVarArg = (
    bool |
    int |
    float |
    _AnyStr |
    _Element |
    list[_Element]
)

# lxml contains many private classes implementing custom accessors
# and mixins that almost behave like common python types.
# It is better for function arguments to accept protocols instead.

class SupportsLaxedItems(Protocol[_KT_co, _VT_co]):
    """Relaxed form of SupportsItems

    Original SupportsItems from typeshed returns generic set which
    is compatible with ItemsView. However, _Attrib doesn't conform
    and returns list instead. Gotta find a common ground here.
    """

    def items(self) -> Collection[tuple[_KT_co, _VT_co]]: ...
