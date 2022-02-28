# Hand-written stub for lxml.etree as used by mypy.report.
# This is *far* from complete, and the stubgen-generated ones crash mypy.
# Any use of `Any` below means I couldn't figure out the type.

from typing import (
    IO,
    Any,
    Callable,
    Collection,
    Iterable,
    Iterator,
    Mapping,
    Reversible,
    Sequence,
    SupportsBytes,
    TypeVar,
    Union,
    overload,
)

from os import PathLike
from typing_extensions import Literal, Protocol, TypeGuard

from .._types import (
    SupportsLaxedItems,
    _AnyStr,
    _ExtensionArg,
    _NonDefaultNSMapArg,
    _NSMapArg,
    _XPathObject,
    _XPathVarArg,
)
from ..cssselect import _CSSTransArg
from ._xmlerror import (
    ErrorDomains as ErrorDomains,
    ErrorLevels as ErrorLevels,
    ErrorTypes as ErrorTypes,
    PyErrorLog as PyErrorLog,
    RelaxNGErrorTypes as RelaxNGErrorTypes,
    _BaseErrorLog,
    _ErrorLog,
    clear_error_log as clear_error_log,
    use_global_python_log as use_global_python_log,
)
from ._xpath import (
    ETXPath as ETXPath,
    XPath as XPath,
    XPathDocumentEvaluator as XPathDocumentEvaluator,
    XPathElementEvaluator as XPathElementEvaluator,
    XPathError as XPathError,
    XPathEvaluator as XPathEvaluator,
    XPathSyntaxError as XPathSyntaxError,
)

#
# Basic variables and constants
#

_T = TypeVar("_T")
_ET = TypeVar("_ET", bound=_Element)

_TagName = _AnyStr | QName
# Note that _TagSelector filters element type not by classes, but
# checks for element _factory functions_ instead
# (that is Element(), Comment() and ProcessingInstruction()).
_TagSelector = Union[_TagName, _ElemFactory[_Element]]
# Elementpath API doesn't do str/byte conversion, only unicode accepted for py3
_ElemPathArg = str | QName
_KnownEncodings = Literal[
    "ASCII",
    "ascii",
    "UTF-8",
    "utf-8",
    "UTF8",
    "utf8",
    "US-ASCII",
    "us-ascii",
]
_ElementOrTree = _Element | _ElementTree
_FileSource = Union[_AnyStr, IO[Any], PathLike[Any]]

class _SmartStr(str):
    """Smart string is a private str subclass documented in
    [return types](https://lxml.de/xpathxslt.html#xpath-return-values)
    of XPath evaluation result. This stub-only class can be utilized like:

    ```python
    if TYPE_CHECKING:
        from lxml.etree import _SmartStr
    def is_smart_str(s: str) -> TypeGuard[_SmartStr]:
        return hasattr(s, 'getparent')
    if is_smart_str(result):
        parent = result.getparent() # identified as lxml.etree._Element
    ```
    """

    is_attribute: bool
    is_tail: bool
    is_text: bool
    attrname: str | None
    def getparent(self) -> _Element | None: ...

class DocInfo:
    root_name = ...  # type: str
    public_id = ...  # type: str | None
    system_id = ...  # type: str | None
    xml_version = ...  # type: str | None
    encoding = ...  # type: str | None
    standalone = ...  # type: bool | None
    URL = ...  # type: str
    internalDTD = ...  # type: "DTD"
    externalDTD = ...  # type: "DTD"
    def __init__(self, tree: _ElementOrTree) -> None: ...
    def clear(self) -> None: ...

