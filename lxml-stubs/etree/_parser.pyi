from abc import ABCMeta, abstractmethod
from typing import Any, Iterable, Iterator, Protocol, TypeVar

from .._types import SupportsLaxedItems, _AnyStr, _NSMapArg, _TagName
from . import (
    ElementClassLookup,
    LxmlError,
    LxmlSyntaxError,
    XMLSchema,
    _Attrib,
    _Element,
    _TagSelector,
)
from ._docloader import _ResolverRegistry
from ._xmlerror import _ErrorLog

Self = TypeVar("Self")

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

class ParserTarget(Protocol, metaclass=ABCMeta):
    """This is a stub-only class representing parser target interface.

    - Because almost all methods are optional, ParserTarget should be
      explicitly inherited in code for type checking. See TreeBuilder
      and the snippet example below.
    - Some IDEs can do method signature autocompletion. See notes below.

    ```python
    if TYPE_CHECKING:
        from lxml.etree import ParserTarget
    else:
        ParserTarget = object

    class MyParserTarget(ParserTarget):
        def start(self,  # 3 argument form is not autocompleted
            tag: str,
            attrib: _Attrib,
            nsmap: Mapping[str, str] = ...,
        ) -> None: ...
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
    def close(self) -> Any: ...
    def comment(self, text: str) -> None: ...
    def data(self, data: str) -> None: ...
    def end(self, tag: str) -> None: ...
    # Base class can only use 2-argument form, in case where
    # start() for inherited class uses 2 arguments too
    def start(self, tag: str, attrib: _Attrib) -> None: ...
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

class _BaseParser:
    @property
    def target(self) -> ParserTarget | None: ...
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
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> _Element: ...
    # Marked as deprecated, identical to snake case method
    def setElementClassLookup(
        self, lookup: ElementClassLookup | None = ...
    ) -> None: ...
    def set_element_class_lookup(
        self, lookup: ElementClassLookup | None = ...
    ) -> None: ...

class _FeedParser(_BaseParser):
    @property
    def feed_error_log(self) -> _ErrorLog: ...
    def close(self) -> _Element: ...
    def feed(self, data: _AnyStr) -> None: ...

class XMLParser(_FeedParser):
    def __init__(
        self,
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
        target: ParserTarget | None = ...,
        compact: bool = ...,
    ) -> None: ...
    resolvers: _ResolverRegistry

class XMLPullParser(XMLParser):
    def __init__(
        self,
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
        target: ParserTarget | None = ...,
        compact: bool = ...,
    ) -> None: ...
    # The iterated items from pull parser events may return anything.
    # Even etree.TreeBuilder, which produce element nodes by default, allows
    # overriding factory functions via arguments to generate anything.
    # Same applies to HTMLPullParser below.
    def read_events(self) -> Iterator[tuple[str, Any]]: ...

# ET compatible parser should be nearly identical to XMLParser
# in nature, but somehow doesn't have 'collect_ids' argument
class ETCompatXMLParser(XMLParser):
    def __init__(
        self,
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
        target: ParserTarget | None = ...,
        compact: bool = ...,
    ) -> None: ...

def set_default_parser(parser: _BaseParser | None) -> None: ...
def get_default_parser() -> _BaseParser | None: ...

class HTMLParser(_FeedParser):
    def __init__(
        self,
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
        target: ParserTarget | None = ...,
    ) -> None: ...

class HTMLPullParser(HTMLParser):
    def __init__(
        self,
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
        target: ParserTarget | None = ...,
        schema: XMLSchema | None = ...,
        recover: bool = ...,
        compact: bool = ...,
        collect_ids: bool = ...,
        huge_tree: bool = ...,
    ) -> None: ...
    def read_events(self) -> Iterator[tuple[str, Any]]: ...
