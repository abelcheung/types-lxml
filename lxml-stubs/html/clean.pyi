#
# lxml.html.clean was removed from lxml proper since 5.2.0,
# and extracted into its own project.
# https://github.com/fedora-python/lxml_html_clean/
#
# Although this part of stub is merged into lxml_html_clean
# project, it will be kept here for a while for compatibility,
# until most people migrate to newer lxml versions.
#
# Some arguments comes with a complex or longish default
# values, it is better to look up API doc or source directly
#

from typing import Collection, Iterable, Literal, Pattern, TypeVar, overload

from .._types import _ElementOrTree
from ..etree import _ElementTree
from . import HtmlElement
from ._funcs import _HtmlDoc_T

# Similar to _funcs._HtmlDoc_T, but also supports ET; only used in Cleaner
_DT = TypeVar("_DT", str, bytes, HtmlElement, _ElementTree[HtmlElement])

class Cleaner:
    @overload  # if allow_tags present, remove_unknown_tags must be False
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
        remove_tags: Collection[str] = (),
        allow_tags: Collection[str] = (),
        kill_tags: Collection[str] = (),
        remove_unknown_tags: Literal[False] = False,
        safe_attrs_only: bool = True,
        safe_attrs: Collection[str] = ...,  # keep ellipsis
        add_nofollow: bool = False,
        host_whitelist: Collection[str] = (),
        whitelist_tags: Collection[str] | None = {"iframe", "embed"},
    ) -> None: ...
    @overload  # ... otherwise allow_tags arg must not exist
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
        remove_tags: Collection[str] = (),
        kill_tags: Collection[str] = (),
        remove_unknown_tags: bool = True,
        safe_attrs_only: bool = True,
        safe_attrs: Collection[str] = ...,  # keep ellipsis
        add_nofollow: bool = False,
        host_whitelist: Collection[str] = (),
        whitelist_tags: Collection[str] = {"iframe", "embed"},
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
    avoid_elements: Collection[str] = ...,  # keep ellipsis
    avoid_hosts: Iterable[Pattern[str]] = ...,  # keep ellipsis
    avoid_classes: Collection[str] = ["nolink"],
) -> None: ...
def autolink_html(
    html: _HtmlDoc_T,
    link_regexes: Iterable[Pattern[str]] = ...,  # keep ellipsis
    avoid_elements: Collection[str] = ...,  # keep ellipsis
    avoid_hosts: Iterable[Pattern[str]] = ...,  # keep ellipsis
    avoid_classes: Collection[str] = ["nolink"],
) -> _HtmlDoc_T: ...
def word_break(
    el: HtmlElement,
    max_width: int = 40,
    avoid_elements: Collection[str] = ["pre", "textarea", "code"],
    avoid_classes: Collection[str] = ["nobreak"],
    break_character: str = chr(0x200B),
) -> None: ...
def word_break_html(
    html: _HtmlDoc_T,
    max_width: int = 40,
    avoid_elements: Collection[str] = ["pre", "textarea", "code"],
    avoid_classes: Collection[str] = ["nobreak"],
    break_character: str = chr(0x200B),
) -> _HtmlDoc_T: ...
