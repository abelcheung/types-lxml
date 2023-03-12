from typing import Iterable

from .._types import _AnyStr, _NSMapArg
from . import _ElementOrTree, _TagSelector

def cleanup_namespaces(
    tree_or_element: _ElementOrTree,
    top_nsmap: _NSMapArg | None = ...,
    keep_ns_prefixes: Iterable[_AnyStr] | None = ...,
) -> None: ...
def strip_attributes(
    tree_or_element: _ElementOrTree,
    *attribute_names: str,
) -> None: ...
def strip_elements(
    tree_or_element: _ElementOrTree,
    *tag_names: _TagSelector,
    with_tail: bool = ...,
) -> None: ...
def strip_tags(
    tree_or_element: _ElementOrTree,
    *tag_names: _TagSelector,
) -> None: ...
