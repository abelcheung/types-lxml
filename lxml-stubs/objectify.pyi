from _typeshed import _T
from abc import abstractmethod
from typing import Any, Callable, Iterable, Iterator, Literal, TypeVar, overload
from typing_extensions import LiteralString, Self, SupportsIndex

from . import etree
from ._types import SupportsLaxedItems, _AnyStr, _FileReadSource, _NSMapArg, _TagName

_DataElem_T = TypeVar("_DataElem_T", bound=ObjectifiedDataElement)

# Exported constants
__version__: LiteralString
PYTYPE_ATTRIBUTE: LiteralString

#
# ObjectifiedElement hierarchy
#

class ObjectifiedElement(etree.ElementBase):
    """Main XML Element class

    Original Docstring
    ------------------
    Element children are accessed as object attributes.  Multiple children
    with the same name are available through a list index.

    Note that you cannot (and must not) instantiate this class or its
    subclasses.

    Example
    -------

    ```pycon
    >>> root = XML("<root><c1><c2>0</c2><c2>1</c2></c1></root>")
    >>> second_c2 = root.c1.c2[1]
    >>> print(second_c2.text)
    1
    ```
    """
    @property  # type: ignore[misc]
    def text(self) -> str | None: ...  # Readonly, unlike _Element counterpart
    # value parameter accepts anything -- it is stringified before adding
    # to attribute
    def addattr(self, tag: _TagName, value: Any) -> None: ...
    def countchildren(self) -> int: ...
    def descendantpaths(self, prefix: str | list[str] | None = ...) -> list[str]: ...
    def getchildren(self) -> list[ObjectifiedElement]: ...
    def __iter__(self) -> Iterator[ObjectifiedElement]: ...
    def __reversed__(self) -> Iterator[ObjectifiedElement]: ...
    def __getattr__(self, __k: str) -> ObjectifiedElement: ...
    # TODO Check if _Element methods need overriding

class ObjectifiedDataElement(ObjectifiedElement):
    """The base class for all data type Elements

    Original Docstring
    ------------------
    Subclasses should override the `pyval` property and possibly
    the `__str__` method.
    """
    # In source code, .pyval return value is stated as str. However,
    # presence of the attribute is supposed to be protocol requirement
    # for subclasses, not that people are allowed to create
    # ObjectifiedDataElement themselves which return string value for .pyval .
    @property
    @abstractmethod
    def pyval(self) -> Any: ...
    def _setText(self, s: _AnyStr | etree.CDATA | None) -> None:
        """Modify text content of objectified element directly.

        Original Docstring
        ------------------
        For use in subclasses only. Don't use unless you know what you are
        doing.
        """
    def _setValueParser(self, function: Callable[[Any], Any]) -> None:
        """Set the function that parses the Python value from a string

        Annotation notice
        -----------------
        This func originates from an abstract subclass of data element
        called `NumberElement`. Since there is no intention to construct
        such class in type annotation (yet?), the function is placed here.

        Original Docstring
        ------------------
        Do not use this unless you know what you are doing.
        """

# Forget about LongElement, which is only for Python 2.x.
#
# These data elements emulate native python data type operations,
# but lack all non-dunder methods. Too lazy to write all dunders
# one by one; directly inheriting from int and float is much more
# succint. Some day, maybe. (See known bug in BoolElement)
#
# Not doing the same for StringElement and BoolElement though,
# each for different reason.
class IntElement(ObjectifiedDataElement, int):
    @property
    def pyval(self) -> int: ...
    @property  # type: ignore[misc]
    def text(self) -> str: ...  # type: ignore[override]

class FloatElement(ObjectifiedDataElement, float):
    @property
    def pyval(self) -> float: ...
    @property  # type: ignore[misc]
    def text(self) -> str: ...  # type: ignore[override]

