import sys
from typing import Iterable, overload

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
@deprecated("Supply an iterable of namespace prefixes, instead of a vanilla prefix.")
def cleanup_namespaces(
    tree_or_element: _ElementOrTree,
    top_nsmap: _NSMapArg | None,
    keep_ns_prefixes: _TextArg,
) -> None:
    """Remove all namespace declarations from a subtree that are not used by any
    of the elements or attributes in that tree.

    Annotation
    ----------
    This overload guards against using a single namespace prefix string in
    `keep_ns_prefixes` argument. Otherwise, the string is split into
    individual characters and each of them is treated as a namespace prefix.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.cleanup_namespaces)
    """

@overload
@deprecated("Supply an iterable of namespace prefixes, instead of a vanilla prefix.")
def cleanup_namespaces(
    tree_or_element: _ElementOrTree,
    top_nsmap: _NSMapArg | None = None,
    *,
    keep_ns_prefixes: _TextArg,
) -> None:
    """Remove all namespace declarations from a subtree that are not used by any
    of the elements or attributes in that tree.

    Annotation
    ----------
    This overload guards against using a single namespace prefix string in
    `keep_ns_prefixes` argument. Otherwise, the string is split into
    individual characters and each of them is treated as a namespace prefix.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.cleanup_namespaces)
    """

@overload
def cleanup_namespaces(
    tree_or_element: _ElementOrTree,
    top_nsmap: _NSMapArg | None = None,
    keep_ns_prefixes: Iterable[_TextArg] | None = None,
) -> None:
    """Remove all namespace declarations from a subtree that are not used by any
    of the elements or attributes in that tree.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.cleanup_namespaces)
    """

# For functions below, the first `tree_or_element` argument
# can never be keyword argument, since tag/attribute names
# that followed are considered positional arguments in
# all possible function signature overloads.

# strip_attributes internally uses _MultiTagMatcher and
# treat attributes like tags
@overload
def strip_attributes(
    tree_or_element: _ElementOrTree,
    *attribute_names: _AttrNameKey,
) -> None: ...
@overload
def strip_attributes(
    tree_or_element: _ElementOrTree,
    attribute_names: Iterable[_AttrNameKey],
    /,
) -> None: ...
@overload
def strip_elements(
    tree_or_element: _ElementOrTree,
    *tag_names: _TagSelector,
    with_tail: bool = True,
) -> None: ...
@overload
def strip_elements(
    tree_or_element: _ElementOrTree,
    tag_names: Iterable[_TagSelector],
    /,
    *,
    with_tail: bool = True,
) -> None: ...
@overload
def strip_tags(
    tree_or_element: _ElementOrTree,
    *tag_names: _TagSelector,
) -> None: ...
@overload
def strip_tags(
    tree_or_element: _ElementOrTree,
    tag_names: Iterable[_TagSelector],
    /,
) -> None: ...
