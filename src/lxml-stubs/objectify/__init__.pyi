import sys
from typing import Final

from ._annotate import (
    PyType as PyType,
    annotate as annotate,
    deannotate as deannotate,
    getRegisteredTypes as getRegisteredTypes,
    pyannotate as pyannotate,
    pytypename as pytypename,
    set_pytype_attribute_tag as set_pytype_attribute_tag,
    xsiannotate as xsiannotate,
)
from ._element import (
    BoolElement as BoolElement,
    FloatElement as FloatElement,
    IntElement as IntElement,
    NoneElement as NoneElement,
    NumberElement as NumberElement,
    ObjectifiedDataElement as ObjectifiedDataElement,
    ObjectifiedElement as ObjectifiedElement,
    StringElement as StringElement,
)
from ._factory import (
    DataElement as DataElement,
    E as E,
    Element as Element,
    ElementMaker as ElementMaker,
    SubElement as SubElement,
)
from ._misc import (
    XML as XML,
    ObjectifyElementClassLookup as ObjectifyElementClassLookup,
    ObjectPath as ObjectPath,
    dump as dump,
    enable_recursive_str as enable_recursive_str,
    fromstring as fromstring,
    makeparser as makeparser,
    parse as parse,
    set_default_parser as set_default_parser,
)

if sys.version_info >= (3, 11):
    from typing import LiteralString
else:
    from typing_extensions import LiteralString

# Exported constants
__version__: Final[LiteralString]
PYTYPE_ATTRIBUTE: Final[LiteralString]

__all__ = [
    "BoolElement",
    "DataElement",
    "E",
    "Element",
    "ElementMaker",
    "FloatElement",
    "IntElement",
    "NoneElement",
    "NumberElement",
    "ObjectPath",
    "ObjectifiedDataElement",
    "ObjectifiedElement",
    "ObjectifyElementClassLookup",
    "PYTYPE_ATTRIBUTE",
    "PyType",
    "StringElement",
    "SubElement",
    "XML",
    "annotate",
    "deannotate",
    "dump",
    "enable_recursive_str",
    "fromstring",
    "getRegisteredTypes",
    "makeparser",
    "parse",
    "pyannotate",
    "pytypename",
    "set_default_parser",
    "set_pytype_attribute_tag",
    "xsiannotate",
]
