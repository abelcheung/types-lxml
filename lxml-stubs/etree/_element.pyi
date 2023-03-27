from _typeshed import _T
from typing import Any, Generic, Iterable, Iterator, Literal, Mapping, overload
from typing_extensions import Never, Self

from .. import _types as _t
from ..cssselect import _CSSTransArg
from ._module_misc import CDATA, DocInfo, QName
from ._parser import _DefEtreeParsers
from ._xslt import XSLTAccessControl, XSLTExtension, _Stylesheet_Param, _XSLTResultTree

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
    def tag(self, value: _t._TagName) -> None: ...
    @property
    def attrib(self) -> _Attrib: ...
    @property
    def text(self) -> str | None: ...
    @text.setter
    def text(self, value: _t._AnyStr | QName | CDATA | None) -> None: ...
    @property
    def tail(self) -> str | None: ...
    @tail.setter
    def tail(self, value: _t._AnyStr | CDATA | None) -> None: ...
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
    def base(self, value: _t._AnyStr | None) -> None: ...
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
    def set(self, key: _t._AttrName, value: _t._AttrVal) -> None: ...
    def append(self, element: Self) -> None: ...
    def extend(self, elements: Iterable[Self]) -> None: ...
    def clear(self, keep_tail: bool = ...) -> None: ...
    def insert(self, index: int, element: Self) -> None: ...
    def remove(self, element: Self) -> None: ...
    def index(
        self, child: Self, start: int | None = ..., end: int | None = ...
    ) -> int: ...
    @overload
    def get(self, key: _t._AttrName) -> str | None: ...
    @overload
    def get(self, key: _t._AttrName, default: _T) -> str | _T: ...
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
        self, *tags: _t._TagSelector, preceding: bool = ...
    ) -> Iterator[Self]: ...
    @overload
    def itersiblings(
        self, *, tag: Iterable[_t._TagSelector] | None = ..., preceding: bool = ...
    ) -> Iterator[Self]: ...
    @overload
    def iterancestors(self, *tags: _t._TagSelector) -> Iterator[Self]: ...
    @overload
    def iterancestors(
        self, *, tag: Iterable[_t._TagSelector] | None = ...
    ) -> Iterator[Self]: ...
    @overload
    def iterdescendants(self, *tags: _t._TagSelector) -> Iterator[Self]: ...
    @overload
    def iterdescendants(
        self, *, tag: Iterable[_t._TagSelector] | None = ...
    ) -> Iterator[Self]: ...
    @overload
    def iterchildren(
        self, *tags: _t._TagSelector, reversed: bool = ...
    ) -> Iterator[Self]: ...
    @overload
    def iterchildren(
        self, *, tag: Iterable[_t._TagSelector] | None = ..., reversed: bool = ...
    ) -> Iterator[Self]: ...
    @overload
    def iter(self, *tags: _t._TagSelector) -> Iterator[Self]: ...
    @overload
    def iter(
        self, *, tag: Iterable[_t._TagSelector] | None = ...
    ) -> Iterator[Self]: ...
    @overload
    def itertext(
        self, *tags: _t._TagSelector, with_tail: bool = ...
    ) -> Iterator[str]: ...
    @overload
    def itertext(
        self, *, tag: Iterable[_t._TagSelector] | None = ..., with_tail: bool = ...
    ) -> Iterator[str]: ...
    def makeelement(
        self,
        _tag: _t._TagName,
        /,
        # Final result is sort of like {**attrib, **_extra}
        attrib: _t.SupportsLaxedItems[str, _t._AnyStr] | None = ...,
        nsmap: _t._NSMapArg | None = ...,
        **_extra: _t._AnyStr,
    ) -> Self: ...
    def find(
        self, path: _t._ElemPathArg, namespaces: _t._NSMapArg | None = ...
    ) -> Self | None: ...
    # Original method has no star. If somebody only supplies
    # 'path' and 'default' argument as positional one, it
    # would be misinterpreted as namespaces argument in first
    # overload form. Add star here to guard against such situation.
    @overload
    def findtext(
        self,
        path: _t._ElemPathArg,
        *,
        namespaces: _t._NSMapArg | None = ...,
    ) -> str | None: ...
    @overload
    def findtext(
        self,
        path: _t._ElemPathArg,
        default: _T,
        namespaces: _t._NSMapArg | None = ...,
    ) -> str | _T: ...
    def findall(
        self, path: _t._ElemPathArg, namespaces: _t._NSMapArg | None = ...
    ) -> list[Self]: ...
    def iterfind(
        self, path: _t._ElemPathArg, namespaces: _t._NSMapArg | None = ...
    ) -> Iterator[Self]: ...
    def xpath(
        self,
        _path: _t._AnyStr,
        /,
        *,
        namespaces: _t._NonDefaultNSMapArg | None = ...,
        extensions: _t._XPathExtFuncArg | None = ...,
        smart_strings: bool = ...,
        **_variables: _t._XPathVarArg,
    ) -> _t._XPathObject: ...
    def cssselect(
        self,
        expr: str,
        *,
        translator: _CSSTransArg = ...,
    ) -> list[Self]: ...
    @_t.deprecated("Since v2.0 (2008); use list(element) or iterate over element")
    def getchildren(self) -> list[Self]: ...
    # Should have been overloaded for accuracy, but we can turn a blind eye
    # for something that is marked deprecated for 15 years
    @_t.deprecated("Since v2.0 (2008); renamed to .iter()")
    def getiterator(
        self, tag: _t._TagSelector | None = ..., *tags: _t._TagSelector
    ) -> Iterator[Self]: ...

