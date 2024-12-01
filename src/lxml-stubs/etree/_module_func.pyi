import sys
from typing import Any, Collection, Iterable, Literal, final, overload

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never

if sys.version_info >= (3, 13):
    from typing import TypeIs
    from warnings import deprecated
else:
    from typing_extensions import TypeIs, deprecated

from .._types import (
    _ET,
    _AnyStr,
    _DefEtreeParsers,
    _ElementOrTree,
    _ET_co,
    _FileReadSource,
    _OutputMethodArg,
)
from ._element import _Element, _ElementTree
from ._parser import HTMLParser, XMLParser

@overload
def HTML(
    text: _AnyStr,
    parser: HTMLParser[_ET_co],
    *,
    base_url: _AnyStr | None = None,
) -> _ET_co: ...
@overload
def HTML(
    text: _AnyStr,
    parser: None = None,
    *,
    base_url: _AnyStr | None = None,
) -> _Element: ...
@overload
def XML(
    text: _AnyStr,
    parser: XMLParser[_ET_co],
    *,
    base_url: _AnyStr | None = None,
) -> _ET_co: ...
@overload
def XML(
    text: _AnyStr,
    parser: None = None,
    *,
    base_url: _AnyStr | None = None,
) -> _Element: ...
@overload
def parse(
    source: _FileReadSource,
    parser: _DefEtreeParsers[_ET_co],
    *,
    base_url: _AnyStr | None = None,
) -> _ElementTree[_ET_co]:
    """Return an ElementTree object loaded with source elements.  If no parser
    is provided as second argument, the default parser is used.

    The ``source`` can be any of the following:

    - a file name/path
    - a file object
    - a file-like object
    - a URL using the HTTP or FTP protocol

    To parse from a string, use the ``fromstring()`` function instead.

    Note that it is generally faster to parse from a file path or URL
    than from an open file object or file-like object.  Transparent
    decompression from gzip compressed sources is supported (unless
    explicitly disabled in libxml2).

    The ``base_url`` keyword allows setting a URL for the document
    when parsing from a file-like object.  This is needed when looking
    up external entities (DTD, XInclude, ...) with relative paths.
    """

@overload
def parse(
    source: _FileReadSource,
    parser: None = None,
    *,
    base_url: _AnyStr | None = None,
) -> _ElementTree: ...
@overload
def fromstring(
    text: _AnyStr,
    parser: _DefEtreeParsers[_ET_co],
    *,
    base_url: _AnyStr | None = None,
) -> _ET_co:
    """Parses an XML document or fragment from a string.  Returns the
    root node (or the result returned by a parser target).

    To override the default parser with a different parser you can pass it to
    the ``parser`` keyword argument.

    The ``base_url`` keyword argument allows to set the original base URL of
    the document to support relative Paths when looking up external entities
    (DTD, XInclude, ...).
    """

@overload
def fromstring(
    text: _AnyStr,
    parser: None = None,
    *,
    base_url: _AnyStr | None = None,
) -> _Element: ...
@overload
@deprecated("Raises exception if input is a single string")
def fromstringlist(
    strings: _AnyStr,
    *args: Any,
    **kw: Any,
) -> Never:
    """Parses an XML document from a sequence of strings.  Returns the
    root node (or the result returned by a parser target).

    To override the default parser with a different parser you can pass it to
    the ``parser`` keyword argument.
    """

@overload
def fromstringlist(
    strings: Iterable[_AnyStr],
    parser: _DefEtreeParsers[_ET_co],
) -> _ET_co: ...
@overload
def fromstringlist(
    strings: Iterable[_AnyStr],
    parser: None = None,
) -> _Element: ...

