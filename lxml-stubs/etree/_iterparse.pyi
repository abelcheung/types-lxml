import sys
from _typeshed import SupportsRead, _T_co
from typing import IO, Iterable, Iterator, Literal, overload

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

if sys.version_info >= (3, 11):
    from typing import LiteralString
else:
    from typing_extensions import LiteralString

from .._types import (
    SupportsLaxedItems,
    _AnyStr,
    _ET_co,
    _FilePath,
    _NSMapArg,
    _SaxEventNames,
    _TagName,
    _TagSelector,
)
from ._classlookup import ElementClassLookup
from ._docloader import _ResolverRegistry
from ._element import _Element, _ElementTree
from ._xmlerror import _ListErrorLog
from ._xmlschema import XMLSchema

# See https://lxml.de/parsing.html#event-types
# Undocumented: 'comment' and 'pi' are actually supported!
_NoNSEventNames: TypeAlias = Literal["start", "end", "comment", "pi"]
_SaxNsEventValues: TypeAlias = tuple[str, str] | None  # for start-ns & end-ns event

class iterparse(Iterator[_T_co]):
    """Incremental parser

    Annotation
    ----------
    Totally 5 function signatures are available:
    - Default XML mode, where only `end` event is emitted
    - `start`, `end`, `comment` and `pi` events, where only
      Element values are produced
    - HTML mode (`html=True`), where namespace events are ignored
    - XML mode with `start-ns` or `end-ns` events, producing
      namespace tuple (for `start-ns`) or nothing (`end-ns`)
    - Final catch-all signature for XML mode

    Original Docstring
    ------------------
    Parses XML into a tree and generates tuples (event, element) in a
    SAX-like fashion. ``event`` is any of 'start', 'end', 'start-ns',
    'end-ns'.

    For 'start' and 'end', ``element`` is the Element that the parser just
    found opening or closing.  For 'start-ns', it is a tuple (prefix, URI) of
    a new namespace declaration.  For 'end-ns', it is simply None.  Note that
    all start and end events are guaranteed to be properly nested.

    The keyword argument ``events`` specifies a sequence of event type names
    that should be generated.  By default, only 'end' events will be
    generated.

    The additional ``tag`` argument restricts the 'start' and 'end' events to
    those elements that match the given tag.  The ``tag`` argument can also be
    a sequence of tags to allow matching more than one tag.  By default,
    events are generated for all elements.  Note that the 'start-ns' and
    'end-ns' events are not impacted by this restriction.

    The other keyword arguments in the constructor are mainly based on the
    libxml2 parser configuration.  A DTD will also be loaded if validation or
    attribute default values are requested."""

    @overload  # default values, only 'end' event emitted
    def __new__(
        cls,
        source: _FilePath | IO[bytes] | SupportsRead[bytes],
        events: None = ...,
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        remove_blank_text: bool = ...,
        compact: bool = ...,
        resolve_entities: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        encoding: _AnyStr | None = ...,
        html: bool = ...,
        recover: bool | None = ...,
        huge_tree: bool = ...,
        collect_ids: bool = ...,
        schema: XMLSchema | None = ...,
    ) -> iterparse[tuple[Literal["end"], _Element]]: ...
    @overload  # element-only events
    def __new__(
        cls,
        source: _FilePath | IO[bytes] | SupportsRead[bytes],
        events: Iterable[_NoNSEventNames],
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        remove_blank_text: bool = ...,
        compact: bool = ...,
        resolve_entities: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        encoding: _AnyStr | None = ...,
        html: bool = ...,
        recover: bool | None = ...,
        huge_tree: bool = ...,
        collect_ids: bool = ...,
        schema: XMLSchema | None = ...,
    ) -> iterparse[tuple[_NoNSEventNames, _Element]]: ...
    @overload  # html mode -> namespace events suppressed
    def __new__(
        cls,
        source: _FilePath | IO[bytes] | SupportsRead[bytes],
        events: Iterable[_SaxEventNames],
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        remove_blank_text: bool = ...,
        compact: bool = ...,
        resolve_entities: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        encoding: _AnyStr | None = ...,
        html: Literal[True],
        recover: bool | None = ...,
        huge_tree: bool = ...,
        collect_ids: bool = ...,
        schema: XMLSchema | None = ...,
    ) -> iterparse[tuple[_NoNSEventNames, _Element]]: ...
    @overload  # xml mode & NS-only events
    def __new__(
        cls,
        source: _FilePath | IO[bytes] | SupportsRead[bytes],
        events: Iterable[Literal["start-ns", "end-ns"]],
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        remove_blank_text: bool = ...,
        compact: bool = ...,
        resolve_entities: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        encoding: _AnyStr | None = ...,
        html: Literal[False] = ...,
        recover: bool | None = ...,
        huge_tree: bool = ...,
        collect_ids: bool = ...,
        schema: XMLSchema | None = ...,
    ) -> iterparse[
        tuple[Literal["start-ns"], tuple[str, str]] | tuple[Literal["end-ns"], None]
    ]: ...
    @overload  # xml mode, catch all
    def __new__(
        cls,
        source: _FilePath | IO[bytes] | SupportsRead[bytes],
        events: Iterable[_SaxEventNames],
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
        attribute_defaults: bool = ...,
        dtd_validation: bool = ...,
        load_dtd: bool = ...,
        no_network: bool = ...,
        remove_blank_text: bool = ...,
        compact: bool = ...,
        resolve_entities: bool = ...,
        remove_comments: bool = ...,
        remove_pis: bool = ...,
        strip_cdata: bool = ...,
        encoding: _AnyStr | None = ...,
        html: Literal[False] = ...,
        recover: bool | None = ...,
        huge_tree: bool = ...,
        collect_ids: bool = ...,
        schema: XMLSchema | None = ...,
    ) -> iterparse[
        tuple[_NoNSEventNames, _Element]
        | tuple[Literal["start-ns"], tuple[str, str]]
        | tuple[Literal["end-ns"], None]
    ]: ...
    def __next__(self) -> _T_co: ...
    # root property only present after parsing is done
    @property
    def root(self) -> _Element | None: ...
    @property
    def error_log(self) -> _ListErrorLog: ...
    @property
    def resolvers(self) -> _ResolverRegistry: ...
    @property
    def version(self) -> LiteralString: ...
    def set_element_class_lookup(
        self,
        lookup: ElementClassLookup | None = ...,
    ) -> None: ...
    def makeelement(
        self,
        _tag: _TagName,
        /,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        **_extra: _AnyStr,
    ) -> _Element: ...  # from etree pull parsers

