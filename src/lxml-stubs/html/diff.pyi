from typing import Callable, Iterable, TypeVar

from ..etree import _Element

_T = TypeVar("_T")

__all__ = ["html_annotate", "htmldiff"]

# annotation attribute can be anything, which is stringified
# later on; but the type would better be consistent though
def html_annotate(
    doclist: Iterable[tuple[str, _T]],
    markup: Callable[[str, _T], str] = ...,  # keep ellipsis
) -> str: ...
def htmldiff(
    old_html: _Element | str,
    new_html: _Element | str,
) -> str: ...
