from typing import Any, Callable, Generic, Mapping, TypeVar, overload

from ._types import _NSMapArg
from .etree import QName, _Element, _ElemFactory

_ET_co = TypeVar("_ET_co", bound=_Element, covariant=True)

_TypeMapArg = Mapping[Any, Callable[[_Element, Any], None]]

class ElementMaker(Generic[_ET_co]):
    @overload
    def __new__(
        cls,
        typemap: _TypeMapArg | None = ...,
        namespace: str | None = ...,
        nsmap: _NSMapArg | None = ...,
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
        typemap: _TypeMapArg | None = ...,
        namespace: str | None = ...,
        nsmap: _NSMapArg | None = ...,
        makeelement: None = ...,
    ) -> ElementMaker[_Element]: ...
    def __call__(
        self,
        tag: str | QName,  # No bytes here
        # Although, by default, the ElementMaker only accepts _Element and types
        # interpretable by the default typemap (that is str, CDATA and dict)
        # as children, the typemap can be expanded to make sure items of any
        # type are accepted.
        *children: Any,
        **attrib: str,
    ) -> _ET_co: ...
    # __getattr__ here is special. ElementMaker is a factory that generates
    # elements with any tag provided as attribute name, as long as the name
    # does not conflict with the basic object methods (including python keywords
    # like "class" and "for", which are common in HTML)
    def __getattr__(self, name: str) -> _ElemFactory[_ET_co]: ...

E: ElementMaker[_Element]
