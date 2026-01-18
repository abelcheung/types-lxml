from typing import overload
from typing_extensions import disjoint_base

from .._types import _ElementOrTree, _FileReadSource
from ._module_misc import LxmlError, _Validator

class XMLSchemaError(LxmlError): ...
class XMLSchemaParseError(XMLSchemaError): ...
class XMLSchemaValidateError(XMLSchemaError): ...

@disjoint_base
class XMLSchema(_Validator):
    """Turn a document into an XML Schema validator.

    Either pass a schema as Element or ElementTree, or pass a file or filename
    through the `file` keyword argument.

    Passing the `attribute_defaults` boolean option will make the schema insert
    default/fixed attributes into validated documents.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLSchema)
    """

    # file arg only useful when etree arg is None
    @overload
    def __init__(
        self,
        etree: _ElementOrTree,
        *,
        file: None = None,
        attribute_defaults: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self,
        etree: None = None,
        *,
        file: _FileReadSource,
        attribute_defaults: bool = False,
    ) -> None: ...
    def __call__(self, etree: _ElementOrTree) -> bool: ...
