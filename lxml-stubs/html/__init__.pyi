#
# Making some compromise for HTML, in that iteration of subelements
# and methods would produce HTML elements instead of the base
# etree._Element. It is technically "correct" that those operations
# may not produce HTML elements when XML nodes are manually inserted
# into documents or fragments. However, arguably 99.9% of user cases
# don't involve such manually constructed hybrid element trees.
# Making it absolutely "correct" harms most users by losing context.
#

from _typeshed import _T
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
from typing_extensions import LiteralString, TypeAlias

from .. import etree
from .._types import (
    SupportsLaxedItems,
    Unused,
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

_HtmlDoc_T = TypeVar(
    "_HtmlDoc_T", str, bytes, HtmlElement, etree._ElementTree[HtmlElement]
)
_HtmlElemParser = etree.XMLParser[HtmlElement] | etree.HTMLParser[HtmlElement]

_HANDLE_FAILURES = Literal["ignore", "discard"]
_FormValues = list[tuple[str, str]]
_HtmlElemOrTree: TypeAlias = HtmlElement | etree._ElementTree[HtmlElement]

XHTML_NAMESPACE: LiteralString

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

#
# Here are some of the biggest difference between html stub and source,
# in order of importance.
#
# 1. Coerce HtmlComment etc to inherit from HtmlElement, instead of HtmlMixin.
# This is for simplifying return type of various ElementPath / ElementTree
# methods (like iter and findall). Instead of handling a long unioned list of
# possible element types, one can now just handle HtmlElement.
# This change doesn't make other content only element types suffer too much;
# most existing methods / properties already aren't applicable to them.
# See comment on etree.__ContentOnlyElement.
#
# 2. Don't expose the notion of HtmlMixin here. The convention of prepending
# underscore for private classes is only selectively followed in lxml, and
# HtmlMixin is one of the exceptions.
#
# 3. HtmlMixin.cssselect() differs by a missing star from _Element counterpart.
# This causes grievance for mypy, which jumps up and down screaming about
# incompatible signature for HtmlElement and EACH AND EVERY subclasses.
# Let's stop the nonsense by promoting the usage in _Element.
#
# 4. Remove HtmlProcessingInstruction from this world. It has never been seen
# in real life; mozilla also explicitly says it won't be supported.
# https://developer.mozilla.org/en-US/docs/Web/API/ProcessingInstruction
#
class HtmlElement(etree.ElementBase):
    #
    # HtmlMixin properties and methods
    #
    # NOTE: set() differs from _Element.set() -- value has default, can accept None,
    # which means boolean attribute without value, like <option selected>
    #
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
    def set(self, key: _AttrName, value: _AttrVal | None = ...) -> None: ...
    def drop_tree(self) -> None: ...
    def drop_tag(self) -> None: ...
    def find_rel_links(
        self,
        rel: str,  # Can be bytes, but never match anything on py3
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
    #
    # HtmlMixin Link functions
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
    # Overriding of most _Element methods
    #
    # Subclassing of _Element should not go beyond HtmlElement. For example,
    # while children of HtmlElement are mostly HtmlElement, FormElement never
    # contains FormElement as child.
    @overload
    def __getitem__(self, __x: int) -> HtmlElement: ...
    @overload
    def __getitem__(self, __x: slice) -> list[HtmlElement]: ...
    @overload
    def __setitem__(self, __x: int, __v: HtmlElement) -> None: ...
    @overload
    def __setitem__(self, __x: slice, __v: Iterable[HtmlElement]) -> None: ...
    def __iter__(self) -> Iterator[HtmlElement]: ...
    def __reversed__(self) -> Iterator[HtmlElement]: ...
    def append(self, element: HtmlElement) -> None: ...
    def extend(self, elements: Iterable[HtmlElement]) -> None: ...
    def insert(self, index: int, element: HtmlElement) -> None: ...
    def remove(self, element: HtmlElement) -> None: ...
    def index(
        self, child: HtmlElement, start: int | None = ..., end: int | None = ...
    ) -> int: ...
    def addnext(self, element: HtmlElement) -> None: ...
    def addprevious(self, element: HtmlElement) -> None: ...
    def replace(self, old_element: HtmlElement, new_element: HtmlElement) -> None: ...
    def getparent(self) -> HtmlElement | None: ...
    def getnext(self) -> HtmlElement | None: ...
    def getprevious(self) -> HtmlElement | None: ...
    def itersiblings(
        self,
        tag: etree._TagSelector | None = ...,
        *tags: etree._TagSelector,
        preceding: bool = ...,
    ) -> Iterator[HtmlElement]: ...
    def iterancestors(
        self, tag: etree._TagSelector | None = ..., *tags: etree._TagSelector
    ) -> Iterator[HtmlElement]: ...
    def iterdescendants(
        self, tag: etree._TagSelector | None = ..., *tags: etree._TagSelector
    ) -> Iterator[HtmlElement]: ...
    def iterchildren(
        self,
        tag: etree._TagSelector | None = ...,
        *tags: etree._TagSelector,
        reversed: bool = ...,
    ) -> Iterator[HtmlElement]: ...
    def getroottree(self) -> etree._ElementTree[HtmlElement]: ...
    def iter(
        self, tag: etree._TagSelector | None = ..., *tags: etree._TagSelector
    ) -> Iterator[HtmlElement]: ...
    def itertext(
        self,
        tag: etree._TagSelector | None = ...,
        *tags: etree._TagSelector,
        with_tail: bool = ...,
    ) -> Iterator[str]: ...
    def makeelement(
        self,
        _tag: _TagName,
        /,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> HtmlElement: ...
    def find(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> HtmlElement | None: ...
    def findall(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> list[HtmlElement]: ...
    def iterfind(
        self, path: _ElemPathArg, namespaces: _NSMapArg | None = ...
    ) -> Iterator[HtmlElement]: ...
    def cssselect(
        self,
        expr: str,
        *,
        translator: _CSSTransArg = ...,
    ) -> list[HtmlElement]: ...

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

def find_rel_links(
    doc: _HtmlDoc_T,
    rel: str,
) -> list[HtmlElement]: ...
def find_class(
    doc: _HtmlDoc_T,
    class_name: _AnyStr,
) -> list[HtmlElement]: ...
def make_links_absolute(
    doc: _HtmlDoc_T,
    base_url: str | None = ...,
    resolve_base_href: bool = ...,
    handle_failures: _HANDLE_FAILURES | None = ...,
) -> _HtmlDoc_T: ...
def resolve_base_href(
    doc: _HtmlDoc_T,
    handle_failures: _HANDLE_FAILURES | None = ...,
) -> _HtmlDoc_T: ...
def iterlinks(
    doc: _HtmlDoc_T,
) -> Iterator[tuple[HtmlElement, str | None, str, int]]: ...
def rewrite_links(
    doc: _HtmlDoc_T,
    link_repl_func: Callable[[str], str | None],
    resolve_base_href: bool = ...,
    base_href: str | None = ...,
) -> _HtmlDoc_T: ...

#
# Types of different HTML elements, note the absence of
# HtmlProcessingInstruction
#
class HtmlComment(HtmlElement, etree.CommentBase): ...
class HtmlEntity(HtmlElement, etree.EntityBase): ...

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
        document: Unused,
        namespace: Unused,
        name: str | None,
    ) -> type[HtmlElement] | None: ...

#
# parsing functions
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

class TextareaElement(InputMixin, HtmlElement):
    value: str

class SelectElement(InputMixin, HtmlElement):
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

class InputElement(InputMixin, HtmlElement):
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

class HTMLParser(etree.HTMLParser[HtmlElement]):
    """An HTML parser configured to return ``lxml.html`` Element
    objects.

    Notes
    -----
    1. The ``target`` parameter is stripped from ``__init__`` definition.  If custom parser target argument were used in ``html.HTMLParser``, its element lookup behavior would be completely nullified, behaving as if ``etree.HTMLParser`` is used, which makes this subclass meaningless.
    2. This subclass is not specialized, unlike the ``etree`` counterpart.  They are designed to always handle ``HtmlElement``; for generating other kinds of ``_Elements``, one should use etree parsers with ``set_element_class_lookup()`` method instead.  In that case, see ``_FeedParser.set_element_class_lookup()`` for more info.
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

    Note that this parser is not really XHTML aware unless you let it
    load a DTD that declares the HTML entities.  To do this, make sure
    you have the XHTML DTDs installed in your catalogs, and create the
    parser like this::

        >>> parser = XHTMLParser(load_dtd=True)

    If you additionally want to validate the document, use this::

        >>> parser = XHTMLParser(dtd_validation=True)

    For catalog support, see http://www.xmlsoft.org/catalog.html.

    Notes
    -----
    1. The ``target`` parameter is stripped from ``__init__`` definition.  If custom parser target argument were used in ``html.XHTMLParser``, its element lookup behavior would be completely nullified, behaving as if ``etree.HTMLParser`` is used, which makes this subclass meaningless.
    2. This subclass is not specialized, unlike the ``etree`` counterpart.  They are designed to always handle ``HtmlElement``; for generating other kinds of ``_Elements``, one should use etree parsers with ``set_element_class_lookup()`` method instead.  In that case, see ``_FeedParser.set_element_class_lookup()`` for more info.

    """

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

# Signature same as etree.Element
def Element(
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **extra: _AnyStr,
) -> HtmlElement: ...
