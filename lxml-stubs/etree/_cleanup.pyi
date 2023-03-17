from typing import Iterable, overload

from .._types import _AnyStr, _ElementOrTree, _NSMapArg, _TagSelector

def cleanup_namespaces(
    tree_or_element: _ElementOrTree,
    top_nsmap: _NSMapArg | None = ...,
    keep_ns_prefixes: Iterable[_AnyStr] | None = ...,
) -> None: ...
def strip_attributes(
    tree_or_element: _ElementOrTree,
    *attribute_names: str,
) -> None: ...
@overload
def strip_elements(
    tree_or_element: _ElementOrTree,
    *tag_names: _TagSelector,
    with_tail: bool = ...,
) -> None: ...
@overload
def strip_elements(
    tree_or_element: _ElementOrTree,
    __tag: Iterable[_TagSelector] | None,
    /,
    with_tail: bool = ...,
) -> None: ...
@overload
def strip_tags(
    tree_or_element: _ElementOrTree,
    *tag_names: _TagSelector,
) -> None: ...
@overload
def strip_tags(
    tree_or_element: _ElementOrTree,
    __tag: Iterable[_TagSelector] | None,
) -> None: ...
