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
    _DefEtreeParsers,
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
    from typing import LiteralString, Never, Self
else:
    from typing_extensions import LiteralString, Never, Self

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

class _PullParserMixin:
    # The iterated items from pull parser events may return anything.
    # Even etree.TreeBuilder, which produce element nodes by default, allows
    # overriding factory functions via arguments to generate anything.
    def read_events(self) -> Iterator[tuple[str, _Element | Any]]: ...

# TODO Write wiki page and add link to this docstring
class CustomTargetParser(Generic[_T]):
    """This is a stub-only class (docstring pending)"""
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
    makeelement: type[_Element]
    """Creates a new element associated with this parser."""
    @property
    def feed_error_log(self) -> _ListErrorLog:
        """The error log of the last (or current) run of the feed parser.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser.feed_error_log)
        """
    def feed(self, data: str | bytes) -> None:
        """Feeds data to the parser. The argument should be an 8-bit string
        buffer containing encoded data, although Unicode is supported as long
        as both string types are not mixed.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser.feed)
        """
    @property
    def target(self) -> ParserTarget[_T]: ...
    def close(self) -> _T:
        """Terminates feeding data to this parser. This tells the parser to
        process any remaining data in the feed buffer, and then returns the root
        Element of the tree that was parsed.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser.close)
        """

# subscripted element typevar needs to be casted manually for type
# checking, and use .set_element_class_lookup() to set the element class
# lookup for runtime.
class XMLParser(Generic[_ET_co]):
    """The XML Parser. Parsers can be supplied as additional argument
    to various parse functions of the lxml API.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser)
    """
    @overload
    def __new__(
        cls,
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
        compact: bool = True,
    ) -> XMLParser[_ET_co]: ...
    @overload
    def __new__(  # type: ignore[misc]
        cls,
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
        target: ParserTarget[_T],
        compact: bool = True,
    ) -> CustomTargetParser[_T]:
        """The XML Parser. Parsers can be supplied as additional argument
        to various parse functions of the lxml API.

        Annotation
        ----------
        This overload handles the case where a custom parser target is provided
        via `target` parameter. Visit [wiki
        page](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser)
        on how to create such custom parser target.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser)
        """
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
    makeelement: type[_ET_co]
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
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser.set_element_class_lookup)
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
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser.feed_error_log)
        """
    def feed(self, data: str | bytes) -> None:
        """Feeds data to the parser. The argument should be an 8-bit string
        buffer containing encoded data, although Unicode is supported as long
        as both string types are not mixed.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser.feed)
        """
    @property
    def target(self) -> None: ...
    def close(self) -> _ET_co:
        """Terminates feeding data to this parser. This tells the parser to
        process any remaining data in the feed buffer, and then returns the root
        Element of the tree that was parsed.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLParser.close)
        """

class XMLPullParser(_PullParserMixin, XMLParser[_ET_co]):
    """XML parser that collects parse events in an iterator.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLPullParser)
    """
    def __init__(
        self,
        events: Iterable[_SaxEventNames] | None = None,
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        base_url: str | bytes | None = None,
        # All arguments from XMLParser, except 'target' which is
        # removed. Leave custom target parser creation to XMLParser
        # and HTMLParser.
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
        compact: bool = True,
    ) -> None: ...

# This is XMLParser with some preset keyword arguments, and without
# 'collect_ids' argument. Removing those keywords here, otherwise
# ETCompatXMLParser has no reason to exist. 'target' argument
# is likewise removed.
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
        compact: bool = True,
    ) -> None: ...

def set_default_parser(parser: _DefEtreeParsers[Any] | None = None) -> None: ...
def get_default_parser() -> _DefEtreeParsers[Any]: ...

# subscripted element typevar needs to be casted manually for type
# checking, and use set_element_class_lookup() to set the element class
# lookup for runtime.
class HTMLParser(Generic[_ET_co]):
    """This parser allows reading HTML into a normal XML tree. By default, it
    can read broken (non well-formed) HTML, depending on the capabilities of
    libxml2.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLParser)
    """
    @overload
    def __new__(
        cls,
        *,
        encoding: _TextArg | None = None,
        remove_blank_text: bool = False,
        remove_comments: bool = False,
        remove_pis: bool = False,
        no_network: bool = True,
        schema: XMLSchema | None = None,
        recover: bool = True,
        compact: bool = True,
        default_doctype: bool = True,
        collect_ids: bool = True,
        huge_tree: bool = False,
    ) -> HTMLParser[_ET_co]: ...
    @overload
    def __new__(  # type: ignore[misc]
        cls,
        *,
        encoding: _TextArg | None = None,
        remove_blank_text: bool = False,
        remove_comments: bool = False,
        remove_pis: bool = False,
        no_network: bool = True,
        target: ParserTarget[_T],
        schema: XMLSchema | None = None,
        recover: bool = True,
        compact: bool = True,
        default_doctype: bool = True,
        collect_ids: bool = True,
        huge_tree: bool = False,
    ) -> CustomTargetParser[_T]:
        """This parser allows reading HTML into a normal XML tree. By default, it
        can read broken (non well-formed) HTML, depending on the capabilities of
        libxml2.

        Annotation
        ----------
        This overload handles the case where a custom parser target is provided
        via `target` parameter. Visit [wiki
        page](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser)
        on how to create such custom parser target.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLParser)
        """
    @overload
    @deprecated("strip_cdata argument was always useless, and dropped after 5.2.2")
    def __new__(
        cls,
        *,
        strip_cdata: bool,
        **__kw: Any,
    ) -> Never:
        """This parser allows reading HTML into a normal XML tree. By default, it
        can read broken (non well-formed) HTML, depending on the capabilities of
        libxml2.

        Annotation
        ----------
        This overload guards against usage of 'strip_cdata' parameter, which is
        found to be completely noop, and ultimate removed since v5.2.2.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLParser)
        """
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
    makeelement: type[_ET_co]
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
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLParser.set_element_class_lookup)
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
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLParser.feed_error_log)
        """
    def feed(self, data: str | bytes) -> None:
        """Feeds data to the parser. The argument should be an 8-bit string
        buffer containing encoded data, although Unicode is supported as long
        as both string types are not mixed.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLParser.feed)
        """
    @property
    def target(self) -> None: ...
    def close(self) -> _ET_co:
        """Terminates feeding data to this parser. This tells the parser to
        process any remaining data in the feed buffer, and then returns the root
        Element of the tree that was parsed.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLParser.close)
        """

class HTMLPullParser(_PullParserMixin, HTMLParser[_ET_co]):
    """HTML parser that collects parse events in an iterator.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLPullParser)
    """
    @overload
    def __init__(
        self,
        events: Iterable[_SaxEventNames] | None = None,
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        base_url: str | bytes | None = None,
        # All arguments from XMLParser, except 'target' which is
        # removed. Leave custom target parser creation to XMLParser
        # and HTMLParser.
        encoding: _TextArg | None = None,
        remove_blank_text: bool = False,
        remove_comments: bool = False,
        remove_pis: bool = False,
        no_network: bool = True,
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
    ) -> Never:
        """HTML parser that collects parse events in an iterator.

        Annotation
        ----------
        This overload guards against usage of 'strip_cdata' parameter, which is
        found to be completely noop, and ultimate removed since v5.2.2.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTMLPullParser)
        """
