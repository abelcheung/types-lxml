from typing import Any, Iterable, Literal, overload
from typing_extensions import TypeGuard

from .._types import (
    _AnyStr,
    _ElementOrTree,
    _ET_co,
    _FileReadSource,
    _KnownEncodings,
    _OutputMethodArg,
    deprecated,
)
from ._element import _Element, _ElementTree
from ._parser import HTMLParser, XMLParser, _DefEtreeParsers

@overload
def HTML(
    text: _AnyStr,
    parser: HTMLParser[_ET_co],
    *,
    base_url: _AnyStr | None = ...,
) -> _ET_co: ...
@overload
def HTML(
    text: _AnyStr,
    parser: None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _Element: ...
@overload
def XML(
    text: _AnyStr,
    parser: XMLParser[_ET_co],
    *,
    base_url: _AnyStr | None = ...,
) -> _ET_co: ...
@overload
def XML(
    text: _AnyStr,
    parser: None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _Element: ...
@overload
def parse(
    source: _FileReadSource,
    parser: _DefEtreeParsers[_ET_co],
    *,
    base_url: _AnyStr | None = ...,
) -> _ElementTree[_ET_co]: ...
@overload
def parse(
    source: _FileReadSource,
    parser: None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _ElementTree[_Element]: ...
@overload
def fromstring(
    text: _AnyStr,
    parser: _DefEtreeParsers[_ET_co],
    *,
    base_url: _AnyStr | None = ...,
) -> _ET_co: ...
@overload
def fromstring(
    text: _AnyStr,
    parser: None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _Element: ...
@overload
def fromstringlist(
    strings: Iterable[_AnyStr],
    parser: _DefEtreeParsers[_ET_co],
) -> _ET_co: ...
@overload
def fromstringlist(
    strings: Iterable[_AnyStr],
    parser: None = ...,
) -> _Element: ...
@overload  # Native str, no XML declaration
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    encoding: type[str] | Literal["unicode"],
    method: _OutputMethodArg = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool | None = ...,
    doctype: str | None = ...,
) -> str: ...
@overload  # byte str, no XML declaration
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    encoding: _KnownEncodings | None = ...,
    method: _OutputMethodArg = ...,
    xml_declaration: bool | None = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool | None = ...,
    doctype: str | None = ...,
) -> bytes: ...

# Under XML Canonicalization (C14N) mode, most arguments are ignored,
# some arguments would even raise exception outright if specified.
@overload  # method="c14n"
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n"],
    exclusive: bool = ...,
    inclusive_ns_prefixes: Iterable[_AnyStr] | None = ...,
    with_comments: bool = ...,
) -> bytes: ...
@overload  # method="c14n2"
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n2"],
    with_comments: bool = ...,
    strip_text: bool = ...,
) -> bytes: ...
@overload  # catch all
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    encoding: str | type[str] = ...,
    method: str = ...,
    xml_declaration: bool | None = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool | None = ...,
    doctype: str | None = ...,
    exclusive: bool = ...,
    with_comments: bool = ...,
    inclusive_ns_prefixes: Any = ...,
) -> _AnyStr: ...
def indent(
    element_or_tree: _ElementOrTree,
    space: str = ...,
    *,
    level: int = ...,
) -> None: ...
@deprecated(
    "For ElementTree 1.3 compat only; result is tostring() output wrapped inside a list"
)
def tostringlist(
    element_or_tree: _ElementOrTree, *args: Any, **__kw: Any
) -> list[str]: ...
@deprecated('Since v3.3.2; use tostring() with encoding="unicode" argument')
def tounicode(
    element_or_tree: _ElementOrTree,
    *,
    method: str,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    doctype: str | None = ...,
) -> None: ...
def iselement(element: object) -> TypeGuard[_Element]: ...

# Debugging only
def dump(
    elem: _Element, *, pretty_print: bool = ..., with_tail: bool = ...
) -> None: ...
