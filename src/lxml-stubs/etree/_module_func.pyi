import sys
from typing import (
    Any,
    Collection,
    Iterable,
    Literal,
    TypeVar,
    final,
    overload,
)

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never

if sys.version_info >= (3, 12):
    from collections.abc import Buffer
else:
    from typing_extensions import Buffer

if sys.version_info >= (3, 13):
    from typing import TypeIs
    from warnings import deprecated
else:
    from typing_extensions import TypeIs, deprecated

from .._types import (
    _ET,
    _DefEtreeParsers,
    _ElementOrTree,
    _ET_co,
    _FileReadSource,
    _OutputMethodArg,
    _TextArg,
)
from ._element import _Element, _ElementTree
from ._parser import CustomTargetParser, HTMLParser, XMLParser

_T = TypeVar("_T")

@overload
def HTML(
    text: str | Buffer,
    parser: HTMLParser[_ET_co],
    *,
    base_url: str | bytes | None = None,
) -> _ET_co:
    """Parses an HTML document or fragment from a string constant.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    When subscripted `etree.HTMLParser` is provided that indicate it can produce
    some `_Element` subclass, `HTML()` returns a node of that subclass.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Using-specialised-class-directly#no-automatic-change-of-subscript)
    on how to create such annotation-only specialized parsers.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTML)
    """

@overload
def HTML(
    text: str | Buffer,
    parser: CustomTargetParser[_T],
    *,
    base_url: str | bytes | None = None,
) -> _T:
    """Parses an HTML document or fragment from a string constant.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    When specially constructed parser with custom parser target is supplied,
    `HTML()` returns that value dictated in parser target definition, that is
    the parser target `.close()` method return value.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser)
    on how to create fully annotated parser with custom target object.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTML)
    """

@overload
def HTML(
    text: str | Buffer,
    parser: None = None,
    *,
    base_url: str | bytes | None = None,
) -> _Element:
    """Parses an HTML document or fragment from a string constant.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    This overload handles usage of `HTML()` with default parser.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.HTML)
    """

@overload
def XML(
    text: str | Buffer,
    parser: XMLParser[_ET_co],
    *,
    base_url: str | bytes | None = None,
) -> _ET_co:
    """Parses an XML document or fragment from a string constant.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    When subscripted `etree.XMLParser` is provided that indicate it can produce
    some `_Element` subclass, `XML()` returns a node of that subclass.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Using-specialised-class-directly#no-automatic-change-of-subscript)
    on how to create such annotation-only specialized parsers.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XML)
    """

@overload
def XML(
    text: str | Buffer,
    parser: CustomTargetParser[_T],
    *,
    base_url: str | bytes | None = None,
) -> _T:
    """Parses an XML document or fragment from a string constant.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    When specially constructed parser with custom parser target is supplied,
    `XML()` returns that value dictated in parser target definition, that is
    the parser target `.close()` method return value.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser)
    on how to create fully annotated parser with custom target object.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XML)
    """

@overload
def XML(
    text: str | Buffer,
    parser: None = None,
    *,
    base_url: str | bytes | None = None,
) -> _Element:
    """Parses an XML document or fragment from a string constant.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    This overload handles usage of `XML()` with default parser.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XML)
    """

@overload  # common parser
def parse(
    source: _FileReadSource,
    parser: _DefEtreeParsers[_ET_co],
    *,
    base_url: str | bytes | None = None,
) -> _ElementTree[_ET_co]:
    """Return an ElementTree object loaded with source elements.

    Annotation
    ----------
    When subscripted `etree.XMLParser` or `etree.HTMLParser` is provided
    that indicate it can produce some `_Element` subclass, this function
    returns an `_ElementTree` containing node of that subclass.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Using-specialised-class-directly#no-automatic-change-of-subscript)
    on how to create such annotation-only specialized parsers.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.parse)
    """

