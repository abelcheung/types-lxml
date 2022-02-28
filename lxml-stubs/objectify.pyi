from ._types import _AnyStr
from .etree import ElementBase, XMLParser

class ObjectifiedElement(ElementBase):
    pass

def fromstring(
    text: _AnyStr,
    parser: XMLParser = ...,
    *,
    base_url: _AnyStr = ...
) -> ObjectifiedElement: ...
