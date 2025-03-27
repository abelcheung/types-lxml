# Like find*() tests, iter*() methods are also mostly similar
# because all of them are based on _MultiTagMatcher logic,
# only differing in element search scope and output order.

from __future__ import annotations

import sys
from inspect import Parameter
from typing import Any

import pytest
from hypothesis import HealthCheck, assume, given, settings
from lxml import etree
from lxml.etree import (
    LXML_VERSION,
    QName,
    _Element,
    iselement,
)

from .._testutils import signature_tester, strategy as _st
from .._testutils.common import is_hashable, tag_selector_types
from .._testutils.errors import (
    raise_non_iterable,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestIter:
    @signature_tester(_Element.iter, (
        ("tag" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    @pytest.mark.parametrize(
        ("arg", "kw", "empty"),
        [  # pyright: ignore[reportUnknownArgumentType]
            ([], {}, False),
            ([], {"tag": None}, False),
            (["title"], {}, False),
            ([], {"tag": b"title"}, False),
            ([QName(None, "price")], {}, False),
            (["quantity", etree.Comment], {}, False),
            ([], {"tag": (QName(None, "price"), etree.Comment)}, False),
            ([["foo", etree.Comment, etree.PI]], {}, False),
            ([()], {}, True),
            ([], {"tag": []}, True),
            ([{}], {}, True),
            ([], {"tag": (e for e in ("quantity", etree.Comment))}, False),
        ],
    )
    def test_input_ok(
        self, xml2_root: _Element, arg: Any, kw: Any, empty: bool
    ) -> None:
        itr = reveal_type(xml2_root.iter(*arg, **kw))
        result = reveal_type([e for e in itr])
        if empty:
            assert len(result) == 0
        else:
            assert len(result) > 0

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        )
    )
    @pytest.mark.slow
    def test_input_bad_1(self, xml2_root: _Element, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_non_iterable:
            xml2_root.iter(thing)

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        ),
        iterable_of=_st.fixed_item_iterables(),
    )
    @pytest.mark.slow
    def test_input_bad_2(
        self, xml2_root: _Element, thing: Any, iterable_of: Any
    ) -> None:
        assume(
            getattr(iterable_of, "type") not in {set, frozenset} or is_hashable(thing)
        )
        with raise_non_iterable:
            xml2_root.iter(iterable_of(thing))


# iterdescendants() is iter() sans root node, so the
# test is identical
class TestIterDescendants:
    @signature_tester(_Element.iterdescendants, (
        ("tag" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    @pytest.mark.parametrize(
        ("arg", "kw", "empty"),
        [  # pyright: ignore[reportUnknownArgumentType]
            ([], {}, False),
            ([], {"tag": None}, False),
            (["title"], {}, False),
            ([], {"tag": b"title"}, False),
            ([QName(None, "price")], {}, False),
            (["quantity", etree.Comment], {}, False),
            ([], {"tag": (QName(None, "price"), etree.Comment)}, False),
            ([["foo", etree.Comment, etree.PI]], {}, False),
            ([()], {}, True),
            ([], {"tag": []}, True),
            ([{}], {}, True),
            ([], {"tag": (e for e in ("quantity", etree.Comment))}, False),
        ],
    )
    def test_input_ok(
        self, xml2_root: _Element, arg: Any, kw: Any, empty: bool
    ) -> None:
        itr = reveal_type(xml2_root.iterdescendants(*arg, **kw))
        result = reveal_type([e for e in itr])
        if empty:
            assert len(result) == 0
        else:
            assert len(result) > 0

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        )
    )
    @pytest.mark.slow
    def test_input_bad_1(self, xml2_root: _Element, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_non_iterable:
            xml2_root.iterdescendants(thing)

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        ),
        iterable_of=_st.fixed_item_iterables(),
    )
    @pytest.mark.slow
    def test_input_bad_2(
        self, xml2_root: _Element, thing: Any, iterable_of: Any
    ) -> None:
        assume(
            getattr(iterable_of, "type") not in {set, frozenset} or is_hashable(thing)
        )
        with raise_non_iterable:
            xml2_root.iterdescendants(iterable_of(thing))


class TestIterAncestors:
    @signature_tester(_Element.iterancestors, (
        ("tag" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    @pytest.mark.parametrize(
        ("arg", "kw", "empty"),
        [  # pyright: ignore[reportUnknownArgumentType]
            ([], {}, False),
            ([], {"tag": None}, False),
            (["desc"], {}, False),
            ([], {"tag": b"desc"}, False),
            ([QName("http://example.org/myfoo", "descr")], {}, False),
            (["svg", etree.Comment], {}, False),
            ([], {"tag": ("svg", etree.Comment)}, False),
            ([{"desc", etree.Comment, etree.PI}], {}, False),
            ([()], {}, True),
            ([], {"tag": []}, True),
            ([{}], {}, True),
            ([], {"tag": (e for e in ("desc", "svg"))}, False),
        ],
    )
    def test_input_ok(self, svg_root: _Element, arg: Any, kw: Any, empty: bool) -> None:
        uri = "http://example.org/myfoo"
        sel = svg_root.xpath("//myfoo:emph", namespaces={"myfoo": uri})
        assert iselement(ggchild := sel[0])
        itr = reveal_type(ggchild.iterancestors(*arg, **kw))
        result = reveal_type([e for e in itr])
        if empty:
            assert len(result) == 0
        else:
            assert len(result) > 0

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        )
    )
    @pytest.mark.slow
    def test_input_bad_1(self, xml2_root: _Element, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_non_iterable:
            xml2_root.iterancestors(thing)

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        ),
        iterable_of=_st.fixed_item_iterables(),
    )
    @pytest.mark.slow
    def test_input_bad_2(
        self, xml2_root: _Element, thing: Any, iterable_of: Any
    ) -> None:
        assume(
            getattr(iterable_of, "type") not in {set, frozenset} or is_hashable(thing)
        )
        with raise_non_iterable:
            xml2_root.iterancestors(iterable_of(thing))


class TestIterSiblings:
    @signature_tester(_Element.itersiblings, (
        ("tag"      , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags"     , Parameter.VAR_POSITIONAL       , Parameter.empty),
        ("preceding", Parameter.KEYWORD_ONLY         , False          ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    # 'preceding' parameter is a truthy/falsy value, no type
    # verficiation is performed

    @pytest.mark.parametrize(
        ("arg", "kw", "empty"),
        [  # pyright: ignore[reportUnknownArgumentType]
            ([], {}, False),
            ([], {"tag": None}, False),
            ([], {"preceding": True}, False),
            (["metadata"], {}, False),
            ([], {"tag": b"metadata", "preceding": False}, False),
            ([b"defs"], {"preceding": True}, False),
            ([], {"preceding": True, "tag": "metadata"}, True),
            ([QName(None, "style")], {}, False),
            (["style", etree.Comment], {}, False),
            ([], {"tag": ("style", etree.Comment)}, False),
            ([["metadata", etree.Comment, "g"]], {}, False),
            ([()], {}, True),
            ([], {"tag": []}, True),
            ([{}], {}, True),
            ([], {"tag": (e for e in ("metadata", "style"))}, False),
        ],
    )
    def test_input_ok(self, svg_root: _Element, arg: Any, kw: Any, empty: bool) -> None:
        child = svg_root[1]
        itr = reveal_type(child.itersiblings(*arg, **kw))
        result = reveal_type([e for e in itr])
        if empty:
            assert len(result) == 0
        else:
            assert len(result) > 0

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        )
    )
    @pytest.mark.slow
    def test_input_bad_1(self, xml2_root: _Element, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        child = xml2_root[1]
        with raise_non_iterable:
            child.itersiblings(thing)

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        ),
        iterable_of=_st.fixed_item_iterables(),
    )
    @pytest.mark.slow
    def test_input_bad_2(
        self, xml2_root: _Element, thing: Any, iterable_of: Any
    ) -> None:
        assume(
            getattr(iterable_of, "type") not in {set, frozenset} or is_hashable(thing)
        )
        child = xml2_root[0]
        with raise_non_iterable:
            child.itersiblings(iterable_of(thing))


class TestIterChildren:
    @signature_tester(_Element.iterchildren, (
        ("tag"     , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags"    , Parameter.VAR_POSITIONAL       , Parameter.empty),
        ("reversed", Parameter.KEYWORD_ONLY         , False          ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    # 'reversed' parameter is a truthy/falsy value, no type
    # verficiation is performed

    @pytest.mark.parametrize(
        ("arg", "kw", "empty"),
        [  # pyright: ignore[reportUnknownArgumentType]
            ([], {}, False),
            ([], {"tag": None, "reversed": True}, False),
            (["shipto"], {}, False),
            ([], {"tag": b"item"}, False),
            (["price"], {}, True),
            ([QName(None, "shipto")], {"reversed": False}, False),
            (["quantity", etree.Comment], {}, False),
            ([], {"tag": (QName(None, "price"), etree.Comment)}, False),
            ([["foo", etree.Comment, etree.PI]], {}, False),
            ([()], {}, True),
            ([], {"tag": []}, True),
            ([{}], {}, True),
            ([], {"tag": (e for e in ("quantity", etree.Comment))}, False),
        ],
    )
    def test_input_ok(
        self, xml2_root: _Element, arg: Any, kw: Any, empty: bool
    ) -> None:
        itr = reveal_type(xml2_root.iterchildren(*arg, **kw))
        result = reveal_type([e for e in itr])
        if empty:
            assert len(result) == 0
        else:
            assert len(result) > 0

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        )
    )
    @pytest.mark.slow
    def test_input_bad_1(self, xml2_root: _Element, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_non_iterable:
            xml2_root.iterchildren(thing)

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        ),
        iterable_of=_st.fixed_item_iterables(),
    )
    @pytest.mark.slow
    def test_input_bad_2(
        self, xml2_root: _Element, thing: Any, iterable_of: Any
    ) -> None:
        assume(
            getattr(iterable_of, "type") not in {set, frozenset} or is_hashable(thing)
        )
        with raise_non_iterable:
            xml2_root.iterchildren(iterable_of(thing))


class TestIterText:
    @signature_tester(_Element.itertext, (
        ("tag"      , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags"     , Parameter.VAR_POSITIONAL       , Parameter.empty),
        ("with_tail", Parameter.KEYWORD_ONLY         , True           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    # 'with_tail' parameter is a truthy/falsy value, no type
    # verficiation is performed

    @pytest.mark.parametrize(
        ("arg", "kw", "empty"),
        [  # pyright: ignore[reportUnknownArgumentType]
            ([], {}, False),
            ([], {"tag": None, "with_tail": False}, False),
            (["title"], {"with_tail": True}, False),
            ([], {"tag": b"title"}, False),
            ([QName(None, "address")], {}, False),
            (["quantity", etree.Comment], {}, False),
            ([], {"tag": (QName(None, "address"), etree.Comment)}, False),
            ([["foo", etree.Comment, etree.PI]], {}, False),
            # output should contain tail text of element even when
            # tag selector is not present, unless 'with_tail' is
            # explicitly set to False. But prevention of tail text
            # is only honored in lxml 5.0.0 and later
            ([()], {"with_tail": False}, False if LXML_VERSION < (5, 0) else True),
            ([], {"tag": []}, False),
            ([{}], {}, False),
            ([], {"tag": (e for e in ("quantity", etree.Comment))}, False),
        ],
    )
    def test_input_ok(
        self, xml2_root: _Element, arg: Any, kw: Any, empty: bool
    ) -> None:
        itr = reveal_type(xml2_root.itertext(*arg, **kw))
        result = reveal_type([s for s in itr])
        if empty:
            assert len(result) == 0
        else:
            assert len(result) > 0

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        )
    )
    @pytest.mark.slow
    def test_input_bad_1(self, xml2_root: _Element, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_non_iterable:
            xml2_root.itertext(thing)

    @settings(
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.function_scoped_fixture,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            *tag_selector_types.allow,
            *tag_selector_types.skip,
        ),
        iterable_of=_st.fixed_item_iterables(),
    )
    @pytest.mark.slow
    def test_input_bad_2(
        self, xml2_root: _Element, thing: Any, iterable_of: Any
    ) -> None:
        assume(
            getattr(iterable_of, "type") not in {set, frozenset} or is_hashable(thing)
        )
        with raise_non_iterable:
            xml2_root.itertext(iterable_of(thing))

