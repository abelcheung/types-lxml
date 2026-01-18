#
# Parsing and other module level functions
#

from collections.abc import Iterable
from typing import Literal, TypeVar, overload
from typing_extensions import disjoint_base

from .. import etree
from .._types import (
    _DefEtreeParsers,
    _FileReadSource,
    _TextArg,
)
from ._element import ObjectifiedDataElement, ObjectifiedElement

_T = TypeVar("_T")

#
# Dumping tree and class lookup
#

def enable_recursive_str(on: bool = True) -> None:
    """Enable a recursively generated tree representation for `str(element)`.

    This uses `objectify.dump(element)` for the tree representation.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.enable_recursive_str)
    """

def dump(element: ObjectifiedElement) -> str:
    """Return a recursively generated string representation of an element.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.dump)
    """

@disjoint_base
class ObjectifyElementClassLookup(etree.ElementClassLookup):
    """Element class lookup method that uses the objectify classes.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.ObjectifyElementClassLookup)
    """

    def __init__(
        self,
        tree_class: type[ObjectifiedElement] | None = None,
        empty_data_class: type[ObjectifiedDataElement] | None = None,
    ) -> None: ...

#
# Parser and parsing
#

def set_default_parser(
    # Not joking, it uses isinstance check
    new_parser: etree.XMLParser[ObjectifiedElement] | None = None,
) -> None:
    """Replace the default parser used by objectify's `Element()` and `fromstring()` functions.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.set_default_parser)
    """

# All XMLParser() arguments, except that remove_black_text
# default value is True
def makeparser(
    *,
    encoding: _TextArg | None = None,
    attribute_defaults: bool = False,
    dtd_validation: bool = False,
    load_dtd: bool = False,
    no_network: bool = True,
    ns_clean: bool = False,
    recover: bool = False,
    schema: etree.XMLSchema | None = None,
    huge_tree: bool = False,
    remove_blank_text: bool = True,
    resolve_entities: bool | Literal["internal"] = "internal",
    remove_comments: bool = False,
    remove_pis: bool = False,
    strip_cdata: bool = True,
    collect_ids: bool = True,
    compact: bool = True,
) -> etree.XMLParser[ObjectifiedElement]:
    """Create a new XML parser for objectify trees.

    You can pass all keyword arguments that are supported by `etree.XMLParser()`.
    Note that this parser defaults to removing blank text. You can disable this
    by passing the `remove_blank_text` boolean keyword option.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.makeparser)
    """

def parse(
    f: _FileReadSource,
    parser: _DefEtreeParsers[ObjectifiedElement] | None = None,
    *,
    base_url: str | bytes | None = None,
) -> etree._ElementTree[ObjectifiedElement]:
    """Parse a file or file-like object with objectify parser.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.parse)
    """

def fromstring(
    xml: str | bytes,
    parser: _DefEtreeParsers[ObjectifiedElement] | None = None,
    *,
    base_url: str | bytes | None = None,
) -> ObjectifiedElement:
    """Variant of corresponding `lxml.etree` function that uses objectify parser.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.fromstring)
    """

XML = fromstring

# Not using ._types._ET, which supports PEP 696, but causes
# problem in 2nd overload of ObjectPath.__call__()
# if _ET has a default type, then all subsequent argument
# TypeVars need default type too (namely, _default: _T)
_ET = TypeVar("_ET", bound=etree._Element)

#
# ObjectPath -- only used within lxml.objectify
# lxml's own invention that behaves somewhat like Element Path
# https://lxml.de/objectify.html#objectpath
#
@disjoint_base
class ObjectPath:
    """Objectify's own path language.

    This path language is modelled similar to lxml's `ETXPath`,
    but with object-like notation. Instances of this class represent
    a compiled object path.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.ObjectPath)
    """

    def __init__(self, path: str | Iterable[str]) -> None: ...
    @overload
    def __call__(self, root: _ET) -> _ET: ...
    @overload
    def __call__(self, root: _ET, _default: _T) -> _ET | _T: ...
    find = __call__
    def hasattr(self, root: etree._Element) -> bool: ...
    def setattr(self, root: etree._Element, value: object) -> None: ...
    def addattr(self, root: etree._Element, value: object) -> None: ...
