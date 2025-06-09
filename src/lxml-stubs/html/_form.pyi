from __future__ import annotations

import sys
from http.client import HTTPResponse
from typing import (
    Callable,
    Collection,
    Iterable,
    Iterator,
    Literal,
    MutableMapping,
    MutableSet,
    TypeVar,
    overload,
)

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never

from .._types import SupportsLaxItems, _TextArg
from ._element import HtmlElement

_T = TypeVar("_T")

_AnyInputElement = InputElement | SelectElement | TextareaElement  # noqa: F821

class FormElement(HtmlElement):
    @property
    def inputs(self) -> InputGetter: ...
    @property
    def fields(self) -> FieldsDict: ...
    @fields.setter
    def fields(self, __v: SupportsLaxItems[str, str]) -> None: ...
    @property
    def action(self) -> str | None: ...
    @action.setter
    def action(self, __v: _TextArg | None) -> None: ...
    @action.deleter
    def action(self) -> None: ...
    method: str
    def form_values(self) -> list[tuple[str, str]]: ...
    def _name(self) -> str: ...

# FieldsDict is actually MutableMapping *sans* __delitem__
# However it is much simpler to keep MutableMapping and only
# override __delitem__
class FieldsDict(MutableMapping[str, str]):
    inputs: InputGetter
    def __init__(self, inputs: InputGetter) -> None: ...
    def __getitem__(self, __k: str) -> str: ...
    def __setitem__(self, __k: str, __v: str) -> None: ...
    # Use Never for argument to issue early warning that
    # __delitem__ can't be used
    def __delitem__(self, __k: Never) -> Never: ...  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...

# Quoting from source: it's unclear if this is a dictionary-like object
# or list-like object
class InputGetter(Collection[_AnyInputElement]):
    form: FormElement
    def __init__(self, form: FormElement) -> None: ...
    # __getitem__ is special here: for checkbox group and radio group,
    # it returns special list-like object instead of HtmlElement
    def __getitem__(
        self, __k: str
    ) -> _AnyInputElement | RadioGroup | CheckboxGroup: ...
    def keys(self) -> list[str]: ...
    def items(
        self,
    ) -> list[tuple[str, _AnyInputElement | RadioGroup | CheckboxGroup]]: ...
    def __contains__(self, __o: object) -> bool: ...
    def __iter__(self) -> Iterator[_AnyInputElement]: ...
    def __len__(self) -> int: ...

class _InputMixin:
    @property
    def name(self) -> str | None: ...
    @name.setter
    def name(self, __v: _TextArg | None) -> None: ...
    @name.deleter
    def name(self) -> None: ...

class TextareaElement(_InputMixin, HtmlElement):
    @property
    def value(self) -> str | None: ...
    @value.setter
    def value(self, __v: _TextArg | None) -> None: ...
    @value.deleter
    def value(self) -> None: ...

class SelectElement(_InputMixin, HtmlElement):
    @property
    def multiple(self) -> bool: ...
    @multiple.setter
    def multiple(self, __v: bool) -> None: ...
    @property
    def value(self) -> str | MultipleSelectOptions | None: ...
    @value.setter
    def value(self, value: str | Collection[str]) -> None: ...
    @value.deleter
    def value(self) -> None: ...
    @property
    def value_options(self) -> list[str]: ...

# Notes for MultipleSelectOptions and CheckboxValues
#
# Not adding any SetMixin methods here. What they do now
# are just functional aliases of standard set operators.
# They make sense for ancient python (2.6 or below), but
# not anymore for code written in these 10 years or so.

class MultipleSelectOptions(MutableSet[str]):
    select: SelectElement
    def __init__(self, select: SelectElement) -> None: ...
    @property
    def options(self) -> Iterator[HtmlElement]: ...
    def __contains__(self, x: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def add(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, item: str
    ) -> None: ...
    def remove(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, item: str
    ) -> None: ...
    def discard(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, item: str
    ) -> None: ...

class RadioGroup(list[InputElement]):
    value: str | None  # bytes or bytearray disallowed
    @property
    def value_options(self) -> list[str]: ...

class CheckboxGroup(list[InputElement]):
    @property
    def value(self) -> CheckboxValues: ...
    @value.setter
    def value(self, __v: str | Collection[str]) -> None: ...
    @value.deleter
    def value(self) -> None: ...
    @property
    def value_options(self) -> list[str]: ...

class CheckboxValues(MutableSet[str]):
    group: CheckboxGroup
    def __init__(self, group: CheckboxGroup) -> None: ...
    def __contains__(self, x: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def add(self, value: str) -> None: ...
    def discard(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, item: str
    ) -> None: ...

class InputElement(_InputMixin, HtmlElement):
    @property
    def type(self) -> str: ...
    @type.setter
    def type(self, __v: _TextArg | None) -> None: ...
    @property
    def value(self) -> str | None: ...
    @value.setter
    def value(self, __v: _TextArg | None) -> None: ...
    @value.deleter
    def value(self) -> None: ...
    checked: bool
    @property
    def checkable(self) -> bool: ...

class LabelElement(HtmlElement):
    @property
    def for_element(self) -> HtmlElement | None: ...
    @for_element.setter
    def for_element(self, __v: HtmlElement) -> None: ...

# open_http argument has signature (method, url, values) -> Any
# Default connection handler is open_http_urllib, which uses
# urllib.request.urlopen internally. Though its return type
# varies with protocol handler (e.g. urllib.response.addinfourl
# for FTP), we are talking about HTTP/HTTPS here, so return type
# is limited.
@overload  # default handler (open_http_urllib)
def submit_form(
    form: FormElement,
    extra_values: Iterable[tuple[str, str]] | SupportsLaxItems[str, str] | None = None,
    open_http: None = None,
) -> HTTPResponse: ...
@overload  # open_http as positional argument
def submit_form(
    form: FormElement,
    extra_values: Iterable[tuple[str, str]] | SupportsLaxItems[str, str] | None,
    open_http: Callable[[Literal["GET", "POST"], str, list[tuple[str, str]]], _T],
) -> _T: ...
@overload  # open_http as keyword argument
def submit_form(
    form: FormElement,
    extra_values: Iterable[tuple[str, str]] | SupportsLaxItems[str, str] | None = None,
    *,
    open_http: Callable[[Literal["GET", "POST"], str, list[tuple[str, str]]], _T],
) -> _T: ...

# No need to annotate open_http_urllib.
# Only intended as callback func object in submit_form() argument,
# and already used as default if open_http argument is absent.
