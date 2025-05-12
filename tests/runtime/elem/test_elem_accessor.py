from __future__ import annotations

import sys
from collections.abc import Iterable
from copy import deepcopy
from decimal import Decimal
from inspect import Parameter
from random import randrange
from types import NoneType
from typing import Any

import pytest
from hypothesis import (
    HealthCheck,
    assume,
    given,
    settings,
    strategies as st,
)
from lxml import etree
from lxml.etree import (
    _Attrib as _Attrib,
    _Comment as _Comment,
    _Element,
    _ElementTree as _ElementTree,
    _Entity as _Entity,
    _ProcessingInstruction as _ProcessingInstruction,
)

from .._testutils import signature_tester, strategy as _st
from .._testutils.errors import (
    raise_non_integer,
    raise_non_iterable,
    raise_wrong_arg_type,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type

raise_lxml_non_integer = (
    raise_non_integer if etree.LXML_VERSION < (5, 1) else raise_wrong_arg_type
)


class TestIndexMethod:
    @signature_tester(_Element.index, (
        ("child", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("start", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("stop" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_basic_behavior(self, xml2_root: _Element) -> None:
        new_root = deepcopy(xml2_root)
        subelem = new_root[3]
        reveal_type(new_root.index(subelem))

        with pytest.raises(ValueError, match="x not in slice"):
            _ = new_root.index(subelem, len(new_root) - 1, len(new_root) - 1)

    @given(thing=_st.all_instances_except_of_type(_Element))
    def test_child_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with raise_wrong_arg_type:
            _ = disposable_element.index(thing)

    @given(iterable_of=_st.fixed_item_iterables())
    def test_child_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_wrong_arg_type:
            _ = disposable_element.index(iterable_of(disposable_element))

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=300,
    )
    @given(thing=_st.all_instances_except_of_type(NoneType, int, Decimal))
    @pytest.mark.slow
    def test_start_arg_bad_1(self, xml2_root: _Element, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_lxml_non_integer:
            _ = xml2_root.index(xml2_root[0], start=thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_start_arg_bad_2(self, xml2_root: _Element, iterable_of: Any) -> None:
        with raise_lxml_non_integer:
            _ = xml2_root.index(xml2_root[0], start=iterable_of(0))

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=300,
    )
    @given(thing=_st.all_instances_except_of_type(NoneType, int, Decimal))
    @pytest.mark.slow
    def test_stop_arg_bad_1(self, xml2_root: _Element, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_lxml_non_integer:
            _ = xml2_root.index(xml2_root[0], stop=thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_stop_arg_bad_2(self, xml2_root: _Element, iterable_of: Any) -> None:
        with raise_lxml_non_integer:
            _ = xml2_root.index(xml2_root[0], stop=iterable_of(len(xml2_root)))


class TestAppendMethod:
    @signature_tester(_Element.append, (
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_basic_behavior(self, xml2_root: _Element) -> None:
        new_root = deepcopy(xml2_root)
        subelem = deepcopy(new_root[-1])
        length = len(new_root)

        assert new_root.append(subelem) is None
        assert len(new_root) == length + 1

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_element_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with raise_wrong_arg_type:
            disposable_element.append(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_element_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_wrong_arg_type:
            disposable_element.append(iterable_of(disposable_element))


class TestInsertMethod:
    @signature_tester(_Element.insert, (
        ("index"  , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_basic_behavior(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)
        comment = etree.Comment("comment")
        pos = randrange(len(elem))
        assert elem.insert(pos, element=comment) is None
        assert elem.index(comment) == pos

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(int))
    @pytest.mark.slow
    def test_index_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        comment = etree.Comment("comment")
        with raise_lxml_non_integer:
            disposable_element.insert(thing, comment)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_index_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        comment = etree.Comment("comment")
        with raise_lxml_non_integer:
            disposable_element.insert(iterable_of(0), comment)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_element_arg_bad(self, disposable_element: _Element, thing: Any) -> None:
        with raise_wrong_arg_type:
            disposable_element.insert(index=0, element=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_element_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_wrong_arg_type:
            disposable_element.insert(index=0, element=iterable_of(disposable_element))


class TestRemoveMethod:
    @signature_tester(_Element.remove, (
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_basic_behavior(self, xml2_root: _Element) -> None:
        new_root = deepcopy(xml2_root)
        assert new_root.remove(new_root[-1]) is None

    # Can construct a new node and fail removing it, but that is
    # pure runtime behavior and doesn't violate annotation
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_element_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with raise_wrong_arg_type:
            disposable_element.remove(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_element_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_wrong_arg_type:
            disposable_element.remove(iterable_of(disposable_element))


class TestReplaceMethod:
    @signature_tester(_Element.replace, (
        ("old_element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("new_element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_basic_behavior(self, xml2_root: _Element) -> None:
        new_root = deepcopy(xml2_root)
        subelem = new_root[-1]
        new_elem = etree.Element("foo", attr="bar")
        assert new_root.replace(subelem, new_elem) is None

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_old_element_arg_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        with raise_wrong_arg_type:
            disposable_element.replace(
                old_element=thing, new_element=disposable_element
            )

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_old_element_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_wrong_arg_type:
            disposable_element.replace(
                old_element=iterable_of(disposable_element),
                new_element=disposable_element,
            )

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_new_element_arg_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        with raise_wrong_arg_type:
            disposable_element.replace(disposable_element, thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_new_element_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_wrong_arg_type:
            disposable_element.replace(
                disposable_element, iterable_of(disposable_element)
            )


class TestExtendMethod:
    @signature_tester(_Element.extend, (
        ("elements", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    @given(value=_st.iterable_of_elements())
    def test_basic_behavior(
        self, disposable_element: _Element, value: Iterable[_Element]
    ) -> None:
        assert disposable_element.extend(value) is None

    def test_degenerate_case(self, xml2_root: _Element) -> None:
        xml2_root.extend([])
        # broken behavior (but no exception though)
        xml2_root.extend(xml2_root[0])

    @given(value=_st.all_instances_except_of_type(Iterable, _Element, NoneType))
    def test_bad_element_1(
        self, disposable_element: _Element, value: Iterable[Any]
    ) -> None:
        with raise_non_iterable:
            disposable_element.extend(value)

    @given(value=st.iterables(
        _st.all_instances_except_of_type(Iterable, _Element, NoneType),
        min_size=1,
        max_size=5,
    ))  # fmt: skip
    def test_bad_element_2(
        self, disposable_element: _Element, value: Iterable[Any]
    ) -> None:
        with pytest.raises(
            TypeError, match=r"Cannot convert \w+(\.\w+)* to .+\._Element"
        ):
            disposable_element.extend(value)


class TestClearMethod:
    @signature_tester(_Element.clear, (
        ("keep_tail", Parameter.POSITIONAL_OR_KEYWORD, False),
    ))  # fmt: skip
    def test_basic_behavior(self, xml2_root: _Element) -> None:
        new_root = deepcopy(xml2_root)
        assert len(new_root) > 0
        assert new_root.tail is None
        new_root.clear()
        assert len(new_root) == 0
        del new_root

        # Not testing keep_tail param independently, as it is
        # just a truthy value and accepts virtually anything
        new_root = deepcopy(xml2_root)
        new_root.tail = "junk"
        new_root.clear(keep_tail=True)
        assert len(new_root) == 0
        assert new_root.tail is not None
