from __future__ import annotations

from _typeshed import SupportsRead, SupportsWrite
from os import PathLike
from typing import (
    Any,
    Callable,
    Collection,
    Generic,
    Iterable,
    Literal,
    Mapping,
    Protocol,
    TypeVar,
)

from .etree import HTMLParser, QName, XMLParser, _Element, _ElementTree

_KT_co = TypeVar("_KT_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

# Dup but deviate from recent _typeshed
Unused = Any

# ElementTree API is notable of canonicalizing byte / unicode input data.
# This type alias should only be used for input arguments, while one would
# expect plain str in return type for most part of API (except a few places),
# as far as python3 annotation is concerned.
# _AnyStr should not to be confused with typing.AnyStr which is TypeVar.
# TODO slowly migrating to _TextArg
_AnyStr = str | bytes
_TextArg = str | bytes | bytearray
"""Generic text arguments or properties supported
throughout lxml API."""

# String argument also support QName in various places;
# also include aliases semantically indicating the purpose
# of text argument
_TagName = _TextArg | QName
_AttrName = _TextArg | QName
_AttrVal = _TextArg | QName  # TODO Consider dropping QName
_AttrNameKey = str | bytes | QName
"""Equivalent to _AttrName or _TagName, but for use in
mapping keys where unhashable type is not allowed."""

# On the other hand, Elementpath API doesn't do str/byte canonicalization,
# only unicode accepted for py3
_ElemPathArg = str | QName

_AttrMapping = SupportsLaxItems[_AttrNameKey, _AttrVal]  # noqa: F821
"""Attribute dict-like mapping

Used in attrib argument of various factories and methods.
Bytearray not supported as key (not hashable).

Internal stuff
--------------
Anything that delves into `_initNodeAttributes()`
(in `apihelper.pxi`) should be able to use it.
Need to make sure `_Attrib` and `dict` are supported in
places wherever this alias is used.
"""

_AttrTuples = Iterable[tuple[_AttrNameKey, _AttrVal]]
"""Tuple form of attribute key/value pairs

Used in attrib argument where tuple form is accepted,
in place of or in addition to `_AttrMapping`.
"""

# Due to Mapping having invariant key types, Mapping[A | B, ...]
# would fail to validate against either Mapping[A, ...] or Mapping[B, ...]
# Try to settle for simpler solution, assuming python3 users would not
# use byte string as namespace prefix.
_NSMapArg = (
    Mapping[      None, _AnyStr] |
    Mapping[str       , _AnyStr] |
    Mapping[str | None, _AnyStr]
)  # fmt: skip
_NonDefaultNSMapArg = Mapping[str, _AnyStr]

# Namespace mapping type specifically for Elementpath methods
#
# Elementpath methods do not sanitize nsmap at all.
# It is possible to use invalid nsmap like {"foo": 0}
# and find*() method family happily accept it, just that
# they would silently fail to output any element afterwards.
# Bytes and strs are treated as different NS entries.
# In order to be useful, dict val must be str.
_StrictNSMap = (
    Mapping[      None, str] |
    Mapping[str       , str] |
    Mapping[str | None, str]
)  # fmt: skip

# Some namespace map arguments also accept tuple form
# like what dict() does
_NSTuples = Iterable[tuple[_AnyStr | None, _AnyStr]]

# https://lxml.de/extensions.html#xpath-extension-functions
# The returned result of extension function itself is not exactly Any,
# but too complex to list.
# And xpath extension func really checks for dict in implementation,
# not just any mapping.
_XPathExtFuncArg = (
    Iterable[
        SupportsLaxItems[
            tuple[str | None, str],
            Callable[..., Any],
        ]
    ]
    | dict[tuple[str       , str], Callable[..., Any]]
    | dict[tuple[      None, str], Callable[..., Any]]
    | dict[tuple[str | None, str], Callable[..., Any]]
)  # fmt: skip

# XPathObject documented in https://lxml.de/xpathxslt.html#xpath-return-values
# However the type is too versatile to be of any use in further processing,
# so users are encouraged to do type narrowing by themselves.
_XPathObject = Any

# XPath variable supports most of the XPathObject types
# as _input_ argument value, but most users would probably
# only use primitive types for substitution.
_XPathVarArg = (
    bool
    | int
    | float
    | str
    | bytes
    | _Element
    | list[_Element]
)  # fmt: skip

# https://lxml.de/element_classes.html#custom-element-class-lookup
_ElemClsLookupArg = Literal["element", "comment", "PI", "entity"]

# serializer.pxi _findOutputMethod()
_OutputMethodArg = Literal[
    "html",
    "text",
    "xml",
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

class _ElementFactory(Protocol, Generic[_ET_co]):
    """Element factory protocol

    This is callback protocol for `makeelement()` method of
    various element objects, with following signature (which
    is identical to `etree.Element()` factory):

    ```python
    (_tag, attrib=..., nsmap=..., **_extra)
    ```

    The mapping in `attrib` argument and all `_extra` keyword
    arguments would be merged together, with `_extra` taking
    precedence over `attrib`.
    """

    def __call__(
        self,
        _tag: _TagName,
        /,
        attrib: _AttrMapping | None = None,
        nsmap: _NSMapArg | None = None,
        **_extra: _AttrVal,
    ) -> _ET_co: ...

# HACK _TagSelector filters element type not by classes,
# but checks for exact element *factory functions* instead
# (etree.Element() and friends). Python typing system doesn't
# support such outlandish usage. Use a generic callable instead.
_TagSelector = _TagName | Callable[..., _Element]

_ElementOrTree = _ET | _ElementTree[_ET]

# The basic parsers bundled in lxml.etree
_DefEtreeParsers = XMLParser[_ET_co] | HTMLParser[_ET_co]

class SupportsLaxItems(Protocol[_KT_co, _VT_co]):
    """Relaxed form of SupportsItems

    Original `SupportsItems` from typeshed returns
    generic set which is compatible with `ItemsView`.
    However, `_Attrib.items()` returns `list` instead.
    Here we find a common ground that satisfies both
    and avoid the mapping invariance culprit.
    """

    def items(self) -> Collection[tuple[_KT_co, _VT_co]]: ...

_FilePath = _AnyStr | PathLike[str] | PathLike[bytes]
# _parseDocument() from parser.pxi
_FileReadSource = (
    _FilePath
    | SupportsRead[str]
    | SupportsRead[bytes]
)  # fmt: skip
_FileWriteSource = _FilePath | SupportsWrite[bytes]
