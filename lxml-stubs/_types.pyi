import sys
from _typeshed import SupportsRead, SupportsWrite, _KT_co, _VT_co
from os import PathLike
from typing import (
    Any,
    Callable,
    Collection,
    Iterable,
    Literal,
    Mapping,
    Protocol,
    TypeVar,
)

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from .etree import QName, _Element, _ElementTree

# Dup but deviate from recent _typeshed
Unused: TypeAlias = Any

# ElementTree API is notable of canonicalizing byte / unicode input data.
# This type alias should only be used for input arguments, while one would
# expect plain str in return type for most part of API (except a few places),
# as far as python3 annotation is concerned.
# Not to be confused with typing.AnyStr which is TypeVar.
_AnyStr: TypeAlias = str | bytes

# String argument also support QName in various places
_TextArg: TypeAlias = str | bytes | QName

# On the other hand, Elementpath API doesn't do str/byte canonicalization,
# only unicode accepted for py3
_ElemPathArg: TypeAlias = str | QName

# Aliases semantically indicating the purpose of text argument
_TagName: TypeAlias = _TextArg
_AttrName: TypeAlias = _TextArg
_AttrVal: TypeAlias = _TextArg

# See https://github.com/python/typing/pull/273
# Due to Mapping having invariant key types, Mapping[A | B, ...]
# would fail to validate against either Mapping[A, ...] or Mapping[B, ...]
# Try to settle for simpler solution, assuming python3 users would not
# use byte string as namespace prefix.
# fmt: off
_NSMapArg = (
    Mapping[None      , _AnyStr] |
    Mapping[str       , _AnyStr] |
    Mapping[str | None, _AnyStr]
)
# fmt: on
_NonDefaultNSMapArg = Mapping[str, _AnyStr]

# https://lxml.de/extensions.html#xpath-extension-functions
# The returned result of extension function itself is not exactly Any,
# but too complex to list.
# And xpath extension func really checks for dict in implementation,
# not just any mapping.
# fmt: off
_XPathExtFuncArg = (
    Iterable[
        SupportsLaxedItems[
            tuple[str | None, str],
            Callable[..., Any],
        ]
    ]
    | dict[tuple[str       , str], Callable[..., Any]]
    | dict[tuple[None      , str], Callable[..., Any]]
    | dict[tuple[str | None, str], Callable[..., Any]]
)
# fmt: on

# XPathObject documented in https://lxml.de/xpathxslt.html#xpath-return-values
# However the type is too versatile to be of any use in further processing,
# so users are encouraged to do type narrowing by themselves.
_XPathObject = Any

# XPath variable supports most of the XPathObject types
# as _input_ argument value, but most users would probably
# only use primivite types for substitution.
# fmt: off
_XPathVarArg = (
    bool
    | int
    | float
    | str
    | bytes
    | _Element
    | list[_Element]
)
# fmt: on

# https://lxml.de/element_classes.html#custom-element-class-lookup
_ElemClsLookupArg = Literal["element", "comment", "PI", "entity"]

# serializer.pxi _findOutputMethod()
_OutputMethodArg = Literal[
    "html",
    "text",
    "xml",
    "HTML",
    "TEXT",
    "XML",
]

# saxparser.pxi _buildParseEventFilter()
_SaxEventNames = Literal[
    "start",
    "end",
    "start-ns",
    "end-ns",
    "comment",
    "pi",
]

_ET = TypeVar("_ET", bound=_Element, default=_Element)
_ET_co = TypeVar("_ET_co", bound=_Element, default=_Element, covariant=True)

# Generic element factory function type. Because arguments are
# mostly optional, accurate typing can't be done.
_ElemFactory: TypeAlias = Callable[..., _ET]

# Note that _TagSelector filters element type not by classes,
# but checks for exact element *factory functions* instead
# (etree.Element() and friends). Python typing system doesn't
# support such outlandish usage. Use a generic callable instead.
_TagSelector: TypeAlias = _TagName | _ElemFactory

_ElementOrTree: TypeAlias = _ET | _ElementTree[_ET]

class SupportsLaxedItems(Protocol[_KT_co, _VT_co]):
    """Relaxed form of SupportsItems

    Original SupportsItems from typeshed returns generic set which
    is compatible with ItemsView. However, _Attrib doesn't conform
    and returns list instead. Gotta find a common ground here.
    """

    def items(self) -> Collection[tuple[_KT_co, _VT_co]]: ...

_FilePath = _AnyStr | PathLike[str] | PathLike[bytes]
# _parseDocument() from parser.pxi
# fmt: off
_FileReadSource = (
    _FilePath
    | SupportsRead[str]
    | SupportsRead[bytes]
)
# fmt: on
_FileWriteSource = _FilePath | SupportsWrite[bytes]
