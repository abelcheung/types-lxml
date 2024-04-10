from _typeshed import SupportsRead
from typing import Any, Sequence

from bs4 import BeautifulSoup, PageElement, SoupStrainer
from bs4.builder import TreeBuilder

from .._types import _ET, _AnyStr, _ElemFactory
from ..etree import _ElementTree
from . import HtmlElement

def fromstring(
    data: _AnyStr | SupportsRead[str] | SupportsRead[bytes],
    beautifulsoup: type[BeautifulSoup] | None = None,
    makeelement: _ElemFactory[HtmlElement] | None = None,
    *,
    # Following arguments taken from types-beautifulsoup4
    #
    # features: instead of "str | Sequence[str] | None = None",
    # following sig should be much more helpful for users
    features: str | Sequence[str] = "html.parser",
    builder: TreeBuilder | type[TreeBuilder] | None = None,
    parse_only: SoupStrainer | None = None,
    from_encoding: str | None = None,
    exclude_encodings: Sequence[str] | None = None,
    element_classes: dict[type[PageElement], type[Any]] | None = None,
) -> HtmlElement: ...
def parse(
    # Technically Path is also accepted, but emits visible warning
    file: _AnyStr | SupportsRead[str] | SupportsRead[bytes],
    beautifulsoup: type[BeautifulSoup] | None = None,
    makeelement: _ElemFactory[HtmlElement] | None = None,
    *,
    features: str | Sequence[str] = "html.parser",
    builder: TreeBuilder | type[TreeBuilder] | None = None,
    parse_only: SoupStrainer | None = None,
    from_encoding: str | None = None,
    exclude_encodings: Sequence[str] | None = None,
    element_classes: dict[type[PageElement], type[Any]] | None = None,
) -> _ElementTree[HtmlElement]: ...
def convert_tree(
    beautiful_soup_tree: BeautifulSoup,
    makeelement: _ElemFactory[HtmlElement] | None = None,
) -> list[HtmlElement]: ...
