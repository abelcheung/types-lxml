#
# Note that this interface only generates lxml.etree Elements, not lxml.html ones
# See https://github.com/html5lib/html5lib-python/issues/102
#

import html5lib as _html5lib

from .._types import _AnyStr
from ..etree import _Element, _ElementTree

# Note that tree arg is dropped, because the sole purpose of using
# this parser is to generate lxml element tree with html5lib parser.
# Other arguments good for html5lib >= 1.0
class HTMLParser(_html5lib.HTMLParser):
    def __init__(
        self, strict: bool = ..., namespaceHTMLElements: bool = ..., debug: bool = ...
    ) -> None: ...

html_parser: HTMLParser

# Notes:
# - No XHTMLParser here. Lxml tries to probe for some hypothetical
#   XHTMLParser class in html5lib which had never existed.
#   The core probing logic of this user-contributed submodule has never
#   changed since last modification at 2010. Probably yet another
#   member of code wasteland.
# - Exception raised for the combination html=<str> and guess_charset=True,
#   but not reflected here. (TODO or?)
# - Although other types of parser _might_ be usable (after implementing
#   parse() method, that is), such usage completely defeats the purpose of
#   creating this submodule. It is intended for subclassing or
#   init argument tweaking instead.

def document_fromstring(
    html: _AnyStr, guess_charset: bool | None = ..., parser: HTMLParser | None = ...
) -> _Element: ...
def fragments_fromstring(
    html: _AnyStr,
    no_leading_text: bool = ...,
    guess_charset: bool | None = ...,
    parser: HTMLParser | None = ...,
) -> list[_Element]: ...
def fragment_fromstring(
    html: _AnyStr,
    create_parent: bool | _AnyStr = ...,
    guess_charset: bool | None = ...,
    parser: HTMLParser | None = ...,
) -> _Element: ...
def fromstring(
    html: _AnyStr,
    guess_charset: bool | None = ...,
    parser: HTMLParser | None = ...,
) -> _Element: ...
def parse(
    filename_url_or_file: _AnyStr,
    guess_charset: bool | None = ...,
    parser: HTMLParser | None = ...,
) -> _ElementTree[_Element]: ...
