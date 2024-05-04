from typing import Generic, overload
from xml.sax.handler import ContentHandler

from ._types import _ElementFactory, _ElementOrTree, _ET_co
from .etree import LxmlError, _ElementTree

class SaxError(LxmlError): ...

# xml.sax.handler is annotated in typeshed since Sept 2023.
# For brevity, only properties and methods
# not present in superclass are listed here.
class ElementTreeContentHandler(Generic[_ET_co], ContentHandler):
    @overload
    def __new__(
        cls, makeelement: _ElementFactory[_ET_co]
    ) -> ElementTreeContentHandler[_ET_co]: ...
    @overload
    def __new__(cls, makeelement: None = None) -> ElementTreeContentHandler: ...
    @property
    def etree(self) -> _ElementTree[_ET_co]: ...

class ElementTreeProducer:
    def __init__(
        self,
        element_or_tree: _ElementOrTree,
        content_handler: ContentHandler,
    ) -> None: ...
    def saxify(self) -> None: ...

# = ElementTreeProducer(args).saxify()
def saxify(
    element_or_tree: _ElementOrTree,
    content_handler: ContentHandler,
) -> None: ...