@overload  # custom target parser
def parse(
    source: _FileReadSource,
    parser: CustomTargetParser[_T],
    *,
    base_url: str | bytes | None = None,
) -> _T:
    """Return an ElementTree object loaded with source elements.

    Annotation
    ----------
    When specially constructed parser with custom parser target is supplied,
    `parse()` returns that value dictated in parser target definition,
    that is the parser target `.close()` method return value.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser)
    on how to create fully annotated parser with custom target object.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.parse)
    """

@overload  # parser not supplied
def parse(
    source: _FileReadSource,
    parser: None = None,
    *,
    base_url: str | bytes | None = None,
) -> _ElementTree:
    """Return an ElementTree object loaded with source elements.

    Annotation
    ----------
    This overload handles usage of `parse()` with default parser.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.parse)
    """

@overload  # common parser
def fromstring(
    text: str | Buffer,
    parser: _DefEtreeParsers[_ET_co],
    *,
    base_url: str | bytes | None = None,
) -> _ET_co:
    """Parses an XML document or fragment from a string.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    When subscripted `etree.XMLParser` or `etree.HTMLParser` is provided
    that indicate it can produce some `_Element` subclass, this function
    returns a node of that subclass.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Using-specialised-class-directly#no-automatic-change-of-subscript)
    on how to create such annotation-only specialized parsers.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.fromstring)
    """

@overload  # custom target parser
def fromstring(
    text: str | Buffer,
    parser: CustomTargetParser[_T],
    *,
    base_url: str | bytes | None = None,
) -> _T:
    """Parses an XML document or fragment from a string.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    When specially constructed parser with custom parser target is supplied,
    `fromstring()` returns that value dictated in parser target definition,
    that is the parser target `.close()` method return value.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser)
    on how to create fully annotated parser with custom target object.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.fromstring)
    """

@overload  # parser not supplied
def fromstring(
    text: str | Buffer,
    parser: None = None,
    *,
    base_url: str | bytes | None = None,
) -> _Element:
    """Parses an XML document or fragment from a string.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    This overload handles usage of `fromstring()` with default parser.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.fromstring)
    """

@overload
@deprecated("Raises exception if input is a single string")
def fromstringlist(
    strings: str | bytes,
    parser: Any = None,
) -> Never:
    """Parses an XML document from a sequence of strings.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    This `@overload` is a guard against using single string as input, which is
    specifically disallowed in source but permitted in typing.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.fromstringlist)
    """

@overload  # common parser
def fromstringlist(
    strings: Iterable[str | bytes],
    parser: _DefEtreeParsers[_ET_co],
) -> _ET_co:
    """Parses an XML document from a sequence of strings.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    When subscripted `etree.XMLParser` or `etree.HTMLParser` is provided
    that indicate it can produce some `_Element` subclass, this function
    returns a node of that subclass.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Using-specialised-class-directly#no-automatic-change-of-subscript)
    on how to create such annotation-only specialized parsers.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.fromstringlist)
    """

@overload  # custom target parser
def fromstringlist(
    strings: Iterable[str | bytes],
    parser: CustomTargetParser[_T],
) -> _T:
    """Parses an XML document from a sequence of strings.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    When specially constructed parser with custom parser target is supplied,
    `fromstringlist()` returns that value dictated in parser target definition,
    that is the parser target `.close()` method return value.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser)
    on how to create fully annotated parser with custom target object.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.fromstringlist)
    """

@overload  # parser not supplied
def fromstringlist(
    strings: Iterable[str | bytes],
    parser: None = None,
) -> _Element:
    """Parses an XML document from a sequence of strings.
    Returns the root node (or the result returned by a parser target).

    Annotation
    ----------
    This overload handles usage of `fromstringlist()` with default parser.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.fromstringlist)
    """

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
) -> str:
    """Serialize an element to an encoded string representation of its XML tree.

    Annotation
    ----------
    This `@overload` covers the case where `encoding` is either literal string
    `"unicode"` or the type `str`. In such case, the returned value is a
    native Python string.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.tostring)
    """

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
) -> bytes:
    """Serialize an element to an encoded string representation of its XML tree.

    Annotation
    ----------
    This `@overload` covers all remaining generic usage of `tostring()`.
    Returns byte string.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.tostring)
    """

