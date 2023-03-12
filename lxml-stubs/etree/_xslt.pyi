from typing import Any, ClassVar, final
from typing_extensions import TypedDict

from .._types import _AnyStr
from . import LxmlError, _Element, _ElementOrTree, _ElementTree
from ._serializer import SerialisationError
from ._xmlerror import _ListErrorLog

# exported constants
LIBXSLT_VERSION: tuple[int, int, int]
LIBXSLT_COMPILED_VERSION: tuple[int, int, int]

class XSLTError(LxmlError):
    """Base class of all XSLT errors"""

class XSLTParseError(XSLTError):
    """Error parsing a stylesheet document"""

class XSLTApplyError(XSLTError):
    """Error running an XSL transformation"""

class XSLTSaveError(XSLTError, SerialisationError):
    """Error serialising an XSLT result"""

class XSLTExtensionError(XSLTError):
    """Error registering an XSLT extension"""

@final
class _XSLTResultTree(_ElementTree[_Element]):
    def write_output(self, file: Any, *, compression: int = ...) -> None: ...
    @property
    def xslt_profile(self) -> _ElementTree[_Element] | None: ...

@final
class _XSLTQuotedStringParam:
    """A wrapper class for literal XSLT string parameters that require
    quote escaping"""
    strval: bytes

class __AccessControlConfig(TypedDict):
    read_file: bool | None
    write_file: bool | None
    create_dir: bool | None
    read_network: bool | None
    write_network: bool | None

class XSLTAccessControl:
    """Access control for XSLT: reading/writing files, directories and
    network I/O.

    Access to a type of resource is granted or denied by
    passing any of the following boolean keyword arguments.  All of
    them default to True to allow access.

    - read_file
    - write_file
    - create_dir
    - read_network
    - write_network

    For convenience, there is also a class member `DENY_ALL` that
    provides an XSLTAccessControl instance that is readily configured
    to deny everything, and a `DENY_WRITE` member that denies all
    write access but allows read access.
    """
    DENY_ALL: ClassVar[XSLTAccessControl]
    DENY_WRITE: ClassVar[XSLTAccessControl]

    def __init__(
        self,
        *,
        read_file: bool = ...,
        write_file: bool = ...,
        create_dir: bool = ...,
        read_network: bool = ...,
        write_network: bool = ...,
    ) -> None: ...
    @property
    def options(self) -> __AccessControlConfig: ...


class XSLT:
    """Turn an XSL document into an XSLT object.

    Calling this object on a tree or Element will execute the XSLT::

        transform = etree.XSLT(xsl_tree)
        result = transform(xml_tree)

    Keyword arguments of the constructor:

    - extensions: a dict mapping ``(namespace, name)`` pairs to
      extension functions or extension elements
    - regexp: enable exslt regular expression support in XPath
      (default: True)
    - access_control: access restrictions for network or file
      system (see `XSLTAccessControl`)

    Keyword arguments of the XSLT call:

    - profile_run: enable XSLT profiling and make the profile available
      as XML document in ``result.xslt_profile`` (default: False)

    Other keyword arguments of the call are passed to the stylesheet
    as parameters.
    """
    def __init__(
        self,
        xslt_input: _ElementOrTree,
        extensions: Any = ...,  # TODO XSLT extension type
        regexp: bool = ...,
        access_control: XSLTAccessControl | None = ...,
    ) -> None: ...
    def __call__(
        self,
        _input: _ElementOrTree,
        /,
        *,
        profile_run: bool = ...,
        **kw: _AnyStr | _XSLTQuotedStringParam,
    ) -> _XSLTResultTree: ...
    @property
    def error_log(self) -> _ListErrorLog: ...
    @staticmethod
    def strparam(s: _AnyStr) -> _XSLTQuotedStringParam: ...
    @staticmethod
    def set_global_max_depth(max_depth: int) -> None: ...

