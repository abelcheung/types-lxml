import sys
from typing import IO, Any, Collection, Iterable, Literal, overload

from bs4 import BeautifulSoup
from bs4.builder import TreeBuilder
from bs4.element import PageElement
from bs4.filter import SoupStrainer

from .._types import _ET, _FileReadSource
from ..etree import _ElementTree
from . import HtmlElement

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

_Features = Literal[
    "fast",
    "permissive",
    "strict",
    "xml",
    "html",
    "html5",
    "html5lib",
    "html.parser",
    "lxml-xml",
    "lxml",
    "lxml-html",
]

__all__ = ["fromstring", "parse", "convert_tree"]

# NOTES:
# - kw only arguments for fromstring() and parse() are
#   taken from types-beautifulsoup4
# - Default value for 'features' argument should have been None,
#   but current modification is much more helpful for code
#   writers; they don't need to lookup source on how lxml behaves
# - makeelement argument provides very exotic feature:
#   it's actually possible to convert BeautifulSoup html tree
#   into lxml XML element tree, not just lxml html tree

@overload  # guard against plain string in exclude_encodings
@deprecated("Use a collection of encoding, not a vanilla encoding string")
def fromstring(
    *args: Any,
    exclude_encodings: str,
    **kw: Any,
) -> Never:
    """Parse a string of HTML data into an Element tree using the
    BeautifulSoup parser.

    Annotation
    ----------
    This overloaded signature bans the use of a plain string as
    `exclude_encodings` argument.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.fromstring)
    """

@overload  # makeelement is positional
def fromstring(
    data: str | bytes | IO[str] | IO[bytes],
    beautifulsoup: type[BeautifulSoup] | None,
    makeelement: type[_ET],
    *,
    features: _Features | Collection[_Features] = "html.parser",
    builder: TreeBuilder | type[TreeBuilder] | None = None,
    parse_only: SoupStrainer | None = None,
    from_encoding: str | None = None,
    exclude_encodings: Iterable[str] | None = None,
    element_classes: dict[type[PageElement], type[Any]] | None = None,
) -> _ET:
    """Parse a string of HTML data into an Element tree using the
    BeautifulSoup parser.

    Annotation
    ----------
    This overloaded signature handles the case when `makeelement`
    is provided as a positional argument.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.fromstring)
    """

@overload  # makeelement is kw
def fromstring(
    data: str | bytes | IO[str] | IO[bytes],
    beautifulsoup: type[BeautifulSoup] | None = None,
    *,
    makeelement: type[_ET],
    features: _Features | Collection[_Features] = "html.parser",
    builder: TreeBuilder | type[TreeBuilder] | None = None,
    parse_only: SoupStrainer | None = None,
    from_encoding: str | None = None,
    exclude_encodings: Iterable[str] | None = None,
    element_classes: dict[type[PageElement], type[Any]] | None = None,
) -> _ET:
    """Parse a string of HTML data into an Element tree using the
    BeautifulSoup parser.

    Annotation
    ----------
    This overloaded signature handles the case when `makeelement`
    is provided as a keyword argument.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.fromstring)
    """

@overload  # makeelement not provided or is default
def fromstring(
    data: str | bytes | IO[str] | IO[bytes],
    beautifulsoup: type[BeautifulSoup] | None = None,
    makeelement: None = None,
    *,
    features: _Features | Collection[_Features] = "html.parser",
    builder: TreeBuilder | type[TreeBuilder] | None = None,
    parse_only: SoupStrainer | None = None,
    from_encoding: str | None = None,
    exclude_encodings: Iterable[str] | None = None,
    element_classes: dict[type[PageElement], type[Any]] | None = None,
) -> HtmlElement:
    """Parse a string of HTML data into an Element tree using the
    BeautifulSoup parser.

    Annotation
    ----------
    This overloaded signature handles the case when `makeelement`
    is not provided or is the default value.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.fromstring)
    """

#
# parse() actually allows supplying file descriptor int
# as input. But this is just a side-effect of implementation
# detail, which is very unintuitive and way off from common
# usage patterns.
#
@overload  # guard against plain string in exclude_encodings
@deprecated("Use encoding collection or iterator, not a vanilla encoding string")
def parse(
    *args: Any,
    exclude_encodings: str,
    **kw: Any,
) -> Never:
    """Parse a file into an ElementTree using the BeautifulSoup parser.

    Annotation
    ----------
    This overloaded signature bans the use of a plain string as
    `exclude_encodings` argument.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.parse)
    """

@overload  # makeelement is positional
def parse(
    file: _FileReadSource,
    beautifulsoup: type[BeautifulSoup] | None,
    makeelement: type[_ET],
    *,
    features: _Features | Collection[_Features] = "html.parser",
    builder: TreeBuilder | type[TreeBuilder] | None = None,
    parse_only: SoupStrainer | None = None,
    from_encoding: str | None = None,
    exclude_encodings: Iterable[str] | None = None,
    element_classes: dict[type[PageElement], type[Any]] | None = None,
) -> _ElementTree[_ET]:
    """Parse a file into an ElementTree using the BeautifulSoup parser.

    Annotation
    ----------
    This overloaded signature handles the case when `makeelement`
    is provided as a positional argument.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.parse)
    """

@overload
def parse(  # makeelement is kw
    file: _FileReadSource,
    beautifulsoup: type[BeautifulSoup] | None = None,
    *,
    makeelement: type[_ET],
    features: _Features | Collection[_Features] = "html.parser",
    builder: TreeBuilder | type[TreeBuilder] | None = None,
    parse_only: SoupStrainer | None = None,
    from_encoding: str | None = None,
    exclude_encodings: Iterable[str] | None = None,
    element_classes: dict[type[PageElement], type[Any]] | None = None,
) -> _ElementTree[_ET]:
    """Parse a file into an ElementTree using the BeautifulSoup parser.

    Annotation
    ----------
    This overloaded signature handles the case when `makeelement`
    is provided as a keyword argument.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.parse)
    """

@overload  # makeelement not provided or is default
def parse(
    file: _FileReadSource,
    beautifulsoup: type[BeautifulSoup] | None = None,
    makeelement: None = None,
    *,
    features: _Features | Collection[_Features] = "html.parser",
    builder: TreeBuilder | type[TreeBuilder] | None = None,
    parse_only: SoupStrainer | None = None,
    from_encoding: str | None = None,
    exclude_encodings: Iterable[str] | None = None,
    element_classes: dict[type[PageElement], type[Any]] | None = None,
) -> _ElementTree[HtmlElement]:
    """Parse a file into an ElementTree using the BeautifulSoup parser.

    Annotation
    ----------
    This overloaded signature handles the case when `makeelement`
    is not provided or is the default value.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.parse)
    """

@overload
def convert_tree(
    beautiful_soup_tree: BeautifulSoup,
    makeelement: type[_ET],
) -> list[_ET]:
    """Convert a BeautifulSoup tree to a list of Element trees.

    Annotation
    ----------
    This overloaded signature handles the case when `makeelement`
    is provided.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.convert_tree)
    """

@overload
def convert_tree(
    beautiful_soup_tree: BeautifulSoup,
    makeelement: None = None,
) -> list[HtmlElement]:
    """Convert a BeautifulSoup tree to a list of Element trees.

    Annotation
    ----------
    This overloaded signature handles the case when `makeelement`
    is not provided or is the default value.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.soupparser.html#lxml.html.soupparser.convert_tree)
    """
