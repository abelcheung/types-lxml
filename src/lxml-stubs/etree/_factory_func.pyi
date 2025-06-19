from typing import TypeVar, overload

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
from ._parser import CustomTargetParser

_T = TypeVar("_T")

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
def ElementTree(
    element: _ET,
    *,
    file: None = None,
) -> _ElementTree[_ET]:
    """ElementTree wrapper class for Element objects.

    Annotation
    ----------
    This overload is used when creating an ElementTree directly from a root
    Element object. Other arguments are ignored in this case.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ElementTree)
    """

@overload  # from file source, standard parser
def ElementTree(
    element: None = None,
    *,
    file: _FileReadSource,
    parser: _DefEtreeParsers[_ET_co],
) -> _ElementTree[_ET_co]:
    """ElementTree wrapper class for Element objects.

    Annotation
    ----------
    This overload is used when creating an ElementTree from a file source with
    user-supplied standard parser.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ElementTree)
    """

@overload  # from file source, custom target parser
def ElementTree(
    element: None = None,
    *,
    file: _FileReadSource,
    parser: CustomTargetParser[_T],
) -> _T:
    """ElementTree wrapper class for Element objects.

    Annotation
    ----------
    This overload is used when creating an ElementTree from a file source with
    custom target parser. Returns the result dictated by parser target object
    instead of ElementTree.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ElementTree)
    """

@overload  # from file source, no parser supplied
def ElementTree(
    element: None = None,
    *,
    file: _FileReadSource,
    parser: None = None,
) -> _ElementTree:
    """ElementTree wrapper class for Element objects.

    Annotation
    ----------
    This overload is used when creating an ElementTree from a file source
    without a parser supplied. The default parser is used in this case.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ElementTree)
    """
