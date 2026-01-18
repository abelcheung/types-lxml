#
# Element factories
#

from typing import (
    Any,
    Literal,
    Protocol,
    TypeVar,
    overload,
    type_check_only,
)
from typing_extensions import disjoint_base

from .._types import (
    _AttrMapping,
    _AttrTuples,
    _AttrVal,
    _NSMapArg,
    _TagName,
)
from ..etree import _Element
from . import _element as _e

_DataElem_T = TypeVar("_DataElem_T", bound=_e.ObjectifiedDataElement)

# Objectified Element factories does extra dict() conversion of
# attrib argument, thus supports tuple form
def Element(
    _tag: _TagName,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: str | None = None,
    **_attributes: _AttrVal,
) -> _e.ObjectifiedElement:
    """Objectify specific version of `lxml.etree` `Element()` factory.

    Requires parser based element class lookup activated in `lxml.etree`!

    Returns
    -------
    ObjectifiedElement
        The generated element.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.Element)
    """

def SubElement(
    _parent: _e.ObjectifiedElement,
    _tag: _TagName,
    /,
    attrib: _AttrMapping | None = None,
    nsmap: _NSMapArg | None = None,
    **_extra: _AttrVal,
) -> _e.ObjectifiedElement: ...

# TODO Current overload situation is unsatisfactory. Will decide
# whether the list should be trimmed or extended in future.
#
# Order matters! float can't be listed before int
#
@overload  # DataElement retains same type if no other hint given
def DataElement(
    _value: _DataElem_T,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: None = None,
    _xsi: None = None,
    **__attr: _AttrVal,
) -> _DataElem_T: ...
@overload  # native type None
def DataElement(
    _value: None,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: None = None,
    _xsi: None = None,
    **__attr: _AttrVal,
) -> _e.NoneElement: ...
@overload  # native type str
def DataElement(
    _value: str,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: None = None,
    _xsi: None = None,
    **__attr: _AttrVal,
) -> _e.StringElement: ...
@overload  # native type bool
def DataElement(  # pyright: ignore[reportOverlappingOverload]
    _value: bool,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: None = None,
    _xsi: None = None,
    **__attr: _AttrVal,
) -> _e.BoolElement: ...
@overload  # native type int
def DataElement(
    _value: int,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: None = None,
    _xsi: None = None,
    **__attr: _AttrVal,
) -> _e.IntElement: ...
@overload  # native type float
def DataElement(
    _value: float,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: None = None,
    _xsi: None = None,
    **__attr: _AttrVal,
) -> _e.FloatElement: ...
@overload  # pytype None
def DataElement(
    _value: object,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: Literal["NoneType", "none"],
    _xsi: str | None = None,
    **__attr: _AttrVal,
) -> _e.NoneElement: ...
@overload  # pytype str
def DataElement(
    _value: object,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: Literal["str"],
    _xsi: str | None = None,
    **__attr: _AttrVal,
) -> _e.StringElement: ...
@overload  # pytype bool
def DataElement(
    _value: object,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: Literal["bool"],
    _xsi: str | None = None,
    **__attr: _AttrVal,
) -> _e.BoolElement: ...
@overload  # pytype int
def DataElement(
    _value: object,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: Literal["int"],
    _xsi: str | None = None,
    **__attr: _AttrVal,
) -> _e.IntElement: ...
@overload  # pytype float
def DataElement(
    _value: object,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: Literal["float"],
    _xsi: str | None = None,
    **__attr: _AttrVal,
) -> _e.FloatElement: ...
@overload  # Generic fallback
def DataElement(
    _value: object,
    /,
    attrib: _AttrMapping | _AttrTuples | None = None,
    nsmap: _NSMapArg | None = None,
    *,
    _pytype: str | None = None,
    _xsi: str | None = None,
    **__attr: _AttrVal,
) -> _e.ObjectifiedElement:
    """Create a new element from a Python value and XML attributes.

    Annotation
    ----------
    Current DataElement stub overloads only represent cases where
    data type is inferred from value or from lxml's own PyType arg.
    If XMLSchema Interface types are involved, the overload list
    becomes very large. The `_xsi` parameter can accept XSI data types
    with the optional `xsd:` namespace prefix.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.DataElement)
    - [XMLSchema Instances data types](https://www.w3.org/TR/2004/REC-xmlschema-2-20041028/datatypes.html)
    - [How lxml determines data type](https://lxml.de/objectify.html#how-data-types-are-matched)
    """

@type_check_only
class _OEMakerCallProtocol(Protocol):
    """Callback Protocol for Objectified ElementMaker

    Annotation
    ----------
    This is the call signature of `lxml.objectify.ElementMaker`
    with `tag` argument removed.
    Thus arguments are effectively the same as, say `E.html()`,
    with all keyword arguments as tag attributes, and positional
    arguments as child element or tag content.
    """
    def __call__(
        self,
        *_children: _Element
        | str
        | bytes
        | bool
        | int
        | float
        | dict[str, Any]
        | _OEMakerCallProtocol
        | None,
        **_attrib: _AttrVal,
    ) -> _e.ObjectifiedElement: ...

@disjoint_base
class ElementMaker:
    """Used for constructing element trees.

    Note that this module has a predefined `ElementMaker` instance called `E`.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.ElementMaker)
    """

    def __init__(
        self,
        *,
        namespace: str | None = None,
        nsmap: _NSMapArg | None = None,
        annotate: bool = True,
        makeelement: type[_e.ObjectifiedElement] | None = None,
    ) -> None: ...
    # Special notes:
    # - Attribute values supplied as children dict will be stringified,
    #   but those as keyword argument _must_ be string itself as they
    #   are not converted
    # - One single child of value 'None' is special, but that doesn't
    #   affect typing
    # - Default children accepts all builtin data types understood
    #   by ObjectifiedElement (bool, float, string etc). In addition,
    #   The PyType registry can register additional support of other
    #   object types. Yet it is decided to not accept anything here,
    #   as even object of wrong type can be used in runtime which
    #   is forcefully stringified into garbage data.
    def __call__(
        self,
        tag: str,  # bytes or namespaced QName object unsupported
        *_children: _Element  # See _OEMakerCallProtocol above
        | str
        | bytes
        | bool
        | int
        | float
        | dict[str, Any]
        | _OEMakerCallProtocol
        | None,
        **_attrib: _AttrVal,
    ) -> _e.ObjectifiedElement: ...
    # __getattr__ here is special. ElementMaker supports using any
    # attribute name as tag, which is sort of like a functools.partial
    # object to ElementMaker.__call__() with tag argument prefilled.
    # So E('html', ...) is equivalent to E.html(...)
    def __getattr__(self, tag: str) -> _OEMakerCallProtocol: ...

E: ElementMaker
