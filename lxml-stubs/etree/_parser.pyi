import sys
from _typeshed import _T
from typing import Any, Generic, Iterable, Iterator

if sys.version_info >= (3, 11):
    from typing import LiteralString, Self
else:
    from typing_extensions import LiteralString, Self

if sys.version_info >= (3, 13):
    from typing import deprecated
else:
    from typing_extensions import deprecated

from .._types import (
    SupportsLaxedItems,
    _AnyStr,
    _ET_co,
    _NSMapArg,
    _SaxEventNames,
    _TagName,
    _TagSelector,
)
from ._classlookup import ElementClassLookup
from ._docloader import _ResolverRegistry
from ._element import _Element
from ._module_misc import LxmlError, LxmlSyntaxError
from ._saxparser import ParserTarget
from ._xmlerror import _ListErrorLog
from ._xmlschema import XMLSchema

# The basic parsers bundled in lxml.etree
_DefEtreeParsers = XMLParser[_ET_co] | HTMLParser[_ET_co]

class ParseError(LxmlSyntaxError):
    lineno: int  # pyright: ignore[reportIncompatibleVariableOverride]
    offset: int  # pyright: ignore[reportIncompatibleVariableOverride]
    code: int
    filename: str | None
    position: tuple[int, int]
    def __init__(
        self,
        message: object,
        code: int,
        line: int,
        column: int,
        filename: str | None = ...,
    ) -> None: ...

class XMLSyntaxError(ParseError): ...
class ParserError(LxmlError): ...

# Includes most stuff in _BaseParser
class _FeedParser(Generic[_ET_co]):
    @property
    def error_log(self) -> _ListErrorLog: ...
    @property
    def resolvers(self) -> _ResolverRegistry: ...
    @property
    def version(self) -> LiteralString: ...
    def copy(self) -> Self: ...
    def makeelement(
        self,
        _tag: _TagName,
        /,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> _ET_co: ...
    # XXX: In terms of annotation, what setting class_lookup
    # does is change _ET_co (type specialization), which can't be
    # done automatically with current python typing system.
    # One has to change it manually during type checking.
    # Very few people would do, if there were any at all.
    def set_element_class_lookup(self, lookup: ElementClassLookup | None = ...) -> None:
        """
        Notes
        -----
        When calling this method, it is advised to also change typing
        specialization of concerned parser too, because current python
        typing system can't change it automatically.

        Example
        -------
        Following code demonstrates how to create ``lxml.html.HTMLParser``
        manually from ``lxml.etree.HTMLParser``::

        ```python
        parser = lxml.etree.HTMLParser()  # type is HTMLParser[_Element]
        if TYPE_CHECKING:
            parser = cast('HTMLParser[HtmlElement]', parser)
        else:
            parser.set_element_class_lookup(lxml.html.HtmlElementClassLookup())
        ```
        """
        ...
    @deprecated(
        "Removed since 5.0; deprecated since v2.0 (2008); renamed to set_element_class_lookup()"
    )
    def setElementClassLookup(
        self, lookup: ElementClassLookup | None = ...
    ) -> None: ...
    @property
    def feed_error_log(self) -> _ListErrorLog: ...
    def feed(self, data: _AnyStr) -> None: ...

# XXX: Custom parser target support is temporarily abandoned,
# see comment in XMLParser
class _ParserTargetMixin(Generic[_T]):
    @property
    def target(self) -> ParserTarget[_T] | None: ...
    def close(self) -> _T: ...

class _PullParserMixin:
    # The iterated items from pull parser events may return anything.
    # Even etree.TreeBuilder, which produce element nodes by default, allows
    # overriding factory functions via arguments to generate anything.
    def read_events(self) -> Iterator[tuple[str, Any]]: ...

# XXX: Python doesn't support Higher Kinded Types, otherwise
# it should have been something like _PT[_Element]. This means
# one can't properly annotate subclassed XMLParser.
# https://github.com/python/typing/issues/548
# Same applies to all other parsers inherited from FeedParser.
#
# XXX: It is unfortunate that, in the end, it is decided to forfeit
# integration of custom target annotation (the 'target' parameter).
# So far all attempts would cause usage of annotation unnecessarily
# complex and convoluted, yet still can't get everything right.
class XMLParser(_ParserTargetMixin[Any], _FeedParser[_ET_co]):
    def __new__(
        cls,
        *,
        encoding: _AnyStr | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        ns_clean: bool = ...,
        recover: bool = ...,
        schema: XMLSchema | None = ...,
        huge_tree: bool = ...,
        remove_blank_text: bool = ...,
        resolve_entities: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        collect_ids: bool = ...,
        target: ParserTarget[Any] | None = ...,
        compact: bool = ...,
    ) -> XMLParser[_Element]: ...

class XMLPullParser(_PullParserMixin, XMLParser[_ET_co]):
    def __new__(
        cls,
        events: Iterable[_SaxEventNames] | None = ...,
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
        base_url: _AnyStr | None = ...,
        # All arguments from XMLParser
        encoding: _AnyStr | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        ns_clean: bool = ...,
        recover: bool = ...,
        schema: XMLSchema | None = ...,
        huge_tree: bool = ...,
        remove_blank_text: bool = ...,
        resolve_entities: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        collect_ids: bool = ...,
        target: ParserTarget[Any] | None = ...,
        compact: bool = ...,
    ) -> XMLPullParser[_Element]: ...

# This is XMLParser with some preset keyword arguments, and without
# 'collect_ids' argument. Removing those keywords here, otherwise
# ETCompatXMLParser has no reason to exist.
class ETCompatXMLParser(XMLParser[_ET_co]):
    def __new__(
        cls,
        *,
        encoding: _AnyStr | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        ns_clean: bool = ...,
        recover: bool = ...,
        schema: XMLSchema | None = ...,
        huge_tree: bool = ...,
        remove_blank_text: bool = ...,
        resolve_entities: bool = ...,
        strip_cdata: bool = ...,
        target: ParserTarget[Any] | None = ...,
        compact: bool = ...,
    ) -> ETCompatXMLParser[_Element]: ...

def set_default_parser(parser: _DefEtreeParsers[Any] | None) -> None: ...
def get_default_parser() -> _DefEtreeParsers[Any]: ...

class HTMLParser(_ParserTargetMixin[Any], _FeedParser[_ET_co]):
    def __new__(
        cls,
        *,
        encoding: _AnyStr | None = ...,
        remove_blank_text: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        no_network: bool = ...,
        target: ParserTarget[Any] | None = ...,
        schema: XMLSchema | None = ...,
        recover: bool = ...,
        compact: bool = ...,
        default_doctype: bool = ...,
        collect_ids: bool = ...,
        huge_tree: bool = ...,
    ) -> HTMLParser[_Element]: ...

class HTMLPullParser(_PullParserMixin, HTMLParser[_ET_co]):
    def __new__(
        cls,
        events: Iterable[_SaxEventNames] | None = ...,
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
        base_url: _AnyStr | None = ...,
        # All arguments from HTMLParser
        encoding: _AnyStr | None = ...,
        remove_blank_text: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        no_network: bool = ...,
        target: ParserTarget[Any] | None = ...,
        schema: XMLSchema | None = ...,
        recover: bool = ...,
        compact: bool = ...,
        default_doctype: bool = ...,
        collect_ids: bool = ...,
        huge_tree: bool = ...,
    ) -> HTMLPullParser[_Element]: ...
