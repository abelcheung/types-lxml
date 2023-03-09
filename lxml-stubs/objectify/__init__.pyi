from typing_extensions import LiteralString

from ._element import (
    ObjectifiedElement as ObjectifiedElement,
    ObjectifiedDataElement as ObjectifiedDataElement,
    IntElement as IntElement,
    FloatElement as FloatElement,
    StringElement as StringElement,
    NoneElement as NoneElement,
    BoolElement as BoolElement,
)

from ._annotate import (
    PyType as PyType,
    set_pytype_attribute_tag as set_pytype_attribute_tag,
    pytypename as pytypename,
    getRegisteredTypes as getRegisteredTypes,
    pyannotate as pyannotate,
    xsiannotate as xsiannotate,
    annotate as annotate,
    deannotate as deannotate,
)

from ._factory import (
    Element as Element,
    SubElement as SubElement,
    DataElement as DataElement,
    ElementMaker as ElementMaker,
    E as E,
)

from ._misc import (
    enable_recursive_str as enable_recursive_str,
    dump as dump,
    ObjectifyElementClassLookup as ObjectifyElementClassLookup,
    set_default_parser as set_default_parser,
    makeparser as makeparser,
    parse as parse,
    fromstring as fromstring,
    XML as XML,
    ObjectPath as ObjectPath,
)

# Exported constants
__version__: LiteralString
PYTYPE_ATTRIBUTE: LiteralString
