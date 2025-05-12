from __future__ import annotations

import sys
from typing import (
    Any,
    Callable,
    Iterator,
    Literal,
    TypeVar,
    overload,
)

from .._types import (
    _AttrVal,
    _ElementOrTree,
    _OutputMethodArg,
)
from ._element import HtmlElement

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

_HtmlDoc_T = TypeVar("_HtmlDoc_T", str, bytes, HtmlElement)

# These are HtmlMixin methods converted to standard functions,
# with element or HTML string as first argument followed by all
# pre-existing args. Quoting from source:
#
#   ... the function takes either an element or an HTML string.  It
#   returns whatever the function normally returns, or if the function
#   works in-place (and so returns None) it returns a serialized form
#   of the resulting document.
#
# Special Notes:
# 1. These functions operate on attributes that only make sense on
#    normal HtmlElements; lxml raises exception otherwise.
# 2. Although extra 'copy' argument is available, it is intended
#    only for internal use by each function, not something to be
#    arbitrarily changed by users, thus not available in stub.
#
# HACK Interesting, a 15+ yrs bug remains undiscovered,
# probably nobody is using them at all?
# All these standalone link functions make use of _MethodFunc
# internal class in html/__init__.py, which has bug when
# converting input data. If input is not Element, the class
# automatically converts input to Element via fromstring(),
# taking in all keyword args used in link function call.
# Many of these keywords are unknown to fromstring(),
# thus causing Exception. Workaround this using @overload.

@overload
@deprecated("Raises exception if keyword argument is used while input is str or bytes")
def find_rel_links(
    doc: str | bytes,
    *,
    rel: Any,
) -> Never: ...
@overload
def find_rel_links(
    doc: str | bytes | HtmlElement,
    rel: str,
) -> list[HtmlElement]: ...
@overload
@deprecated("Raises exception if keyword argument is used while input is str or bytes")
def find_class(
    doc: str | bytes,
    *,
    class_name: Any,
) -> Never: ...
@overload
def find_class(
    doc: str | bytes | HtmlElement,
    class_name: str | bytes,  # bytearray banned in etree._wrapXPathObject
) -> list[HtmlElement]: ...

# fromstring() accepts 'base_url' keyword
@overload
@deprecated("Raises exception if keyword argument is used while input is str or bytes")
def make_links_absolute(
    doc: str | bytes,
    *arg: Any,
    resolve_base_href: Any,
    **kw: Any,
) -> Never: ...
@overload
@deprecated("Raises exception if keyword argument is used while input is str or bytes")
def make_links_absolute(  # pyright: ignore[reportOverlappingOverload]
    doc: str | bytes,
    *arg: Any,
    handle_failures: Any,
    **kw: Any,
) -> Never: ...
@overload
def make_links_absolute(
    doc: _HtmlDoc_T,
    base_url: str | None = None,
    resolve_base_href: bool = True,
    handle_failures: Literal["ignore", "discard"] | None = None,
) -> _HtmlDoc_T: ...
@overload
@deprecated("Raises exception if keyword argument is used while input is str or bytes")
def resolve_base_href(
    doc: str | bytes,
    *,
    handle_failures: Any,
) -> Never: ...
@overload
def resolve_base_href(
    doc: _HtmlDoc_T,
    handle_failures: Literal["ignore", "discard"] | None = None,
) -> _HtmlDoc_T: ...
def iterlinks(
    doc: str | bytes | HtmlElement,
) -> Iterator[tuple[HtmlElement, str | None, str, int]]: ...
@overload
@deprecated("Raises exception if keyword argument is used while input is str or bytes")
def rewrite_links(
    doc: str | bytes,
    *,
    link_repl_func: Any,
    **kw: Any,
) -> Never: ...
@overload
@deprecated("Raises exception if keyword argument is used while input is str or bytes")
def rewrite_links(
    doc: str | bytes,
    link_repl_func: Callable[[str], _AttrVal | None],
    *,
    resolve_base_href: Any,
    **kw: Any,
) -> Never: ...
@overload
@deprecated("Raises exception if keyword argument is used while input is str or bytes")
def rewrite_links(  # pyright: ignore[reportOverlappingOverload]
    doc: str | bytes,
    link_repl_func: Callable[[str], _AttrVal | None],
    *,
    base_href: Any,
    **kw: Any,
) -> Never: ...
@overload
def rewrite_links(
    doc: _HtmlDoc_T,
    link_repl_func: Callable[[str], _AttrVal | None],
    resolve_base_href: bool = True,
    base_href: str | None = None,
) -> _HtmlDoc_T: ...

#
# Tree conversion
#
def html_to_xhtml(html: _ElementOrTree[HtmlElement]) -> None: ...
def xhtml_to_html(xhtml: _ElementOrTree[HtmlElement]) -> None: ...

#
# Tree output
#
# 1. Encoding issue is similar to etree.tostring().
#
# 2. Unlike etree.tostring(), all arguments here are not explicitly
#    keyword-only. Using overload with no default value would be
#    impossible, as the two arguments before it has default value.
#    Need to make a choice here: enforce all arguments to be keyword-only.
#    Less liberal code, but easier to maintain in long term for users.
#
# 3. Although html.tostring() does not forbid method="c14n" (or c14n2),
#    calling tostring() this way would render almost all keyword arguments
#    useless, defeating the purpose of existence of html.tostring().
#    Besides, no c14n specific arguments are accepted here, so it is
#    better to let etree.tostring() handle C14N.
@overload  # encoding=str / "unicode"
def tostring(  # type: ignore[overload-overlap]  # pyright: ignore[reportOverlappingOverload]
    doc: _ElementOrTree[HtmlElement],
    *,
    pretty_print: bool = False,
    include_meta_content_type: bool = False,
    encoding: type[str] | Literal["unicode"],
    method: _OutputMethodArg = "html",
    with_tail: bool = True,
    doctype: str | None = None,
) -> str: ...
@overload  # encoding="..." / None, no encoding arg
def tostring(
    doc: _ElementOrTree[HtmlElement],
    *,
    pretty_print: bool = False,
    include_meta_content_type: bool = False,
    encoding: str | None = None,
    method: _OutputMethodArg = "html",
    with_tail: bool = True,
    doctype: str | None = None,
) -> bytes: ...

#
# For debugging
#
def open_in_browser(
    doc: _ElementOrTree[HtmlElement], encoding: str | type[str] | None = None
) -> None: ...