# Under XML Canonicalization (C14N) mode, most arguments are ignored,
# some arguments would even raise exception outright if specified.
@overload  # warn if inclusive_ns_prefixes is not collection
@deprecated(
    "'inclusive_ns_prefixes' should be collection, otherwise "
    "will either search for wrong NS prefix or raise exception"
)
def tostring(
    element_or_tree: Any,
    *,
    inclusive_ns_prefixes: _AnyStr,
    **_kw: Any,
) -> Never:
    """Serialize an element to an encoded string representation of its XML tree.

    Annotation
    ----------
    There are 4 function overloads:
    1. C14N version 1 (``method="c14n"``) with its keyword arguments
    2. C14N version 2 (``method="c14n2"``) with its keyword arguments
    3. Other output methods, with ``encoding=str`` or ``encoding="unicode"``.
    Returns native string. In this case the usage of ``xml_declaration``
    argument is disallowed.
    4. Other output methods, with all other encodings. Returns byte string.

    Original docstring
    ------------------
    Defaults to ASCII encoding without XML declaration.  This
    behavior can be configured with the keyword arguments ``encoding``
    (string) and ``xml_declaration`` (bool).  Note that changing the
    encoding to a non UTF-8 compatible encoding will enable a
    declaration by default.

    You can also serialise to a Unicode string without declaration by
    passing the name ``'unicode'`` as encoding (or the ``str`` function
    in Py3 or ``unicode`` in Py2).  This changes the return value from
    a byte string to an unencoded unicode string.

    The keyword argument ``pretty_print`` (bool) enables formatted XML.

    The keyword argument ``method`` selects the output method: 'xml',
    'html', plain 'text' (text content without tags), 'c14n' or 'c14n2'.
    Default is 'xml'.

    With ``method="c14n"`` (C14N version 1), the options ``exclusive``,
    ``with_comments`` and ``inclusive_ns_prefixes`` request exclusive
    C14N, include comments, and list the inclusive prefixes respectively.

    With ``method="c14n2"`` (C14N version 2), the ``with_comments`` and
    ``strip_text`` options control the output of comments and text space
    according to C14N 2.0.

    Passing a boolean value to the ``standalone`` option will output
    an XML declaration with the corresponding ``standalone`` flag.

    The ``doctype`` option allows passing in a plain string that will
    be serialised before the XML tree.  Note that passing in non
    well-formed content here will make the XML output non well-formed.
    Also, an existing doctype in the document tree will not be removed
    when serialising an ElementTree instance.

    You can prevent the tail text of the element from being serialised
    by passing the boolean ``with_tail`` option.  This has no impact
    on the tail text of children, which will always be serialised.
    """

@overload  # method="c14n"
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n"],
    exclusive: bool = False,
    inclusive_ns_prefixes: Collection[_AnyStr] | None = None,
    with_comments: bool = True,
) -> bytes: ...
@overload  # method="c14n2"
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n2"],
    with_comments: bool = True,
    strip_text: bool = False,
) -> bytes: ...
@overload  # Native str, no XML declaration allowed
def tostring(  # type: ignore[overload-overlap]  # pyright: ignore[reportOverlappingOverload]
    element_or_tree: _ElementOrTree,
    *,
    encoding: type[str] | Literal["unicode"],
    method: _OutputMethodArg = "xml",
    pretty_print: bool = False,
    with_tail: bool = True,
    standalone: bool | None = None,
    doctype: str | None = None,
) -> str: ...
@overload  # byte str
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    encoding: str | None = None,
    method: _OutputMethodArg = "xml",
    xml_declaration: bool | None = None,
    pretty_print: bool = False,
    with_tail: bool = True,
    standalone: bool | None = None,
    doctype: str | None = None,
) -> bytes: ...
def indent(
    tree: _ElementOrTree,
    space: str = "  ",
    *,
    level: int = 0,
) -> None:
    """Indent an XML document by inserting newlines and indentation space
    after elements.

    ``tree`` is the ElementTree or Element to modify.  The (root) element
    itself will not be changed, but the tail text of all elements in its
    subtree will be adapted.

    ``space`` is the whitespace to insert for each indentation level, two
    space characters by default.

    ``level`` is the initial indentation level. Setting this to a higher
    value than 0 can be used for indenting subtrees that are more deeply
    nested inside of a document.
    """