class iterwalk(Iterator[_T_co]):
    """Tree walker that generates events from an existing tree as if it
    was parsing XML data with ``iterparse()``

    Annotation
    ----------
    Totally 4 function signatures, depending on `events` argument:
    - Default value, where only `end` event is emitted
    - `start`, `end`, `comment` and `pi` events, where only
      Element values are produced
    - Namespace events (`start-ns` or `end-ns`), producing
      namespace tuple (for `start-ns`) or nothing (`end-ns`)
    - Final catch-all for custom events combination


    Original Docstring
    ------------------
    Just as for ``iterparse()``, the ``tag`` argument can be a single tag or a
    sequence of tags.

    After receiving a 'start' or 'start-ns' event, the children and
    descendants of the current element can be excluded from iteration
    by calling the ``skip_subtree()`` method.
    """

    # There is no concept of html mode in iterwalk; namespace events
    # are not supressed like iterparse might do
    @overload  # default events
    def __new__(
        cls,
        element_or_tree: _ET_co | _ElementTree[_ET_co],
        events: None = ...,
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
    ) -> iterwalk[tuple[Literal["end"], _ET_co]]: ...
    @overload  # element-only events
    def __new__(
        cls,
        element_or_tree: _ET_co | _ElementTree[_ET_co],
        events: Iterable[_NoNSEventNames],
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
    ) -> iterwalk[tuple[_NoNSEventNames, _ET_co]]: ...
    @overload  # namespace-only events
    def __new__(
        cls,
        element_or_tree: _ET_co | _ElementTree[_ET_co],
        events: Iterable[Literal["start-ns", "end-ns"]],
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
    ) -> iterwalk[
        tuple[Literal["start-ns"], tuple[str, str]] | tuple[Literal["end-ns"], None]
    ]: ...
    @overload  # catch-all
    def __new__(
        cls,
        element_or_tree: _ET_co | _ElementTree[_ET_co],
        events: Iterable[_SaxEventNames],
        tag: _TagSelector | Iterable[_TagSelector] | None = ...,
    ) -> iterwalk[
        tuple[_NoNSEventNames, _ET_co]
        | tuple[Literal["start-ns"], tuple[str, str]]
        | tuple[Literal["end-ns"], None]
    ]: ...
    def __next__(self) -> _T_co: ...
    def skip_subtree(self) -> None: ...