class StringElement(ObjectifiedDataElement):
    """String data class

    Note that this class does *not* support the sequence protocol of strings:
    `len()`, `iter()`, `str_attr[0]`, `str_attr[0:1]`, etc. are *not* supported.
    Instead, use the `.text` attribute to get a 'real' string.
    """
    # For empty string element, .pyval = __str__ = '', .text = None
    @property
    def pyval(self) -> str: ...
    def strlen(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __ge__(self, other: Self | str) -> bool: ...
    def __gt__(self, other: Self | str) -> bool: ...
    def __le__(self, other: Self | str) -> bool: ...
    def __lt__(self, other: Self | str) -> bool: ...
    # Stringify any object before concat
    def __add__(self, other: Any) -> str: ...
    def __radd__(self, other: Any) -> str: ...
    def __mul__(self, other: SupportsIndex) -> str: ...
    def __rmul__(self, other: SupportsIndex) -> str: ...
    @overload
    def __mod__(
        self, other: LiteralString | tuple[LiteralString, ...]
    ) -> LiteralString: ...
    @overload
    def __mod__(self, other: Any) -> str: ...
    def __float__(self) -> float: ...
    def __int__(self) -> int: ...
    def __complex__(self) -> complex: ...

class NoneElement(ObjectifiedDataElement):
    @property
    def pyval(self) -> None: ...
    @property  # type: ignore[misc]
    def text(self) -> None: ...  # type: ignore[override]
    def __bool__(self) -> Literal[False]: ...

# BoolElement can't inherit from bool, which is marked @final
class BoolElement(IntElement):
    @property
    def pyval(self) -> bool: ...
    @property  # type: ignore[misc]
    def text(self) -> str: ...  # type: ignore[override]
    def __bool__(self) -> bool: ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    @overload
    def __and__(self, __n: bool | BoolElement) -> bool: ...
    @overload
    def __and__(self, __n: int) -> int: ...
    @overload
    def __or__(self, __n: bool | BoolElement) -> bool: ...
    @overload
    def __or__(self, __n: int) -> int: ...
    @overload
    def __xor__(self, __n: bool | BoolElement) -> bool: ...
    @overload
    def __xor__(self, __n: int) -> int: ...
    # BUG Under current implementation, reverse boolean operators
    # won't work. BoolElement is considered as int
    # (BoolElement -> IntElement -> int), and the result of
    # (bool <op> BoolElement) is always int. Besides, native bool
    # is marked @final, so the reverse operators can't be
    # overrided. This is only fixable if IntElement is decoupled
    # from int.

#
# Pytype management and annotation
#
class PyType:
    """User defined type

    Origianl Docstring
    ------------------
    Named type that contains a type check function, a type class that
    inherits from `ObjectifiedDataElement` and an optional "stringification"
    function.  The type check must take a string as argument and raise
    `ValueError` or `TypeError` if it cannot handle the string value.  It may be
    None in which case it is not considered for type guessing.  For registered
    named types, the 'stringify' function (or `unicode()` if None) is used to
    convert a Python object with type name 'name' to the string representation
    stored in the XML tree.

    Note that the order in which types are registered matters.  The first
    matching type will be used.

    Example
    -------
    ```python
    PyType('int', int, MyIntClass).register()
    ```

    See Also
    --------
    - [lxml "Python data types" documentation](https://lxml.de/objectify.html#python-data-types)
    """
    @property  # tired of dealing with bytes
    def xmlSchemaTypes(self) -> list[str]: ...
    @xmlSchemaTypes.setter
    def xmlSchemaTypes(self, types: Iterable[str]) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def type_check(self) -> Callable[[Any], None]: ...
    @property
    def stringify(self) -> Callable[[Any], str]: ...
    def __init__(
        self,
        name: _AnyStr,
        type_check: Callable[[Any], None] | None,
        type_class: type[ObjectifiedDataElement],
        stringify: Callable[[Any], str] | None = ...,
    ) -> None: ...
    def register(
        self,
        before: Iterable[str] | None = ...,
        after: Iterable[str] | None = ...,
    ) -> None: ...
    def unregister(self) -> None: ...

def set_pytype_attribute_tag(attribute_tag: str | None = ...) -> None:
    """Change name and namespace of the XML attribute that holds Python
    type information

    Original Docstring
    ------------------
    Do not use this unless you know what you are doing.

    Parameters
    ----------
    attribute_tag: str, optional
        Clark notation namespace and tag of `pytype` attribute. Default is None,
        which means the default value
        `"{http://codespeak.net/lxml/objectify/pytype}pytype"`
    """
def pytypename(obj: object) -> str:
    """Find the name of the corresponding PyType for a Python object"""
def getRegisteredTypes() -> list[PyType]:
    """Returns a list of the currently registered PyType objects

    Original Docstring
    ------------------
    To add a new type, retrieve this list and call `unregister()` for all
    entries.  Then add the new type at a suitable position (possibly replacing
    an existing one) and call `register()` for all entries.

    This is necessary if the new type interferes with the type check functions
    of existing ones (normally only int/float/bool) and must the tried before
    other types.  To add a type that is not yet parsable by the current type
    check functions, you can simply `register()` it, which will append it to the
    end of the type list.
    """
def pyannotate(
    element_or_tree: etree._ElementOrAnyTree,
    *,
    ignore_old: bool = ...,
    ignore_xsi: bool = ...,
    empty_pytype: _AnyStr | None = ...,
) -> None:
    """Recursively annotates elements of an XML tree with `py:pytype` attributes

    Parameters
    ----------
    element_or_tree: `_Element` or `_ElementTree`
        The XML Element or XML Tree to be precessed
    ignore_old: bool, optional
        If True, current `py:pytype` attributes will always be replaced.
        Otherwise, they will be checked and only replaced if they no longer
        fit the current text value. Default is False, which means checking is done.
    ignore_xsi: bool, optional
        If True, `xsi:type` annotations are completely ignored during element
        type determination. If False (which is default), use them as initial hint.
    empty_pytype: str or bytes, optioanl
        Sets the default pytype annotation of empty elements. Pass 'str',
        for example, to annotate them as string elements. Default is None,
        which means not to process empty elements at all.
    """
def xsiannotate(
    element_or_tree: etree._ElementOrAnyTree,
    *,
    ignore_old: bool = ...,
    ignore_pytype: bool = ...,
    empty_type: _AnyStr | None = ...,
) -> None:
    """Recursively annotates elements of an XML tree with `xsi:type` attributes

    Note that the mapping from Python types to XSI types is usually ambiguous.
    Currently, only the first XSI type name in the corresponding PyType
    definition will be used for annotation.  Thus, you should consider naming
    the widest type first if you define additional types.

    Parameters
    ----------
    element_or_tree: `_Element` or `_ElementTree`
        The XML Element or XML Tree to be precessed
    ignore_old: bool, optional
        If True, current `xsi:type` attributes will always be replaced.
        Otherwise, they will be checked and only replaced if they no longer
        fit the current text value. Default is False, which means checking is done.
    ignore_pytype:
        If True, `py:pytype` annotations are completely ignored during element
        type determination. If False (which is default), use them as initial hint.
    empty_pytype: str or bytes, optioanl
        Sets the default `xsi:type` attribute of empty elements.
        Pass 'string', for example, to annotate them as string elements. Default
        is None, which means not to process empty elements at all. In particular,
        `xsi:nil` attribute is not added.
    """
def annotate(
    element_or_tree: etree._ElementOrAnyTree,
    *,
    ignore_old: bool = ...,
    ignore_xsi: bool = ...,
    empty_pytype: _AnyStr | None = ...,
    empty_type: _AnyStr | None = ...,
    annotate_xsi: bool = ...,
    annotate_pytype: bool = ...,
) -> None:
    """Recursively annotates elements of an XML tree with `py:pytype`
    and/or `xsi:type` attributes

    Annotation notice
    -----------------
    This function serves as a basis of both `pyannotate()` and
    `xsiannotate()` functions. Beware that `annotate_xsi` and
    `annotate_pytype` parameter type deviates from documentation,
    which is marked as having default value 0 and 1 respectively.
    The underlying internal function uses type `bint` (which means
    bool for Cython). The parameters do act as feature on/off toggle.

    Parameters
    ----------
    element_or_tree: `_Element` or `_ElementTree`
        The XML Element or XML Tree to be precessed
    ignore_old: bool, optional
        If True, current `py:pytype` attributes will always be replaced.
        Otherwise, they will be checked and only replaced if they no longer
        fit the current text value. Default is False, which means checking is done.
    ignore_xsi: bool, optional
        If True, `xsi:type` annotations are completely ignored during element
        type determination. If False (which is default), use them as initial hint.
    empty_pytype: str or bytes, optioanl
        Sets the default pytype annotation of empty elements. Pass `str`,
        for example, to annotate them as string elements. Default is None,
        which means not to process empty elements at all.
    empty_type: str or bytes, optioanl
        Sets the default `xsi:type` annotation of empty elements. Pass `string`,
        for example, to annotate them as string elements. Default is None,
        which means not to process empty elements at all.
    annotate_xsi: bool, optional
        Determines if `xsi:type` annotations would be updated or created,
        default is no (False).
    annotate_pytype: bool, optional
        Determines if `py:pytype` annotations would be updated or created,
        default is yes (True).
    """
def deannotate(
    element_or_tree: etree._ElementOrAnyTree,
    *,
    pytype: bool = ...,
    xsi: bool = ...,
    xsi_nil: bool = ...,
    cleanup_namespaces: bool = ...,
) -> None:
    """Recursively de-annotate elements of an XML tree

    This is achieved by removing `py:pytype`, `xsi:type` and/or `xsi:nil` attributes.

    Parameters
    ----------
    element_or_tree: `_Element` or `_ElementTree`
        The XML Element or XML Tree to be precessed
    pytype: bool, optional
        Whether `py:pytype` attributes should be removed, default is True
    xsi: bool, optional
        Whether `xsi:type` attributes should be removed, default is True
    xsi_nil: bool, optional
        Whether `xsi:nil` attributes should be removed, default is False
    cleanup_namespaces: bool, optional
        Controls if unused namespace declarations should be removed from
        XML tree, default is False
    """

#
# Element factories
#

def Element(
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: str | None = ...,
    **__attr: _AnyStr,
) -> ObjectifiedElement:
    """Objectify specific version of `lxml.etree` `Element()` factory

    Original Docstring
    ------------------
    Requires parser based element class lookup activated in `lxml.etree`!

    Parameters
    ----------
    _tag : str, bytes or QName
        Element tag name
    attrib : mapping of string key/value, optional
        Attributes to be added to element. Default is None.
    nsmap : mapping of namespace prefix/URI, optional
        Extra namespaces added to element. Default is None.
    _pytype : str | None, optional
        The `pytype` to be used for this element. Default is None, which implies
        no pytype annotation would be added to inner tree element. See `PyType`
        class docstring for more info.

    Returns
    -------
    ObjectifiedElement
        The generated element.
    """
def SubElement(
    _parent: ObjectifiedElement,
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **__attr: _AnyStr,
) -> ObjectifiedElement: ...

# TODO Current overload situation is unsatisfactory. Will decide
# whether the list should be trimmed or extended in future.
#
# XXX Order matters! float can't be listed before int
#
@overload  # DataElement retains same type if no other hint given
def DataElement(
    _value: _DataElem_T,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: None = ...,
    _xsi: None = ...,
    **__attr: _AnyStr,
) -> _DataElem_T: ...
@overload  # native type None
def DataElement(
    _value: None,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: None = ...,
    _xsi: None = ...,
    **__attr: _AnyStr,
) -> NoneElement: ...
@overload  # native type str
def DataElement(
    _value: str,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: None = ...,
    _xsi: None = ...,
    **__attr: _AnyStr,
) -> StringElement: ...
@overload  # native type bool
def DataElement(
    _value: bool,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: None = ...,
    _xsi: None = ...,
    **__attr: _AnyStr,
) -> BoolElement: ...
@overload  # native type int
def DataElement(
    _value: int,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: None = ...,
    _xsi: None = ...,
    **__attr: _AnyStr,
) -> IntElement: ...
@overload  # native type float
def DataElement(
    _value: float,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: None = ...,
    _xsi: None = ...,
    **__attr: _AnyStr,
) -> FloatElement: ...
@overload  # pytype None
def DataElement(
    _value: Any,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: Literal["NoneType", "none"],
    _xsi: str | None = ...,
    **__attr: _AnyStr,
) -> NoneElement: ...
@overload  # pytype str
def DataElement(
    _value: Any,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: Literal["str"],
    _xsi: str | None = ...,
    **__attr: _AnyStr,
) -> StringElement: ...
@overload  # pytype bool
def DataElement(
    _value: Any,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: Literal["bool"],
    _xsi: str | None = ...,
    **__attr: _AnyStr,
) -> BoolElement: ...
@overload  # pytype int
def DataElement(
    _value: Any,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: Literal["int"],
    _xsi: str | None = ...,
    **__attr: _AnyStr,
) -> IntElement: ...
@overload  # pytype float
def DataElement(
    _value: Any,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: Literal["float"],
    _xsi: str | None = ...,
    **__attr: _AnyStr,
) -> FloatElement: ...
@overload  # Generic fallback
def DataElement(
    _value: Any,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    *,
    _pytype: str | None = ...,
    _xsi: str | None = ...,
    **__attr: _AnyStr,
) -> ObjectifiedElement:
    """Create a new element from a Python value and XML attributes taken
    from keyword arguments or a dictionary passed as second argument.

    Annotation notice
    -----------------
    1. Current DataElement stub overloads only represent cases where
    data type is inferred from value or from lxml's own PyType arg.
    If XMLSchema Interface types are involved, the overload list
    will become unbearably long (well, it alreaday is), which is
    both a nightmare for maintainer and users alike. As a result,
    please read description of `_xsi` parameter carefully
    before using, which is not covered in original docstring.

    2. `DataElement()` allows a special case handling: if value
    is an `ObjectifiedElement` (not data element), AND no other
    arguments are supplied, simply return a copy of itself.
    Such silly usage is ignored here, when `copy.copy(element)`
    already suffices.

    Original Docstring
    ------------------
    Automatically guesses `py:pytype` attribute from basic Python data type of
    the value if it can be identified.  If `_pytype` or `_xsi` are among the
    keyword arguments, they will be used instead of auto detection.

    If the `_value` argument is an `ObjectifiedDataElement` instance,
    its `py:pytype`, `xsi:type`, `nsmap` and other attributes are
    reused unless redefined in attrib and/or keyword arguments.

    See Also
    --------
    - [XMLSchema Instances data types](https://www.w3.org/TR/2004/REC-xmlschema-2-20041028/datatypes.html)
    - [How lxml determines data type](https://lxml.de/objectify.html#how-data-types-are-matched)

    Parameters
    ----------
    _value : Any
        The value to be used in new element
    attrib : mapping of str to str, optional
        Attributes to be added to element, by default `None`.
        Usually specified as a `dict` or lxml's own `_Attrib`.
    nsmap : mapping of str to str, optional
        Mapping of namespace prefixes to URI. Default is `None`, which uses
        lxml's internal mapping.
    _pytype : str, keyword, optional
        Coerce value into specified data type, such as `"int"` or `"bool"`.
        Default is `None`, which means data type is autodetected by other
        mechanisms.
    _xsi : str, keyword, optional
        lxml can use XMLSchema Instances data types to help guessing correct
        pytype (see previous parameter). Some of the XSI data types
        can be used, and the `nsd:` namespace prefix is optional.
        Beware that this argument becomes a dummy if `_pytype` argument
        is specified, yet still would be present in element, even if it's
        wrong or can't be resolved. Default is `None`, which means
        XSI data type is not involved in type determination.
    """

class ElementMaker:
    """Used for constructing trees

    Note that this module has a predefined `ElementMaker` instance called `E`.

    Example
    -------

    ```pycon
    >>> M = ElementMaker(annotate=False)
    >>> attributes = {'class': 'par'}
    >>> html = M.html( M.body( M.p('hello', attributes, M.br, 'objectify', style="font-weight: bold") ) )

    >>> from lxml.etree import tostring
    >>> print(tostring(html, method='html').decode('ascii'))
    <html><body><p style="font-weight: bold" class="par">hello<br>objectify</p></body></html>
    ```

    To create tags that are not valid Python identifiers, call the factory
    directly and pass the tag name as first argument::

    ```pycon
    >>> root = M('tricky-tag', 'some text')
    >>> print(root.tag)
    tricky-tag
    >>> print(root.text)
    some text
    ```
    """
    def __init__(
        self,
        *,
        namespace: str | None = ...,
        nsmap: _NSMapArg | None = ...,
        annotate: bool = ...,
        makeelement: etree._ElemFactory[ObjectifiedElement] | None = ...,
    ) -> None: ...
    def __call__(
        self,
        tag: str,
        *args: Any,
        **kwargs: Any,
    ) -> ObjectifiedElement: ...
    def __getattr__(self, tag: str) -> etree._ElemFactory[ObjectifiedElement]: ...

E: ElementMaker

#
# Dumping tree and class lookup
#

def enable_recursive_str(on: bool) -> None:
    """Enable a recursively generated tree representation for
    `str(element)`, based on `objectify.dump(element)`"""
def dump(element: ObjectifiedElement) -> str:
    """Return a recursively generated string representation of an element"""
class ObjectifyElementClassLookup(etree.ElementClassLookup):
    """Element class lookup method that uses the objectify classes"""

    def __init__(
        self,
        tree_class: type[ObjectifiedElement] | None = ...,
        empty_data_class: type[ObjectifiedDataElement] | None = ...,
    ) -> None:
        """
        Parameters
        ----------
        tree_class : `type[ObjectifiedElement]`, optional
            Defines inner tree classes; it can be replaced by subclass of
            `ObjectifiedElement`. Default is None, which implies `ObjectifiedElement`.
        empty_data_class : `type[ObjectifiedDataElement]`, optional
            Defines the default class for empty data elements. Any existing
            or custom `ObjectifiedDataElement` subclass can be used.
            Default is `None`, which implies `StringElement`.
        """

#
# Parser and parsing
#

def set_default_parser(
    # Not joking, it uses isinstance check
    new_parser: etree.XMLParser[ObjectifiedElement] | None = ...,
) -> None:
    """Replace the default parser used by objectify's `Element()`
    and `fromstring()` functions.

    Parameters
    ----------
    new_parser: `etree.XMLParser`, optional
        The new parser intended to replace the default one. If not
        specified, defaults to `None`, which means reverting to
        original parser.
    """
def makeparser(
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
) -> etree.XMLParser[ObjectifiedElement]:
    """Create a new XML parser for objectify trees.

    Original Docstring
    ------------------
    You can pass all keyword arguments that are supported by
    `etree.XMLParser()`.  Note that this parser defaults to
    removing blank text.  You can disable this by passing the
    `remove_blank_text` boolean keyword option yourself.
    """
def parse(
    source: _FileReadSource,
    parser: etree._parser._DefEtreeParsers[ObjectifiedElement] | None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> etree._ElementTree[ObjectifiedElement]:
    """Parse a file or file-like object with objectify parser

    Parameters
    ----------
    parser: `etree.XMLParser` or `etree.HTMLParser`, optional
        Using different parser is allowed. If not specified, default
        value is `None`, which means using `objectify` module's internal
        default parser.
    base_url: str or bytes, optional
        Allows setting a URL for the document when parsing from a file-like
        object. This is needed when looking up external entities
        (DTD, XInclude, ...) with relative paths.
    """
def fromstring(
    xml: _AnyStr,
    parser: etree._parser._DefEtreeParsers[ObjectifiedElement] | None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> ObjectifiedElement:
    """Variant of corresponding `lxml.etree` function that uses objectify parser

    Parameters
    ----------
    parser: `etree.XMLParser` or `etree.HTMLParser`, optional
        Using different parser is allowed. If not specified, default
        value is `None`, which means using `objectify` module's internal
        default parser.
    base_url: str or bytes, optional
        Allows setting a URL for the document when parsing from a file-like
        object. This is needed when looking up external entities
        (DTD, XInclude, ...) with relative paths.
    """

XML = fromstring

#
# ObjectPath -- only used within lxml.objectify
# lxml's own invention that behaves somewhat like Element Path
# https://lxml.de/objectify.html#objectpath
#
class ObjectPath:
    """`objectify`'s own path language

    This path language is modelled similar to lxml's `ETXPath`,
    but with object-like notation. Instances of this class represent
    a compiled object path.

    Example
    -------
    `root.child[1].{other}child[25]`

    See Also
    --------
    - [Web documentation](https://lxml.de/objectify.html#objectpath)
    """
    def __init__(self, path: str | Iterable[str]) -> None: ...
    @overload
    def __call__(self, root: etree._ET) -> etree._ET: ...
    @overload
    def __call__(self, root: etree._ET, _default: _T) -> etree._ET | _T: ...
    find = __call__
    def hasattr(self, root: etree._Element) -> bool: ...
    def setattr(self, root: etree._Element, value: Any) -> None: ...
    def addattr(self, root: etree._Element, value: Any) -> None: ...
