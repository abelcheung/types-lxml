from typing import Any, Iterator
from typing_extensions import LiteralString

from ._types import SupportsLaxedItems, _AnyStr, _FileReadSource, _NSMapArg, _TagName
from .etree import ElementBase, XMLParser, XMLSchema, _ElementTree, _ElemFactory

# Exported constants
__version__: LiteralString
PYTYPE_ATTRIBUTE: LiteralString

class ObjectifiedElement(ElementBase):
    @property  # type: ignore[misc]
    def text(self) -> str | None: ...  # Readonly, unlike _Element counterpart
    # addattr value *really* accepts anything. Some reasonable, like strings
    # or numbers (or list of them), some not so ok (such as an Element), and
    # some totally insane (such as class object(!), which is converted to __str__)
    def addattr(self, tag: _TagName, value: Any) -> None: ...
    def countchildren(self) -> int: ...
    def descendantpaths(self, prefix: str | list[str] | None = ...) -> list[str]: ...
    def getchildren(self) -> list[ObjectifiedElement]: ...
    def __iter__(self) -> Iterator[ObjectifiedElement]: ...
    def __reversed__(self) -> Iterator[ObjectifiedElement]: ...
    def __getattr__(self, __k: str) -> ObjectifiedElement: ...

class ElementMaker:
    def __init__(
        self,
        *,
        namespace: str | None = ...,
        nsmap: _NSMapArg | None = ...,
        annotate: bool = ...,
        makeelement: _ElemFactory[ObjectifiedElement] | None = ...,
    ) -> None: ...
    def __call__(
        self,
        tag: str,
        *args: Any,
        **kwargs: Any,
    ) -> ObjectifiedElement: ...
    def __getattr__(self, tag: str) -> _ElemFactory[ObjectifiedElement]: ...

E: ElementMaker

def set_default_parser(
    new_parser: XMLParser[ObjectifiedElement] | None = ...,
) -> None: ...
def makeparser(
    *,
    encoding: _AnyStr | None = ...,
    attribute_defaults: bool = ...,
    dtd_validation: bool = ...,
    load_dtd: bool = ...,
    no_network: bool = ...,
    ns_clean: bool = ...,
    recover: bool = ...,
    schema: XMLSchema | None = ...,
    huge_tree: bool = ...,
    remove_blank_text: bool = ...,
    resolve_entities: bool = ...,
    remove_comments: bool = ...,
    remove_pis: bool = ...,
    strip_cdata: bool = ...,
    collect_ids: bool = ...,
    compact: bool = ...,
) -> XMLParser[ObjectifiedElement]: ...

#
# ElementTree functional API for objectify elements
#

def fromstring(
    xml: _AnyStr,
    parser: XMLParser[ObjectifiedElement] | None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> ObjectifiedElement: ...
XML = fromstring
def parse(
    source: _FileReadSource,
    parser: XMLParser[ObjectifiedElement] | None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _ElementTree[ObjectifiedElement]: ...
def Element(
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: str | None = ...,
    **__attr: _AnyStr,
) -> ObjectifiedElement: ...
def SubElement(
    _parent: ObjectifiedElement,
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **__attr: _AnyStr,
) -> ObjectifiedElement: ...
def DataElement(
    _value: Any,  # TODO overload for various data types
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: str | None = ...,
    _xsi: str | None = ...,
    **__attr: _AnyStr,
) -> ObjectifiedElement: ...
