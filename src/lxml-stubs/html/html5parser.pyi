#
# This interface only generates lxml.etree Elements, not lxml.html ones.
# See https://github.com/html5lib/html5lib-python/issues/102
#
import sys
from _typeshed import SupportsRead
from typing import Literal, overload

import html5lib as _html5lib

from ..etree import _Element, _ElementTree

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

# Beware that tree arg is dropped, because the sole purpose of using this parser
# is to generate lxml element tree with html5lib parser. Other arguments good
# for html5lib >= 1.0
class HTMLParser(_html5lib.HTMLParser):
    """An html5lib HTML parser with lxml as tree."""

    def __init__(
        self,
        strict: bool = False,
        *,
        namespaceHTMLElements: bool = True,
        debug: bool = False,
    ) -> None: ...

# No XHTMLParser here. Lxml tries to probe for some hypothetical
# XHTMLParser class in html5lib which had never existed.
html_parser: HTMLParser

# Notes:
# - Exception raised when html=<str> and guess_charset
#   are used together. This is due to flawed argument passing
#   into html5lib. We cover the situation with @overload
# - Although other types of parser _might_ be usable (after implementing
#   parse() method, that is), such usage completely defeats the purpose of
#   creating this submodule. It is intended for subclassing or
#   init argument tweaking instead.

@overload
@deprecated("`str` input and `guess_charset` argument together results in exception")
def document_fromstring(
    html: str,
    guess_charset: bool,
    parser: HTMLParser | None = None,
) -> Never:
    """Parse a whole document into a string.

    Annotation
    ----------
    This overload signature guards against using `str` input data and
    `guess_charset` argument together, which results in an exception.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.document_fromstring)
    """

@overload
def document_fromstring(
    html: str | bytes,
    guess_charset: bool | None = None,
    parser: HTMLParser | None = None,
) -> _Element:
    """Parse a whole document into a string.

    This overload signature covers generic usage of `document_fromstring`.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.document_fromstring)
    """

@overload  # str html + kw guess_charset
@deprecated("`str` input and `guess_charset` argument together results in exception")
def fragments_fromstring(
    html: str,
    no_leading_text: bool = False,
    *,
    guess_charset: bool,
    parser: HTMLParser | None = None,
) -> Never:
    """Parses several HTML elements, returning a list of elements.

    Annotation
    ----------
    This overload signature guards against using `str` input data and
    `guess_charset` argument together, which results in an exception.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fragments_fromstring)
    """

@overload  # str html + positional guess_charset
@deprecated("`str` input and `guess_charset` argument together results in exception")
def fragments_fromstring(
    html: str,
    no_leading_text: bool,
    guess_charset: bool,
    parser: HTMLParser | None = None,
) -> Never:
    """Parses several HTML elements, returning a list of elements.

    Annotation
    ----------
    This overload signature guards against using `str` input data and
    `guess_charset` argument together, which results in an exception.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fragments_fromstring)
    """

@overload  # no_leading_text=true
def fragments_fromstring(  # type: ignore[overload-overlap]  # pyright: ignore[reportOverlappingOverload]
    html: str | bytes,
    no_leading_text: Literal[True],
    guess_charset: bool | None = None,
    parser: HTMLParser | None = None,
) -> list[_Element]:
    """Parses several HTML elements, returning a list of elements.

    Annotation
    ----------
    This overload signature handles the case where `no_leading_text` is set to
    `True`, which means no leading text is present in output.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fragments_fromstring)
    """

@overload  # no_leading_text=other cases
def fragments_fromstring(
    html: str | bytes,
    no_leading_text: bool = False,
    guess_charset: bool | None = None,
    parser: HTMLParser | None = None,
) -> list[str | _Element]:
    """Parses several HTML elements, returning a list of elements.

    Annotation
    ----------
    This overload signature handles the case where `no_leading_text` is not
    `True`, which means the first item of output list may be the leading text.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fragments_fromstring)
    """

@overload  # str html + kw guess_charset
@deprecated("`str` input and `guess_charset` argument together results in exception")
def fragment_fromstring(
    html: str,
    create_parent: bool | str | bytes = False,
    *,
    guess_charset: bool,
    parser: HTMLParser | None = None,
) -> Never:
    """Parses a single HTML element; it is an error if there is more than
    one element, or if anything but whitespace precedes or follows the
    element.

    Annotation
    ----------
    This overload signature guards against using `str` input data and
    `guess_charset` argument together, which results in an exception.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fragment_fromstring)
    """

@overload  # str html + positional guess_charset
@deprecated("`str` input and `guess_charset` argument together results in exception")
def fragment_fromstring(
    html: str,
    create_parent: bool | str | bytes,
    guess_charset: bool,
    parser: HTMLParser | None = None,
) -> Never:
    """Parses a single HTML element; it is an error if there is more than
    one element, or if anything but whitespace precedes or follows the
    element.

    Annotation
    ----------
    This overload signature guards against using `str` input data and
    `guess_charset` argument together, which results in an exception.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fragment_fromstring)
    """

@overload
def fragment_fromstring(
    html: str | bytes,
    create_parent: bool | str | bytes = False,
    guess_charset: bool | None = None,
    parser: HTMLParser | None = None,
) -> _Element:
    """Parses a single HTML element; it is an error if there is more than
    one element, or if anything but whitespace precedes or follows the
    element.

    Annotation
    ----------
    This overload signature covers generic usage of `fragment_fromstring`.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fragment_fromstring)
    """

@overload
@deprecated("`str` input and `guess_charset` argument together results in exception")
def fromstring(
    html: str,
    guess_charset: bool,
    parser: HTMLParser | None = None,
) -> Never:
    """Parse the html, returning a single element/document.

    Annotation
    ----------
    This overload signature guards against using `str` input data and
    `guess_charset` argument together, which results in an exception.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fromstring)
    """

@overload
def fromstring(
    html: str | bytes,
    guess_charset: bool | None = None,
    parser: HTMLParser | None = None,
) -> _Element:
    """Parse the html, returning a single element/document.

    Annotation
    ----------
    This overload signature covers generic usage of `fromstring`.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.fromstring)
    """

# html5lib doesn't support pathlib
@overload
@deprecated(
    "guess_charset=True with file object that generate str content causes exception"
)
def parse(
    filename_url_or_file: SupportsRead[str],
    guess_charset: Literal[True],
    parser: HTMLParser | None = None,
) -> Never:
    """Parse a filename, URL, or file-like object into an HTML document tree.

    Annotation
    ----------
    This overload signature guards against using `guess_charset=True` together
    with file object that generate `str` content (like `io.StringIO` or
    `open(mode="rt")`, which results in an exception.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.parse)
    """

@overload
def parse(
    filename_url_or_file: str | bytes | SupportsRead[str] | SupportsRead[bytes],
    guess_charset: bool | None = None,
    parser: HTMLParser | None = None,
) -> _ElementTree:
    """Parse a filename, URL, or file-like object into an HTML document tree.

    Annotation
    ----------
    This overload signature covers generic usage of `parse()`. But it has a bug
    of its own: if supplied input is a bytes URL (e.g.
    `b'http://example.com/some.html'`), it will raise exception under Windows.

    See Also
    --------
    [API documentation](https://lxml.de/apidoc/lxml.html.html5parser.html#lxml.html.html5parser.parse)
    """
