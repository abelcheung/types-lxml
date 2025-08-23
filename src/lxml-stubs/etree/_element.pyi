import sys
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    TypeAlias,
    TypeVar,
    final,
    overload,
)

from .. import _types as _t
from ..cssselect import _CSSTransArg
from ._module_misc import CDATA, DocInfo, QName
from ._parser import CustomTargetParser
from ._xslt import XSLTAccessControl, XSLTExtension, _Stylesheet_Param, _XSLTResultTree

if sys.version_info >= (3, 11):
    from typing import Never, Self
else:
    from typing_extensions import Never, Self

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

_T = TypeVar("_T")

# The base of _Element is *almost* an amalgam of MutableSequence[_Element]
# plus mixin methods for _Attrib.
# Extra methods follow the order of _Element source approximately
class _Element:
    """Element class. References a document object and a libxml node.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element)
    """

    def __init__(  # Args identical to Element.makeelement
        self,
        _tag: _t._TagName,
        /,
        attrib: _t._AttrMapping | None = ...,
        nsmap: _t._NSMapArg | None = ...,
        **_extra: _t._AttrVal,
    ) -> None: ...

    #
    # Common properties
    #
    # Tag type is str only on initial doc parsing. When tag
    # is manually set, supplied value is directly stored
    # in element and never normalized.
    @property
    def tag(self) -> _t._TagName:
        """Element tag name

        Annotation
        ----------
        - input type: `str | bytes | bytearray | QName`
        - output type: `str | bytes | bytearray | QName`

        Value is initially `str` after parsing tree or content, but can be
        modified to any value manually. Modified value is stored as-is.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.tag)
        """
    @tag.setter
    def tag(self, value: _t._TagName) -> None: ...
    @property
    def attrib(self) -> _Attrib:
        """Element attribute dictionary. Where possible, use `get()`, `set()`,
        `keys()`, `values()` and `items()` to access element attributes.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.attrib)
        - [`_Attrib` API](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Attrib)
        """
    @property
    def text(self) -> str | None:
        """Text before the first subelement.

        Annotation
        ----------
        - input type: `str | bytes | bytearray | QName | CDATA | None`
        - output type: `str | None`

        Value is always normalised to `str` unless it is explicitly
        set to `None`.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.text)
        """
    @text.setter
    def text(self, value: _t._TextArg | QName | CDATA | None) -> None: ...
    @property
    def tail(self) -> str | None:
        """Text after this element's end tag, but before the next sibling
        element's start tag.

        Annotation
        ----------
        - input type: `str | bytes | bytearray | CDATA | None`
        - output type: `str | None`

        Value is always normalised to `str` unless it is explicitly
        set to `None`.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.tail)
        """
    @tail.setter
    def tail(self, value: _t._TextArg | CDATA | None) -> None: ...
    #
    # _Element-only properties
    # Following props are marked as read-only in comment,
    # but .sourceline and .base provide __set__() method.
    # However, we only implement rw property for base, as
    # modifying .sourceline is meaningless.
    #
    @property
    def prefix(self) -> str | None:
        """Namespace prefix

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.prefix)
        """
    @property
    def sourceline(self) -> int | None:
        """Original line number as found by the parser or None if unknown.

        Annotation
        ----------
        This annotation package pretends the property is read-only, but
        it is actually read-write. However, modifying the value is
        meaningless, as its only purpose is to reflect the line number
        this element appears in original content.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.sourceline)
        """
    @property
    def nsmap(self) -> dict[str | None, str]:
        """Namespace prefix->URI mapping known in the context of this
        Element.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.nsmap)
        """
    @property
    def base(self) -> str | None:
        """The base URI of the Element (xml:base or HTML base URL).

        Annotation
        ----------
        - input type: `str | bytes | None`
        - output type: `str | None`

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.base)
        """
    @base.setter
    def base(self, value: str | bytes | None) -> None: ...
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
    # An element itself can be treated as container of other elements. When used
    # like elem[:] = new_elem, only subelements within new_elem will be
    # inserted, but not new_elem itself. If there is none, the whole slice would
    # be silently deleted. Though permitted in runtime, this is not an expected
    # behavior.
    # Although normal class methods (like extend()) can be @deprecated, same
    # doesn't apply to magic methods, at least for Pylance. Thus we create
    # additional overload for extend() but not here.
    @overload
    def __setitem__(self, __x: slice, __v: Iterable[Self]) -> None: ...
    def __contains__(self, __o: object) -> bool: ...
    def __len__(self) -> int: ...
    # There are a hoard of element iterators used in lxml, but
    # they only differ in implementation detail and don't affect typing.
    def __iter__(self) -> Iterator[Self]: ...
    def __reversed__(self) -> Iterator[Self]: ...
    def set(self, key: _t._AttrName, value: _t._AttrVal) -> None:
        """Sets an element attribute.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.set)
        """
    def append(self, element: Self) -> None:
        """Adds a subelement to the end of this element.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.append)
        """
    @overload  # see __setitem__ for explanation
    @deprecated("Expects iterable of elements as value, not single element")
    def extend(self, elements: _Element) -> Never:
        """Extends the current children by the elements in the iterable.

        Annotation
        ----------
        This overload discourages supplying a single element as value, because
        only its children (if any) are inserted, not the element itself.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.extend)
        """
    @overload
    def extend(self, elements: Iterable[Self]) -> None:
        """Extends the current children by the elements in the iterable.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.extend)
        """
    def clear(self, keep_tail: bool = False) -> None:
        """Resets an element.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.clear)
        """
    def insert(self, index: int, element: Self) -> None:
        """Inserts a subelement at the given position in this element

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.insert)
        """
    def remove(self, element: Self) -> None:
        """Removes a matching subelement.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.remove)
        """
    def index(
        self,
        child: Self,
        start: int | None = None,
        stop: int | None = None,
    ) -> int:
        """Find the position of the child within the parent.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.index)
        """
    @overload
    def get(self, key: _t._AttrName) -> str | None:
        """Gets an element attribute.

        Annotation
        ----------
        This overload handles the case where default value is not supplied.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.get)
        """
    @overload
    def get(self, key: _t._AttrName, default: _T) -> str | _T:
        """Gets an element attribute.

        Annotation
        ----------
        This overload handles the case where default value is given.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.get)
        """
    def keys(self) -> list[str]:
        """Gets a list of attribute names.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.keys)
        """
    def values(self) -> list[str]:
        """Gets element attribute values as a sequence of strings.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.values)
        """
    def items(self) -> list[tuple[str, str]]:
        """Gets element attributes, as a sequence.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.items)
        """
    #
    # extra Element / ET methods
    #
    def addnext(self, element: Self) -> None:
        """Adds the element as a following sibling directly after this element.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.addnext)
        """
    def addprevious(self, element: Self) -> None:
        """Adds the element as a preceding sibling directly before this element.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.addprevious)
        """
    def replace(self, old_element: Self, new_element: Self) -> None:
        """Replaces a subelement with the element passed as second argument.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.replace)
        """
    def getparent(self) -> Self | None:
        """Returns the parent of this element or None for the root element.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.getparent)
        """
    def getnext(self) -> Self | None:
        """Returns the following sibling of this element or None.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.getnext)
        """
    def getprevious(self) -> Self | None:
        """Returns the preceding sibling of this element or None.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.getprevious)
        """
    def getroottree(self) -> _ElementTree[Self]:
        """Return an ElementTree for the root node of the document that
        contains this element.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.getroottree)
        """
    @overload
    def itersiblings(
        self, *tags: _t._TagSelector, preceding: bool = False
    ) -> Iterator[Self]:
        """Iterate over the following or preceding siblings of this element.

        Annotation
        ----------
        This overload handles the case where all tags are supplied as positional
        arguments.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.itersiblings)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def itersiblings(
        self,
        tag: _t._TagSelector | Iterable[_t._TagSelector] | None = None,
        *,
        preceding: bool = False,
    ) -> Iterator[Self]:
        """Iterate over the following or preceding siblings of this element.

        Annotation
        ----------
        This overload handles following cases:
        - A single tag is supplied as keyword argument
        - Multiple tags are grouped into an iterable

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.itersiblings)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def iterancestors(self, *tags: _t._TagSelector) -> Iterator[Self]:
        """Iterate over the ancestors of this element (from parent to parent).

        Annotation
        ----------
        This overload handles the case where all tags are supplied as positional
        arguments.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iterancestors)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def iterancestors(
        self, tag: _t._TagSelector | Iterable[_t._TagSelector] | None = None
    ) -> Iterator[Self]:
        """Iterate over the ancestors of this element (from parent to parent).

        Annotation
        ----------
        This overload handles following cases:
        - A single tag is supplied as keyword argument
        - Multiple tags are grouped into an iterable

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iterancestors)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def iterdescendants(self, *tags: _t._TagSelector) -> Iterator[Self]:
        """Iterate over the descendants of this element in document order.

        Annotation
        ----------
        This overload handles the case where all tags are supplied as positional
        arguments.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iterdescendants)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def iterdescendants(
        self, tag: _t._TagSelector | Iterable[_t._TagSelector] | None = None
    ) -> Iterator[Self]:
        """Iterate over the descendants of this element in document order.

        Annotation
        ----------
        This overload handles following cases:
        - A single tag is supplied as keyword argument
        - Multiple tags are grouped into an iterable

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iterdescendants)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def iterchildren(
        self, *tags: _t._TagSelector, reversed: bool = False
    ) -> Iterator[Self]:
        """Iterate over the children of this element.

        Annotation
        ----------
        This overload handles the case where all tags are supplied as positional
        arguments.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iterchildren)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def iterchildren(
        self,
        tag: _t._TagSelector | Iterable[_t._TagSelector] | None = None,
        *,
        reversed: bool = False,
    ) -> Iterator[Self]:
        """Iterate over the children of this element.

        Annotation
        ----------
        This overload handles following cases:
        - A single tag is supplied as keyword argument
        - Multiple tags are grouped into an iterable

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iterchildren)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def iter(self, *tags: _t._TagSelector) -> Iterator[Self]:
        """Iterate over all elements in the subtree in document order (depth
        first pre-order), starting with this element.

        Annotation
        ----------
        This overload handles the case where all tags are supplied as positional
        arguments.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def iter(
        self, tag: _t._TagSelector | Iterable[_t._TagSelector] | None = None
    ) -> Iterator[Self]:
        """Iterate over all elements in the subtree in document order (depth
        first pre-order), starting with this element.

        Annotation
        ----------
        This overload handles following cases:
        - A single tag is supplied as keyword argument
        - Multiple tags are grouped into an iterable

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def itertext(self, *tags: _t._TagSelector, with_tail: bool = True) -> Iterator[str]:
        """Iterates over the text content of a subtree.

        Annotation
        ----------
        This overload handles the case where all tags are supplied as positional
        arguments.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.itertext)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    @overload
    def itertext(
        self,
        tag: _t._TagSelector | Iterable[_t._TagSelector] | None = None,
        *,
        with_tail: bool = True,
    ) -> Iterator[str]:
        """Iterates over the text content of a subtree.

        Annotation
        ----------
        This overload handles following cases:
        - A single tag is supplied as keyword argument
        - Multiple tags are grouped into an iterable

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.itertext)
        - [Possible tag values in `iter()`](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iter)
        """
    makeelement: type[Self]
    """Creates a new element associated with the same document.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.makeelement)
    """
    def find(
        self, path: _t._ElemPathArg, namespaces: _t._StrOnlyNSMap | None = None
    ) -> Self | None:
        """Creates a new element associated with the same document.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.find)
        """
    @overload
    def findtext(
        self,
        path: _t._ElemPathArg,
        default: _T,
        namespaces: _t._StrOnlyNSMap | None = None,
    ) -> str | _T:
        """Finds text for the first matching subelement, by tag name or path.

        Annotation
        ----------
        This overload handles the case where default value is given.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.findtext)
        """
    @overload
    def findtext(
        self,
        path: _t._ElemPathArg,
        default: None = None,
        namespaces: _t._StrOnlyNSMap | None = None,
    ) -> str | None:
        """Finds text for the first matching subelement, by tag name or path."

        Annotation
        ----------
        This overload handles the case where default value is not supplied.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.findtext)
        """
    def findall(
        self, path: _t._ElemPathArg, namespaces: _t._StrOnlyNSMap | None = None
    ) -> list[Self]:
        """Finds all matching subelements, by tag name or path.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.findall)
        """
    def iterfind(
        self, path: _t._ElemPathArg, namespaces: _t._StrOnlyNSMap | None = None
    ) -> Iterator[Self]:
        """Iterates over all matching subelements, by tag name or path.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.iterfind)
        """
    def xpath(
        self,
        _path: _t._TextArg,
        /,
        *,
        namespaces: _t._XPathNSArg | None = None,
        extensions: _t._XPathExtFuncArg | None = None,
        smart_strings: bool = True,
        **_variables: _t._XPathVarArg,
    ) -> _t._XPathObject:
        """Evaluate an xpath expression using the element as context node.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Element.xpath)
        """
    def cssselect(
        self,
        expr: str,
        *,
        translator: _CSSTransArg = "xml",
    ) -> list[Self]:
        """Run the CSS expression on this element and its children,
        returning a list of the results.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._Entity.cssselect)
        """
    @deprecated("Since v2.0 (2008); use list(element) or iterate over element")
    def getchildren(self) -> list[Self]: ...
    # Should have been overloaded for accuracy, but we can turn a blind eye
    # for something that is marked deprecated for 15 years
    @deprecated("Since v2.0 (2008); renamed to .iter()")
    def getiterator(
        self, tag: _t._TagSelector | None = None, *tags: _t._TagSelector
    ) -> Iterator[Self]: ...

Element: TypeAlias = _Element

_ET2_co = TypeVar("_ET2_co", bound=_Element, default=_Element, covariant=True)

# ET class notation is specialized, indicating the type of element
# it is holding (e.g. XML element, HTML element or Objectified
# Element).
# Although it is also possible to be an empty tree containing no
# element, the absolute majority of lxml API will fail to work.
# It is considered harmful to support such corner case, which
# adds much complexity without any benefit.
class _ElementTree(Generic[_t._ET_co]):
    @overload  # from element, parser ignored
    def __new__(
        cls,
        element: _t._ET_co,
        *,
        file: None = None,
    ) -> _ElementTree[_t._ET_co]: ...
    @overload  # from file source, standard parser
    def __new__(
        cls,
        element: None = None,
        *,
        file: _t._FileReadSource,
        parser: _t._DefEtreeParsers[_t._ET_co],
    ) -> _ElementTree[_t._ET_co]: ...
    @overload  # from file source, custom target parser
    def __new__(  # type: ignore[misc]
        cls,
        element: None = None,
        *,
        file: _t._FileReadSource,
        parser: CustomTargetParser[_T],
    ) -> _T: ...
    @overload  # from file source, no parser supplied
    def __new__(
        cls,
        element: None = None,
        *,
        file: _t._FileReadSource,
        parser: None = None,
    ) -> _ElementTree[_t._ET_co]: ...
    @property
    def parser(self) -> _t._DefEtreeParsers[_t._ET_co] | None: ...
    @property
    def docinfo(self) -> DocInfo: ...
    @overload  # common parser
    def parse(
        self,
        source: _t._FileReadSource,
        parser: _t._DefEtreeParsers[_ET2_co],
        *,
        base_url: str | bytes | None = None,
    ) -> _ET2_co:
        """Updates self with the content of source and returns its root.

        Annotation
        ----------
        This overload handles the case where a common parser is supplied.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.parse)
        """
    @overload  # custom target parser
    def parse(
        self,
        source: _t._FileReadSource,
        parser: CustomTargetParser[_ET2_co],
        *,
        base_url: str | bytes | None = None,
    ) -> _ET2_co:
        """Updates self with the content of source and returns its root.

        Annotation
        ----------
        This overload handles the case where a custom target parser is supplied.
        Note that target object must return an element, i.e. compatible with
        `etree.TreeBuilder`.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.parse)
        """
    @overload  # parser not supplied
    def parse(
        self,
        source: _t._FileReadSource,
        parser: None = None,
        *,
        base_url: str | bytes | None = None,
    ) -> _Element:
        """Updates self with the content of source and returns its root.

        Annotation
        ----------
        This overload handles the case where no parser is supplied (thus
        default parser is utilised).

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.parse)
        """
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
    @overload  # generic write methods
    def write(
        self,
        file: _t._FileWriteSource,
        *,
        encoding: str | None = None,  # unicode not allowed
        method: _t._OutputMethodArg = "xml",
        pretty_print: bool = False,
        xml_declaration: bool | None = None,
        with_tail: bool = True,
        standalone: bool | None = None,
        doctype: str | None = None,
        compression: int | None = 0,
    ) -> None:
        """Write the tree to a filename, file or file-like object.

        Annotation
        ----------
        This overload handles the most generic usage of method,
        where the `method` argument is `"xml"` (default value),
        `"html"` or `"text"`.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.write)
        """
    @overload  # method=c14n2
    def write(
        self,
        file: _t._FileWriteSource,
        *,
        method: Literal["c14n2"],
        with_comments: bool = True,
        compression: int | None = 0,
        strip_text: bool = False,
    ) -> None:
        """Write the tree to a filename, file or file-like object.

        Annotation
        ----------
        This overload handles the case where `method` is `"c14n2"`
        (Canonical XML version 2).

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.write)
        """
    @overload  # guard against plain str inclusive_ns_prefixes
    @deprecated(
        "'inclusive_ns_prefixes' should be an iterable even when "
        "just a single namespace prefix is included"
    )
    def write(
        self,
        file: _t._FileWriteSource,
        *,
        method: Literal["c14n"],
        exclusive: bool = False,
        with_comments: bool = True,
        compression: int | None = 0,
        inclusive_ns_prefixes: str | bytes,
    ) -> None:
        """Write the tree to a filename, file or file-like object.

        Annotation
        ----------
        This overload guards against using a plain string in
        `inclusive_ns_prefixes` argument which is only used in
        `method="c14n"` (Canonical XML version 1).

        If it is specified as a single string, it will be split
        as individual letter and each treated as a namespace
        prefix.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.write)
        """
    @overload  # method=c14n
    def write(
        self,
        file: _t._FileWriteSource,
        *,
        method: Literal["c14n"],
        exclusive: bool = False,
        with_comments: bool = True,
        compression: int | None = 0,
        inclusive_ns_prefixes: Iterable[str | bytes] | None = None,
    ) -> None:
        """Write the tree to a filename, file or file-like object.

        Annotation
        ----------
        This overload handles the case where `method` is `"c14n"`
        (Canonical XML version 1).

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.write)
        """
    @overload  # deprecated usage of docstring param
    @deprecated('Since v3.8.0; use "doctype" parameter instead')
    def write(
        self,
        *args: Any,
        docstring: str,
        **kw: Any,
    ) -> None:
        """Write the tree to a filename, file or file-like object.

        Annotation
        ----------
        This overload handles the deprecated usage of `docstring`
        parameter, which is replaced by `doctype` parameter.

        See Also
        --------
        - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree.write)
        """
    def getpath(self: _ElementTree[_t._ET], element: _t._ET) -> str: ...
    def getelementpath(self: _ElementTree[_t._ET], element: _t._ET) -> str: ...
    @overload
    def iter(self, *tags: _t._TagSelector) -> Iterator[_t._ET_co]: ...
    @overload
    def iter(
        self, tag: _t._TagSelector | Iterable[_t._TagSelector] | None = None
    ) -> Iterator[_t._ET_co]: ...
    #
    # ElementPath methods calls the same method on root node,
    # so signature should be the same as _Element ones
    #
    def find(
        self, path: _t._ElemPathArg, namespaces: _t._StrOnlyNSMap | None = None
    ) -> _t._ET_co | None: ...
    @overload
    def findtext(
        self,
        path: _t._ElemPathArg,
        *,
        namespaces: _t._StrOnlyNSMap | None = None,
    ) -> str | None: ...
    @overload
    def findtext(
        self,
        path: _t._ElemPathArg,
        default: _T,
        namespaces: _t._StrOnlyNSMap | None = None,
    ) -> str | _T: ...
    def findall(
        self, path: _t._ElemPathArg, namespaces: _t._StrOnlyNSMap | None = None
    ) -> list[_t._ET_co]: ...
    def iterfind(
        self, path: _t._ElemPathArg, namespaces: _t._StrOnlyNSMap | None = None
    ) -> Iterator[_t._ET_co]: ...
    def xpath(
        self,
        _path: _t._TextArg,
        /,
        *,
        namespaces: _t._XPathNSArg | None = None,
        extensions: _t._XPathExtFuncArg | None = None,
        smart_strings: bool = True,
        **_variables: _t._XPathVarArg,
    ) -> _t._XPathObject: ...
    def xslt(
        self,
        _xslt: _t._ElementOrTree,
        /,
        extensions: _t.SupportsLaxItems[tuple[str | bytes, str | bytes], XSLTExtension]
        | None = None,
        access_control: XSLTAccessControl | None = None,
        *,  # all keywords are passed to XSLT.__call__
        profile_run: bool = False,
        **__kw: _Stylesheet_Param,
    ) -> _XSLTResultTree: ...
    def relaxng(self, relaxng: _t._ElementOrTree) -> bool: ...
    def xmlschema(self, xmlschema: _t._ElementOrTree) -> bool: ...
    def xinclude(self) -> None: ...
    # Should have been overloaded for accuracy, but we can turn a blind eye
    # for something that is marked deprecated for 15 years
    @deprecated("Since v2.0 (2008); renamed to .iter()")
    def getiterator(
        self, tag: _t._TagSelector | None = None, *tags: _t._TagSelector
    ) -> Iterator[_t._ET_co]: ...
    @deprecated('Since v4.4; use .write() with method="c14n" argument')
    def write_c14n(
        self,
        file: _t._FileWriteSource,
        *,
        exclusive: bool = False,
        with_comments: bool = True,
        compression: int | None = 0,
        inclusive_ns_prefixes: Iterable[str | bytes] | None = None,
    ) -> None: ...

ElementTree: TypeAlias = _ElementTree

# Behaves like MutableMapping but deviates a lot in details
@final
class _Attrib:
    def __setitem__(self, __k: _t._AttrName, __v: _t._AttrVal) -> None: ...
    def __delitem__(self, __k: _t._AttrName) -> None: ...
    # _only_ checks for dict and _Attrib to do
    # .items() conversion, not any Mapping
    def update(
        self,
        sequence_or_dict: (
            _Attrib
            | dict[Any, Any]  # Compromise with MutableMapping key/val invariance
            | Iterable[tuple[_t._AttrName, _t._AttrVal]]
        ),
    ) -> None: ...
    # Signature is actually pop(self, key, *default), yet
    # followed by runtime check and raise exception if multiple
    # default argument is supplied.
    # get() is forgiving with non-existent key yet pop() isn't.
    @overload
    def pop(self, key: _t._AttrName) -> str: ...
    @overload
    def pop(self, key: _t._AttrName, default: _T, /) -> str | _T: ...
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
    # richcmp() dropped, mapping has no concept of inequality comparison

#
# Element types and content node types
#

#
# Mypy: Liskov!
# Lxml: No Liskov!
# Mypy: I am *THE* authority here!
# Lxml: I will *NEVER* submit to you! Fuck off!
# Mypy: Now die!
#
# So here we are.
#
# It is decided to not decouple other content only elements
# from _Element, even though their interfaces are vastly different
# from _Element. The notion of or'ing different kind of elements
# throughout all element methods would cause great inconvenience
# for me and all users alike -- using some _AnyHtmlElement alias
# to represent union of all elements was a failure for users.
# We opt for convenience and ease of use in the future.
class __ContentOnlyElement(_Element):
    #
    # Useful properties
    # .text and .tag are overridden in each concrete class below
    #
    @property
    def attrib(self) -> Mapping[_t.Unused, _t.Unused]: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    def get(self, key: _t.Unused, default: _t.Unused = None) -> None: ...  # type: ignore[override]
    def set(self, key: Never, value: Never) -> Never: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    def append(self, element: Never) -> Never: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    def insert(self, index: Never, value: Never) -> Never: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    def __setitem__(self, __k: Never, __v: Never) -> Never: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    # The intention is to discourage elem.__getitem__, allowing slice
    # argument in runtime doesn't make any sense
    def __getitem__(self, __k: Never) -> Never: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    # Methods above are explicitly defined in source, while those below aren't
    def __delitem__(self, __k: Never) -> Never: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
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
    def tag(self) -> Callable[..., _Comment]: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    @property  # type: ignore[override]
    def text(self) -> str: ...
    @text.setter  # type: ignore[override]
    def text(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, value: _t._TextArg | None
    ) -> None: ...

# signature of .get() for _PI and _Element are the same
class _ProcessingInstruction(__ContentOnlyElement):
    @property  # type: ignore[misc]
    def tag(self) -> Callable[..., _ProcessingInstruction]: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    @property  # type: ignore[override]
    def text(self) -> str: ...
    @text.setter  # type: ignore[override]
    def text(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, value: _t._TextArg | None
    ) -> None: ...
    @property
    def target(self) -> str: ...
    @target.setter
    def target(self, value: _t._TextArg) -> None: ...
    @property
    def attrib(self) -> dict[str, str]: ...  # type: ignore[override]

class _Entity(__ContentOnlyElement):
    @property  # type: ignore[misc]
    def tag(self) -> Callable[..., _Entity]: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    @property  # type: ignore[misc]
    def text(self) -> str: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    @property
    def name(self) -> str: ...
    @name.setter
    def name(self, value: _t._TextArg) -> None: ...
