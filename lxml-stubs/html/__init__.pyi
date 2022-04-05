#
# Making some compromise for HTML, in that iteration of subelements
# and methods would produce HTML elements instead of the base
# etree._Element. It is technically "correct" that those operations
# may not produce HTML elements when XML nodes are manually inserted
# into documents or fragments. However, arguably 99.9% of user cases
# don't involve such manually constructed hybrid element trees.
# Making it absolutely "correct" harms most users by losing context.
#

from typing import (
    Any,
    Callable,
    Collection,
    Iterable,
    Iterator,
    Literal,
    MutableMapping,
    MutableSet,
    NoReturn,
    TypeVar,
    overload,
)

from typing_extensions import TypeAlias

from .. import etree
from .._types import (
    SupportsLaxedItems,
    _AnyStr,
    _AttrName,
    _AttrVal,
    _ElemClsLookupArg,
    _ElemPathArg,
    _FileReadSource,
    _NSMapArg,
    _OutputMethodArg,
    _TagName,
)
from ..cssselect import _CSSTransArg
from ..etree._xmlschema import XMLSchema

_T = TypeVar("_T")

_HANDLE_FAILURES = Literal["ignore", "discard"]
_FormValues = list[tuple[str, str]]
_HtmlElemOrTree: TypeAlias = HtmlElement | etree._ElementTree[HtmlElement]

XHTML_NAMESPACE: str

