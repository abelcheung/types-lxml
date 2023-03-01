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
    def _setText(self, s: _AnyStr | etree.CDATA | None) -> None: ...

class ObjectifiedDataElement(ObjectifiedElement):
    @property
    @abstractmethod
    def pyval(self) -> Any: ...
    def _setValueParser(self, function: Callable[[Any], Any]) -> None: ...

# Forget about LongElement, which is only for Python 2.x.
#
# These data elements emulate native python data type operations,
# but lack all non-dunder methods. Too lazy to write all dunders
# one by one; directly inheriting from int and float is much more
# succint. Some day, maybe.
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

# StringElement is incompatible with str for some behavior;
# see objectify.pyx source for more info.
class StringElement(ObjectifiedDataElement):
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

def set_pytype_attribute_tag(attribute_tag: str | None = ...) -> None: ...
def pytypename(obj: object) -> str: ...
def getRegisteredTypes() -> list[PyType]: ...
def pyannotate(
    element_or_tree: etree._ElementOrAnyTree,
    *,
    ignore_old: bool = ...,
    ignore_xsi: bool = ...,
    empty_pytype: _AnyStr | None = ...,
) -> None: ...
def xsiannotate(
    element_or_tree: etree._ElementOrAnyTree,
    *,
    ignore_old: bool = ...,
    ignore_pytype: bool = ...,
    empty_type: _AnyStr | None = ...,
) -> None: ...
def annotate(
    element_or_tree: etree._ElementOrAnyTree,
    *,
    ignore_old: bool = ...,
    ignore_xsi: bool = ...,
    empty_pytype: _AnyStr | None = ...,
    empty_type: _AnyStr | None = ...,
    annotate_xsi: bool = ...,
    annotate_pytype: bool = ...,
) -> None: ...
def deannotate(
    element_or_tree: etree._ElementOrAnyTree,
    *,
    pytype: bool = ...,
    xsi: bool = ...,
    xsi_nil: bool = ...,
    cleanup_namespaces: bool = ...,
) -> None: ...

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
) -> ObjectifiedElement: ...
def SubElement(
    _parent: ObjectifiedElement,
    _tag: _TagName,
    /,
    attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
    nsmap: _NSMapArg | None = ...,
    **__attr: _AnyStr,
) -> ObjectifiedElement: ...

# lxml promotes its own pytype prefix over xsi/xsd types.
# https://lxml.de/objectify.html#how-data-types-are-matched
# If pytype is specified, xsi argument is completely ignored.
#
# TODO Current DataElement stub overloads only represent cases where
# data type is inferred from value or from lxml's own PyType arg.
# If XMLSchema Interface types are involved, the overload list
# will become unbearably long (well, it alreaday is), which is
# both a nightmare for maintainer and users alike.
# See if this decision needs to be reconsidered in future.
#
# DataElement() allows a special case handling: if value
# is an ObjectifiedElement (not data element), AND no other
# arguments are supplied, simply return a copy of itself.
# Totally ignore such silly usage, when copy.copy(element) suffices.
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
    """Create a new element from a Python value and XML attributes taken from
    keyword arguments or a dictionary passed as second argument.

    Automatically guesses ``pytype`` attribute from basic Python data type of
    the value if it can be identified.  If ``_pytype`` or ``_xsi`` are among the
    keyword arguments, they will be used instead of auto detection.

    If the ``_value`` argument is an ``ObjectifiedDataElement`` instance,
    its ``py:pytype``, ``xsi:type``, ``nsmap`` and other attributes are
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
        Attributes to be added to element, by default ``None``.
        Usually specified as a ``dict`` or lxml's own ``_Attrib``.
    nsmap : mapping of str to str, optional
        Mapping of namespace prefixes to URI. Default is ``None``, which uses
        lxml's internal mapping.
    _pytype : str, keyword, optional
        Coerce value into specified data type, such as ``"int"`` or ``"bool"``.
        Default is ``None``, which means data type is autodetected by other
        mechanisms.
    _xsi : str, keyword, optional
        lxml can use XMLSchema Instances data types to help guessing correct
        pytype (see previous parameter). Some of the XSI data types
        can be used, and the ``nsd:`` namespace prefix is optional.
        Beware that this argument becomes a dummy if ``_pytype`` argument
        is specified, yet still would be present in element, even if it's
        wrong or can't be resolved. Default is ``None``, which means
        XSI data type is not involved in type determination.
    """

class ElementMaker:
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

def enable_recursive_str(on: bool) -> None: ...
def dump(element: ObjectifiedElement) -> str: ...

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
        tree_class : ``type[ObjectifiedElement]``, optional
            Defines inner tree classes; it can be replaced by subclass of
            ``ObjectifiedElement``. Default is None, which implies ``ObjectifiedElement``.
        empty_data_class : ``type[ObjectifiedDataElement]``, optional
            Defines the default class for empty data elements. Any existing
            or custom ``ObjectifiedDataElement`` subclass can be used.
            Default is ``None``, which implies ``StringElement``.
        """

#
# Parser and parsing
#

def set_default_parser(
    new_parser: etree.XMLParser[ObjectifiedElement] | None = ...,
) -> None: ...
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
) -> etree.XMLParser[ObjectifiedElement]: ...
def parse(
    source: _FileReadSource,
    parser: etree.XMLParser[ObjectifiedElement] | None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> etree._ElementTree[ObjectifiedElement]: ...
def fromstring(
    xml: _AnyStr,
    parser: etree.XMLParser[ObjectifiedElement] | None = ...,
    *,
    base_url: _AnyStr | None = ...,
) -> ObjectifiedElement: ...

XML = fromstring

#
# ObjectPath -- only used within lxml.objectify
# lxml's own invention that behaves somewhat like Element Path
# https://lxml.de/objectify.html#objectpath
#
class ObjectPath:
    def __init__(self, path: str | Iterable[str]) -> None: ...
    @overload
    def __call__(self, root: etree._ET) -> etree._ET: ...
    @overload
    def __call__(self, root: etree._ET, *_default: _T) -> etree._ET | _T: ...
    find = __call__
    def hasattr(self, root: etree._Element) -> bool: ...
    def setattr(self, root: etree._Element, value: Any) -> None: ...
    def addattr(self, root: etree._Element, value: Any) -> None: ...
