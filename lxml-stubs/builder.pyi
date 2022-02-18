from typing import Any, Callable, Mapping, Optional

from ._types import _AnyStr
from .etree import _Element

class ElementMaker:
    def __init__(
        self,
        typemap: Optional[Mapping[Any, Callable[[_Element, Any], None]]] = ...,
        namespace: Optional[str] = ...,
        nsmap: Optional[Mapping[Any, _AnyStr]] = ...,
        # same signature as etree.Element()
        makeelement: Optional[Callable[..., _Element]] = ...,
    ) -> None: ...
    def __call__(
        self,
        tag: str,
        # Although, by default, the ElementMaker only accepts _Element and types
        # interpretable by the default typemap (that is str, CDATA and dict)
        # as children, the typemap can be expanded to make sure items of any
        # type are accepted.
        *children: Any,
        **attrib: str,
    ) -> _Element: ...
    # __getattr__ here is special. ElementMaker is a factory that generates
    # elements with any tag provided as attribute name, as long as the name
    # does not conflict with the basic object methods (including python keywords
    # like "class" and "for", which are common in HTML)
    def __getattr__(self, name: str) -> Callable[..., _Element]: ...

E: ElementMaker