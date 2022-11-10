from typing import Any, Iterator

from ._types import _AnyStr, _NSMapArg, _TagName
from .etree import ElementBase, XMLParser, _ElemFactory

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

def fromstring(
    xml: _AnyStr,
    # only XMLParser or subclasses usable in lxml.objectify
    parser: XMLParser[Any] | None = ...,
    *,
    base_url: _AnyStr | None = ...,
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
