#
# Exception classes and functions defined in
# etree/_extension.pxi are merged here.
#

import sys
from abc import abstractmethod
from types import ModuleType
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Protocol,
    final,
    overload,
)

from .._types import (
    _ET,
    SupportsLaxItems,
    _ElementOrTree,
    _TextArg,
    _XPathExtFuncArg,
    _XPathNSArg,
    _XPathObject,
    _XPathVarArg,
)
from ._element import _Element, _ElementTree
from ._module_misc import LxmlError, LxmlSyntaxError
from ._xmlerror import _ListErrorLog

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

class XPathError(LxmlError):
    """Base class of all XPath errors"""

class XPathEvalError(XPathError):
    """Error during XPath evaluation"""

class XPathFunctionError(XPathEvalError):
    """Internal error looking up an XPath extension function"""

class XPathResultError(XPathEvalError):
    """Error handling an XPath result"""

class XPathSyntaxError(LxmlSyntaxError, XPathError):
    """Error in XPath expression"""

class _XPathEvaluatorBase(Protocol):
    @property
    def error_log(self) -> _ListErrorLog: ...
    @abstractmethod
    def __call__(self, _arg: Any, /, **__var: _XPathVarArg) -> _XPathObject: ...
    # evaluate() should have been abstract like __call__(), but requiring all
    # subclasses to add deprecated method is idiocy
    @deprecated("Removed since 5.0; call instance directly instead")
    def evaluate(self, _arg: Any, /, **__var: _XPathVarArg) -> _XPathObject: ...

class XPath(_XPathEvaluatorBase):
    def __init__(
        self,
        path: _TextArg,
        *,
        namespaces: _XPathNSArg | None = None,
        extensions: _XPathExtFuncArg | None = None,
        regexp: bool = True,
        smart_strings: bool = True,
    ) -> None: ...
    def __call__(
        self, _etree_or_element: _ElementOrTree, /, **_variables: _XPathVarArg
    ) -> _XPathObject: ...
    @property
    def path(self) -> str: ...

class ETXPath(XPath):
    def __init__(
        self,
        path: _TextArg,
        *,
        extensions: _XPathExtFuncArg | None = None,
        regexp: bool = True,
        smart_strings: bool = True,
    ) -> None: ...

class XPathElementEvaluator(_XPathEvaluatorBase):
    def __init__(
        self,
        element: _Element,
        *,
        namespaces: _XPathNSArg | None = None,
        extensions: _XPathExtFuncArg | None = None,
        regexp: bool = True,
        smart_strings: bool = True,
    ) -> None: ...
    def __call__(
        self, _path: _TextArg, /, **_variables: _XPathVarArg
    ) -> _XPathObject: ...
    def register_namespace(self, prefix: str | bytes, uri: str | bytes) -> None: ...
    def register_namespaces(
        self, namespaces: SupportsLaxItems[str | bytes, str | bytes]
    ) -> None: ...

class XPathDocumentEvaluator(XPathElementEvaluator):
    def __init__(
        self,
        etree: _ElementTree,
        *,
        namespaces: _XPathNSArg | None = None,
        extensions: _XPathExtFuncArg | None = None,
        regexp: bool = True,
        smart_strings: bool = True,
    ) -> None: ...

@overload
def XPathEvaluator(
    etree_or_element: _Element,
    *,
    namespaces: _XPathNSArg | None = None,
    extensions: _XPathExtFuncArg | None = None,
    regexp: bool = True,
    smart_strings: bool = True,
) -> XPathElementEvaluator: ...
@overload
def XPathEvaluator(
    etree_or_element: _ElementTree,
    *,
    namespaces: _XPathNSArg | None = None,
    extensions: _XPathExtFuncArg | None = None,
    regexp: bool = True,
    smart_strings: bool = True,
) -> XPathDocumentEvaluator: ...

@final
class _ElementUnicodeResult(str, Generic[_ET]):
    """Smart string is a private str subclass documented in
    [return types](https://lxml.de/xpathxslt.html#xpath-return-values)
    of XPath evaluation result.

    Please [visit wiki page](https://github.com/abelcheung/types-lxml/wiki/Smart-string-usage)
    on description and how to use it in you code.
    """

    @property
    def is_attribute(self) -> bool: ...
    @property
    def is_tail(self) -> bool: ...
    @property
    def is_text(self) -> bool: ...
    @property
    def attrname(self) -> str | None: ...
    def getparent(self: _ElementUnicodeResult[_ET]) -> _ET | None: ...

@overload  # namespace present
def Extension(
    module: object | ModuleType,
    function_mapping: dict[str, str] | Iterable[str] | None = None,
    *,
    ns: str,
) -> dict[tuple[str, str], Callable[..., Any]]:
    """Build a dictionary of extension functions from the functions
    defined in a module or the methods of an object.

    Annotation
    ----------
    This overload handles the case where a namespace is provided
    via `ns` parameter.

    See Also
    --------
    - [User documentation](https://lxml.de/extensions.html#evaluator-local-extensions)
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.Extension)
    """

@overload  # no namespace
def Extension(
    module: object | ModuleType,
    function_mapping: dict[str, str] | Iterable[str] | None = None,
    *,
    ns: None = None,
) -> dict[tuple[None, str], Callable[..., Any]]:
    """Build a dictionary of extension functions from the functions
    defined in a module or the methods of an object.

    Annotation
    ----------
    This overload handles the case where namespace is not supplied.

    See Also
    --------
    - [User documentation](https://lxml.de/extensions.html#evaluator-local-extensions)
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.Extension)
    """
