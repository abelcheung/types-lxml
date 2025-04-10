import sys
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    Literal,
    TypeVar,
    overload,
)

from .._types import (
    _AnyStr,
    _DefEtreeParsers,
    _ElementFactory,
    _ET_co,
    _SaxEventNames,
    _TagSelector,
    _TextArg,
)
from ._classlookup import ElementClassLookup
from ._docloader import _ResolverRegistry
from ._element import _Element
from ._module_misc import LxmlError, LxmlSyntaxError
from ._saxparser import ParserTarget
from ._xmlerror import _ListErrorLog
from ._xmlschema import XMLSchema

if sys.version_info >= (3, 11):
    from typing import LiteralString, Self
else:
    from typing_extensions import LiteralString, Self

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

_T = TypeVar("_T")

class ParseError(LxmlSyntaxError):
    code: int
    @property
    def position(self) -> tuple[int, int]: ...
    @position.setter
    def position(self, value: tuple[int, int]) -> None: ...
    def __init__(
        self,
        message: object,
        code: int,
        line: int,
        column: int,
        filename: str | None = None,
    ) -> None: ...

class XMLSyntaxError(ParseError): ...
class ParserError(LxmlError): ...

# Custom parser target support is abandoned,
# see comment in XMLParser
class _ParserTargetMixin(Generic[_T]):
    @property
    def target(self) -> ParserTarget[_T] | None: ...
    def close(self) -> _T: ...

class _PullParserMixin:
    # The iterated items from pull parser events may return anything.
    # Even etree.TreeBuilder, which produce element nodes by default, allows
    # overriding factory functions via arguments to generate anything.
    def read_events(self) -> Iterator[tuple[str, _Element | Any]]: ...

# It is unfortunate that, in the end, it is decided to forfeit
# integration of custom target annotation (the 'target' parameter).
# So far all attempts would cause usage of annotation unnecessarily
# complex and convoluted, yet still can't get everything right.
class XMLParser(_ParserTargetMixin[Any], Generic[_ET_co]):
    """The XML Parser. Parsers can be supplied as additional argument
    to various parse functions of the lxml API.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser)
    """
    def __init__(
        self,
        *,
        encoding: _TextArg | None = None,
        attribute_defaults: bool = False,
        dtd_validation: bool = False,
        load_dtd: bool = False,
        no_network: bool = True,
        ns_clean: bool = False,
        recover: bool = False,
        schema: XMLSchema | None = None,
        huge_tree: bool = False,
        remove_blank_text: bool = False,
        resolve_entities: bool | Literal["internal"] = "internal",
        remove_comments: bool = False,
        remove_pis: bool = False,
        strip_cdata: bool = True,
        collect_ids: bool = True,
        target: ParserTarget[Any] | None = None,
        compact: bool = True,
    ) -> None: ...
    @property
    def error_log(self) -> _ListErrorLog:
        """The error log of the last parser run."""
    @property
    def resolvers(self) -> _ResolverRegistry:
        """The custom resolver registry of this parser."""
    @property
    def version(self) -> LiteralString:
        """The version of the underlying XML parser."""
    def copy(self) -> Self:
        """Create a new parser with the same configuration."""
    makeelement: _ElementFactory[_ET_co]
    """Creates a new element associated with this parser."""
    def set_element_class_lookup(
        self, lookup: ElementClassLookup | None = None
    ) -> None:
        """Set a lookup scheme for element classes generated from this parser.

        Annotation
        ----------
        When calling this method, user would want to
        [change typing specialization](https://github.com/abelcheung/types-lxml/wiki/Using-specialised-class-directly#no-automatic-change-of-subscript)
        of concerned parser manually, because current python
        typing system can't change it automatically.
        Above link contains example on how to do it.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._FeedParser.set_element_class_lookup)
        """
    @deprecated("Removed since 5.0; renamed to set_element_class_lookup()")
    def setElementClassLookup(
        self, lookup: ElementClassLookup | None = None
    ) -> None: ...
    @property
    def feed_error_log(self) -> _ListErrorLog:
        """The error log of the last (or current) run of the feed parser.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._FeedParser.feed_error_log)
        """
    def feed(self, data: _AnyStr) -> None:
        """Feeds data to the parser. The argument should be an 8-bit string
        buffer containing encoded data, although Unicode is supported as long
        as both string types are not mixed.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._FeedParser.feed)
        """

class XMLPullParser(_PullParserMixin, XMLParser[_ET_co]):
    def __init__(
        self,
        events: Iterable[_SaxEventNames] | None = None,
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        base_url: str | bytes | None = None,
        # All arguments from XMLParser
        encoding: _TextArg | None = None,
        attribute_defaults: bool = False,
        dtd_validation: bool = False,
        load_dtd: bool = False,
        no_network: bool = True,
        ns_clean: bool = False,
        recover: bool = False,
        schema: XMLSchema | None = None,
        huge_tree: bool = False,
        remove_blank_text: bool = False,
        resolve_entities: bool | Literal["internal"] = "internal",
        remove_comments: bool = False,
        remove_pis: bool = False,
        strip_cdata: bool = True,
        collect_ids: bool = True,
        target: ParserTarget[Any] | None = None,
        compact: bool = True,
    ) -> None: ...

