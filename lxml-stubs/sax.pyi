from typing import Generic, TypeVar, overload
from xml.sax.handler import ContentHandler

from .etree import LxmlError, _Element, _ElementOrAnyTree, _ElementTree, _ElemFactory
from .html import HtmlElement

_ETree_T = TypeVar("_ETree_T", _Element, HtmlElement)

class SaxError(LxmlError): ...

# Most annotation should be done in xml.sax.handler,
# which is unannotated as of writing. Only properties and methods
# not present in superclass are listed here.
class ElementTreeContentHandler(Generic[_ETree_T], ContentHandler):
    @overload
    def __new__(
        cls, makeelement: _ElemFactory[_ETree_T]
    ) -> ElementTreeContentHandler[_ETree_T]: ...
    @overload
    def __new__(
        cls, makeelement: None = ...
    ) -> ElementTreeContentHandler[_Element]: ...
    @property
    def etree(self) -> _ElementTree[_ETree_T]: ...

class ElementTreeProducer:
    def __init__(
        self,
        element_or_tree: _ElementOrAnyTree,
        content_handler: ContentHandler,
    ) -> None: ...
    def saxify(self) -> None: ...

# = ElementTreeProducer(args).saxify()
def saxify(
    element_or_tree: _ElementOrAnyTree,
    content_handler: ContentHandler,
) -> None: ...
