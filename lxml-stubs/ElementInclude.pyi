from typing import Any, Callable, Literal, overload

from lxml.etree import LxmlSyntaxError, _Element, _ElementTree

from ._types import _ET, _FilePath

class FatalIncludeError(LxmlSyntaxError): ...
class LimitedRecursiveIncludeError(FatalIncludeError): ...

# The only purpose of default_loader is for the
# 'loader' arg in include() below, so
# accurate @overload is unneeded
def default_loader(
    href: _FilePath,
    parse: Literal["xml", "text"],
    encoding: str | None = None,
) -> _ElementTree[_Element] | str: ...
@overload
def include(
    elem: _ET,
    loader: Callable[[_FilePath, Literal["xml", "text"]], Any] | None = None,
    base_url: str | None = None,
    max_depth: int = 6,
) -> _ET: ...
@overload
def include(
    elem: _ElementTree[_ET],
    loader: Callable[[_FilePath, Literal["xml", "text"]], Any] | None = None,
    base_url: str | None = None,
    max_depth: int = 6,
) -> _ElementTree[_ET]: ...
