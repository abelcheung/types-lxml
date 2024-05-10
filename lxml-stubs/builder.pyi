from typing import Any, Callable, Generic, Mapping, overload
from functools import partial

from ._types import _ElementFactory, _ET_co, _NSMapArg, _TagName
from .etree import CDATA, _Element

# Mapping should have been something like
# Mapping[type[_T], Callable[[_Element, _T], None]]
# but invariant key/value causes it to be incompatible
# with anything
_TypeMapArg = Mapping[Any, Callable[[_Element, Any], None]]

# One might be tempted to use artibrary callable in
# makeelement argument, because ElementMaker
# constructor can actually accept any callable as
# makeelement. However all element creation attempt
# would fail, as 'nsmap' keyword argument is expected
# to be usable in the makeelement function call.
class ElementMaker(Generic[_ET_co]):
    @overload  # makeelement is keyword
    def __new__(
        cls,
        typemap: _TypeMapArg | None = None,
        namespace: str | None = None,
        nsmap: _NSMapArg | None = None,
        *,
        makeelement: _ElementFactory[_ET_co],
    ) -> ElementMaker[_ET_co]: ...
    @overload  # makeelement is positional
    def __new__(
        cls,
        typemap: _TypeMapArg | None,
        namespace: str | None,
        nsmap: _NSMapArg | None,
        makeelement: _ElementFactory[_ET_co],
    ) -> ElementMaker[_ET_co]: ...
    @overload  # makeelement is default or absent
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
        *__child: object
        | str
        | CDATA
        | dict[Any, Any]
        | _Element
        | Callable[[], object],
        **__attr: str,
    ) -> _ET_co: ...
    # __getattr__ here is special. ElementMaker supports using any
    # attribute name as tag, returning a functools.partial
    # object to ElementMaker.__call__() with tag argument prefilled.
    def __getattr__(self, name: str) -> partial[_ET_co]: ...

E: ElementMaker
