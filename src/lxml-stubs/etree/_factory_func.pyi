from typing import overload

from .._types import (
    _ET,
    _AttrMapping,
    _AttrVal,
    _DefEtreeParsers,
    _ElementFactory,
    _ET_co,
    _FileReadSource,
    _NSMapArg,
    _TagName,
    _TextArg,
)
from ..html import HtmlElement
from ..objectify import ObjectifiedElement, StringElement
from ._element import _Comment, _ElementTree, _Entity, _ProcessingInstruction

def Comment(text: _TextArg | None = None) -> _Comment: ...
def ProcessingInstruction(
    target: _TextArg, text: _TextArg | None = None
) -> _ProcessingInstruction: ...

PI = ProcessingInstruction

def Entity(name: _TextArg) -> _Entity: ...

Element: _ElementFactory

# SubElement is a bit more complex than expected, as it
# handles other kinds of element, like HtmlElement
# and ObjectifiedElement.
#
# - If parent is HtmlElement, generated subelement is
# HtmlElement or its relatives, depending on the tag name
# used. For example, with "label" as tag, it generates
# a LabelElement.
#
# - For ObjectifiedElement, subelements generated this way
# are always of type StringElement. Once the object is
# constructed, the object type won't change, even when
# type annotation attribute is modified.
# OE users need to use E-factory for more flexibility.
@overload
def SubElement(  # type: ignore[overload-overlap]
    _parent: ObjectifiedElement,
    _tag: _TagName,
    /,
    attrib: _AttrMapping | None = None,
    nsmap: _NSMapArg | None = None,
    **_extra: _AttrVal,
) -> StringElement: ...
@overload
def SubElement(
    _parent: HtmlElement,
    _tag: _TagName,
    /,
    attrib: _AttrMapping | None = None,
    nsmap: _NSMapArg | None = None,
    **_extra: _AttrVal,
) -> HtmlElement: ...
@overload
def SubElement(
    _parent: _ET,
    _tag: _TagName,
    /,
    attrib: _AttrMapping | None = None,
    nsmap: _NSMapArg | None = None,
    **_extra: _AttrVal,
) -> _ET: ...
@overload  # from element, parser ignored
def ElementTree(element: _ET) -> _ElementTree[_ET]: ...
@overload  # from file source, custom parser
def ElementTree(
    element: None = None,
    *,
    file: _FileReadSource,
    parser: _DefEtreeParsers[_ET_co],
) -> _ElementTree[_ET_co]: ...
@overload  # from file source, default parser
def ElementTree(
    element: None = None,
    *,
    file: _FileReadSource,
    parser: None = None,
) -> _ElementTree: ...
