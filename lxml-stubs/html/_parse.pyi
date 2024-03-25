import sys
from typing import Any, Iterable, MutableMapping

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from .. import etree
from .._types import Unused, _AnyStr, _ElemClsLookupArg, _FileReadSource
from ._element import HtmlElement

_HtmlElemParser: TypeAlias = etree._parser._DefEtreeParsers[HtmlElement]

#
# Parser
#

# Stub version before March 2023 used to omit 'target' parameter, which
# would nullify default HTML element lookup behavior, degenerating html
# submodule parsers into etree ones. Since it is decided to not support
# custom target parser for now, we just add back 'target' parameter for
# coherence. Same for XHTMLParser below.
class HTMLParser(etree.HTMLParser[HtmlElement]):
    """An HTML parser configured to return ``lxml.html`` Element
    objects.

    Notes
    -----
    This subclass is not specialized, unlike the ``etree`` counterpart.
    They are designed to always handle ``HtmlElement``;
    for generating other kinds of ``_Elements``, one should use
    etree parsers with ``set_element_class_lookup()`` method instead.
    In that case, see ``_FeedParser.set_element_class_lookup()`` for more info.
    """

    def __init__(
        self,
        *,
        encoding: _AnyStr | None = ...,
        remove_blank_text: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        no_network: bool = ...,
        target: etree.ParserTarget[Any] | None = ...,
        schema: etree.XMLSchema | None = ...,
        recover: bool = ...,
        compact: bool = ...,
        default_doctype: bool = ...,
        collect_ids: bool = ...,
        huge_tree: bool = ...,
    ) -> None: ...
    @property
    def target(self) -> None: ...

class XHTMLParser(etree.XMLParser[HtmlElement]):
    """An XML parser configured to return ``lxml.html`` Element
    objects.

    Notes
    -----
    This subclass is not specialized, unlike the ``etree`` counterpart.
    They are designed to always handle ``HtmlElement``;
    for generating other kinds of ``_Elements``, one should use
    etree parsers with ``set_element_class_lookup()`` method instead.
    In that case, see ``_FeedParser.set_element_class_lookup()`` for more info.

    Original doc
    ------------
    Note that this parser is not really XHTML aware unless you let it
    load a DTD that declares the HTML entities.  To do this, make sure
    you have the XHTML DTDs installed in your catalogs, and create the
    parser like this::

        >>> parser = XHTMLParser(load_dtd=True)

    If you additionally want to validate the document, use this::

        >>> parser = XHTMLParser(dtd_validation=True)

    For catalog support, see http://www.xmlsoft.org/catalog.html.
    """

    def __init__(
        self,
        *,
        encoding: _AnyStr | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        target: etree.ParserTarget[Any] | None = ...,
        ns_clean: bool = ...,
        recover: bool = ...,
        schema: etree.XMLSchema | None = ...,
        huge_tree: bool = ...,
        remove_blank_text: bool = ...,
        resolve_entities: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        collect_ids: bool = ...,
        compact: bool = ...,
    ) -> None: ...
    @property
    def target(self) -> None: ...

html_parser: HTMLParser
xhtml_parser: XHTMLParser

#
# Parsing funcs
#

# Calls etree.fromstring(html, parser, **kw) which has signature
# fromstring(text, parser, *, base_url)
def document_fromstring(
    html: _AnyStr,
    parser: _HtmlElemParser | None = ...,
    ensure_head_body: bool = ...,
    *,
    base_url: str | None = ...,
) -> HtmlElement: ...
def fragments_fromstring(
    html: _AnyStr,
    no_leading_text: bool = ...,
    base_url: str | None = ...,
    parser: _HtmlElemParser | None = ...,
    **kw: Unused,
) -> list[HtmlElement]: ...
def fragment_fromstring(
    html: _AnyStr,
    create_parent: bool = ...,
    base_url: str | None = ...,
    parser: _HtmlElemParser | None = ...,
    **kw: Unused,
) -> HtmlElement: ...
def fromstring(
    html: _AnyStr,
    base_url: str | None = ...,
    parser: _HtmlElemParser | None = ...,
    **kw: Unused,
) -> HtmlElement: ...
def parse(
    filename_or_url: _FileReadSource,
    parser: _HtmlElemParser | None = ...,
    base_url: str | None = ...,
    **kw: Unused,
) -> etree._ElementTree[HtmlElement]: ...

#
# Element Lookup
#

class HtmlElementClassLookup(etree.CustomElementClassLookup):
    def __init__(
        self,
        # Should have been something like Mapping[str, type[HtmlElement]],
        # but unfortunately classes mapping is required to be mutable
        classes: MutableMapping[str, Any] | None = ...,
        # docstring says mixins is mapping, but implementation says otherwise
        mixins: Iterable[tuple[str, type[HtmlElement]]] = ...,
    ) -> None: ...
    # Both argument names and types are incompatible with base class
    # This is a standard practise for lxml
    def lookup(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        node_type: _ElemClsLookupArg | None,
        document: Unused,
        namespace: Unused,
        name: str,  # type: ignore[override]
    ) -> type[HtmlElement] | None: ...
