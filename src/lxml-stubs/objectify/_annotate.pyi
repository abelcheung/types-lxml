#
# PyType management and annotation
#

from collections.abc import (
    Callable,
    Iterable,
)
from typing import Any
from typing_extensions import disjoint_base

from .._types import _ElementOrTree
from ._element import ObjectifiedDataElement

@disjoint_base
class PyType:
    """User defined type.

    A named type containing a type check function, a type class that
    inherits from `ObjectifiedDataElement`, and an optional "stringification"
    function. The type check takes a string as argument and raises
    `ValueError` or `TypeError` if it cannot handle the string value.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.PyType)
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
        name: str | bytes,
        type_check: Callable[[Any], None] | None,
        type_class: type[ObjectifiedDataElement],
        stringify: Callable[[Any], str] | None = None,
    ) -> None: ...
    def register(
        self,
        before: Iterable[str] | None = None,
        after: Iterable[str] | None = None,
    ) -> None: ...
    def unregister(self) -> None: ...

def set_pytype_attribute_tag(attribute_tag: str | None = None) -> None:
    """Change name and namespace of the XML attribute that holds Python type information.

    Do not use this unless you know what you are doing.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.set_pytype_attribute_tag)
    """

def pytypename(obj: object) -> str:
    """Find the name of the corresponding PyType for a Python object.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.pytypename)
    """

def getRegisteredTypes() -> list[PyType]:
    """Returns a list of the currently registered PyType objects.

    To add a new type, retrieve this list and call `unregister()` for all
    entries.  Then add the new type at a suitable position and call
    `register()` for all entries.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.getRegisteredTypes)
    """

def pyannotate(
    element_or_tree: _ElementOrTree,
    *,
    ignore_old: bool = False,
    ignore_xsi: bool = False,
    empty_pytype: str | bytes | None = None,
) -> None:
    """Recursively annotates elements of an XML tree with `py:pytype` attributes.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.pyannotate)
    """

def xsiannotate(
    element_or_tree: _ElementOrTree,
    *,
    ignore_old: bool = False,
    ignore_pytype: bool = False,
    empty_type: str | bytes | None = None,
) -> None:
    """Recursively annotates elements of an XML tree with `xsi:type` attributes.

    Note that the mapping from Python types to XSI types is usually ambiguous.
    Currently, only the first XSI type name in the corresponding PyType
    definition will be used for annotation.  Thus, you should consider naming
    the widest type first if you define additional types.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.xsiannotate)
    """

def annotate(
    element_or_tree: _ElementOrTree,
    *,
    ignore_old: bool = True,
    ignore_xsi: bool = False,
    empty_pytype: str | bytes | None = None,
    empty_type: str | bytes | None = None,
    # following arguments are typed 'bint' in source
    annotate_xsi: bool = False,
    annotate_pytype: bool = True,
) -> None:
    """Recursively annotates elements of an XML tree with `py:pytype` and/or `xsi:type` attributes.

    Annotation
    ----------
    The `annotate_xsi` and `annotate_pytype` parameter types deviate from documentation,
    which is marked as having default values 0 and 1 respectively.
    The underlying internal function uses type `bint` (which means
    bool for Cython). The parameters act as feature on/off toggles.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.annotate)
    """

def deannotate(
    element_or_tree: _ElementOrTree,
    *,
    pytype: bool = True,
    xsi: bool = True,
    xsi_nil: bool = False,
    cleanup_namespaces: bool = False,
) -> None:
    """Recursively de-annotate elements of an XML tree.

    This is achieved by removing `py:pytype`, `xsi:type` and/or `xsi:nil` attributes.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.deannotate)
    """