# This is XMLParser with some preset keyword arguments, and without
# 'collect_ids' argument. Removing those keywords here, otherwise
# ETCompatXMLParser has no reason to exist.
class ETCompatXMLParser(XMLParser[_ET_co]):
    def __init__(
        self,
        *,
        encoding: _TextArg | None = None,
        attribute_defaults: bool = False,
        dtd_validation: bool = False,
        load_dtd: bool = False,
        no_network: bool = True,
        ns_clean: bool = False,
        recover: bool = False,
        schema: XMLSchema | None = None,
        huge_tree: bool = False,
        remove_blank_text: bool = False,
        resolve_entities: bool | Literal["internal"] = True,
        strip_cdata: bool = True,
        target: ParserTarget[Any] | None = None,
        compact: bool = True,
    ) -> None: ...

def set_default_parser(parser: _DefEtreeParsers[Any] | None) -> None: ...
def get_default_parser() -> _DefEtreeParsers[Any]: ...

class HTMLParser(_ParserTargetMixin[Any], Generic[_ET_co]):
    """This parser allows reading HTML into a normal XML tree. By default, it
    can read broken (non well-formed) HTML, depending on the capabilities of
    libxml2.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLParser)
    """
    @overload
    def __init__(
        self,
        *,
        encoding: _TextArg | None = None,
        remove_blank_text: bool = False,
        remove_comments: bool = False,
        remove_pis: bool = False,
        no_network: bool = True,
        target: ParserTarget[Any] | None = None,
        schema: XMLSchema | None = None,
        recover: bool = True,
        compact: bool = True,
        default_doctype: bool = True,
        collect_ids: bool = True,
        huge_tree: bool = False,
    ) -> None: ...
    @overload
    @deprecated("strip_cdata argument was always useless, and dropped after 5.2.2")
    def __init__(
        self,
        *,
        strip_cdata: bool,
        **__kw: Any,
    ) -> None: ...
    @property
    def error_log(self) -> _ListErrorLog:
        """The error log of the last parser run."""
    @property
    def resolvers(self) -> _ResolverRegistry:
        """The custom resolver registry of this parser."""
    @property
    def version(self) -> LiteralString:
        """The version of the underlying XML parser."""
    def copy(self) -> Self:
        """Create a new parser with the same configuration."""
    makeelement: _ElementFactory[_ET_co]
    """Creates a new element associated with this parser."""
    def set_element_class_lookup(
        self, lookup: ElementClassLookup | None = None
    ) -> None:
        """Set a lookup scheme for element classes generated from this parser.

        Annotation
        ----------
        When calling this method, user would want to
        [change typing specialization](https://github.com/abelcheung/types-lxml/wiki/Using-specialised-class-directly#no-automatic-change-of-subscript)
        of concerned parser manually, because current python
        typing system can't change it automatically.
        Above link contains example on how to do it.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._FeedParser.set_element_class_lookup)
        """
    @deprecated("Removed since 5.0; renamed to set_element_class_lookup()")
    def setElementClassLookup(
        self, lookup: ElementClassLookup | None = None
    ) -> None: ...
    @property
    def feed_error_log(self) -> _ListErrorLog:
        """The error log of the last (or current) run of the feed parser.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._FeedParser.feed_error_log)
        """
    def feed(self, data: _AnyStr) -> None:
        """Feeds data to the parser. The argument should be an 8-bit string
        buffer containing encoded data, although Unicode is supported as long
        as both string types are not mixed.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._FeedParser.feed)
        """

class HTMLPullParser(_PullParserMixin, HTMLParser[_ET_co]):
    @overload
    def __init__(
        self,
        events: Iterable[_SaxEventNames] | None = None,
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        base_url: str | bytes | None = None,
        # All arguments from HTMLParser
        encoding: _TextArg | None = None,
        remove_blank_text: bool = False,
        remove_comments: bool = False,
        remove_pis: bool = False,
        no_network: bool = True,
        target: ParserTarget[Any] | None = None,
        schema: XMLSchema | None = None,
        recover: bool = True,
        compact: bool = True,
        default_doctype: bool = True,
        collect_ids: bool = True,
        huge_tree: bool = False,
    ) -> None: ...
    @overload
    @deprecated("strip_cdata argument was always useless, and dropped after 5.2.2")
    def __init__(
        self,
        *,
        strip_cdata: bool,
        **__kw: Any,
    ) -> None: ...
