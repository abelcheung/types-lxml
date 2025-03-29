#
# lxml.etree helper classes, exceptions and constants
#

import sys
from abc import ABCMeta, abstractmethod
from typing import Final, overload

from .._types import (
    _ElementOrTree,
    _TagName,
    _TextArg,
)
from ._dtd import DTD
from ._element import _Element
from ._xmlerror import _BaseErrorLog, _ListErrorLog

if sys.version_info >= (3, 11):
    from typing import LiteralString
else:
    from typing_extensions import LiteralString

DEBUG: int
ICONV_COMPILED_VERSION: Final[tuple[int, int]]
LIBXML_COMPILED_VERSION: Final[tuple[int, int, int]]
LIBXML_COMPILED_FEATURES: Final[set[str]]
LIBXML_FEATURES: Final[set[str]]
LIBXML_VERSION: Final[tuple[int, int, int]]
LXML_VERSION: Final[tuple[int, int, int, int]]
__version__: Final[LiteralString]

class DocInfo:
    """Document information provided by parser and DTD"""
    # Can't be empty, otherwise it means tree contains no element
    @property
    def root_name(self) -> str:
        """Returns the name of the root node as defined by the DOCTYPE."""
    @property
    def public_id(self) -> str | None:
        """Public ID of the DOCTYPE.

        Mutable.  May be set to a valid string or None.  If a DTD does not
        exist, setting this variable (even to None) will create one.
        """
    @public_id.setter
    def public_id(self, __v: str | None) -> None: ...
    @property
    def system_url(self) -> str | None:
        """System ID of the DOCTYPE.

        Mutable.  May be set to a valid string or None.  If a DTD does not
        exist, setting this variable (even to None) will create one.
        """
    @system_url.setter
    def system_url(self, __v: _TextArg | None) -> None: ...
    @property
    def xml_version(self) -> str:  # fallback is "1.0"
        """Returns the XML version as declared by the document."""
    @property
    def encoding(self) -> str:  # fallback is "UTF-8" or "ISO-8859-1"
        """Returns the encoding name as declared by the document."""
    @property
    def standalone(self) -> bool | None:
        """Returns the standalone flag as declared by the document.

        The possible values are:
        - ``True`` (``standalone='yes'``)
        - ``False`` (``standalone='no'`` or flag not provided in the declaration), and
        - ``None`` (unknown or no declaration found).

        Note that a normal truth test on this value will always tell
        if the ``standalone`` flag was set to ``'yes'`` or not.
        """
    @property
    def URL(self) -> str | None:
        """The source URL of the document (or None if unknown)."""
    @URL.setter
    def URL(self, __v: str | bytes | None) -> None: ...
    @property
    def doctype(self) -> str:
        """Returns a DOCTYPE declaration string for the document."""
    @property
    def internalDTD(self) -> DTD | None:
        """Returns a DTD validator based on the internal subset of the document."""
    @property
    def externalDTD(self) -> DTD | None:
        """Returns a DTD validator based on the external subset of the document."""
    def clear(self) -> None:
        """Removes DOCTYPE and internal subset from the document."""

class QName:
    """QName wrapper for qualified XML names.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.QName)
    """
    @overload  # first arg non-empty
    def __init__(
        self,
        text_or_uri_or_element: str | bytes | QName | _Element,
        tag: _TextArg | None = None,
    ) -> None: ...
    @overload  # first arg empty
    def __init__(
        self,
        text_or_uri_or_element: None,
        tag: str | bytes | QName | _Element,
    ) -> None: ...
    @property
    def localname(self) -> str: ...
    @property
    def namespace(self) -> str | None: ...
    @property
    def text(self) -> str:
        """Holds the qualified name in `{namespace}tagname` notation"""
    # Emulate __richcmp__()
    def __ge__(self, other: _TagName) -> bool: ...
    def __gt__(self, other: _TagName) -> bool: ...
    def __le__(self, other: _TagName) -> bool: ...
    def __lt__(self, other: _TagName) -> bool: ...

class CDATA:
    """CDATA factory.  This factory creates an opaque data object that
    can be used to set Element text.  The usual way to use it is:

    ```python
        >>> el = Element('content')
        >>> el.text = CDATA('a string')

        >>> print(el.text)
        a string
        >>> print(tostring(el, encoding="unicode"))
        <content><![CDATA[a string]]></content>
    ```
    """
    def __init__(self, data: _TextArg) -> None: ...

class Error(Exception):
    """Error superclass for ElementTree compatibility"""

class LxmlError(Error):
    """Main exception base class for lxml.
    All other exceptions inherit from this one."""
    def __init__(
        self, message: object, error_log: _BaseErrorLog | None = None
    ) -> None: ...
    # Even when LxmlError is initiated with PyErrorLog, it fools
    # error_log property by creating a dummy _ListErrorLog object
    error_log: _ListErrorLog

class DocumentInvalid(LxmlError): ...

class LxmlSyntaxError(LxmlError, SyntaxError):
    """Base class for all syntax errors."""

class C14NError(LxmlError):
    """Error during C14N serialisation."""

class _Validator(metaclass=ABCMeta):
    def assert_(self, etree: _ElementOrTree) -> None: ...
    def assertValid(self, etree: _ElementOrTree) -> None: ...
    def validate(self, etree: _ElementOrTree) -> bool: ...
    @property
    def error_log(self) -> _ListErrorLog: ...
    # all methods implicitly require a concrete __call__()
    # implementation in subclasses in order to be usable
    @abstractmethod
    def __call__(self, etree: _ElementOrTree) -> bool: ...

# Though etree.Schematron is not implemented in stub,
# lxml.isoschematron reuses related exception classes,
# so list them here
class SchematronError(LxmlError):
    """Base class of all Schematron errors"""

class SchematronParseError(SchematronError):
    """Error while parsing an XML document as Schematron schema"""

class SchematronValidateError(SchematronError):
    """Error while validating an XML document with a Schematron schema"""
