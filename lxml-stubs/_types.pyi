from _typeshed import _T, SupportsRead, SupportsWrite, _KT_co, _T_co, _VT_co
from os import PathLike
from typing import (
    IO,
    Any,
    Callable,
    Collection,
    Iterable,
    Literal,
    Mapping,
    Protocol,
    TypeVar,
    Union,
)
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

# For tostring() encoding. In theory it should be any encoding name
# except "unicode", but is not representable in current typing system.
# Settle for commonly encodings explicitly checked by lxml.
_KnownEncodings = Literal[
    "ASCII",
    "ascii",
    "UTF-8",
    "utf-8",
    "UTF8",
    "utf8",
    "US-ASCII",
    "us-ascii",
]

# serializer.pxi _findOutputMethod()
_OutputMethodArg = Literal[
    "html",
    "text",
    "xml",
    "HTML",
    "TEXT",
    "XML",
]

# It is unknown if mypy will ever implemenet PEP 696; therefore,
# pyright will enjoy shorthand while mypy doesn't,
# while more specialization of classes are to be implemeneted,
# such as _Attrib -> _Attrib[_Element]
#
# XXX Here is the trick:
# 1. mypy claims it doesn't understand MYPY variable, but actually
#    it does, and skips over to else block
# 2. pyright truly does not understand MYPY variable. Under default
#    behavior, it sort of merges definition of both blocks. With
#    compatible enough definition, it doesn't modify the desired result.
# 3. Replace MYPY with any name, and mypy will break.
#
# While pyright supports defining constants in config, it is not
# reasonable to ask all pyright users to modify their own config.
#
if not MYPY:  # type: ignore
    _ET = TypeVar("_ET", bound=_Element, default=_Element)
    _ET_co = TypeVar("_ET_co", bound=_Element, default=_Element, covariant=True)
else:
    _ET = TypeVar("_ET", bound=_Element)  # pyright: ignore[reportConstantRedefinition]
    _ET_co = TypeVar("_ET_co", bound=_Element, covariant=True)

# Generic element factory function type. Because arguments are
# mostly optional, accurate typing can't be done.
_ElemFactory: TypeAlias = Callable[..., _ET]

# Note that _TagSelector filters element type not by classes,
# but checks for exact element *factory functions* instead;
# that is Element(), Comment(), ProcessingInstruction() and
# Entity(). Python typing system doesn't support such outlandish
# usage. We use a generic callable instead.
_TagSelector: TypeAlias = Union[_TagName, _ElemFactory[_Element]]

_ElementOrTree: TypeAlias = _Element | _ElementTree[_Element]

class SupportsLaxedItems(Protocol[_KT_co, _VT_co]):
    """Relaxed form of SupportsItems

    Original SupportsItems from typeshed returns generic set which
    is compatible with ItemsView. However, _Attrib doesn't conform
    and returns list instead. Gotta find a common ground here.
    """

    def items(self) -> Collection[tuple[_KT_co, _VT_co]]: ...

# Borrow from typeshed xml.sax
class SupportsReadClose(SupportsRead[_T_co], Protocol[_T_co]):
    def close(self) -> None: ...

_FilePath = _AnyStr | PathLike[str] | PathLike[bytes]
# _parseDocument() from parser.pxi
# fmt: off
_FileReadSource = (
    _FilePath
    | IO[str]
    | IO[bytes]
    | SupportsReadClose[str]
    | SupportsReadClose[bytes]
)
# fmt: on
_FileWriteSource = _FilePath | SupportsWrite[bytes]

# Draft PEP 702, add support here since it is pretty unintrusive
# Type checker that doesn't support it would ignore silently
# Following signature borrowed from typing_extensions 4.5
#
def deprecated(
    __msg: str, *, category: type[Warning] | None = ..., stacklevel: int = ...
) -> Callable[[_T], _T]: ...