# ET class notation is specialized, indicating the type of element
# it is holding (e.g. XML element, HTML element or Objectified
# Element).
# Although it is also possible to be an empty tree containing no
# element, the absolute majority of lxml API will fail to work.
# It is considered harmful to support such corner case, which
# adds much complexity without any benefit.
class _ElementTree(Generic[_t._ET_co]):
    @property
    def parser(self) -> _DefEtreeParsers[_t._ET_co] | None: ...
    @property
    def docinfo(self) -> DocInfo: ...
    def parse(
        self,
        source: _t._FileReadSource,
        parser: _DefEtreeParsers[_t._ET_co] | None = ...,
        *,
        base_url: _t._AnyStr | None = ...,
    ) -> None: ...
    # Changes root node; in terms of typing, this means changing
    # specialization of ElementTree. This is not expressible in
    # current typing system.
    def _setroot(self, root: _Element) -> None: ...
    def getroot(self) -> _t._ET_co: ...
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
    @_t.deprecated('Since v3.8.0; use "doctype" parameter instead')
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
        file: _t._FileWriteSource,
        *,
        method: Literal["c14n"],
        exclusive: bool = ...,
        with_comments: bool = ...,
        compression: int | None = ...,
        inclusive_ns_prefixes: Iterable[_t._AnyStr] | None = ...,
    ) -> None: ...
    @overload  # method=c14n2
    def write(
        self,
        file: _t._FileWriteSource,
        *,
        method: Literal["c14n2"],
        with_comments: bool = ...,
        compression: int | None = ...,
        strip_text: bool = ...,
    ) -> None: ...
    @overload  # other write methods
    def write(
        self,
        file: _t._FileWriteSource,
        *,
        encoding: str | None = ...,  # unicode not allowed
        method: _t._OutputMethodArg = ...,
        pretty_print: bool = ...,
        xml_declaration: bool | None = ...,
        with_tail: bool = ...,
        standalone: bool | None = ...,
        doctype: str | None = ...,
        compression: int | None = ...,
    ) -> None: ...
    def getpath(self: _ElementTree[_t._ET], element: _t._ET) -> str: ...
    def getelementpath(self: _ElementTree[_t._ET], element: _t._ET) -> str: ...
    @overload
    def iter(self, *tags: _t._TagSelector) -> Iterator[_t._ET_co]: ...
    @overload
    def iter(self, *, tag: _t._TagSelector | None = ...) -> Iterator[_t._ET_co]: ...
    #
    # ElementPath methods calls the same method on root node,
    # so signature should be the same as _Element ones
    #
    def find(
        self, path: _t._ElemPathArg, namespaces: _t._NSMapArg | None = ...
    ) -> _t._ET_co | None: ...
    @overload
    def findtext(
        self,
        path: _t._ElemPathArg,
        *,
        namespaces: _t._NSMapArg | None = ...,
    ) -> str | None: ...
    @overload
    def findtext(
        self,
        path: _t._ElemPathArg,
        default: _T,
        namespaces: _t._NSMapArg | None = ...,
    ) -> str | _T: ...
    def findall(
        self, path: _t._ElemPathArg, namespaces: _t._NSMapArg | None = ...
    ) -> list[_t._ET_co]: ...
    def iterfind(
        self, path: _t._ElemPathArg, namespaces: _t._NSMapArg | None = ...
    ) -> Iterator[_t._ET_co]: ...
    def xpath(
        self,
        _path: _t._AnyStr,
        /,
        *,
        namespaces: _t._NonDefaultNSMapArg | None = ...,
        extensions: _t._XPathExtFuncArg | None = ...,
        smart_strings: bool = ...,
        **_variables: _t._XPathVarArg,
    ) -> _t._XPathObject: ...
    def xslt(
        self,
        _xslt: _t._ElementOrTree,
        /,
        extensions: _t.SupportsLaxedItems[tuple[_t._AnyStr, _t._AnyStr], XSLTExtension]
        | None = ...,
        access_control: XSLTAccessControl | None = ...,
        *,  # all keywords are passed to XSLT.__call__
        profile_run: bool = ...,
        **__kw: _Stylesheet_Param,
    ) -> _XSLTResultTree: ...
    def relaxng(self, relaxng: _t._ElementOrTree) -> bool: ...
    def xmlschema(self, xmlschema: _t._ElementOrTree) -> bool: ...
    def xinclude(self) -> None: ...
    # Should have been overloaded for accuracy, but we can turn a blind eye
    # for something that is marked deprecated for 15 years
    @_t.deprecated("Since v2.0 (2008); renamed to .iter()")
    def getiterator(
        self, tag: _t._TagSelector | None = ..., *tags: _t._TagSelector
    ) -> Iterator[_t._ET_co]: ...
    @_t.deprecated('Since v4.4; use .write() with method="c14n" argument')
    def write_c14n(
        self,
        file: _t._FileWriteSource,
        *,
        exclusive: bool = ...,
        with_comments: bool = ...,
        compression: int | None = ...,
        inclusive_ns_prefixes: Iterable[_t._AnyStr] | None = ...,
    ) -> None: ...

