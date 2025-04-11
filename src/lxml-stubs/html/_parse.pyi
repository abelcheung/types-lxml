import sys
from typing import Any, Iterable, Literal, MutableMapping, overload

from .. import etree
from .._types import (
    Unused,
    _FileReadSource,
)
from ._element import HtmlElement

if sys.version_info >= (3, 12):
    from collections.abc import Buffer
else:
    from typing_extensions import Buffer

#
# Parser
#

class HTMLParser(etree.HTMLParser[HtmlElement]):
    """An HTML parser configured to return `lxml.html` Element objects.

    Annotation
    ----------
    This is not a generic parser class like the `etree` counterpart. Parsers
    from `html` submodule are designed to always handle `HtmlElement`. for
    generating other kinds of elements, use `etree` parsers with
    `set_element_class_lookup()` method instead.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.html.html#lxml.html.HTMLParser)
    """

class XHTMLParser(etree.XMLParser[HtmlElement]):
    """An XML parser configured to return `lxml.html` Element objects.

    Annotation
    ----------
    This is not a generic parser class like the `etree` counterpart. Parsers
    from `html` submodule are designed to always handle `HtmlElement`. for
    generating other kinds of elements, use `etree` parsers with
    `set_element_class_lookup()` method instead.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.html.html#lxml.html.XHTMLParser)
    """

html_parser: HTMLParser
xhtml_parser: XHTMLParser

#
# Parsing functions
#

# Calls etree.fromstring(html, parser, **kw) which has signature
# fromstring(text, parser, *, base_url)
def document_fromstring(
    html: str | Buffer,
    parser: HTMLParser | XHTMLParser | None = None,
    ensure_head_body: bool = False,
    *,
    base_url: str | None = None,
) -> HtmlElement: ...
@overload
def fragments_fromstring(  # type: ignore[overload-overlap]  # pyright: ignore[reportOverlappingOverload]_parse
    html: str | bytes,
    no_leading_text: Literal[True],
    base_url: str | None = None,
    parser: HTMLParser | XHTMLParser | None = None,
) -> list[HtmlElement]: ...
@overload
def fragments_fromstring(
    html: str | bytes,
    no_leading_text: bool = False,
    base_url: str | None = None,
    parser: HTMLParser | XHTMLParser | None = None,
) -> list[str | HtmlElement]: ...
def fragment_fromstring(
    html: str | bytes,
    create_parent: bool | str = False,
    base_url: str | None = None,
    parser: HTMLParser | XHTMLParser | None = None,
) -> HtmlElement: ...
def fromstring(
    html: str | bytes,
    base_url: str | None = None,
    parser: HTMLParser | XHTMLParser | None = None,
) -> HtmlElement: ...
def parse(
    filename_or_url: _FileReadSource,
    parser: HTMLParser | XHTMLParser | None = None,
    base_url: str | None = None,
) -> etree._ElementTree[HtmlElement]: ...

#
# Element Lookup
#

class HtmlElementClassLookup(etree.CustomElementClassLookup):
    def __init__(
        self,
        # Should have been something like Mapping[str, type[HtmlElement]],
        # but unfortunately classes mapping is required to be mutable
        classes: MutableMapping[str, Any] | None = None,
        # docstring says mixins is mapping, but implementation says otherwise
        mixins: Iterable[tuple[str, type[HtmlElement]]] | None = None,
    ) -> None: ...
    def lookup(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        node_type: Literal["element", "comment", "PI", "entity"] | None,
        document: Unused,
        namespace: Unused,
        name: str,  # type: ignore[override]
    ) -> type[HtmlElement] | None: ...
