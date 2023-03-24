from typing import overload

from .._types import (
    _ET,
    SupportsLaxedItems,
    _AnyStr,
    _ET_co,
    _FileReadSource,
    _NSMapArg,
    _TagName,
)
from ._element import _Comment, _Element, _ElementTree, _Entity, _ProcessingInstruction
from ._parser import _DefEtreeParsers

def Comment(text: _AnyStr | None = ...) -> _Comment: ...
def ProcessingInstruction(
    target: _AnyStr, text: _AnyStr | None = ...
) -> _ProcessingInstruction: ...

PI = ProcessingInstruction

def Entity(name: _AnyStr) -> _Entity: ...
def Element(  # Args identical to _Element.makeelement
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **_extra: _AnyStr,
) -> _Element: ...
def SubElement(
    _parent: _ET,
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **_extra: _AnyStr,
) -> _ET: ...
@overload  # from element, parser ignored
def ElementTree(element: _ET) -> _ElementTree[_ET]: ...
@overload  # from file source, custom parser
def ElementTree(
    element: None = ...,
    *,
    file: _FileReadSource,
    parser: _DefEtreeParsers[_ET_co],
) -> _ElementTree[_ET_co]: ...
@overload  # from file source, default parser
def ElementTree(
    element: None = ...,
    *,
    file: _FileReadSource,
    parser: None = ...,
) -> _ElementTree[_Element]: ...
