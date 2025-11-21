from typing import (
    Final,
    Literal,
    Protocol,
    overload,
    type_check_only,
)

from ._types import Unused, _ElementOrTree
from .etree import LxmlSyntaxError, _Element

# exported constants
XINCLUDE: Final[Literal["{http://www.w3.org/2001/XInclude}"]]
XINCLUDE_INCLUDE: Final[Literal["{http://www.w3.org/2001/XInclude}include"]]
XINCLUDE_FALLBACK: Final[Literal["{http://www.w3.org/2001/XInclude}fallback"]]
XINCLUDE_ITER_TAG: Final[Literal["{http://www.w3.org/2001/XInclude}*"]]
DEFAULT_MAX_INCLUSION_DEPTH: Final[Literal[6]]

class FatalIncludeError(LxmlSyntaxError): ...
class LimitedRecursiveIncludeError(FatalIncludeError): ...

# The default_loader() in lxml.ElementInclude is completely
# retired (lxml uses its own internal loader)

@type_check_only
class _LoaderProtocol(Protocol):
    """Protocol for loader func argument in `ElementInclude.include()`

    Annotation
    ----------
    `loader=` argument in `ElementInclude.include()` specifies the function
    object to load URL or file resource. It has the following overloaded
    function signature:
    - `(_href: str, _mode: Literal["xml"], /, encoding: str = None) -> _Element`
    - `(_href: str, _mode: Literal["text"], /, encoding: str = None) -> str`
    """

    @overload
    def __call__(
        self,
        _href: str,  # URL or local path from href="..." attribute
        _mode: Literal["xml"],
        /,
        encoding: Unused = None,  # Under XML mode this param is ignored
        # but must be present nonetheless
    ) -> _Element: ...
    @overload
    def __call__(
        self,
        _href: str,
        _mode: Literal["text"],
        /,
        encoding: str | None = None,
    ) -> str: ...

def include(
    elem: _ElementOrTree,
    loader: _LoaderProtocol | None = None,
    base_url: str | None = None,
    max_depth: int = 6,
) -> None:
    """Expand XInclude directives

    Annotation
    ----------
    - Source documentation above `include()` is outdated; this function
    does not return at all.
    - Try using `from lxml.ElementInclude import _LoaderProtocol` from
    within IDEs to lookup its purpose and usage. This is annotation
    only and doesn't exist in lxml source.
    """
