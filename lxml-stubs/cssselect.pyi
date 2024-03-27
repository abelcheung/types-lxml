from typing import Literal

import cssselect as _csel
from cssselect.parser import Function
from cssselect.xpath import XPathExpr

from ._types import _ET, _NonDefaultNSMapArg, _XPathVarArg
from .etree import XPath, _ElementTree

_CSSTransArg = LxmlTranslator | Literal["xml", "html", "xhtml"]

SelectorError = _csel.SelectorError
SelectorSyntaxError = _csel.SelectorSyntaxError
ExpressionError = _csel.ExpressionError

class LxmlTranslator(_csel.GenericTranslator):
    def xpath_contains_function(
        self, xpath: XPathExpr, function: Function
    ) -> XPathExpr: ...

class LxmlHTMLTranslator(LxmlTranslator, _csel.HTMLTranslator):
    pass

class CSSSelector(XPath):
    # Although 'css' is implemented as plain attribute, it is
    # meaningless to modify it, because instance is initialized
    # with translated XPath expression, not the CSS expression.
    # Allowing attribute modification would cause confusion as
    # CSS expression and the underlying XPath expression don't
    # match.
    @property
    def css(self) -> str: ...
    def __init__(
        self,
        css: str,
        namespaces: _NonDefaultNSMapArg | None = ...,
        translator: _CSSTransArg = ...,
    ) -> None: ...
    # It is safe to assume cssselect always selects element
    # representable in original element tree, because CSS expression
    # is transformed into XPath via css_to_xpath() which doesn't support
    # pseudo-element by default.
    def __call__(
        self,
        _etree_or_element: _ET | _ElementTree[_ET],
        /,
        **_variables: _XPathVarArg,
    ) -> list[_ET]: ...
