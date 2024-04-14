from typing import Any, Callable, Generic, Mapping, overload

from ._types import _ElemFactory, _ET_co, _NSMapArg, _TagName
from .etree import _Element

_TypeMapArg = Mapping[Any, Callable[[_Element, Any], None]]

class ElementMaker(Generic[_ET_co]):
    @overload
    def __new__(
        cls,
        typemap: _TypeMapArg | None = None,
        namespace: str | None = None,
        nsmap: _NSMapArg | None = None,
        *,
        makeelement: _ElemFactory[_ET_co],
    ) -> ElementMaker[_ET_co]: ...
    @overload
    def __new__(
        cls,
        typemap: _TypeMapArg | None,
        namespace: str | None,
        nsmap: _NSMapArg | None,
        makeelement: _ElemFactory[_ET_co],
    ) -> ElementMaker[_ET_co]: ...
    @overload
    def __new__(
        cls,
        typemap: _TypeMapArg | None = None,
        namespace: str | None = None,
        nsmap: _NSMapArg | None = None,
        makeelement: None = None,
    ) -> ElementMaker: ...
    def __call__(
        self,
        tag: _TagName,
        # Although, by default, the ElementMaker only accepts _Element and types
        # interpretable by the default typemap (that is str, CDATA and dict)
        # as children, the typemap can be expanded to make sure items of any
        # type are accepted.
        *children: object,
        **attrib: str,
    ) -> _ET_co: ...
    # __getattr__ here is special. ElementMaker is a factory that generates
    # elements with any tag provided as attribute name, as long as the name
    # does not conflict with the basic object methods (including python keywords
    # like "class" and "for", which are common in HTML)
    def __getattr__(self, name: str) -> _ElemFactory[_ET_co]: ...

E: ElementMaker
