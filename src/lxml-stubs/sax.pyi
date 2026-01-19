"""SAX-related utilities for `lxml`.

This module provides SAX integration helpers such as a content handler
that builds an `ElementTree` as well as utilities to produce SAX events
from an existing tree.

See Also
--------
- [API Documentation](https://lxml.de/apidoc/lxml.sax.html)
"""

from typing import Generic, overload
from typing_extensions import disjoint_base
from xml.sax.handler import ContentHandler

from ._types import _ET, SupportsLaxItems, Unused, _ElementOrTree
from .etree import LxmlError, _ElementTree, _ProcessingInstruction

class SaxError(LxmlError):
    """Base exception for SAX-related errors.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.sax.html#lxml.sax.SaxError)
    """

# xml.sax.handler is annotated in typeshed since Sept 2023.
class ElementTreeContentHandler(Generic[_ET], ContentHandler):
    """A SAX `ContentHandler` that builds an `ElementTree`.

    Instances of this handler receive SAX events and construct an
    `ElementTree` root element. It is useful when parsing SAX streams
    into `lxml` element trees.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.sax.html#lxml.sax.ElementTreeContentHandler)
    """

    _root: _ET | None
    _root_siblings: list[_ProcessingInstruction]
    _element_stack: list[_ET]
    _default_ns: str | None
    _ns_mapping: dict[str | None, list[str | None]]
    _new_mappings: dict[str | None, str]
    # Not adding _get_etree(), already available as public property
    @overload
    def __new__(cls, makeelement: type[_ET]) -> ElementTreeContentHandler[_ET]: ...
    @overload
    def __new__(cls, makeelement: None = None) -> ElementTreeContentHandler[_ET]: ...
    @property
    def etree(self) -> _ElementTree[_ET]: ...

    # Incompatible method overrides; some args are similar
    # but use other structures or names
    # pyrefly: ignore[bad-param-name-override]
    def startElementNS(  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]  # ty: ignore[invalid-method-override]
        self,
        ns_name: tuple[str, str],
        qname: Unused,
        attributes: SupportsLaxItems[tuple[str | None, str], str] | None = None,
    ) -> None: ...
    # pyrefly: ignore[bad-param-name-override]
    def endElementNS(  # pyright: ignore[reportIncompatibleMethodOverride]  # ty: ignore[invalid-method-override]
        self,
        ns_name: tuple[str | None, str],
        qname: Unused,
    ) -> None: ...
    # pyrefly: ignore[bad-param-name-override]
    def characters(  # pyright: ignore[reportIncompatibleMethodOverride]  # ty: ignore[invalid-method-override]
        self,
        data: str,
    ) -> None: ...
    # pyrefly: ignore[bad-param-name-override]
    def startElement(  # pyright: ignore[reportIncompatibleMethodOverride]  # ty: ignore[invalid-method-override]
        self,
        name: str,
        attributes: SupportsLaxItems[str, str] | None = None,
    ) -> None: ...
    # pyrefly: ignore[bad-param-name-override]
    ignorableWhitespace = characters  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]  # ty: ignore[invalid-method-override]

@disjoint_base
class ElementTreeProducer(Generic[_ET]):
    """Produce SAX events from an `ElementTree` or element.

    This helper wraps an element or tree and drives a SAX `ContentHandler`
    with corresponding SAX events representing the tree structure.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.sax.html#lxml.sax.ElementTreeProducer)
    """

    _element: _ET
    _content_handler: ContentHandler
    # The purpose of _attr_class and _empty_attributes is
    # more like a shortcut. These attributes are constant and
    # doesn't help debugging
    def __init__(
        self,
        element_or_tree: _ElementOrTree[_ET],
        content_handler: ContentHandler,
    ) -> None: ...
    def saxify(self) -> None: ...

# equivalent to saxify() in ElementTreeProducer
def saxify(
    element_or_tree: _ElementOrTree,
    content_handler: ContentHandler,
) -> None: ...