# The base of _Element is *almost* an amalgam of MutableSequence[_Element]
# plus mixin methods for _Attrib.
# Extra methods follow the order of _Element source approximately
class _Element(Collection[_Element], Reversible[_Element]):
    #
    # Common properties
    #
    @property
    def tag(self) -> str: ...
    @tag.setter
    def tag(self, value: _TagName) -> None: ...
    @property
    def attrib(self) -> _Attrib: ...
    @property
    def text(self) -> str | None: ...
    @text.setter
    def text(self, value: _AnyStr | QName | CDATA | None) -> None: ...
    @property
    def tail(self) -> str | None: ...
    @tail.setter
    def tail(self, value: _AnyStr | CDATA | None) -> None: ...
    #
    # _Element-only properties
    # Following props are marked as read-only in comment,
    # but 'sourceline' and 'base' provide __set__ method
    # --- and they do work.
    #
    @property
    def prefix(self) -> str | None: ...
    @property
    def sourceline(self) -> int | None: ...
    @sourceline.setter
    def sourceline(self, value: int) -> None: ...
    @property
    def nsmap(self) -> dict[str | None, str]: ...
    @property
    def base(self) -> str | None: ...
    @base.setter
    def base(self, value: _AnyStr | None) -> None: ...
    #
    # Accessors
    #
    def __delitem__(self, __k: int | slice) -> None: ...
    @overload
    def __getitem__(self, __x: int) -> _Element: ...
    @overload
    def __getitem__(self, __x: slice) -> list[_Element]: ...
    @overload
    def __setitem__(self, __x: int, __v: _Element) -> None: ...
    @overload
    def __setitem__(self, __x: slice, __v: Iterable[_Element]) -> None: ...
    def __contains__(self, __x: object) -> bool: ...
    def __len__(self) -> int: ...
    # There are a hoard of element iterators used in lxml, but
    # they only differ in implementation detail and don't affect typing.
    def __iter__(self) -> Iterator[_Element]: ...
    def __reversed__(self) -> Iterator[_Element]: ...
    def set(self, key: _TagName, value: _AnyStr) -> None: ...
    def append(self, element: _Element) -> None: ...
    def extend(self, elements: Iterable[_Element]) -> None: ...
    def clear(self, keep_tail: bool = ...) -> None: ...
    def insert(self, index: int, element: _Element) -> None: ...
    def remove(self, element: _Element) -> None: ...
    def index(
        self, child: _Element, start: int | None = ..., end: int | None = ...
    ) -> int: ...
    @overload
    def get(self, key: _TagName) -> str | None: ...
    @overload
    def get(self, key: _TagName, default: _T) -> str | _T: ...
    def keys(self) -> list[str]: ...
    def values(self) -> list[str]: ...
    def items(self) -> list[tuple[str, str]]: ...
    #
    # extra Element / ET methods
    #
    def addnext(self, element: _Element) -> None: ...
    def addprevious(self, element: _Element) -> None: ...
    def replace(self, old_element: _Element, new_element: _Element) -> None: ...
    def getparent(self) -> _Element | None: ...
    def getnext(self) -> _Element | None: ...
    def getprevious(self) -> _Element | None: ...
    def itersiblings(
        self,
        tag: _TagSelector | None = ...,
        *tags: _TagSelector,
        preceding: bool = ...,
    ) -> Iterator[_Element]: ...
    def iterancestors(
        self, tag: _TagSelector | None = ..., *tags: _TagSelector
    ) -> Iterator[_Element]: ...
    def iterdescendants(
        self, tag: _TagSelector | None = ..., *tags: _TagSelector
    ) -> Iterator[_Element]: ...
    def iterchildren(
        self,
        tag: _TagSelector | None = ...,
        *tags: _TagSelector,
        reversed: bool = ...,
    ) -> Iterator[_Element]: ...
    def getroottree(self) -> _ElementTree: ...
    def iter(
        self, tag: _TagSelector | None = ..., *tags: _TagSelector
    ) -> Iterator[_Element]: ...
    def itertext(
        self,
        tag: _TagSelector | None = ...,
        *tags: _TagSelector,
        with_tail: bool = ...,
    ) -> Iterator[str]: ...
    def makeelement(
        self,
        _tag: _TagName,
        # Final result is sort of like {**attrib, **_extra}
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg = ...,
        **_extra: _AnyStr,
    ) -> _Element: ...
    def find(
        self, path: _ElemPathArg, namespaces: _NSMapArg = ...
    ) -> _Element | None: ...
    # Original method has no star. If somebody only supplies
    # 'path' and 'default' argument as positional one, it
    # would be misinterpreted as namespaces argument in first
    # overload form. Add star here to guard against such situation.
    @overload
    def findtext(
        self,
        path: _ElemPathArg,
        *,
        namespaces: _NSMapArg = ...,
    ) -> str | None: ...
    @overload
    def findtext(
        self,
        path: _ElemPathArg,
        default: _T,
        namespaces: _NSMapArg = ...,
    ) -> str | _T: ...
    def findall(
        self, path: _ElemPathArg, namespaces: _NSMapArg = ...
    ) -> list[_Element]: ...
    def iterfind(
        self, path: _ElemPathArg, namespaces: _NSMapArg = ...
    ) -> Iterator[_Element]: ...
    def xpath(
        self,
        _path: _AnyStr,
        namespaces: _NonDefaultNSMapArg = ...,
        extensions: Any = ...,
        smart_strings: bool = ...,
        **_variables: _XPathVarArg,
    ) -> _XPathObject: ...
    def cssselect(
        self,
        expression: str,
        *,
        translator: _CSSTransArg = ...,
    ) -> list[_Element]: ...
    # Following methods marked as deprecated upstream
    def getchildren(self) -> list[_Element]: ...  # = list(self)
    def getiterator(
        self,
        tag: _TagSelector | None,
        *tags: _TagSelector,
    ) -> Iterator[_Element]: ...

