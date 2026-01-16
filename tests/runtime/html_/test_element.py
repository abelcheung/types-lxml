from __future__ import annotations

import sys
from collections.abc import (
    Callable,
    Iterable,
)
from typing import TYPE_CHECKING, Any, cast

import pytest
from hypothesis import (
    HealthCheck,
    assume,
    given,
    settings,
    strategies as st,
)
from lxml.etree import LXML_VERSION
from lxml.html import (
    Classes as Classes,
    FormElement as FormElement,
    HtmlElement,
    InputElement,
    LabelElement,
    fragment_fromstring,
)

from .._testutils import strategy as _st
from .._testutils.common import (
    attr_name_types,
    attr_value_types,
)
from .._testutils.errors import (
    raise_no_attribute,
    raise_prop_not_writable,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type

if TYPE_CHECKING:
    from lxml._types import (  # pyright: ignore[reportMissingModuleSource]
        _AttrVal,
    )


class TestMixinProperties:
    def test_property_ro_1(
        self,
        bightml_root: HtmlElement,
    ) -> None:
        reveal_type(bightml_root.head)
        reveal_type(bightml_root.body)
        reveal_type(bightml_root.forms)
        reveal_type(bightml_root.base_url)

        for a in ["head", "body", "forms", "base_url"]:
            with raise_prop_not_writable:
                setattr(bightml_root, a, getattr(bightml_root, a))

    def test_property_ro_2(self) -> None:
        root = fragment_fromstring("<div>")
        if LXML_VERSION > (6, 0):
            reveal_type(root.head)
        else:
            with pytest.raises(IndexError, match=r"list index out of range"):
                _ = root.head

        reveal_type(root.body)
        reveal_type(root.forms)
        reveal_type(root.base_url)

    def test_classes_property_rw_good(
        self,
        disposable_html_element: HtmlElement,
    ) -> None:
        reveal_type(disposable_html_element.classes)
        assert len(disposable_html_element.classes) == 1
        disposable_html_element.classes = disposable_html_element.classes

        disposable_html_element.classes |= {"dummy"}
        assert len(disposable_html_element.classes) == 2

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type())
    @pytest.mark.slow
    def test_classes_property_rw_bad(
        self,
        disposable_html_element: HtmlElement,
        thing: Any,
    ) -> None:
        with pytest.raises(AssertionError):
            disposable_html_element.classes = thing

    @given(
        iterable_of=_st.fixed_item_iterables(),
        v=_st.xml_attr_value_arg(),
    )
    def test_classes_property_rw_bad_2(
        self,
        disposable_html_element: HtmlElement,
        iterable_of: Callable[[_AttrVal], Iterable[_AttrVal]],
        v: _AttrVal,
    ) -> None:
        # unhashable types not addable to set
        assume(not (
            getattr(iterable_of, "type") in {set, frozenset}
            and v.__hash__ is None
        ))  # fmt: skip
        with pytest.raises(AssertionError):
            disposable_html_element.classes = cast(Any, iterable_of(v))

    @pytest.mark.notypechecker("mypy")
    def test_label_property_rw_ok(
        self,
        disposable_html_input_label: HtmlElement,
    ) -> None:
        label: LabelElement = disposable_html_input_label.xpath("//label")[0]
        input: InputElement = disposable_html_input_label.xpath("//input")[0]

        reveal_type(disposable_html_input_label.label)
        reveal_type(input.label)

        # mypy forcefully sets input.label type to LabelElement here,
        # thus fails reveal_type() check below
        input.label = label
        del input.label
        reveal_type(input.label)
        assert input.label is None

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type())
    @pytest.mark.slow
    def test_label_property_rw_bad(
        self,
        disposable_html_input_label: HtmlElement,
        thing: Any,
    ) -> None:
        input: InputElement = disposable_html_input_label.xpath("//input")[0]
        try:
            _ = getattr(thing, "tag")
        except AttributeError:
            with raise_no_attribute:
                input.label = thing
        else:
            with pytest.raises(
                TypeError, match=r"can only assign label to a label element"
            ):
                input.label = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_label_property_rw_bad_2(
        self,
        disposable_html_input_label: HtmlElement,
        iterable_of: Callable[[LabelElement], Iterable[LabelElement]],
    ) -> None:
        label: LabelElement = disposable_html_input_label.xpath("//label")[0]
        input: InputElement = disposable_html_input_label.xpath("//input")[0]

        with raise_no_attribute:
            input.label = cast(Any, iterable_of(label))


class TestSetMethod:
    @settings(
        suppress_health_check=[HealthCheck.too_slow], deadline=None, max_examples=300
    )
    @given(key=_st.xml_name_arg(), value=st.one_of(st.none(), _st.xml_attr_value_arg()))
    @pytest.mark.slow
    def test_set_method_ok(
        self,
        disposable_html_element: HtmlElement,
        key: Any,
        value: Any,
    ) -> None:
        disposable_html_element.set(key, value)
        reveal_type(disposable_html_element.get(key))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(
        value=_st.all_instances_except_of_type(
            *attr_value_types.allow, *attr_value_types.skip, type(None)
        )
    )
    @pytest.mark.slow
    def test_set_method_bad_1(
        self,
        disposable_html_element: HtmlElement,
        value: Any,
    ) -> None:
        with pytest.raises(TypeError):
            disposable_html_element.set("key", value)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(
        key=_st.all_instances_except_of_type(
            *attr_name_types.allow, *attr_name_types.skip
        )
    )
    @pytest.mark.slow
    def test_set_method_bad_2(
        self,
        disposable_html_element: HtmlElement,
        key: Any,
    ) -> None:
        with pytest.raises(TypeError):
            disposable_html_element.set(key, "value")
