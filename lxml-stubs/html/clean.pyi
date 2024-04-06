#
# lxml.html.clean was removed from lxml proper since 5.2.0,
# and extracted into its own project.
# https://github.com/fedora-python/lxml_html_clean/
#
# This stub will be kept for a while for compatibility,
# until most people migrate to newer lxml versions.
#
# Some arguments comes with a complex or longish default
# values, it is better to look up API doc or source directly
#

import sys
from typing import Iterable, Pattern, TypeVar, Union, overload

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from .._types import _ElementOrTree, _ElemFactory
from ..etree import _ElementTree
from . import HtmlElement
from ._funcs import _HtmlDoc_T

# Version of tag selector that doesn't support QName helper
_HTagSelector: TypeAlias = Union[str, bytes, _ElemFactory]

# Similar to _funcs._HtmlDoc_T, but also supports ET; only used in Cleaner
_DT = TypeVar("_DT", str, bytes, HtmlElement, _ElementTree[HtmlElement])

class Cleaner:
    @overload  # allow_tags present and remove_unknown_tags absent
    def __init__(
        self,
        *,
        scripts: bool = True,
        javascript: bool = True,
        comments: bool = True,
        style: bool = False,
        inline_style: bool | None = None,
        links: bool = True,
        meta: bool = True,
        page_structure: bool = True,
        processing_instructions: bool = True,
        embedded: bool = True,
        frames: bool = True,
        forms: bool = True,
        annoying_tags: bool = True,
        remove_tags: Iterable[_HTagSelector] = (),
        allow_tags: Iterable[_HTagSelector] = (),
        kill_tags: Iterable[_HTagSelector] = (),
        safe_attrs_only: bool = True,
        safe_attrs: Iterable[str] = ...,  # keep ellipsis
        add_nofollow: bool = False,
        host_whitelist: Iterable[str] = (),
        whitelist_tags: Iterable[str] | None = {"iframe", "embed"},
    ) -> None: ...
    @overload  # vice versa
    def __init__(
        self,
        *,
        scripts: bool = True,
        javascript: bool = True,
        comments: bool = True,
        style: bool = False,
        inline_style: bool | None = None,
        links: bool = True,
        meta: bool = True,
        page_structure: bool = True,
        processing_instructions: bool = True,
        embedded: bool = True,
        frames: bool = True,
        forms: bool = True,
        annoying_tags: bool = True,
        remove_tags: Iterable[_HTagSelector] = (),
        kill_tags: Iterable[_HTagSelector] = (),
        remove_unknown_tags: bool = True,
        safe_attrs_only: bool = True,
        safe_attrs: Iterable[str] = ...,  # keep ellipsis
        add_nofollow: bool = False,
        host_whitelist: Iterable[str] = (),
        whitelist_tags: Iterable[str] = {"iframe", "embed"},
    ) -> None: ...
    def __call__(self, doc: _ElementOrTree[HtmlElement]) -> None: ...
    def allow_follow(self, anchor: HtmlElement) -> bool: ...
    def allow_element(self, el: HtmlElement) -> bool: ...
    def allow_embedded_url(self, el: HtmlElement, url: str) -> bool: ...
    def kill_conditional_comments(self, doc: _ElementOrTree[HtmlElement]) -> None: ...
    def clean_html(self, html: _DT) -> _DT: ...

clean: Cleaner
clean_html = clean.clean_html

def autolink(
    el: HtmlElement,
    link_regexes: Iterable[Pattern[str]] = ...,  # keep ellipsis
    avoid_elements: Iterable[str] = ...,  # keep ellipsis
    avoid_hosts: Iterable[Pattern[str]] = ...,  # keep ellipsis
    avoid_classes: Iterable[str] = ["nolink"],
) -> None: ...
def autolink_html(
    html: _HtmlDoc_T,
    link_regexes: Iterable[Pattern[str]] = ...,  # keep ellipsis
    avoid_elements: Iterable[str] = ...,  # keep ellipsis
    avoid_hosts: Iterable[Pattern[str]] = ...,  # keep ellipsis
    avoid_classes: Iterable[str] = ["nolink"],
) -> _HtmlDoc_T: ...
def word_break(
    el: HtmlElement,
    max_width: int = 40,
    avoid_elements: Iterable[str] = ["pre", "textarea", "code"],
    avoid_classes: Iterable[str] = ["nobreak"],
    break_character: str = chr(0x200B),
) -> None: ...
def word_break_html(
    html: _HtmlDoc_T,
    max_width: int = 40,
    avoid_elements: Iterable[str] = ["pre", "textarea", "code"],
    avoid_classes: Iterable[str] = ["nobreak"],
    break_character: str = chr(0x200B),
) -> _HtmlDoc_T: ...
