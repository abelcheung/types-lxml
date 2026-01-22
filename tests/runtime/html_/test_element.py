from __future__ import annotations

import ipaddress
import sys
from collections.abc import (
    Callable,
    Iterable,
    Iterator,
)
from random import randrange
from typing import TYPE_CHECKING, Any, cast

import pytest
from hypothesis import (
    HealthCheck,
    assume,
    given,
    settings,
    strategies as st,
)
from lxml.etree import (
    LXML_VERSION,
    _Element,
)
from lxml.html import (
    Classes as Classes,
    Element,
    FormElement as FormElement,
    HtmlComment,
    HtmlElement,
    HtmlEntity,
    HtmlProcessingInstruction,
    InputElement,
    LabelElement,
)

from .._testutils import strategy as _st
from .._testutils.common import (
    attr_name_types,
    attr_value_types,
    hashable_elem_if_is_set,
)
from .._testutils.errors import (
    raise_cannot_convert,
    raise_no_attribute,
    raise_non_integer,
    raise_non_iterable,
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
        el = Element("div")
        if LXML_VERSION > (6, 0):
            reveal_type(el.head)
            reveal_type(el.body)
        else:
            with pytest.raises(IndexError, match=r"list index out of range"):
                _ = el.head
            with pytest.raises(IndexError, match=r"list index out of range"):
                _ = el.body

        reveal_type(el.forms)
        reveal_type(el.base_url)

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
        assume(hashable_elem_if_is_set(iterable_of, v))
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


# Almost a dup of runtime/elem/test_basic.py counterpart
class TestBasicBehavior:
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(int, slice))
    @pytest.mark.slow
    def test_sequence_read_bad(
        self, disposable_html_element: HtmlElement, thing: Any
    ) -> None:
        with raise_non_integer:
            _ = cast(Any, disposable_html_element[thing])

    def test_sequence_read_ok(self, bightml_root: HtmlElement) -> None:
        reveal_type(len(bightml_root))
        length = len(bightml_root)
        reveal_type(bightml_root[randrange(length)])
        reveal_type(bightml_root[: 2])  # fmt: skip  # ast: why the space???

        itr = iter(bightml_root)
        reveal_type(itr)
        item = next(itr)
        reveal_type(item)
        assert bightml_root.index(item) == 0
        del itr

        for sub in bightml_root:
            reveal_type(sub)

        assert bightml_root.body is not None
        subelem = bightml_root.body[3]
        reveal_type(subelem in bightml_root)
        o = object()
        reveal_type(o in bightml_root)

        with raise_non_integer:
            _ = bightml_root[cast(int, "0")]

    # mypy and ty don't support magic method and always treat
    # reversed(...) as `reversed` object
    @pytest.mark.notypechecker("mypy", "ty")
    def test_reversed_seq_read_1(self, bightml_root: HtmlElement) -> None:
        rev = reversed(bightml_root)
        reveal_type(rev)
        reveal_type(list(rev))

    @pytest.mark.onlytypechecker("mypy", "ty")
    def test_reversed_seq_read_2(self, bightml_root: HtmlElement) -> None:
        rev = bightml_root.__reversed__()
        reveal_type(rev)
        reveal_type(list(rev))

    def test_sequence_modify_ok(self, disposable_html_element: HtmlElement) -> None:
        comment = HtmlComment("comment")
        comment2 = HtmlComment("comment2")
        entity = HtmlEntity("foo")
        pi = HtmlProcessingInstruction("target", "data")
        div = HtmlElement("div")

        length = len(disposable_html_element)
        disposable_html_element.insert(0, comment)
        assert len(disposable_html_element) == length + 1
        length = length + 1

        disposable_html_element[length - 1] = entity
        assert len(disposable_html_element) == length

        disposable_html_element[length:] = [comment, pi, div]
        assert disposable_html_element[-3] is comment
        assert len(disposable_html_element) == length + 3
        length = length + 3

        disposable_html_element[length - 2 : length] = {div, comment2}
        assert len(disposable_html_element) == length

        del disposable_html_element[0:2]
        assert len(disposable_html_element) == length - 2

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_sequence_modify_bad_1(
        self, disposable_html_element: HtmlElement, thing: Any
    ) -> None:
        if thing is None:
            with pytest.raises(ValueError, match=r"cannot assign None"):
                disposable_html_element[0] = cast(Any, thing)  # pyright: ignore[reportUnnecessaryCast]
        else:
            with raise_cannot_convert:
                disposable_html_element[0] = thing

    # some iterables may cause indefinite hang when lxml diligently try inserting
    # items into element tree (e.g. huge ranges)
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(
        _Element,
        Iterator,
        range,
        ipaddress.IPv4Network,
        ipaddress.IPv6Network,
    ).filter(lambda x: x is not NotImplemented and bool(x)))
    @pytest.mark.slow
    def test_sequence_modify_bad_2(
        self, disposable_html_element: HtmlElement, thing: Any
    ) -> None:
        if isinstance(thing, (Iterable)):
            with raise_cannot_convert:
                disposable_html_element[:] = cast(Any, thing)
        else:
            with raise_non_iterable:
                disposable_html_element[:] = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_sequence_modify_bad_3(
        self,
        disposable_html_element: HtmlElement,
        iterable_of: Callable[[HtmlElement], Iterable[HtmlElement]],
    ) -> None:
        div = Element("div")
        with raise_cannot_convert:
            disposable_html_element[0] = cast(Any, iterable_of(div))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(
        thing=_st.all_instances_except_of_type(_Element).filter(lambda x: x is not NotImplemented and bool(x)),
        iterable_of=_st.fixed_item_iterables(),
    )
    @pytest.mark.slow
    def test_sequence_modify_bad_4(
        self,
        disposable_html_element: HtmlElement,
        thing: Any,
        iterable_of: Callable[[Any], Iterable[Any]],
    ) -> None:
        assume(hashable_elem_if_is_set(iterable_of, thing))
        with raise_cannot_convert:
            disposable_html_element[:] = iterable_of(thing)


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
