import sys
from _typeshed import SupportsRead
from typing import Iterable, Iterator, Literal, TypeVar, overload

from .._types import (
    _ElementOrTree,
    _ET_co,
    _FilePath,
    _SaxEventNames,
    _TagSelector,
    _TextArg,
)
from ._classlookup import ElementClassLookup
from ._docloader import _ResolverRegistry
from ._element import _Element
from ._xmlerror import _ListErrorLog
from ._xmlschema import XMLSchema

if sys.version_info >= (3, 11):
    from typing import LiteralString
else:
    from typing_extensions import LiteralString

_T_co = TypeVar("_T_co", covariant=True)

# See https://lxml.de/parsing.html#event-types
# Undocumented: 'comment' and 'pi' are actually supported!
_NoNSEventNames = Literal["start", "end", "comment", "pi"]
_SaxNsEventValues = tuple[str, str] | None  # for start-ns & end-ns event

class iterparse(Iterator[_T_co]):
    """Incremental parser. Parses XML into a tree and generates tuples (event, element) in a
    SAX-like fashion.

    Annotation
    ----------
    Totally 5 function signatures are available:
    - HTML mode (`html=True`), where namespace events are ignored
    - `start`, `end`, `comment` and `pi` events, where only
      Element values are produced
    - `start-ns` or `end-ns` events, producing
      namespace tuple (for `start-ns`) or nothing (`end-ns`)
    - Catch-all signature where `events` arg is specified
    - `events` arg absent, implying only `end` event is emitted

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.iterparse)
    """

    @overload  # html mode -> namespace events suppressed
    def __new__(  # type: ignore[overload-overlap]  # pyright: ignore[reportOverlappingOverload]
        cls,
        source: _FilePath | SupportsRead[bytes],
        events: Iterable[_SaxEventNames] = ("end",),
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        no_network: bool = True,
        remove_blank_text: bool = False,
        compact: bool = True,
        remove_comments: bool = False,
        remove_pis: bool = False,
        encoding: _TextArg | None = None,
        html: Literal[True],
        recover: bool | None = None,
        schema: XMLSchema | None = None,
    ) -> iterparse[tuple[_NoNSEventNames, _Element]]: ...
    @overload  # element-only events
    def __new__(
        cls,
        source: _FilePath | SupportsRead[bytes],
        events: Iterable[_NoNSEventNames],
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        attribute_defaults: bool = False,
        dtd_validation: bool = False,
        load_dtd: bool = False,
        no_network: bool = True,
        remove_blank_text: bool = False,
        compact: bool = True,
        resolve_entities: bool = True,
        remove_comments: bool = False,
        remove_pis: bool = False,
        strip_cdata: bool = True,
        encoding: _TextArg | None = None,
        html: bool = False,
        recover: bool | None = None,
        huge_tree: bool = False,
        collect_ids: bool = True,
        schema: XMLSchema | None = None,
    ) -> iterparse[tuple[_NoNSEventNames, _Element]]: ...
    @overload  # NS-only events
    def __new__(
        cls,
        source: _FilePath | SupportsRead[bytes],
        events: Iterable[Literal["start-ns", "end-ns"]],
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        attribute_defaults: bool = False,
        dtd_validation: bool = False,
        load_dtd: bool = False,
        no_network: bool = True,
        remove_blank_text: bool = False,
        compact: bool = True,
        resolve_entities: bool = True,
        remove_comments: bool = False,
        remove_pis: bool = False,
        strip_cdata: bool = True,
        encoding: _TextArg | None = None,
        html: bool = False,
        recover: bool | None = None,
        huge_tree: bool = False,
        collect_ids: bool = True,
        schema: XMLSchema | None = None,
    ) -> iterparse[
        tuple[Literal["start-ns"], tuple[str, str]] | tuple[Literal["end-ns"], None]
    ]: ...
    @overload  # other mixed events
    def __new__(
        cls,
        source: _FilePath | SupportsRead[bytes],
        events: Iterable[_SaxEventNames],
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        attribute_defaults: bool = False,
        dtd_validation: bool = False,
        load_dtd: bool = False,
        no_network: bool = True,
        remove_blank_text: bool = False,
        compact: bool = True,
        resolve_entities: bool = True,
        remove_comments: bool = False,
        remove_pis: bool = False,
        strip_cdata: bool = True,
        encoding: _TextArg | None = None,
        html: bool = False,
        recover: bool | None = None,
        huge_tree: bool = False,
        collect_ids: bool = True,
        schema: XMLSchema | None = None,
    ) -> iterparse[
        tuple[_NoNSEventNames, _Element]
        | tuple[Literal["start-ns"], tuple[str, str]]
        | tuple[Literal["end-ns"], None]
    ]: ...
    @overload  # events absent -> only 'end' event emitted
    def __new__(
        cls,
        source: _FilePath | SupportsRead[bytes],
        *,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
        attribute_defaults: bool = False,
        dtd_validation: bool = False,
        load_dtd: bool = False,
        no_network: bool = True,
        remove_blank_text: bool = False,
        compact: bool = True,
        resolve_entities: bool = True,
        remove_comments: bool = False,
        remove_pis: bool = False,
        strip_cdata: bool = True,
        encoding: _TextArg | None = None,
        html: bool = False,
        recover: bool | None = None,
        huge_tree: bool = False,
        collect_ids: bool = True,
        schema: XMLSchema | None = None,
    ) -> iterparse[tuple[Literal["end"], _Element]]: ...
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
        lookup: ElementClassLookup | None = None,
    ) -> None: ...
    makeelement: type[_T_co]

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

    # There is no concept of html mode in iterwalk(); namespace events
    # are not suppressed like iterparse()
    @overload  # element-only events
    def __new__(
        cls,
        element_or_tree: _ElementOrTree[_ET_co],
        events: Iterable[_NoNSEventNames],
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
    ) -> iterwalk[tuple[_NoNSEventNames, _ET_co]]: ...
    @overload  # namespace-only events
    def __new__(
        cls,
        element_or_tree: _ElementOrTree[_ET_co],
        events: Iterable[Literal["start-ns", "end-ns"]],
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
    ) -> iterwalk[
        tuple[Literal["start-ns"], tuple[str, str]] | tuple[Literal["end-ns"], None]
    ]: ...
    @overload  # all other events combination
    def __new__(
        cls,
        element_or_tree: _ElementOrTree[_ET_co],
        events: Iterable[_SaxEventNames],
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
    ) -> iterwalk[
        tuple[_NoNSEventNames, _ET_co]
        | tuple[Literal["start-ns"], tuple[str, str]]
        | tuple[Literal["end-ns"], None]
    ]: ...
    @overload  # default events ('end' only)
    def __new__(
        cls,
        element_or_tree: _ElementOrTree[_ET_co],
        /,
        tag: _TagSelector | Iterable[_TagSelector] | None = None,
    ) -> iterwalk[tuple[Literal["end"], _ET_co]]: ...
    def __next__(self) -> _T_co: ...
    def skip_subtree(self) -> None: ...