class Classes(MutableSet[str]):
    # Theorectically, the internal structure need not be _Attrib,
    # any Protocol that conforms would suffice. (Needs get(),
    # __setitem__ and __delitem__)
    # But practically, if other python generic data type were used,
    # there is no way to get a proper HTML element back.
    _attributes: etree._Attrib
    def __init__(
        self,
        attributes: etree._Attrib,
    ) -> None: ...
    def __contains__(self, __o: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def add(self, value: str) -> None: ...
    def discard(self, value: str) -> None: ...
    def update(self, values: Iterable[str]) -> None: ...
    def toggle(self, value: str) -> bool: ...

class HtmlMixin:
    classes: Classes
    label: LabelElement | None
    @property
    def base_url(self) -> str | None: ...
    @property
    def forms(self) -> list[FormElement]: ...
    @property
    def body(self) -> HtmlElement: ...
    @property
    def head(self) -> HtmlElement: ...
    # Differs from _Element.set(): value has default, can accept None
    # (boolean attribute without value)
    def set(self, key: _AttrName, value: _AttrVal | None = ...) -> None: ...
    def drop_tree(self) -> None: ...
    def drop_tag(self) -> None: ...
    def find_rel_links(
        self,
        # Can be bytes, but guaranteed to not match any element on py3
        rel: str,
    ) -> list[HtmlElement]: ...
    def find_class(
        self,
        class_name: _AnyStr,  # needs check
    ) -> list[HtmlElement]: ...
    # Signature is actually (self, id, *default), but situation is
    # similar to _Attrib.pop(); all defaults except the first
    # is discarded. No point to honor such useless signature.
    @overload
    def get_element_by_id(self, id: _AnyStr) -> HtmlElement: ...
    @overload
    def get_element_by_id(self, id: _AnyStr, default: _T) -> HtmlElement | _T: ...
    # text_content() returns smart string by default. It is suggested
    # to use etree.SmartStr (stub-only class) to do type narrowing.
    def text_content(self) -> str: ...
    # Note the difference of return type from _Element.cssselect
    # as well as lack of star
    def cssselect(
        self, expr: str, translator: _CSSTransArg = ...
    ) -> list[HtmlElement]: ...
    #
    # Link functions
    #
    def make_links_absolute(
        self,
        base_url: str | None = ...,  # not bytes
        resolve_base_href: bool = ...,
        handle_failures: _HANDLE_FAILURES | None = ...,
    ) -> None: ...
    def resolve_base_href(
        self,
        handle_failures: _HANDLE_FAILURES | None = ...,
    ) -> None: ...
    # (element, attribute, link, pos)
    def iterlinks(self) -> Iterator[tuple[HtmlElement, str | None, str, int]]: ...
    def rewrite_links(
        self,
        link_repl_func: Callable[[str], str | None],
        resolve_base_href: bool = ...,
        base_href: str | None = ...,
    ) -> None: ...

# These are HtmlMixin methods converted to standard functions,
# with element or HTML string as first argument followed by all
# pre-existing args. Quoting from source:
#
#   ... the function takes either an element or an HTML string.  It
#   returns whatever the function normally returns, or if the function
#   works in-place (and so returns None) it returns a serialized form
#   of the resulting document.
#
# Special Notes:
# 1. These funcs operate on attributes that only make sense on
#    normal HtmlElements; lxml raises exception otherwise.
# 2. Although extra 'copy' argument is available, it is intended
#    only for internal use by each function, not something to be
#    arbitrarily changed by users.

_DT = TypeVar("_DT", str, bytes, HtmlElement, etree._ElementTree)

def find_rel_links(
    doc: _DT,
    rel: str,
) -> list[HtmlElement]: ...
def find_class(
    doc: _DT,
    class_name: _AnyStr,
) -> list[HtmlElement]: ...
def make_links_absolute(
    doc: _DT,
    base_url: str | None = ...,
    resolve_base_href: bool = ...,
    handle_failures: _HANDLE_FAILURES | None = ...,
) -> _DT: ...
def resolve_base_href(
    doc: _DT,
    handle_failures: _HANDLE_FAILURES | None = ...,
) -> _DT: ...
def iterlinks(
    doc: _DT,
) -> Iterator[tuple[HtmlElement, str | None, str, int]]: ...
def rewrite_links(
    doc: _DT,
    link_repl_func: Callable[[str], str | None],
    resolve_base_href: bool = ...,
    base_href: str | None = ...,
) -> _DT: ...

#
# Types of different HTML elements
#

# 1. Type checkers always compare methods from all subclasses,
# the inheritance order doesn't stop checkers from complaining.
# Both mypy and pyright consider the overriding of cssselect() and set()
# too distorted and complain very loudly in multiple places,
# including _all_ elements that inherit from HtmlElement.
#
# 2. Many methods overrided to return HTML elements.
# It is not a simple return type replacement though, since
# XML and HTML elements have different inheritance structure (!),
# and some operations only make sense on subset of HTML elements.
# Methods (beyond basic accessor) not overrided:
# addnext, addprevious, replace, getroottree, itertext, findtext, xpath
class HtmlElement(HtmlMixin, etree.ElementBase):  # type: ignore[misc]
    @overload  # type: ignore[override]
    def __getitem__(self, x: int) -> _AnyHtmlElement: ...
    @overload
    def __getitem__(self, x: slice) -> list[_AnyHtmlElement]: ...
    def __iter__(self) -> Iterator[_AnyHtmlElement]: ...
    def __reversed__(self) -> Iterator[_AnyHtmlElement]: ...
    def getparent(self) -> _AnyHtmlElement | None: ...
    def getnext(self) -> _AnyHtmlElement | None: ...
    def getprevious(self) -> _AnyHtmlElement | None: ...
    def itersiblings(
        self,
        tag: etree._TagSelector | None = ...,
        *tags: etree._TagSelector,
        preceding: bool = ...,
    ) -> Iterator[_AnyHtmlElement]: ...
    def iterancestors(
        self,
        tag: etree._TagSelector | None = ...,
        *tags: etree._TagSelector,
    ) -> Iterator[_AnyHtmlElement]: ...
    def iterdescendants(
        self,
        tag: etree._TagSelector | None = ...,
        *tags: etree._TagSelector,
    ) -> Iterator[_AnyHtmlElement]: ...
    def iterchildren(
        self,
        tag: etree._TagSelector | None = ...,
        *tags: etree._TagSelector,
        reversed: bool = ...,
    ) -> Iterator[_AnyHtmlElement]: ...
    def iter(
        self,
        tag: etree._TagSelector | None = ...,
        *tags: etree._TagSelector,
    ) -> Iterator[_AnyHtmlElement]: ...
    def makeelement(
        self,
        _tag: _TagName,
        /,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> HtmlElement: ...
    def getroottree(self) -> etree._ElementTree[HtmlElement]: ...  # type: ignore[override]
    #
    # ElementPath API in lxml doesn't include Comment and such in result
    # https://bugs.launchpad.net/lxml/+bug/1921675
    #
    def find(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> HtmlElement | None: ...
    def findall(  # type: ignore[override]
        self,
        path: _ElemPathArg,
        namespaces: _NSMapArg | None = ...,
    ) -> list[HtmlElement]: ...
    def iterfind(
        self,
        path: _ElemPathArg,
        namespaces: _NSMapArg | None = ...,
    ) -> Iterator[HtmlElement]: ...

class HtmlComment(HtmlMixin, etree.CommentBase):  # type: ignore[misc]
    def getroottree(self) -> etree._ElementTree[HtmlElement]: ...  # type: ignore[override]

class HtmlEntity(HtmlMixin, etree.EntityBase):  # type: ignore[misc]
    def getroottree(self) -> etree._ElementTree[HtmlElement]: ...  # type: ignore[override]

class HtmlProcessingInstruction(HtmlMixin, etree.PIBase):  # type: ignore[misc]
    def getroottree(self) -> etree._ElementTree[HtmlElement]: ...  # type: ignore[override]

_AnyHtmlElement = HtmlComment | HtmlElement | HtmlEntity | HtmlProcessingInstruction

_AnyInputElement = InputElement | SelectElement | TextareaElement

# Only useful when somebody wants to create custom markup language
# parser (or extension based on HTMLParser)
class HtmlElementClassLookup(etree.CustomElementClassLookup):
    def __init__(
        self,
        # Should have been something like Mapping[str, type[HtmlElement]],
        # but unfortunately classes mapping is required to be mutable
        classes: MutableMapping[str, Any] | None = ...,
        # docstring says mixins is mapping, but implementation says otherwise
        mixins: Iterable[tuple[str, type[HtmlElement]]] = ...,
    ) -> None: ...
    def lookup(
        self,
        node_type: _ElemClsLookupArg | None,
        document: Any,  # argument unused
        namespace: str | None,
        name: str | None,
    ) -> type[_AnyHtmlElement] | None: ...

#
# parsing functions
#

# Calls etree.fromstring(html, parser, **kw) which has signature
# fromstring(text, parser, *, base_url)
def document_fromstring(
    html: _AnyStr,
    parser: HTMLParser | XHTMLParser | None = ...,
    ensure_head_body: bool = ...,
    *,
    base_url: str | None = ...,
) -> HtmlElement: ...
def fragments_fromstring(
    html: _AnyStr,
    no_leading_text: bool = ...,
    base_url: str | None = ...,
    parser: HTMLParser | XHTMLParser | None = ...,
    **kw: Any,  # seems unused
) -> list[_AnyHtmlElement]: ...
def fragment_fromstring(
    html: _AnyStr,
    create_parent: bool = ...,
    base_url: str | None = ...,
    parser: HTMLParser | XHTMLParser | None = ...,
    **kw: Any,  # seems unused
) -> _AnyHtmlElement: ...
def fromstring(
    html: _AnyStr,
    base_url: str | None = ...,
    parser: HTMLParser | XHTMLParser | None = ...,
    **kw: Any,  # seems unused
) -> _AnyHtmlElement: ...
def parse(
    filename_or_url: _FileReadSource,
    parser: HTMLParser | XHTMLParser | None = ...,
    base_url: str | None = ...,
    **kw: Any,  # seems unused
) -> etree._ElementTree[HtmlElement]: ...

#
# Form handling
#

class FormElement(HtmlElement):
    @property
    def inputs(self) -> InputGetter: ...
    @property
    def fields(self) -> FieldsDict: ...
    @fields.setter
    def fields(self, __v: SupportsLaxedItems[str, str]) -> None: ...
    action: str
    method: str
    def form_values(self) -> _FormValues: ...

def submit_form(
    form: FormElement,
    extra_values: _FormValues | SupportsLaxedItems[str, str] | None = ...,
    # open_http(method, url, values)
    open_http: Callable[[str, str, _FormValues], Any] | None = ...,
) -> Any: ...

# fallback function for open_http
def open_http_urllib(
    method: str,
    url: str,
    # Actually any structure acceptable by urllib.parse.urlencode() is fine.
    # But this func is generally only used with submit_form, there is not
    # much reason to support all of the data types.
    values: _FormValues,
) -> Any: ...

# FieldsDict is actually MutableMapping *sans* __delitem__
# However it is much simpler to keep MutableMapping and only
# override __delitem__
class FieldsDict(MutableMapping[str, str]):
    inputs: InputGetter
    def __init__(self, inputs: InputGetter) -> None: ...
    def __getitem__(self, __k: str) -> str: ...
    def __setitem__(self, __k: str, __v: str) -> None: ...
    def __delitem__(self, __k: Any) -> NoReturn: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...

# Quoting from source: it's unclear if this is a dictionary-like object
# or list-like object
class InputGetter(Collection[_AnyInputElement]):
    form: FormElement
    def __init__(self, form: FormElement) -> None: ...
    # __getitem__ is special here: for checkbox group and radio group,
    # it returns special list-like object instead of HtmlElement
    def __getitem__(
        self, name: str
    ) -> _AnyInputElement | RadioGroup | CheckboxGroup: ...
    def keys(self) -> list[str]: ...
    def items(
        self,
    ) -> list[tuple[str, _AnyInputElement | RadioGroup | CheckboxGroup]]: ...
    def __contains__(self, __o: object) -> bool: ...
    def __iter__(self) -> Iterator[_AnyInputElement]: ...
    def __len__(self) -> int: ...

class InputMixin:
    @property
    def name(self) -> str | None: ...
    @name.setter
    def name(self, __v: _AnyStr | None) -> None: ...

class TextareaElement(InputMixin, HtmlElement):  # type: ignore[misc]
    value: str

class SelectElement(InputMixin, HtmlElement):  # type: ignore[misc]
    multiple: bool
    @property
    def value(self) -> str | MultipleSelectOptions: ...
    @value.setter
    def value(self, value: _AnyStr | Collection[str]) -> None: ...
    @property
    def value_options(self) -> list[str]: ...

class MultipleSelectOptions(MutableSet[str]):
    select: SelectElement
    def __init__(self, select: SelectElement) -> None: ...
    @property
    def options(self) -> Iterator[HtmlElement]: ...
    def __contains__(self, __o: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def add(self, item: str) -> None: ...
    def remove(self, item: str) -> None: ...
    def discard(self, item: str) -> None: ...

class RadioGroup(list[InputElement]):
    value: str | None
    @property
    def value_options(self) -> list[str]: ...

class CheckboxGroup(list[InputElement]):
    @property
    def value(self) -> CheckboxValues: ...
    @value.setter
    def value(self, __v: Iterable[str]) -> None: ...
    @property
    def value_options(self) -> list[str]: ...

class CheckboxValues(MutableSet[str]):
    group: CheckboxGroup
    def __init__(self, group: CheckboxGroup) -> None: ...
    def __contains__(self, __o: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def add(self, value: str) -> None: ...
    def discard(self, item: str) -> None: ...

class InputElement(InputMixin, HtmlElement):  # type: ignore[misc]
    type: str
    value: str | None
    checked: bool
    @property
    def checkable(self) -> bool: ...

class LabelElement(HtmlElement):
    @property
    def for_element(self) -> HtmlElement | None: ...
    @for_element.setter
    def for_element(self, __v: HtmlElement) -> None: ...

def html_to_xhtml(html: _HtmlElemOrTree) -> None: ...
def xhtml_to_html(xhtml: _HtmlElemOrTree) -> None: ...

# 1. Encoding issue is similar to etree.tostring().
#
# 2. Unlike etree.tostring(), all arguments here are not explicitly
#    keyword-only. Using overload with no default value would be
#    impossible, as the two arguments before it has default value.
#    Need to make a choice here: enforce all arguments to be keyword-only.
#    Less liberal code, but easier to maintain in long term for users.
#
# 3. Although html.tostring() does not forbid method="c14n" (or c14n2),
#    calling tostring() this way would render almost all keyword arguments
#    useless, defeating the purpose of existence of html.tostring().
#    Besides, no c14n specific arguments are accepted here, so it is
#    better to let etree.tostring() handle C14N.
@overload  # encoding=str, encoding="unicode"
def tostring(
    doc: _HtmlElemOrTree,
    *,
    pretty_print: bool = ...,
    include_meta_content_type: bool = ...,
    encoding: type[str] | Literal["unicode"],
    method: _OutputMethodArg = ...,
    with_tail: bool = ...,
    doctype: str | None = ...,
) -> str: ...
@overload  # encoding="..." / None, no encoding arg
def tostring(
    doc: _HtmlElemOrTree,
    *,
    pretty_print: bool = ...,
    include_meta_content_type: bool = ...,
    encoding: etree._KnownEncodings | None = ...,
    method: _OutputMethodArg = ...,
    with_tail: bool = ...,
    doctype: str | None = ...,
) -> bytes: ...
@overload  # catch all
def tostring(
    doc: _HtmlElemOrTree,
    *,
    pretty_print: bool = ...,
    include_meta_content_type: bool = ...,
    encoding: str | type,
    method: _OutputMethodArg = ...,
    with_tail: bool = ...,
    doctype: str | None = ...,
) -> _AnyStr: ...

# Intended for debugging only
def open_in_browser(
    doc: _HtmlElemOrTree, encoding: str | type[str] | None = ...
) -> None: ...

# Custom parser target support is stripped here, otherwise it would
# completely nullify element lookup behavior of html.HTMLParser,
# as if etree.HTMLParser is used. Same applies to XHTMLParser below.
class HTMLParser(etree.HTMLParser[HtmlElement]):
    # Copies etree.HTMLParser.__init__, with target arg stripped
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
    ) -> None: ...
    def makeelement(
        self,
        _tag: _TagName,
        /,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> HtmlElement: ...
    @property
    def target(self) -> None: ...

class XHTMLParser(etree.XMLParser[HtmlElement]):
    # Copies etree.XMLParser.__init__, with target arg stripped
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
        compact: bool = ...,
    ) -> None: ...
    def makeelement(
        self,
        _tag: _TagName,
        /,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> HtmlElement: ...
    @property
    def target(self) -> None: ...

html_parser: HTMLParser
xhtml_parser: XHTMLParser

# Signature same as etree.Element
def Element(
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **extra: _AnyStr,
) -> HtmlElement: ...
