from typing import Any, Callable, Mapping, Optional

from .etree import _AnyStr, _Element

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
        # Although default ElementMaker only accepts _Element and types
        # interpretable by default typemap (that is str, CDATA and dict)
        # as children, typemap can be expanded to make sure item of any
        # type is accepted.
        *children: Any,
        **attrib: _AnyStr,
    ) -> _Element: ...
    # __getattr__ here is special. ElementMaker is a factory that generates
    # element of *any* tag, as long as tag name does not conflict with basic
    # object methods (including python keywords like "class" and "for",
    # which are common in HTML)
    def __getattr__(self, name: str) -> Callable[..., _Element]: ...

E: ElementMaker
