from typing import Union

from .etree import ElementBase, XMLParser

class ObjectifiedElement(ElementBase):
    pass

def fromstring(
    text: Union[bytes, str],
    parser: XMLParser = ...,
    *,
    base_url: Union[bytes, str] = ...
) -> ObjectifiedElement: ...