# Under XML Canonicalization (C14N) mode, most arguments are ignored,
# some arguments would even raise exception outright if specified.
@overload  # method="c14n2"
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n2"],
    with_comments: bool = True,
    strip_text: bool = False,
) -> bytes:
    """Serialize an element to an encoded string representation of its XML tree.

    Annotation
    ----------
    This `@overload` covers C14N version 2 (``method="c14n2"``), along with its
    specific keyword arguments.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.tostring)
    """

@overload  # warn if inclusive_ns_prefixes is not collection
@deprecated(
    "`inclusive_ns_prefixes` should be collection, otherwise "
    "will either search for wrong NS prefix or raise exception"
)
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n"],
    exclusive: bool = False,
    with_comments: bool = True,
    inclusive_ns_prefixes: _TextArg,
) -> Never:
    """Serialize an element to an encoded string representation of its XML tree.

    Annotation
    ----------
    This `@overload` is a guard against using plain string in
    `inclusive_ns_prefixes` argument, which can result in subtle bug.
    The prefix string would be split into single characters and each
    treated as a separate namespace prefix.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.tostring)
    """

@overload  # method="c14n"
def tostring(
    element_or_tree: _ElementOrTree,
    *,
    method: Literal["c14n"],
    exclusive: bool = False,
    inclusive_ns_prefixes: Collection[_TextArg] | None = None,
    with_comments: bool = True,
) -> bytes:
    """Serialize an element to an encoded string representation of its XML tree.

    Annotation
    ----------
    This `@overload` covers C14N version 1 (``method="c14n"``), along with its
    specific keyword arguments.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.tostring)
    """

def indent(
    tree: _ElementOrTree,
    space: str = "  ",
    *,
    level: int = 0,
) -> None:
    """Indent an XML document by inserting newlines and indentation space
    after elements.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.indent)
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
def iselement(element: object) -> TypeIs[_Element]: ...

# HACK PyCapsule needs annotation of ctypes.pythonapi, which has no
# annotation support currently. Use generic object for now.
@overload
def adopt_external_document(
    capsule: object,
    parser: _DefEtreeParsers[_ET],
) -> _ElementTree[_ET]:
    """Unpack a libxml2 document pointer from a PyCapsule and
    wrap it in an lxml ElementTree object.

    Annotation
    ----------
    When subscripted `etree.XMLParser` or `etree.HTMLParser` is provided
    that indicate it can produce some `_Element` subclass, this function
    returns an `_ElementTree` containing node of that subclass.

    Please [refer to wiki](https://github.com/abelcheung/types-lxml/wiki/Using-specialised-class-directly#no-automatic-change-of-subscript)
    on how to create such annotation-only specialized parsers.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.adopt_external_document)
    """

@overload
def adopt_external_document(
    capsule: object,
    parser: None = None,
) -> _ElementTree:
    """Unpack a libxml2 document pointer from a PyCapsule and
    wrap it in an lxml ElementTree object.

    See Also
    --------
    [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.adopt_external_document)
    """

def register_namespace(prefix: _TextArg, uri: _TextArg) -> None: ...

# Debugging only
def dump(
    elem: _Element, *, pretty_print: bool = True, with_tail: bool = True
) -> None: ...

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
    @deprecated("Removed since 6.0, due to corresponding removal in libxml2")
    def dump(
        self, output_file: str | bytes | None = None, byte_count: int | None = None
    ) -> None:
        """Dumps the current memory blocks allocated by libxml2 to a file

        Parameters
        ----------
        output_file : str or bytes, optional
            Output file path, default is ".memorylist" under current directory
        byte_count : int, optional
            Limits number of bytes in the dump, default is None (unlimited)
        """
    @deprecated("Removed since 6.0, due to corresponding removal in libxml2")
    def show(
        self, output_file: str | bytes | None = None, block_count: int | None = None
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