class ElementBase(_Element): ...

class _ElementTree:
    parser = ...  # type: XMLParser
    docinfo = ...  # type: DocInfo
    def find(self, path: str, namespaces: _NSMapArg = ...) -> _Element | None: ...
    def findtext(
        self,
        path: str,
        default: str | None = ...,
        namespaces: _NSMapArg = ...,
    ) -> str | None: ...
    def findall(self, path: str, namespaces: _NSMapArg = ...) -> list[_Element]: ...
    def getpath(self, element: _Element) -> str: ...
    def getroot(self) -> _Element: ...
    def iter(
        self, tag: _TagSelector | None = ..., *tags: _TagSelector
    ) -> Iterable[_Element]: ...
    def write(
        self,
        file: _FileSource,
        encoding: _AnyStr = ...,
        method: _AnyStr = ...,
        pretty_print: bool = ...,
        xml_declaration: Any = ...,
        with_tail: Any = ...,
        standalone: bool = ...,
        compression: int = ...,
        exclusive: bool = ...,
        with_comments: bool = ...,
        inclusive_ns_prefixes: Iterable[_AnyStr] = ...,
    ) -> None: ...
    def write_c14n(
        self,
        file: _FileSource,
        with_comments: bool = ...,
        compression: int = ...,
        inclusive_ns_prefixes: Iterable[_AnyStr] = ...,
    ) -> None: ...
    def _setroot(self, root: _Element) -> None: ...
    def xinclude(self) -> None: ...
    def xpath(
        self,
        _path: _AnyStr,
        namespaces: _NonDefaultNSMapArg = ...,
        extensions: Any = ...,
        smart_strings: bool = ...,
        **_variables: _XPathVarArg,
    ) -> _XPathObject: ...
    def xslt(
        self,
        _xslt: XSLT,
        extensions: _ExtensionArg | None = ...,
        access_control: XSLTAccessControl | None = ...,
        **_variables: Any,
    ) -> _ElementTree: ...

class _Attrib:
    def __setitem__(self, key: _AnyStr, value: _AnyStr) -> None: ...
    def __delitem__(self, key: _AnyStr) -> None: ...
    def update(
        self,
        sequence_or_dict: _Attrib | Mapping[_AnyStr, _AnyStr] | Sequence[tuple[_AnyStr, _AnyStr]],
    ) -> None: ...
    def pop(self, key: _AnyStr, default: _AnyStr) -> _AnyStr: ...
    def clear(self) -> None: ...
    def __repr__(self) -> str: ...
    def __getitem__(self, key: _AnyStr) -> _AnyStr: ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def get(self, key: _AnyStr, default: _AnyStr = ...) -> _AnyStr | None: ...
    def keys(self) -> list[str]: ...
    def __iter__(self) -> Iterator[_AnyStr]: ...  # actually _AttribIterator
    def iterkeys(self) -> Iterator[_AnyStr]: ...
    def values(self) -> list[str]: ...
    def itervalues(self) -> Iterator[_AnyStr]: ...
    def items(self) -> list[tuple[_AnyStr, _AnyStr]]: ...
    def iteritems(self) -> Iterator[tuple[_AnyStr, _AnyStr]]: ...
    def has_key(self, key: _AnyStr) -> bool: ...
    def __contains__(self, key: _AnyStr) -> bool: ...
    def __richcmp__(self, other: _Attrib, op: int) -> bool: ...

# Qualified Name helper
class QName:
    @overload
    def __init__(
        self,
        text_or_uri_or_element: _TagName | _Element,
        tag: _TagName | None = ...,
    ) -> None: ...
    @overload
    def __init__(
        self,
        text_or_uri_or_element: None,
        tag: _TagName,
    ) -> None: ...
    @property
    def localname(self) -> str: ...
    @property
    def namespace(self) -> str | None: ...
    @property
    def text(self) -> str: ...
    # Emulate __richcmp__()
    def __ge__(self, other: _TagName) -> bool: ...
    def __gt__(self, other: _TagName) -> bool: ...
    def __le__(self, other: _TagName) -> bool: ...
    def __lt__(self, other: _TagName) -> bool: ...

class _XSLTResultTree(_ElementTree, SupportsBytes):
    def __bytes__(self) -> bytes: ...