# Behaves like MutableMapping but deviates a lot in details
class _Attrib:
    @property
    def _element(self) -> _Element: ...
    def __setitem__(self, __k: _t._AttrName, __v: _t._AttrVal) -> None: ...
    def __delitem__(self, __k: _t._AttrName) -> None: ...
    # explicitly checks for dict and _Attrib
    def update(
        self,
        sequence_or_dict: _Attrib
        | dict[Any, Any]  # Compromise with MutableMapping key/val invariance
        | Iterable[tuple[_t._AttrName, _t._AttrVal]],
    ) -> None: ...
    # Signature is pop(self, key, *default), yet followed by runtime
    # check and raise exception if multiple default argument is supplied
    # Note that get() is forgiving with non-existent key yet pop() isn't.
    @overload
    def pop(self, key: _t._AttrName) -> str: ...
    @overload
    def pop(self, key: _t._AttrName, default: _T) -> str | _T: ...
    def clear(self) -> None: ...
    def __getitem__(self, __k: _t._AttrName) -> str: ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    @overload
    def get(self, key: _t._AttrName) -> str | None: ...
    @overload
    def get(self, key: _t._AttrName, default: _T) -> str | _T: ...
    def keys(self) -> list[str]: ...
    def __iter__(self) -> Iterator[str]: ...
    def iterkeys(self) -> Iterator[str]: ...
    def values(self) -> list[str]: ...
    def itervalues(self) -> Iterator[str]: ...
    def items(self) -> list[tuple[str, str]]: ...
    def iteritems(self) -> Iterator[tuple[str, str]]: ...
    def has_key(self, key: _t._AttrName) -> bool: ...
    def __contains__(self, __o: object) -> bool: ...
    # richcmp dropped, mapping has no concept of inequality comparison

#
# Element types and content node types
#

# It is decided to not decouple other content only elements
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
    @property
    def text(self) -> str | None: ...
    @text.setter
    def text(self, value: _t._AnyStr | None) -> None: ...
    #
    # Mypy: Liskov!
    # Lxml: No Liskov!
    # Mypy: I am *THE* authority here!
    # Lxml: I will *NEVER* submit to you! Fuck off!
    # Mypy: Now die!
    #
    # So here we are.
    #
    @property
    def attrib(self) -> Mapping[_t.Unused, _t.Unused]: ...  # type: ignore[override]
    def get(self, key: _t.Unused, default: _t.Unused = ...) -> None: ...  # type: ignore[override]
    def set(self, key: Never, value: Never) -> Never: ...  # type: ignore[override]
    def append(self, element: Never) -> Never: ...  # type: ignore[override]
    def insert(self, index: Never, value: Never) -> Never: ...  # type: ignore[override]
    def __setitem__(self, __k: Never, __v: Never) -> Never: ...  # type: ignore[override]
    # The intention is to forbid elem.__getitem__, allowing slice
    # doesn't make any sense
    def __getitem__(self, __k: Never) -> Never: ...  # type: ignore[override]
    # Methods above are explicitly defined in source, while those below aren't
    def __delitem__(self, __k: Never) -> Never: ...  # type: ignore[override]
    def __iter__(self) -> Never: ...

    # TODO (low priority) There are many, many more methods that
    # don't work for content only elements, such as most
    # ElementTree / ElementPath ones, and all inherited
    # HTML element methods. None of those are handled in
    # source code -- users are left to bump into wall themselves.
    # For example, append(elem) explicitly raises exception, yet
    # one can use extend([elem]) to circumvent restriction.
    # Go figure.

class _Comment(__ContentOnlyElement):
    @property  # type: ignore[misc]
    def tag(self) -> _t._ElemFactory[_Comment]: ...  # type: ignore[override]

# signature of .get() for _PI and _Element are the same
class _ProcessingInstruction(__ContentOnlyElement):
    @property  # type: ignore[misc]
    def tag(self) -> _t._ElemFactory[_ProcessingInstruction]: ...  # type: ignore[override]
    @property
    def target(self) -> str: ...
    @target.setter
    def target(self, value: _t._AnyStr) -> None: ...
    @property
    def attrib(self) -> dict[str, str]: ...  # type: ignore[override]

class _Entity(__ContentOnlyElement):
    @property  # type: ignore[misc]
    def tag(self) -> _t._ElemFactory[_Entity]: ...  # type: ignore[override]
    @property  # type: ignore[misc]
    def text(self) -> str: ...  # type: ignore[override]
    @property
    def name(self) -> str: ...
    @name.setter
    def name(self, value: _t._AnyStr) -> None: ...
