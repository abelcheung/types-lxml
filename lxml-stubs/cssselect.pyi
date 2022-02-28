from typing_extensions import Literal

from ._types import _NonDefaultNSMapArg, _XPathVarArg
from .etree import XPath, _Element, _ElementOrTree

_CSSTransArg = LxmlTranslator | Literal["xml", "html", "xhtml"]

class SelectorError(Exception): ...
class SelectorSyntaxError(SelectorError, SyntaxError): ...
class ExpressionError(SelectorError, RuntimeError): ...

# Cssselect has never had stub in typeshed or official repo.
# Only include the bare minimum init argument to make following
# classes self-contained, as long as users are not creating
# customized translators.
class LxmlTranslator: ...

class LxmlHTMLTranslator(LxmlTranslator):
    def __init__(self, xhtml: bool = ...) -> None: ...

class CSSSelector(XPath):
    css: str
    def __init__(
        self,
        css: str,
        namespaces: _NonDefaultNSMapArg = ...,
        translator: _CSSTransArg = ...,
    ) -> None: ...
    def __call__(  # type: ignore[override]
        self,
        _etree_or_element: _ElementOrTree,
        **_variables: _XPathVarArg,
    ) -> list[_Element]: ...  # XPath() returns XPathObject