@deprecated(
    "For ElementTree 1.3 compat only; result is tostring() output wrapped inside a list"
)
def tostringlist(
    element_or_tree: _ElementOrTree, *args: Any, **__kw: Any
) -> list[str]: ...
@deprecated('Since v3.3.2; use tostring() with encoding="unicode" argument')
def tounicode(
    element_or_tree: _ElementOrTree,
    *,
    method: str = "xml",
    pretty_print: bool = False,
    with_tail: bool = True,
    doctype: str | None = None,
) -> None: ...
def iselement(element: object) -> TypeIs[_Element]:
    """Checks if an object appears to be a valid element object."""

# HACK PyCapsule needs annotation of ctypes.pythonapi, which has no
# annotation support currently. Use generic object for now.
@overload
def adopt_external_document(
    capsule: object,
    parser: _DefEtreeParsers[_ET],
) -> _ElementTree[_ET]:
    """Unpack a libxml2 document pointer from a PyCapsule and
    wrap it in an lxml ElementTree object.

    Original Docstring
    ------------------
    This allows external libraries to build XML/HTML trees using libxml2
    and then pass them efficiently into lxml for further processing.

    If a ``parser`` is provided, it will be used for configuring the
    lxml document.  No parsing will be done.

    The capsule must have the name ``"libxml2:xmlDoc"`` and its pointer
    value must reference a correct libxml2 document of type ``xmlDoc*``.
    The creator of the capsule must take care to correctly clean up the
    document using an appropriate capsule destructor.  By default, the
    libxml2 document will be copied to let lxml safely own the memory
    of the internal tree that it uses.

    If the capsule context is non-NULL, it must point to a C string that
    can be compared using ``strcmp()``.  If the context string equals
    ``"destructor:xmlFreeDoc"``, the libxml2 document will not be copied
    but the capsule invalidated instead by clearing its destructor and
    name.  That way, lxml takes ownership of the libxml2 document in memory
    without creating a copy first, and the capsule destructor will not be
    called.  The document will then eventually be cleaned up by lxml using
    the libxml2 API function ``xmlFreeDoc()`` once it is no longer used.

    If no copy is made, later modifications of the tree outside of lxml
    should not be attempted after transferring the ownership.
    """

@overload
def adopt_external_document(
    capsule: object,
    parser: None = None,
) -> _ElementTree: ...
def register_namespace(prefix: _AnyStr, uri: _AnyStr) -> None:
    """Registers a namespace prefix that newly created Elements in that
    namespace will use.  The registry is global, and any existing
    mapping for either the given prefix or the namespace URI will be
    removed."""

# Debugging only
def dump(elem: _Element, *, pretty_print: bool = True, with_tail: bool = True) -> None:
    """Writes an element tree or element structure to sys.stdout.
    This function should be used for debugging only."""
@final
class _MemDebug:
    """Debugging support for the memory allocation in libxml2"""

    def bytes_used(self) -> int:
        """
        Returns
        -------
        int
            The total amount of memory (in bytes) currently used by libxml2.
            Note that libxml2 constrains this value to a C int, which limits
            the accuracy on 64 bit systems.
        """
    def blocks_used(self) -> int:
        """
        Returns
        -------
        int
            The total number of memory blocks currently allocated by libxml2.
            Note that libxml2 constrains this value to a C int, which limits
            the accuracy on 64 bit systems.
        """
    def dict_size(self) -> int:
        """
        Returns
        -------
        int
            The current size of the global name dictionary used by libxml2
            for the current thread.  Each thread has its own dictionary.
        """
    def dump(
        self, output_file: _AnyStr | None = None, byte_count: int | None = None
    ) -> None:
        """Dumps the current memory blocks allocated by libxml2 to a file

        Parameters
        ----------
        output_file : str or bytes, optional
            Output file path, default is ".memorylist" under current directory
        byte_count : int, optional
            Limits number of bytes in the dump, default is None (unlimited)
        """
    def show(
        self, output_file: _AnyStr | None = None, block_count: int | None = None
    ) -> None:
        """Dumps the current memory blocks allocated by libxml2 to a file
        The output file format is suitable for line diffing.

        Parameters
        ----------
        output_file : str or bytes, optional
            Output file path, default is ".memorydump" under current directory
        block_count : int, optional
            Limits number of blocks in the dump, default is None (unlimited)
        """

memory_debugger: _MemDebug
"""Debugging support for the memory allocation in libxml2"""
