from xml.sax.handler import ContentHandler

from .etree import LxmlError, _Element, _ElementOrTree, _ElementTree, _ElemFactory

class SaxError(LxmlError): ...

# Most annotation should be done in xml.sax.handler,
# which is unannotated as of writing. Only properties and methods
# not present in superclass are listed here.
# TODO specialize element factory and etree property
class ElementTreeContentHandler(ContentHandler):
    def __init__(self, makeelement: _ElemFactory[_Element] | None = ...) -> None: ...
    @property
    def etree(self) -> _ElementTree: ...

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
