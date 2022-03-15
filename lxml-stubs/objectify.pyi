from ._types import _AnyStr
from .etree import ElementBase, _Element
from .etree._parser import _DefEtreeParsers

class ObjectifiedElement(ElementBase):
    def __getattr__(self, __k: str) -> ObjectifiedElement: ...

def fromstring(
    text: _AnyStr,
    parser: _DefEtreeParsers[_Element] | None = ...,
    *,
    base_url: _AnyStr = ...
) -> ObjectifiedElement: ...
