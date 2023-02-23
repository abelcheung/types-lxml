from typing import Iterable, Pattern, Union, overload

from ..etree import _Element, _ElementTree, _ElemFactory
from . import HtmlElement, _HtmlDoc_T
from .._types import Unused

# Version of tag selector that doesn't support QName helper
_HTagSelector = Union[str, bytes, _ElemFactory[_Element]]

class Cleaner:
    # allow_tags and remove_unknown_tags can't coexist
    @overload
    def __init__(
        self,
        *,
        scripts: bool = ...,
        javascript: bool = ...,
        comments: bool = ...,
        style: bool = ...,
        inline_style: bool | None = ...,
        links: bool = ...,
        meta: bool = ...,
        page_structure: bool = ...,
        processing_instructions: bool = ...,
        embedded: bool = ...,
        frames: bool = ...,
        forms: bool = ...,
        annoying_tags: bool = ...,
        remove_tags: Iterable[_HTagSelector] | None = ...,
        allow_tags: Iterable[_HTagSelector] | None = ...,
        kill_tags: Iterable[_HTagSelector] | None = ...,
        safe_attrs_only: bool = ...,
        safe_attrs: Iterable[str] = ...,
        add_nofollow: bool = ...,
        host_whitelist: Iterable[str] = ...,
        whitelist_tags: Iterable[str] | None = ...,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        scripts: bool = ...,
        javascript: bool = ...,
        comments: bool = ...,
        style: bool = ...,
        inline_style: bool | None = ...,
        links: bool = ...,
        meta: bool = ...,
        page_structure: bool = ...,
        processing_instructions: bool = ...,
        embedded: bool = ...,
        frames: bool = ...,
        forms: bool = ...,
        annoying_tags: bool = ...,
        remove_tags: Iterable[_HTagSelector] | None = ...,
        kill_tags: Iterable[_HTagSelector] | None = ...,
        remove_unknown_tags: bool = ...,
        safe_attrs_only: bool = ...,
        safe_attrs: Iterable[str] = ...,
        add_nofollow: bool = ...,
        host_whitelist: Iterable[str] = ...,
        whitelist_tags: Iterable[str] | None = ...,
    ) -> None: ...
    def __call__(self, doc: HtmlElement | _ElementTree[HtmlElement]) -> None: ...
    def allow_follow(self, anchor: HtmlElement) -> bool: ...
    def allow_element(self, el: HtmlElement) -> bool: ...
    def allow_embedded_url(self, el: HtmlElement, url: str) -> bool: ...
    def kill_conditional_comments(
        self, doc: HtmlElement | _ElementTree[HtmlElement]
    ) -> None: ...
    def clean_html(self, html: _HtmlDoc_T) -> _HtmlDoc_T: ...

clean: Cleaner
clean_html = clean.clean_html

def autolink(
    el: HtmlElement,
    link_regexes: Iterable[Pattern[str]] = ...,
    avoid_elements: Iterable[str] = ...,
    avoid_hosts: Iterable[Pattern[str]] = ...,
    avoid_classes: Iterable[str] = ...,
) -> None: ...
def autolink_html(
    html: _HtmlDoc_T,
    link_regexes: Iterable[Pattern[str]] = ...,
    avoid_elements: Iterable[str] = ...,
    avoid_hosts: Iterable[Pattern[str]] = ...,
    avoid_classes: Iterable[str] = ...,
) -> _HtmlDoc_T: ...
def word_break(
    el: HtmlElement,
    max_width: int = ...,
    avoid_elements: Unused = ...,
    avoid_classes: Iterable[str] = ...,
    break_character: str = ...,
) -> None: ...
def word_break_html(
    html: _HtmlDoc_T,
    max_width: int = ...,
    avoid_elements: Unused = ...,
    avoid_classes: Iterable[str] = ...,
    break_character: str = ...,
) -> _HtmlDoc_T: ...