class _XSLTQuotedStringParam: ...

# https://lxml.de/parsing.html#the-target-parser-interface
class ParserTarget(Protocol):
    def comment(self, text: _AnyStr) -> None: ...
    def close(self) -> Any: ...
    def data(self, data: _AnyStr) -> None: ...
    def end(self, tag: _AnyStr) -> None: ...
    def start(self, tag: _AnyStr, attrib: dict[_AnyStr, _AnyStr]) -> None: ...

class ElementClassLookup: ...

class FallbackElementClassLookup(ElementClassLookup):
    fallback: ElementClassLookup | None
    def __init__(self, fallback: ElementClassLookup | None = ...): ...
    def set_fallback(self, lookup: ElementClassLookup) -> None: ...

class CustomElementClassLookup(FallbackElementClassLookup):
    def lookup(
        self, type: str, doc: str, namespace: str, name: str
    ) -> type[ElementBase] | None: ...

class _BaseParser:
    def copy(self) -> _BaseParser: ...
    def makeelement(
        self,
        _tag: _TagName,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg = ...,
        **_extra: _AnyStr,
    ) -> _Element: ...
    def setElementClassLookup(
        self, lookup: ElementClassLookup | None = ...
    ) -> None: ...
    def set_element_class_lookup(
        self, lookup: ElementClassLookup | None = ...
    ) -> None: ...
    @property
    def error_log(self) -> _ErrorLog: ...

class _FeedParser(_BaseParser):
    def close(self) -> _Element: ...
    def feed(self, data: _AnyStr) -> None: ...

