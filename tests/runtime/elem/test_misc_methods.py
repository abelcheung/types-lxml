from __future__ import annotations

from inspect import Parameter
from typing import Any

import pytest
from hypothesis import HealthCheck, given, settings
from lxml.etree import (
    Comment,
    Element,
    ElementBase,
    _Element,
)

from .._testutils import signature_tester, strategy as _st
from .._testutils.errors import (
    raise_wrong_arg_type,
)


class TestAddMethods:
    comm = Comment("some comment")

    class MyElement(ElementBase):
        pass

    @signature_tester(
        _Element.addnext,
        (("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_addnext_input_ok(self, disposable_element: _Element) -> None:
        assert disposable_element.addnext(self.comm) is None
        # Only PI and comments can be siblings of the root element
        disposable_element.append(self.MyElement("foo"))
        disposable_element[0].addnext(self.MyElement("bar"))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_addnext_input_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        disposable_element.append(Element("foo"))
        with raise_wrong_arg_type:
            disposable_element[0].addnext(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_addnext_input_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        disposable_element.append(Element("foo"))
        with raise_wrong_arg_type:
            disposable_element[0].addnext(iterable_of(self.comm))

    @signature_tester(
        _Element.addprevious,
        (("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_addprevious_input_ok(self, disposable_element: _Element) -> None:
        assert disposable_element.addprevious(self.comm) is None
        # Only PI and comments can be siblings of the root element
        disposable_element.append(self.MyElement("foo"))
        disposable_element[0].addprevious(self.MyElement("bar"))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_addprevious_input_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        disposable_element.append(Element("foo"))
        with raise_wrong_arg_type:
            disposable_element[0].addprevious(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_addprevious_input_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        disposable_element.append(Element("foo"))
        with raise_wrong_arg_type:
            disposable_element[0].addprevious(iterable_of(self.comm))
