#
# Internal classes and functions from lxml/xpath.pxi
#

from typing import Any, overload

from .._types import (
    _AnyStr,
    _NonDefaultNSMapArg,
    _XPathExtFuncArg,
    _XPathObject,
    _XPathVarArg,
)
from . import LxmlError, LxmlSyntaxError, _Element, _ElementOrAnyTree, _ElementTree
from ._xmlerror import _ErrorLog

# TODO Belongs to extensions.pxi, to be moved
class XPathError(LxmlError): ...
class XPathSyntaxError(LxmlSyntaxError, XPathError): ...

class _XPathEvaluatorBase:
    @property
    def error_log(self) -> _ErrorLog: ...
    # evaluate() is deprecated

class XPath(_XPathEvaluatorBase):
    def __init__(
        self,
        path: _AnyStr,
        *,
        namespaces: _NonDefaultNSMapArg | None = ...,
        extensions: _XPathExtFuncArg | None = ...,
        regexp: bool = ...,
        smart_strings: bool = ...,
    ) -> None: ...
    def __call__(
        self, _etree_or_element: _ElementOrAnyTree, /, **_variables: _XPathVarArg
    ) -> _XPathObject: ...
    @property
    def path(self) -> str: ...

class ETXPath(XPath):
    def __init__(
        self,
        path: _AnyStr,
        *,
        extensions: _XPathExtFuncArg | None = ...,
        regexp: bool = ...,
        smart_strings: bool = ...,
    ) -> None: ...

class XPathElementEvaluator(_XPathEvaluatorBase):
    def __init__(
        self,
        element: _Element,
        *,
        namespaces: _NonDefaultNSMapArg | None = ...,
        extensions: _XPathExtFuncArg | None = ...,
        regexp: bool = ...,
        smart_strings: bool = ...,
    ) -> None: ...
    def __call__(
        self, _path: _AnyStr, /, **_variables: _XPathVarArg
    ) -> _XPathObject: ...
    def register_namespace(self, prefix: _AnyStr, uri: _AnyStr) -> None: ...
    def register_namespaces(self, namespaces: _NonDefaultNSMapArg | None) -> None: ...

class XPathDocumentEvaluator(XPathElementEvaluator):
    def __init__(
        self,
        etree: _ElementTree[Any],
        *,
        namespaces: _NonDefaultNSMapArg | None = ...,
        extensions: _XPathExtFuncArg | None = ...,
        regexp: bool = ...,
        smart_strings: bool = ...,
    ) -> None: ...

@overload
def XPathEvaluator(
    etree_or_element: _Element,
    *,
    namespaces: _NonDefaultNSMapArg | None = ...,
    extensions: _XPathExtFuncArg | None = ...,
    regexp: bool = ...,
    smart_strings: bool = ...,
) -> XPathElementEvaluator: ...
@overload
def XPathEvaluator(
    etree_or_element: _ElementTree[Any],
    *,
    namespaces: _NonDefaultNSMapArg | None = ...,
    extensions: _XPathExtFuncArg | None = ...,
    regexp: bool = ...,
    smart_strings: bool = ...,
) -> XPathDocumentEvaluator: ...
@overload
def XPathEvaluator(
    etree_or_element: _ElementOrAnyTree,
    *,
    namespaces: _NonDefaultNSMapArg | None = ...,
    extensions: _XPathExtFuncArg | None = ...,
    regexp: bool = ...,
    smart_strings: bool = ...,
) -> XPathElementEvaluator | XPathDocumentEvaluator: ...