class XMLParser(_FeedParser):
    def __init__(
        self,
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
    resolvers = ...  # type: _ResolverRegistry

class HTMLParser(_FeedParser):
    def __init__(
        self,
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

class _ResolverRegistry:
    def add(self, resolver: Resolver) -> None: ...
    def remove(self, resolver: Resolver) -> None: ...

class Resolver:
    def resolve(self, system_url: str, public_id: str): ...
    def resolve_file(
        self, f: IO[Any], context: Any, *, base_url: _AnyStr | None, close: bool
    ): ...
    def resolve_string(
        self, string: _AnyStr, context: Any, *, base_url: _AnyStr | None
    ): ...

class XMLSchema(_Validator):
    def __init__(
        self,
        etree: _ElementOrTree = ...,
        file: _FileSource = ...,
    ) -> None: ...
    def __call__(self, etree: _ElementOrTree) -> bool: ...

class XSLTAccessControl: ...

class XSLT:
    def __init__(
        self,
        xslt_input: _ElementOrTree,
        extensions:_ExtensionArg | None = ...,
        regexp: bool = ...,
        access_control: XSLTAccessControl = ...,
    ) -> None: ...
    def __call__(
        self,
        _input: _ElementOrTree,
        profile_run: bool = ...,
        **kwargs: _AnyStr | _XSLTQuotedStringParam,
    ) -> _XSLTResultTree: ...
    @staticmethod
    def strparam(s: _AnyStr) -> _XSLTQuotedStringParam: ...
    @property
    def error_log(self) -> _ErrorLog: ...

#
# Element types and content node types
#

# __ContentOnlyElement is just a noop layer in class inheritance
# Maybe re-add if decided to override various _Element methods
# or simply discouple __ContentOnlyElement from _Element

# class __ContentOnlyElement(_Element): ...

class _Comment(_Element):
    # Signature of "tag" incompatible with supertype "_Element"
    @property  # type: ignore[misc]
    def tag(self) -> _ElemFactory[_Comment]: ...  # type: ignore[override]

class _ProcessingInstruction(_Element):
    @property  # type: ignore[misc]
    def tag(self) -> _ElemFactory[_ProcessingInstruction]: ...  # type: ignore[override]
    @property
    def target(self) -> str: ...
    @target.setter
    def target(self, value: _AnyStr) -> None: ...
    @overload
    def get(self, key: _AnyStr | QName) -> str | None: ...
    @overload
    def get(self, key: _AnyStr | QName, default: _T = ...) -> str | _T: ...
    @property
    def attrib(self) -> dict[str, str]: ...  # type: ignore[override]

class _Entity(_Element):
    @property  # type: ignore[misc]
    def tag(self) -> _ElemFactory[_Entity]: ...  # type: ignore[override]
    @property  # type: ignore[misc]
    def text(self) -> str: ...
    @property
    def name(self) -> str: ...
    @name.setter
    def name(self, value: _AnyStr) -> None: ...

class CDATA:
    def __init__(self, data: _AnyStr) -> None: ...

# Element factory functions
#

# Most arguments for factories functions are optional, so accurate
# typing can't be done. Opt for generic aliases instead.
_ElemFactory = Callable[..., _ET]

def Comment(text: _AnyStr | None = ...) -> _Comment: ...
def ProcessingInstruction(
    target: _AnyStr, text: _AnyStr | None = ...
) -> _ProcessingInstruction: ...

PI = ProcessingInstruction

def Entity(name: _AnyStr) -> _Entity: ...
def Element(  # Args identical to _Element.makeelement
    _tag: _TagName,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg = ...,
    **_extra: _AnyStr,
) -> _Element: ...
def SubElement(
    _parent: _Element,
    _tag: _TagName,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg = ...,
    **_extra: _AnyStr,
) -> _Element: ...
def ElementTree(
    element: _Element = ...,
    *,
    file: _FileSource = ...,
    parser: XMLParser = ...,
) -> _ElementTree: ...
def HTML(
    text: _AnyStr,
    parser: HTMLParser | None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _Element: ...
def XML(
    text: _AnyStr,
    parser: XMLParser | None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _Element: ...
def cleanup_namespaces(
    tree_or_element: _ElementOrTree,
    top_nsmap: _NSMapArg = ...,
    keep_ns_prefixes: Iterable[_AnyStr] | None = ...,
) -> None: ...
def parse(
    source: _FileSource, parser: XMLParser = ..., base_url: _AnyStr = ...
) -> _ElementTree: ...
def fromstring(
    text: _AnyStr, parser: XMLParser = ..., *, base_url: _AnyStr = ...
) -> _Element: ...
@overload
def tostring(
    element_or_tree: _ElementOrTree,
    encoding: type[str] | Literal["unicode"],
    method: str = ...,
    xml_declaration: bool = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool = ...,
    doctype: str = ...,
    exclusive: bool = ...,
    with_comments: bool = ...,
    inclusive_ns_prefixes: Any = ...,
) -> str: ...
@overload
def tostring(
    element_or_tree: _ElementOrTree,
    # Should be anything but "unicode", cannot be typed
    encoding: _KnownEncodings | None = ...,
    method: str = ...,
    xml_declaration: bool = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool = ...,
    doctype: str = ...,
    exclusive: bool = ...,
    with_comments: bool = ...,
    inclusive_ns_prefixes: Any = ...,
) -> bytes: ...
@overload
def tostring(
    element_or_tree: _ElementOrTree,
    encoding: str | type = ...,
    method: str = ...,
    xml_declaration: bool = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool = ...,
    doctype: str = ...,
    exclusive: bool = ...,
    with_comments: bool = ...,
    inclusive_ns_prefixes: Any = ...,
) -> _AnyStr: ...

class Error(Exception): ...

class LxmlError(Error):
    def __init__(
        self, message: Any, error_log: _BaseErrorLog | None = ...
    ) -> None: ...
    error_log: _BaseErrorLog = ...

class DocumentInvalid(LxmlError): ...
class LxmlSyntaxError(LxmlError, SyntaxError): ...

class ParseError(LxmlSyntaxError):
    position: tuple[int, int]

class XMLSyntaxError(ParseError): ...

class _Validator:
    def assert_(self, etree: _ElementOrTree) -> None: ...
    def assertValid(self, etree: _ElementOrTree) -> None: ...
    def validate(self, etree: _ElementOrTree) -> bool: ...
    @property
    def error_log(self) -> _ErrorLog: ...

class DTD(_Validator):
    def __init__(self, file: _FileSource = ..., *, external_id: Any = ...) -> None: ...
    def __call__(self, etree: _ElementOrTree) -> bool: ...

class TreeBuilder:
    def __init__(
        self,
        element_factory: _ElemFactory[_Element] | None = ...,
        parser: _BaseParser | None = ...,
        comment_factory: _ElemFactory[_Comment] | None = ...,
        pi_factory: _ElemFactory[_ProcessingInstruction] | None = ...,
        insert_comments: bool = ...,
        insert_pis: bool = ...,
    ) -> None: ...
    def close(self) -> _Element: ...
    def comment(self, text: _AnyStr) -> None: ...
    def data(self, data: _AnyStr) -> None: ...
    def end(self, tag: _AnyStr) -> None: ...
    def pi(self, target: _AnyStr, data: _AnyStr | None = ...) -> Any: ...
    def start(self, tag: _AnyStr, attrib: dict[_AnyStr, _AnyStr]) -> None: ...

def iselement(element: Any) -> TypeGuard[_Element]: ...
