from _typeshed import _T
from abc import ABCMeta, abstractmethod
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Literal,
    TypeVar,
    Union,
    final,
    overload,
)
from typing_extensions import LiteralString, Self, TypeAlias, TypeGuard

from .._types import (
    SupportsLaxedItems,
    _AnyStr,
    _AttrName,
    _AttrVal,
    _ElemPathArg,
    _FileReadSource,
    _FileWriteSource,
    _NonDefaultNSMapArg,
    _NSMapArg,
    _OutputMethodArg,
    _TagName,
    _XPathExtFuncArg,
    _XPathObject,
    _XPathVarArg,
    deprecated,
)
from ..cssselect import _CSSTransArg
from ._classlookup import (
    CommentBase as CommentBase,
    CustomElementClassLookup as CustomElementClassLookup,
    ElementBase as ElementBase,
    ElementClassLookup as ElementClassLookup,
    EntityBase as EntityBase,
    FallbackElementClassLookup as FallbackElementClassLookup,
    PIBase as PIBase,
)
from ._cleanup import (
    cleanup_namespaces as cleanup_namespaces,
    strip_attributes as strip_attributes,
    strip_elements as strip_elements,
    strip_tags as strip_tags,
)
from ._docloader import Resolver as Resolver
from ._dtd import (
    DTD as DTD,
    DTDError as DTDError,
    DTDParseError as DTDParseError,
    DTDValidateError as DTDValidateError,
)
from ._parser import (
    ETCompatXMLParser as ETCompatXMLParser,
    HTMLParser as HTMLParser,
    HTMLPullParser as HTMLPullParser,
    ParseError as ParseError,
    ParserError as ParserError,
    ParserTarget as ParserTarget,
    XMLParser as XMLParser,
    XMLPullParser as XMLPullParser,
    XMLSyntaxError as XMLSyntaxError,
    _DefEtreeParsers,
    get_default_parser as get_default_parser,
    set_default_parser as set_default_parser,
)
from ._relaxng import (
    RelaxNG as RelaxNG,
    RelaxNGError as RelaxNGError,
    RelaxNGParseError as RelaxNGParseError,
    RelaxNGValidateError as RelaxNGValidateError,
)
from ._serializer import (
    C14NWriterTarget as C14NWriterTarget,
    SerialisationError as SerialisationError,
    _AsyncIncrementalFileWriter as _AsyncIncrementalFileWriter,
    _IncrementalFileWriter as _IncrementalFileWriter,
    canonicalize as canonicalize,
    htmlfile as htmlfile,
    xmlfile as xmlfile,
)
from ._xmlerror import (
    ErrorDomains as ErrorDomains,
    ErrorLevels as ErrorLevels,
    ErrorTypes as ErrorTypes,
    PyErrorLog as PyErrorLog,
    RelaxNGErrorTypes as RelaxNGErrorTypes,
    _BaseErrorLog,
    _ListErrorLog,
    clear_error_log as clear_error_log,
    use_global_python_log as use_global_python_log,
)
from ._xmlid import (
    XMLDTDID as XMLDTDID,
    XMLID as XMLID,
    _IDDict as _IDDict,
    parseid as parseid,
)
from ._xmlschema import (
    XMLSchema as XMLSchema,
    XMLSchemaError as XMLSchemaError,
    XMLSchemaParseError as XMLSchemaParseError,
    XMLSchemaValidateError as XMLSchemaValidateError,
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
from ._xslt import (
    LIBXSLT_COMPILED_VERSION as LIBXSLT_COMPILED_VERSION,
    LIBXSLT_VERSION as LIBXSLT_VERSION,
    XSLT as XSLT,
    XSLTAccessControl as XSLTAccessControl,
    XSLTApplyError as XSLTApplyError,
    XSLTError as XSLTError,
    XSLTExtensionError as XSLTExtensionError,
    XSLTParseError as XSLTParseError,
    XSLTSaveError as XSLTSaveError,
    _XSLTResultTree as _XSLTResultTree,
)

#
# Basic variables and constants
#

# It is unknown if mypy will ever implemenet PEP 696; therefore,
# pyright will enjoy shorthand while mypy doesn't,
# while more specialization of classes are to be implemeneted,
# such as _Attrib -> _Attrib[_Element]
#
# XXX Here is the trick:
# 1. mypy claims it doesn't understand MYPY variable, but actually
#    it does, and skips over to else block
# 2. pyright truly does not understand MYPY variable. Under default
#    behavior, it sort of merges definition of both blocks. With
#    compatible enough definition, it doesn't modify the desired result.
# 3. Replace MYPY with any name, and mypy will break.
#
# While pyright supports defining constants in config, it is not
# reasonable to ask all pyright users to modify their own config.
#
if not MYPY:  # type: ignore
    _ET = TypeVar("_ET", bound=_Element, default=_Element)
    _ET_co = TypeVar("_ET_co", bound=_Element, default=_Element, covariant=True)
else:
    _ET = TypeVar("_ET", bound=_Element)  # pyright: ignore[reportConstantRedefinition]
    _ET_co = TypeVar("_ET_co", bound=_Element, covariant=True)

# Note that _TagSelector filters element type not by classes,
# but checks for element _factory functions_ instead
# (that is Element(), Comment() and ProcessingInstruction()).
_TagSelector = Union[_TagName, _ElemFactory[_Element]]
# For tostring() encoding. In theory it should be any encoding name
# except "unicode", but is not representable in current typing system.
# Settle for commonly seen encodings in XML.
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
_ElementOrTree: TypeAlias = _Element | _ElementTree[_Element]

DEBUG: int
LIBXML_VERSION: tuple[int, int, int]
LIBXML_COMPILED_VERSION: tuple[int, int, int]
LXML_VERSION: tuple[int, int, int, int]
__version__: LiteralString

@final
class _ElementUnicodeResult(str, Generic[_ET]):
    """Smart string is a private str subclass documented in
    [return types](https://lxml.de/xpathxslt.html#xpath-return-values)
    of XPath evaluation result.

    Please [visit wiki page](https://github.com/abelcheung/types-lxml/wiki/Smart-string-usage)
    on description and how to use it in you code.
    """

    @property
    def is_attribute(self) -> bool: ...
    @property
    def is_tail(self) -> bool: ...
    @property
    def is_text(self) -> bool: ...
    @property
    def attrname(self) -> str | None: ...
    def getparent(self: _ElementUnicodeResult[_ET]) -> _ET | None: ...

class DocInfo:
    @property
    def root_name(self) -> str | None: ...
    @property
    def public_id(self) -> str | None: ...
    @public_id.setter
    def public_id(self, __v: _AnyStr | None) -> None: ...
    @property
    def system_url(self) -> str | None: ...
    @system_url.setter
    def system_url(self, __v: _AnyStr | None) -> None: ...
    @property
    def xml_version(self) -> str | None: ...
    @property
    def encoding(self) -> str | None: ...
    @property
    def standalone(self) -> bool | None: ...
    @property
    def URL(self) -> str | None: ...
    @URL.setter
    def URL(self, __v: _AnyStr | None) -> None: ...
    @property
    def doctype(self) -> str: ...
    @property
    def internalDTD(self) -> DTD | None: ...
    @property
    def externalDTD(self) -> DTD | None: ...
    def clear(self) -> None: ...

# The base of _Element is *almost* an amalgam of MutableSequence[_Element]
# plus mixin methods for _Attrib.
# Extra methods follow the order of _Element source approximately
class _Element:
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
    # but 'sourceline' and 'base' provide __set__ method.
    # However, we only implement rw property for base, as
    # modifying sourceline is meaningless.
    #
    @property
    def prefix(self) -> str | None: ...
    @property
    def sourceline(self) -> int | None: ...
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
    def __getitem__(self, __x: int) -> Self: ...
    @overload
    def __getitem__(self, __x: slice) -> list[Self]: ...
    @overload
    def __setitem__(self, __x: int, __v: Self) -> None: ...
    @overload
    def __setitem__(self, __x: slice, __v: Iterable[Self]) -> None: ...
    def __contains__(self, __o: object) -> bool: ...
    def __len__(self) -> int: ...
    # There are a hoard of element iterators used in lxml, but
    # they only differ in implementation detail and don't affect typing.
    def __iter__(self) -> Iterator[Self]: ...
    def __reversed__(self) -> Iterator[Self]: ...
    def set(self, key: _AttrName, value: _AttrVal) -> None: ...
    def append(self, element: Self) -> None: ...
    def extend(self, elements: Iterable[Self]) -> None: ...
    def clear(self, keep_tail: bool = ...) -> None: ...
    def insert(self, index: int, element: Self) -> None: ...
    def remove(self, element: Self) -> None: ...
    def index(
        self, child: Self, start: int | None = ..., end: int | None = ...
    ) -> int: ...
    @overload
    def get(self, key: _AttrName) -> str | None: ...
    @overload
    def get(self, key: _AttrName, default: _T) -> str | _T: ...
    def keys(self) -> list[str]: ...
    def values(self) -> list[str]: ...
    def items(self) -> list[tuple[str, str]]: ...
    #
    # extra Element / ET methods
    #
    def addnext(self, element: Self) -> None: ...
    def addprevious(self, element: Self) -> None: ...
    def replace(self, old_element: Self, new_element: Self) -> None: ...
    def getparent(self) -> Self | None: ...
    def getnext(self) -> Self | None: ...
    def getprevious(self) -> Self | None: ...
    def getroottree(self) -> _ElementTree[Self]: ...
    @overload
    def itersiblings(
        self, *, tag: _TagSelector | None = ..., preceding: bool = ...
    ) -> Iterator[Self]: ...
    @overload
    def itersiblings(  # pyright: ignore[reportOverlappingOverload]
        self, *tags: _TagSelector, preceding: bool = ...
    ) -> Iterator[Self]: ...
    @overload
    def iterancestors(self, *, tag: _TagSelector | None = ...) -> Iterator[Self]: ...
    @overload
    def iterancestors(  # pyright: ignore[reportOverlappingOverload]
        self, *tags: _TagSelector
    ) -> Iterator[Self]: ...
    @overload
    def iterdescendants(self, *, tag: _TagSelector | None = ...) -> Iterator[Self]: ...
    @overload
    def iterdescendants(  # pyright: ignore[reportOverlappingOverload]
        self, *tags: _TagSelector
    ) -> Iterator[Self]: ...
    @overload
    def iterchildren(
        self, *, tag: _TagSelector | None = ..., reversed: bool = ...
    ) -> Iterator[Self]: ...
    @overload
    def iterchildren(  # pyright: ignore[reportOverlappingOverload]
        self, *tags: _TagSelector, reversed: bool = ...
    ) -> Iterator[Self]: ...
    @overload
    def iter(self, *tags: _TagSelector) -> Iterator[Self]: ...
    @overload
    def iter(self, *, tag: _TagSelector | None = ...) -> Iterator[Self]: ...
    @overload
    def itertext(
        self, *, tag: _TagSelector | None = ..., with_tail: bool = ...
    ) -> Iterator[str]: ...
    @overload
    def itertext(  # pyright: ignore[reportOverlappingOverload]
        self, *tags: _TagSelector, with_tail: bool = ...
    ) -> Iterator[str]: ...
    def makeelement(
        self,
        _tag: _TagName,
        /,
        # Final result is sort of like {**attrib, **_extra}
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> Self: ...
    def find(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> Self | None: ...
    # Original method has no star. If somebody only supplies
    # 'path' and 'default' argument as positional one, it
    # would be misinterpreted as namespaces argument in first
    # overload form. Add star here to guard against such situation.
    @overload
    def findtext(
        self,
        path: _ElemPathArg,
        *,
        namespaces: _NSMapArg | None = ...,
    ) -> str | None: ...
    @overload
    def findtext(
        self,
        path: _ElemPathArg,
        default: _T,
        namespaces: _NSMapArg | None = ...,
    ) -> str | _T: ...
    def findall(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> list[Self]: ...
    def iterfind(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> Iterator[Self]: ...
    def xpath(
        self,
        _path: _AnyStr,
        /,
        *,
        namespaces: _NonDefaultNSMapArg | None = ...,
        extensions: _XPathExtFuncArg | None = ...,
        smart_strings: bool = ...,
        **_variables: _XPathVarArg,
    ) -> _XPathObject: ...
    def cssselect(
        self,
        expr: str,
        *,
        translator: _CSSTransArg = ...,
    ) -> list[Self]: ...
    @deprecated("Since v2.0 (2008); use list(element) or iterate over element")
    def getchildren(self) -> list[Self]: ...
    # Should have been overloaded for accuracy, but we can turn a blind eye
    # for something that is marked deprecated for 15 years
    @deprecated("Since v2.0 (2008); renamed to .iter()")
    def getiterator(
        self, tag: _TagSelector | None = ..., *tags: _TagSelector
    ) -> Iterator[Self]: ...

# ET class notation is specialized, indicating the type of element
# it is holding (e.g. XML element, HTML element or Objectified
# Element).
# Although it is also possible to be an empty tree containing no
# element, the absolute majority of lxml API will fail to work.
# It is considered harmful to support such corner case, which
# adds much complexity without any benefit.
class _ElementTree(Generic[_ET_co]):
    @property
    def parser(self) -> _DefEtreeParsers[_ET_co] | None: ...
    @property
    def docinfo(self) -> DocInfo: ...
    def parse(
        self,
        source: _FileReadSource,
        parser: _DefEtreeParsers[_ET_co] | None = ...,
        *,
        base_url: _AnyStr | None = ...,
    ) -> None: ...
    # Changes root node; in terms of typing, this means changing
    # specialization of ElementTree. This is not expressible in
    # current typing system.
    def _setroot(self, root: _Element) -> None: ...
    def getroot(self) -> _ET_co: ...
    # Special notes for write()
    # For write(), there are quite many combination of keyword
    # arguments that have no effect. But it's a bit too complex
    # to handle in stub, so keep it simple and only divide
    # keyword usage by writing method as documented.
    # For example, following combination raises exception in lxml:
    #     - file argument is file name or path like, and
    #     - method is 'c14n2', and
    #     - no compression
    #
    @overload  # deprecated usage of docstring param
    @deprecated('Since v3.8.0; use "doctype" parameter instead')
    def write(
        self,
        file: Any,
        *,
        docstring: str,
        __kw: Any,
    ) -> None: ...
    @overload  # method=c14n
    def write(
        self,
        file: _FileWriteSource,
        *,
        method: Literal["c14n"],
        exclusive: bool = ...,
        with_comments: bool = ...,
        compression: int | None = ...,
        inclusive_ns_prefixes: Iterable[_AnyStr] | None = ...,
    ) -> None: ...
    @overload  # method=c14n2
    def write(
        self,
        file: _FileWriteSource,
        *,
        method: Literal["c14n2"],
        with_comments: bool = ...,
        compression: int | None = ...,
        strip_text: bool = ...,
    ) -> None: ...
    @overload  # other write methods
    def write(
        self,
        file: _FileWriteSource,
        *,
        encoding: str | None = ...,  # unicode not allowed
        method: _OutputMethodArg = ...,
        pretty_print: bool = ...,
        xml_declaration: bool | None = ...,
        with_tail: bool = ...,
        standalone: bool | None = ...,
        doctype: str | None = ...,
        compression: int | None = ...,
    ) -> None: ...
    def getpath(self: _ElementTree[_ET], element: _ET) -> str: ...
    def getelementpath(self: _ElementTree[_ET], element: _ET) -> str: ...
    @overload
    def iter(self, *tags: _TagSelector) -> Iterator[_ET_co]: ...
    @overload
    def iter(self, *, tag: _TagSelector | None = ...) -> Iterator[_ET_co]: ...
    #
    # ElementPath methods calls the same method on root node,
    # so signature should be the same as _Element ones
    #
    def find(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> _ET_co | None: ...
    @overload
    def findtext(
        self,
        path: _ElemPathArg,
        *,
        namespaces: _NSMapArg | None = ...,
    ) -> str | None: ...
    @overload
    def findtext(
        self,
        path: _ElemPathArg,
        default: _T,
        namespaces: _NSMapArg | None = ...,
    ) -> str | _T: ...
    def findall(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> list[_ET_co]: ...
    def iterfind(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> Iterator[_ET_co]: ...
    def xpath(
        self,
        _path: _AnyStr,
        /,
        *,
        namespaces: _NonDefaultNSMapArg | None = ...,
        extensions: _XPathExtFuncArg | None = ...,
        smart_strings: bool = ...,
        **_variables: _XPathVarArg,
    ) -> _XPathObject: ...
    def xslt(
        self,
        _xslt: _ElementOrTree,
        /,
        extensions: Any = ...,  # TODO XSLT extension type
        access_control: XSLTAccessControl | None = ...,
        **_kw: Any,
    ) -> _ElementTree[_Element]: ...
    def relaxng(self, relaxng: _ElementOrTree) -> bool: ...
    def xmlschema(self, xmlschema: _ElementOrTree) -> bool: ...
    def xinclude(self) -> None: ...
    # Should have been overloaded for accuracy, but we can turn a blind eye
    # for something that is marked deprecated for 15 years
    @deprecated("Since v2.0 (2008); renamed to .iter()")
    def getiterator(
        self, tag: _TagSelector | None = ..., *tags: _TagSelector
    ) -> Iterator[_ET_co]: ...
    @deprecated('Since v4.4; use .write() with method="c14n" argument')
    def write_c14n(
        self,
        file: _FileWriteSource,
        *,
        exclusive: bool = ...,
        with_comments: bool = ...,
        compression: int | None = ...,
        inclusive_ns_prefixes: Iterable[_AnyStr] | None = ...,
    ) -> None: ...

# Behaves like MutableMapping but deviates a lot in details
class _Attrib:
    @property
    def _element(self) -> _Element: ...
    def __setitem__(self, __k: _AttrName, __v: _AttrVal) -> None: ...
    def __delitem__(self, __k: _AttrName) -> None: ...
    # explicitly checks for dict and _Attrib
    def update(
        self,
        sequence_or_dict: _Attrib
        | dict[Any, Any]  # Compromise with MutableMapping key/val invariance
        | Iterable[tuple[_AttrName, _AttrVal]],
    ) -> None: ...
    # Signature is pop(self, key, *default), yet followed by runtime
    # check and raise exception if multiple default argument is supplied
    # Note that get() is forgiving with non-existent key yet pop() isn't.
    @overload
    def pop(self, key: _AttrName) -> str: ...
    @overload
    def pop(self, key: _AttrName, default: _T) -> str | _T: ...
    def clear(self) -> None: ...
    def __getitem__(self, __k: _AttrName) -> str: ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    @overload
    def get(self, key: _AttrName) -> str | None: ...
    @overload
    def get(self, key: _AttrName, default: _T) -> str | _T: ...
    def keys(self) -> list[str]: ...
    def __iter__(self) -> Iterator[str]: ...
    def iterkeys(self) -> Iterator[str]: ...
    def values(self) -> list[str]: ...
    def itervalues(self) -> Iterator[str]: ...
    def items(self) -> list[tuple[str, str]]: ...
    def iteritems(self) -> Iterator[tuple[str, str]]: ...
    def has_key(self, key: _AttrName) -> bool: ...
    def __contains__(self, __o: object) -> bool: ...
    # richcmp dropped, mapping has no concept of inequality comparison

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

#
# Element types and content node types
#

# NOTE: Follow lxml source code -- shove all dirt under these classes
# NOTE: It is decided to not decouple other content only elements
# from _Element, even though their interfaces are vastly different
# from _Element. The notion of or'ing different kind of elements
# throughout all element methods would cause great inconvenience
# for me and all users alike -- _AnyHtmlElement turns out to be a
# failure.
# We opt for convenience and ease of use in the future.
class __ContentOnlyElement(_Element):
    #
    # Useful properties
    #
    @property  # type: ignore[misc]
    def tag(self) -> _ElemFactory[Self]: ...  # type: ignore[override]
    @property
    def text(self) -> str | None: ...
    @text.setter
    def text(self, value: _AnyStr | None) -> None: ...
    #
    # Explicitly dummified properties and methods
    #
    # def set(self, key: Any, value: Any) -> NoReturn: ...
    # def append(self, element: Any) -> NoReturn: ...
    # def insert(self, index: Any, element: Any) -> NoReturn: ...
    # def __setitem__(self, __x: Any, __v: Any) -> NoReturn: ...
    # @property
    # def attrib(self) -> Incomplete: ...  # type: ignore[override]
    # The intention is to forbid elem.__getitem__, allowing slice
    # doesn't make sense
    # def __getitem__(self, __x: Any) -> NoReturn: ...  # type: ignore[override]
    # def get(self, key: Any, default: Any = ...) -> None: ...  # type: ignore[override]
    # def keys(self) -> list[Incomplete]: ...
    # def values(self) -> list[Incomplete]: ...
    # def items(self) -> list[Incomplete]: ...
    #
    # FIXME There are many, many more methods that don't work for
    # content only elements (e.g. most ElementTree / ElementPath ones)
    # But adding them to annotation would mean HUGE amount of manual
    # type ignoring, not to mention that none of those are handled in
    # source code -- users are left to bump into wall themselves.
    # Let's not care about the half-assed overriding for now, and just
    # concentrate on useful properties.
    #

class _Comment(__ContentOnlyElement): ...

# signature of .get() for _PI and _Element are the same
class _ProcessingInstruction(__ContentOnlyElement):
    @property
    def target(self) -> str: ...
    @target.setter
    def target(self, value: _AnyStr) -> None: ...
    @property
    def attrib(self) -> dict[str, str]: ...  # type: ignore[override]

class _Entity(__ContentOnlyElement):
    @property  # type: ignore[misc]
    def text(self) -> str: ...  # type: ignore[override]
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
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **_extra: _AnyStr,
) -> _Element: ...
def SubElement(
    _parent: _ET,
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **_extra: _AnyStr,
) -> _ET: ...
@overload  # from element, parser ignored
def ElementTree(element: _ET) -> _ElementTree[_ET]: ...
@overload  # from file source, custom parser
def ElementTree(
    element: None = ...,
    *,
    file: _FileReadSource,
    parser: _DefEtreeParsers[_ET_co],
) -> _ElementTree[_ET_co]: ...
@overload  # from file source, default parser
def ElementTree(
    element: None = ...,
    *,
    file: _FileReadSource,
    parser: None = ...,
) -> _ElementTree[_Element]: ...

# FIXME Missing case: element = file = None,
# parser must use custom target that generates something
# even when there is no input data. Low priority.

@overload
def HTML(
    text: _AnyStr,
    parser: HTMLParser[_ET_co],
    *,
    base_url: _AnyStr | None = ...,
) -> _ET_co: ...
@overload
def HTML(
    text: _AnyStr,
    parser: None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _Element: ...
@overload
def XML(
    text: _AnyStr,
    parser: XMLParser[_ET_co],
    *,
    base_url: _AnyStr | None = ...,
) -> _ET_co: ...
@overload
def XML(
    text: _AnyStr,
    parser: None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _Element: ...
@overload
def parse(
    source: _FileReadSource,
    parser: _DefEtreeParsers[_ET_co],
    *,
    base_url: _AnyStr | None = ...,
) -> _ElementTree[_ET_co]: ...
@overload
def parse(
    source: _FileReadSource,
    parser: None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _ElementTree[_Element]: ...
@overload
def fromstring(
    text: _AnyStr,
    parser: _DefEtreeParsers[_ET_co],
    *,
    base_url: _AnyStr | None = ...,
) -> _ET_co: ...
@overload
def fromstring(
    text: _AnyStr,
    parser: None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> _Element: ...
@overload
def fromstringlist(
    strings: Iterable[_AnyStr],
    parser: _DefEtreeParsers[_ET_co],
) -> _ET_co: ...
@overload
def fromstringlist(
    strings: Iterable[_AnyStr],
    parser: None = ...,
) -> _Element: ...
@overload  # Native str, no XML declaration
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    encoding: type[str] | Literal["unicode"],
    method: _OutputMethodArg = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool | None = ...,
    doctype: str | None = ...,
) -> str: ...
@overload  # byte str, no XML declaration
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    encoding: _KnownEncodings | None = ...,
    method: _OutputMethodArg = ...,
    xml_declaration: bool | None = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool | None = ...,
    doctype: str | None = ...,
) -> bytes: ...

# Under XML Canonicalization (C14N) mode, most arguments are ignored,
# some arguments would even raise exception outright if specified.
@overload  # method="c14n"
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n"],
    exclusive: bool = ...,
    inclusive_ns_prefixes: Iterable[_AnyStr] | None = ...,
    with_comments: bool = ...,
) -> bytes: ...
@overload  # method="c14n2"
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n2"],
    with_comments: bool = ...,
    strip_text: bool = ...,
) -> bytes: ...
@overload  # catch all
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    encoding: str | type[str] = ...,
    method: str = ...,
    xml_declaration: bool | None = ...,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    standalone: bool | None = ...,
    doctype: str | None = ...,
    exclusive: bool = ...,
    with_comments: bool = ...,
    inclusive_ns_prefixes: Any = ...,
) -> _AnyStr: ...
def indent(
    element_or_tree: _ElementOrTree,
    space: str = ...,
    *,
    level: int = ...,
) -> None: ...
@deprecated(
    "For ElementTree 1.3 compat only; result is tostring() output wrapped inside a list"
)
def tostringlist(
    element_or_tree: _ElementOrTree, *args: Any, **__kw: Any
) -> list[str]: ...
@deprecated('Since v3.3.2; use tostring() with encoding="unicode" argument')
def tounicode(
    element_or_tree: _ElementOrTree,
    *,
    method: str,
    pretty_print: bool = ...,
    with_tail: bool = ...,
    doctype: str | None = ...,
) -> None: ...

class Error(Exception): ...

class LxmlError(Error):
    def __init__(
        self, message: object, error_log: _BaseErrorLog | None = ...
    ) -> None: ...
    # Even when LxmlError is initiated with PyErrorLog, it fools
    # error_log property by creating a dummy _ListErrorLog object
    error_log: _ListErrorLog

class DocumentInvalid(LxmlError): ...
class LxmlSyntaxError(LxmlError, SyntaxError): ...

class _Validator(metaclass=ABCMeta):
    def assert_(self, etree: _ElementOrTree) -> None: ...
    def assertValid(self, etree: _ElementOrTree) -> None: ...
    def validate(self, etree: _ElementOrTree) -> bool: ...
    @property
    def error_log(self) -> _ListErrorLog: ...
    # all methods implicitly require a concrete __call__()
    # implementation in subclasses in order to be usable
    @abstractmethod
    def __call__(self, etree: _ElementOrTree) -> bool: ...

class TreeBuilder(ParserTarget[_Element]):
    def __init__(
        self,
        *,
        element_factory: _ElemFactory[_Element] | None = ...,
        parser: _DefEtreeParsers[_Element] | None = ...,
        comment_factory: _ElemFactory[_Comment] | None = ...,
        pi_factory: _ElemFactory[_ProcessingInstruction] | None = ...,
        insert_comments: bool = ...,
        insert_pis: bool = ...,
    ) -> None: ...
    def close(self) -> _Element: ...

def iselement(element: object) -> TypeGuard[_Element]: ...

# Debugging only
def dump(
    elem: _Element, *, pretty_print: bool = ..., with_tail: bool = ...
) -> None: ...
