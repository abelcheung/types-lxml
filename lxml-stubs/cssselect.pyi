from typing import List, Union

from typing_extensions import Literal

from ._types import NonDefaultNSMapArg
from .etree import XPath, _Element, _ElementOrTree, _XPathVarArg

_CSSTransArg = Union[LxmlTranslator, Literal["xml", "html", "xhtml"]]

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
        css: str,  # byte str unaccepted
        namespaces: NonDefaultNSMapArg = ...,
        translator: _CSSTransArg = ...,
    ) -> None: ...
    def __call__(  # type: ignore[override]
        self,
        _etree_or_element: _ElementOrTree,
        **_variables: _XPathVarArg,
    ) -> List[_Element]: ...  # XPath() returns XPathObject
