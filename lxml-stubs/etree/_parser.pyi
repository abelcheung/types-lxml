from abc import abstractmethod
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Protocol,
    TypeVar,
    overload,
)

from .._types import SupportsLaxedItems, _AnyStr, _NSMapArg, _TagName
from . import (
    ElementClassLookup,
    LxmlError,
    LxmlSyntaxError,
    XMLSchema,
    _Element,
    _TagSelector,
)
from ._docloader import _ResolverRegistry
from ._xmlerror import _ErrorLog

Self = TypeVar("Self")
_T_co = TypeVar("_T_co", covariant=True)
# The basic parsers bundled in lxml.etree
_DefEtreeParsers = XMLParser[_T_co] | HTMLParser[_T_co]

class ParseError(LxmlSyntaxError):
    lineno: int
    offset: int
    # XXX OK, now it might make sense to generate all error constants
    # since they are behaving like IntEnum. But it's low priority.
    code: int
    filename: str | None
    position: tuple[int, int]
    def __init__(
        self,
        message: Any,
        code: int,
        line: int,
        column: int,
        filename: str | None = ...,
    ) -> None: ...

class XMLSyntaxError(ParseError): ...
class ParserError(LxmlError): ...

class ParserTarget(Protocol[_T_co]):
    """This is a stub-only class representing parser target interface.

    - Because almost all methods are optional, ParserTarget should be
      explicitly inherited in code for type checking. See TreeBuilder
      and the snippet example below.
    - Some IDEs can do method signature autocompletion. See notes below.

    Example
    -------
    ```python
    from lxml import etree
    if not TYPE_CHECKING:
        etree.ParserTarget = object

    class MyParserTarget(etree.ParserTarget):
        def __init__(self) -> None: ...
        def start(self,  # 3 argument form is not autocompleted
            tag: str, attrib: _Attrib, nsmap: Mapping[str, str] = ...,
        ) -> None: ...
            # Do something
        def close(self) -> str:
            return "something"

    parser = etree.HTMLParser()  # type is HTMLParser[_Element]
    result = parser.close()  # _Element

    t1 = MyParserTarget()
    parser = etree.HTMLParser(target=t1)  # mypy -> HTMLParser[Any]
                                          # pyright -> HTMLParser[Unknown]

    t2 = cast("etree.ParserTarget[str]", MyParserTarget())
    parser = etree.HTMLParser(target=t2)  # HTMLParser[str]
    result = parser.close()  # str
    ```

    Notes
    -----
    - Only `close()` is mandatory. In extreme case, a vanilla class instance
      with noop `close()` is a valid null parser target that does nothing.
    - `start()` can take either 2 or 3 extra arguments, but 3rd argument
      must be entered manually after autocompletion, with following
      signature: `nsmap: Mapping[str, str]`.
    - Some methods are undocumented. They are included in stub nonetheless.

    See Also
    --------
    - `_PythonSaxParserTarget()` in `src/lxml/parsertarget.pxi`
    - [Target parser official document](https://lxml.de/parsing.html#the-target-parser-interface)
    """

    @abstractmethod
    def close(self) -> _T_co: ...
    def comment(self, text: str) -> None: ...
    def data(self, data: str) -> None: ...
    def end(self, tag: str) -> None: ...
    # FIXME start() is particularly troublesome, as it could be in either
    # 2 argument or 3 argument form. Both @overload and union of callable
    # won't stop mypy from complaining about incompatibility.
    start: Callable[..., None]
    # Methods below are undocumented. Lxml has described
    # 'start-ns' and 'end-ns' events however.
    def pi(self, target: str, data: str | None) -> None: ...
    # Default namespace prefix is empty string, not None
    def start_ns(self, prefix: str, uri: str) -> None: ...
    def end_ns(self, prefix: str) -> None: ...
    def doctype(
        self,
        root_tag: str | None,
        public_id: str | None,
        system_id: str | None,
    ) -> None: ...

