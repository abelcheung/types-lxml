from typing import Any, Iterator

from ._types import _AnyStr, _NSMapArg
from .etree import ElementBase, XMLParser, _ElemFactory

class ObjectifiedElement(ElementBase):
    def __iter__(self) -> Iterator[ObjectifiedElement]: ...
    def __reversed__(self) -> Iterator[ObjectifiedElement]: ...
    def __getattr__(self, __k: str) -> ObjectifiedElement: ...

def fromstring(
    xml: _AnyStr,
    # only XMLParser or subclasses usable in lxml.objectify
    parser: XMLParser[Any] | None = ...,
    *,
    base_url: _AnyStr = ...,
) -> ObjectifiedElement: ...

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
