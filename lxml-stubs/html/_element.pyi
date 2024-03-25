import sys
from _typeshed import _T
from typing import Callable, Iterable, Iterator, Literal, MutableSet, overload

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from .. import etree
from .._types import (
    SupportsLaxedItems,
    _AnyStr,
    _AttrName,
    _AttrVal,
    _ElemPathArg,
    _NSMapArg,
    _TagName,
    _TagSelector,
)
from ..cssselect import _CSSTransArg
from ._form import FormElement, LabelElement

_HANDLE_FAILURES = Literal["ignore", "discard"]

#
# Making some compromise for HTML, in that iteration of subelements
# and methods would produce HTML elements instead of the base
# etree._Element. It is technically "correct" that those operations
# may not produce HTML elements when XML nodes are manually inserted
# into documents or fragments. However, arguably 99.9% of user cases
# don't involve such manually constructed hybrid element trees.
# Making it absolutely "correct" harms most users by losing context.
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
class HtmlElement(etree.ElementBase):
    #
    # HtmlMixin properties and methods
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
    # set() differs from _Element.set() -- value has default, can accept None,
    # which means boolean attribute without value, like <option selected>
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
    # text_content() uses XPath behind the scene, and smart string
    # subscript should point to original element type
    # XXX But acutally the result is always None, as it uses XPath
    # string() to merge text content and destroy element heritage info
    def text_content(self) -> etree._ElementUnicodeResult[Self]: ...
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
    def getroottree(self) -> etree._ElementTree[HtmlElement]: ...
    @overload
    def itersiblings(
        self, *tags: _TagSelector, preceding: bool = ...
    ) -> Iterator[HtmlElement]: ...
    @overload
    def itersiblings(
        self, *, tag: Iterable[_TagSelector] | None = ..., preceding: bool = ...
    ) -> Iterator[HtmlElement]: ...
    @overload
    def iterancestors(self, *tags: _TagSelector) -> Iterator[HtmlElement]: ...
    @overload
    def iterancestors(
        self, *, tag: Iterable[_TagSelector] | None = ...
    ) -> Iterator[HtmlElement]: ...
    @overload
    def iterdescendants(self, *tags: _TagSelector) -> Iterator[HtmlElement]: ...
    @overload
    def iterdescendants(
        self, *, tag: Iterable[_TagSelector] | None = ...
    ) -> Iterator[HtmlElement]: ...
    @overload
    def iterchildren(
        self, *tags: _TagSelector, reversed: bool = ...
    ) -> Iterator[HtmlElement]: ...
    @overload
    def iterchildren(
        self, *, tag: Iterable[_TagSelector] | None = ..., reversed: bool = ...
    ) -> Iterator[HtmlElement]: ...
    @overload
    def iter(self, *tags: _TagSelector) -> Iterator[HtmlElement]: ...
    @overload
    def iter(
        self, *, tag: Iterable[_TagSelector] | None = ...
    ) -> Iterator[HtmlElement]: ...
    @overload
    def itertext(self, *tags: _TagSelector, with_tail: bool = ...) -> Iterator[str]: ...
    @overload
    def itertext(
        self, *, tag: Iterable[_TagSelector] | None = ..., with_tail: bool = ...
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

#
# HTML element class attribute
#
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
    def __contains__(self, x: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def add(self, value: str) -> None: ...
    def discard(self, value: str) -> None: ...
    def update(self, values: Iterable[str]) -> None: ...
    def toggle(self, value: str) -> bool: ...

#
# Types of other HTML elements
#
# Processing Instruction is only useful for XML in real life;
# it is considered bogus error in HTML spec, but still allowed
# to be constructed in lxml nontheless.
# https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
#
# HtmlEntity is also rare; it can only appear if a specially constructed
# HTML parser is used. By default entities are merged into text content.
#
# Note the reversed MRO order -- fatal dunders from __ContentOnlyElement
# are dominant in runtime
#
class HtmlProcessingInstruction(etree.PIBase, HtmlElement): ...  # type: ignore
class HtmlComment(etree.CommentBase, HtmlElement): ...  # type: ignore
class HtmlEntity(etree.EntityBase, HtmlElement): ...  # type: ignore

#
# Factory func, signature same as etree.Element
#
def Element(
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **extra: _AnyStr,
) -> HtmlElement: ...
