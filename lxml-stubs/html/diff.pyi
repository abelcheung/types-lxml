from typing import Callable, Iterable

from .._types import _AnyStr
from ..etree import _Element

def html_annotate(
    doclist: Iterable[tuple[str, object]],
    markup: Callable[[str, object], str] = ...,
) -> str: ...
def htmldiff(
    old_html: _Element | _AnyStr,
    new_html: _Element | _AnyStr,
) -> str: ...
