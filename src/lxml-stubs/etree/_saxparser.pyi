from abc import abstractmethod
from typing import Callable, Protocol, TypeVar

from .._types import _DefEtreeParsers
from ._element import _Comment, _Element, _ProcessingInstruction
from ._parser import XMLSyntaxError

_T_co = TypeVar("_T_co", covariant=True)

class XMLSyntaxAssertionError(XMLSyntaxError, AssertionError):
    def __init__(self, message: object) -> None: ...

class ParserTarget(Protocol[_T_co]):
    """This is a stub-only class representing parser target interface.

    Annotation
    ----------
    All custom target objects should inherit from this class if they
    want to be fully annotated. Please [check out wiki
    page](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser)
    on how to do this and how to use the custom target parser.

    See Also
    --------
    - [Target parser official document](https://lxml.de/parsing.html#the-target-parser-interface)
    - [`_PythonSaxParserTarget()`](https://github.com/lxml/lxml/blob/820db896be83f72f1cb653981362c682c8fc0d1f/src/lxml/parsertarget.pxi#L20)
    """

    @abstractmethod
    def close(self) -> _T_co: ...
    # All parameters marked positional, to stop pyright from
    # complaining about incompatible parameter names. They are
    # never called with keyword arguments anyway.
    def comment(self, text: str, /) -> None: ...
    def data(self, data: str, /) -> None: ...
    def end(self, tag: str, /) -> None: ...
    # TODO Think about how to handle 3-argument form later,
    # presumably for SaxParserTarget.
    def start(
        self,
        tag: str,
        attrib: dict[str, str],
        /,
    ) -> None: ...
    # Methods below are undocumented. Lxml has described
    # 'start-ns' and 'end-ns' events however.
    def pi(self, target: str, data: str, /) -> None: ...
    # Default namespace prefix is empty string, not None
    def start_ns(self, prefix: str, uri: str, /) -> None: ...
    def end_ns(self, prefix: str, /) -> None: ...
    def doctype(
        self,
        root_tag: str | None,
        public_id: str | None,
        system_id: str | None,
        /,
    ) -> None: ...

class TreeBuilder(ParserTarget[_Element]):
    def __init__(
        self,
        *,
        element_factory: type[_Element] | None = None,
        parser: _DefEtreeParsers | None = None,
        comment_factory: Callable[..., _Comment] | None = None,
        pi_factory: Callable[..., _ProcessingInstruction] | None = None,
        insert_comments: bool = True,
        insert_pis: bool = True,
    ) -> None: ...
    def close(self) -> _Element: ...