# Includes most stuff in _BaseParser; when custom parser target is used,
# _CustomParserTargetMixin below enlists specialized methods and properties
class _FeedParser:
    @property
    def error_log(self) -> _ErrorLog: ...
    @property
    def resolvers(self) -> _ResolverRegistry: ...
    @property
    def version(self) -> str: ...
    def copy(self: Self) -> Self: ...
    def makeelement(
        self,
        _tag: _TagName,
        /,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> _Element: ...
    def set_element_class_lookup(
        self, lookup: ElementClassLookup | None = ...
    ) -> None: ...
    @property
    def feed_error_log(self) -> _ErrorLog: ...
    def feed(self, data: _AnyStr) -> None: ...

# Contains specialized properties and methods from _BaseParser and _FeedParser,
# when custom parser target is used. Only applies to basic parsers defined
# in lxml.etree.
class _CustomParserTargetMixin(Generic[_T_co]):
    @property
    def target(self) -> ParserTarget[_T_co] | None: ...
    def close(self) -> _T_co: ...

class XMLParser(_CustomParserTargetMixin[_T_co], _FeedParser):
    @overload
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
        target: ParserTarget[_T_co],
        compact: bool = ...,
    ) -> XMLParser[_T_co]: ...
    @overload
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
        target: None = ...,
        compact: bool = ...,
    ) -> XMLParser[_Element]: ...

class XMLPullParser(XMLParser[_T_co]):
    @overload
    def __new__(
        cls,
        events: Iterable[str] | None = ...,
        *,
        tag: _TagSelector = ...,
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
        target: ParserTarget[_T_co],
        compact: bool = ...,
    ) -> XMLPullParser[_T_co]: ...
    @overload
    def __new__(
        cls,
        events: Iterable[str] | None = ...,
        *,
        tag: _TagSelector = ...,
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
        target: None = ...,
        compact: bool = ...,
    ) -> XMLPullParser[_Element]: ...
    # The iterated items from pull parser events may return anything.
    # Even etree.TreeBuilder, which produce element nodes by default, allows
    # overriding factory functions via arguments to generate anything.
    # Same applies to HTMLPullParser below.
    def read_events(self) -> Iterator[tuple[str, Any]]: ...

# This is XMLParser with some preset keyword arguments, and without
# 'collect_ids' argument. Removing those keywords here, otherwise
# ETCompatXMLParser has no reason to exist.
class ETCompatXMLParser(XMLParser[_T_co]):
    @overload
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
        target: ParserTarget[_T_co],
        compact: bool = ...,
    ) -> ETCompatXMLParser[_T_co]: ...
    @overload
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
        target: None = ...,
        compact: bool = ...,
    ) -> ETCompatXMLParser[_Element]: ...

def set_default_parser(parser: _DefEtreeParsers[Any] | None) -> None: ...
def get_default_parser() -> _DefEtreeParsers[Any]: ...

class HTMLParser(_CustomParserTargetMixin[_T_co], _FeedParser):
    @overload
    def __new__(
        cls,
        *,
        encoding: _AnyStr | None = ...,
        collect_ids: bool = ...,
        compact: bool = ...,
        huge_tree: bool = ...,
        no_network: bool = ...,
        recover: bool = ...,
        remove_blank_text: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        schema: XMLSchema | None = ...,
        strip_cdata: bool = ...,
        target: ParserTarget[_T_co],
    ) -> HTMLParser[_T_co]: ...
    @overload
    def __new__(
        cls,
        *,
        encoding: _AnyStr | None = ...,
        collect_ids: bool = ...,
        compact: bool = ...,
        huge_tree: bool = ...,
        no_network: bool = ...,
        recover: bool = ...,
        remove_blank_text: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        schema: XMLSchema | None = ...,
        strip_cdata: bool = ...,
        target: None = ...,
    ) -> HTMLParser[_Element]: ...

class HTMLPullParser(HTMLParser[_T_co]):
    @overload
    def __new__(
        cls,
        events: Iterable[str] | None = ...,
        *,
        tag: _TagSelector = ...,
        base_url: _AnyStr | None = ...,
        # All arguments from HTMLParser
        encoding: _AnyStr | None = ...,
        remove_blank_text: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        no_network: bool = ...,
        target: ParserTarget[_T_co],
        schema: XMLSchema | None = ...,
        recover: bool = ...,
        compact: bool = ...,
        collect_ids: bool = ...,
        huge_tree: bool = ...,
    ) -> HTMLPullParser[_T_co]: ...
    @overload
    def __new__(
        cls,
        events: Iterable[str] | None = ...,
        *,
        tag: _TagSelector = ...,
        base_url: _AnyStr | None = ...,
        # All arguments from HTMLParser
        encoding: _AnyStr | None = ...,
        remove_blank_text: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        no_network: bool = ...,
        target: None = ...,
        schema: XMLSchema | None = ...,
        recover: bool = ...,
        compact: bool = ...,
        collect_ids: bool = ...,
        huge_tree: bool = ...,
    ) -> HTMLPullParser[_Element]: ...
    def read_events(self) -> Iterator[tuple[str, Any]]: ...
