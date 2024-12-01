import sys
from typing import Collection, Iterable, overload

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

from .._types import (
    _AttrNameKey,
    _ElementOrTree,
    _NSMapArg,
    _TagSelector,
    _TextArg,
)

@overload
@deprecated("Supply an iterator or collection of namespace prefixes instead.")
def cleanup_namespaces(
    tree_or_element: _ElementOrTree,
    top_nsmap: _NSMapArg | None = None,
    keep_ns_prefixes: _TextArg | None = None,
) -> None: ...
@overload
def cleanup_namespaces(
    tree_or_element: _ElementOrTree,
    top_nsmap: _NSMapArg | None = None,
    keep_ns_prefixes: Iterable[_TextArg] | None = None,
) -> None: ...

# For functions below, the first `tree_or_element` argument
# can never be keyword argument, since tag/attribute names
# that followed are considered positional arguments in
# all possible function signature overloads.

# internal: bytearray disallowed for _MultiTagMatcher
@overload
def strip_attributes(
    tree_or_elem: _ElementOrTree,
    *attribute_names: _AttrNameKey,
) -> None: ...
@overload
def strip_attributes(
    tree_or_elem: _ElementOrTree, attribute_names: Iterable[_AttrNameKey], /
) -> None: ...
@overload
def strip_elements(
    __tree_or_elem: _ElementOrTree,
    *tag_names: _TagSelector,
    with_tail: bool = True,
) -> None: ...
@overload
def strip_elements(
    __tree_or_elem: _ElementOrTree,
    __tag: Collection[_TagSelector],
    /,
    with_tail: bool = True,
) -> None: ...
@overload
def strip_tags(
    __tree_or_elem: _ElementOrTree,
    *tag_names: _TagSelector,
) -> None: ...
@overload
def strip_tags(
    __tree_or_elem: _ElementOrTree, __tag: Collection[_TagSelector], /
) -> None: ...
