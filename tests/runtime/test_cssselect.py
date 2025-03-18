from __future__ import annotations

import copy
import sys
from collections.abc import Iterable
from inspect import Parameter
from io import BytesIO, StringIO
from pathlib import Path
from types import NoneType
from typing import TYPE_CHECKING, Any, cast

import pytest
from hypothesis import HealthCheck, given, settings
from lxml.cssselect import CSSSelector
from lxml.etree import (
    ElementBase,
    ElementDefaultClassLookup,
    XMLParser,
    _Element,
    _ElementTree,
    _ListErrorLog as _ListErrorLog,
    parse,
)
from lxml.html import HtmlElement

from ._testutils import signature_tester, strategy as _st
from ._testutils.errors import (
    raise_attr_not_writable,
    raise_invalid_lxml_type,
    raise_non_iterable,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestCSSSelectorInit:
    @signature_tester(CSSSelector.__init__, (
            ('css'       , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
            ('namespaces', Parameter.POSITIONAL_OR_KEYWORD, None           ),
            ('translator', Parameter.POSITIONAL_OR_KEYWORD, 'xml'          ),
    ))  # fmt: skip
    def test_properties(self) -> None:
        selector = CSSSelector("#id")
        reveal_type(selector)

        reveal_type(selector.css)
        assert selector.css == "#id"
        reveal_type(selector.path)

        reveal_type(selector.error_log)
        assert len(selector.error_log) == 0

        # not checking .css properties because it is actually writable;
        # we lie to users about it being read-only.
        for attr in ("path", "error_log"):
            with raise_attr_not_writable:
                setattr(selector, attr, getattr(selector, attr))

    def test_xml_return_type(
        self, xml2_root: _Element, xml2_tree: _ElementTree
    ) -> None:
        selector = CSSSelector("shiporder price")
        result = selector(xml2_root)
        reveal_type(result)
        assert len(result) > 0
        assert result == selector(xml2_tree)

    def test_html_return_type(
        self, html2_root: HtmlElement, html2_tree: _ElementTree[HtmlElement]
    ) -> None:
        selector = CSSSelector("*[content]", translator="html")
        result = selector(html2_root)
        reveal_type(result)
        assert len(result) > 0
        assert result == selector(html2_tree)


class TestCSSSelectorArgs:
    # test_css_arg_ok already intrinsic to test_properties test above

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str))
    @pytest.mark.slow
    def test_css_arg_bad_1(self, thing: Any) -> None:
        with pytest.raises(
            TypeError,
            match=r"(string pattern on a|expected string or) bytes-like object",
        ):
            _ = CSSSelector(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_css_arg_bad_2(self, iterable_of: Any) -> None:
        with pytest.raises(TypeError, match=r"expected string or bytes-like object"):
            _ = CSSSelector(iterable_of("#id"))

    def test_namespaces_arg_ok(
        self, svg_root: _Element, svg_tree: _ElementTree
    ) -> None:
        rdfns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        selector = CSSSelector("rdf|Bag > rdf|li", namespaces={"rdf": rdfns})
        result = selector(svg_root)
        reveal_type(result)
        assert len(result) > 0
        assert result == selector(svg_tree)

        foons = b"http://example.org/myfoo"
        appns = "http://example.org/myapp"
        ns = iter([("rdf", rdfns), ("myfoo", foons), (b"myapp", appns)])
        selector = CSSSelector("myfoo|what", namespaces=cast(Any, ns))
        result = selector(svg_root)
        reveal_type(result)
        assert len(result) > 0
        assert result == selector(svg_tree)

    # regret diving into this rabbit hole
    @staticmethod
    def _namespace_aux_filter(obj: Any) -> bool:
        if obj == NotImplemented:  # avoid DeprecationWarning
            return False
        if not bool(obj):
            return False
        # Some objects can be iterated to yield nothing, like enumerate(()).
        # They become false positives because no exception is raised.
        if not hasattr(obj, "__next__"):
            return True
        try:
            obj_copy = copy.copy(obj)  # requires pickleable
        except TypeError:
            # no choice, can't test iterator without changing it
            return False
        try:
            next(obj_copy)
        except (StopIteration, TypeError):
            return False
        else:
            return True

    # StringIO and BytesIO can be iterated, and resulting string
    # can be unpacked to treat as prefix/URI pair(!)
    @settings(
        suppress_health_check=[
            HealthCheck.function_scoped_fixture,
            HealthCheck.too_slow,
        ],
        max_examples=300,
    )
    @given(
        thing=_st.all_instances_except_of_type(
            dict, NoneType, StringIO, BytesIO
        ).filter(_namespace_aux_filter)
    )
    @pytest.mark.slow
    def test_namespaces_arg_bad(self, svg_root: _Element, thing: Any) -> None:
        if not isinstance(thing, Iterable):
            raise_cm = raise_non_iterable
        else:
            raise_cm = pytest.raises((TypeError, ValueError))  # type: ignore[arg-type]
        with raise_cm:
            _ = CSSSelector("li", namespaces=thing)  # pyright: ignore[reportUnknownArgumentType]

    # Translator argument not tested, it just become a noop if required
    # values are not matched, not raising or doing anything.

    @settings(max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_call_arg_bad_1(self, thing: Any) -> None:
        selector = CSSSelector("#id")
        with raise_invalid_lxml_type:
            _ = selector(thing)  # pyright: ignore[reportUnknownVariableType]

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_arg_bad_2(
        self, iterable_of: Any, svg_root: _Element, svg_tree: _ElementTree
    ) -> None:
        selector = CSSSelector(".thing")
        with raise_invalid_lxml_type:
            _ = selector(iterable_of(svg_root))  # pyright: ignore[reportUnknownVariableType]
        with raise_invalid_lxml_type:
            _ = selector(iterable_of(svg_tree))  # pyright: ignore[reportUnknownVariableType]


class TestElementMethod:
    @signature_tester(_Element.cssselect, (
        ('expr'      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ('translator', Parameter.KEYWORD_ONLY         , 'xml'          ),
    ))  # fmt: skip
    def test_xml_element(self, xml2_root: _Element) -> None:
        for expr in ("note + quantity", "item > price"):
            result = xml2_root.cssselect(expr)
            reveal_type(result)
            assert len(result) > 0
            selector = CSSSelector(expr)
            assert result == selector(xml2_root)

    def test_html_element(self, html2_root: HtmlElement) -> None:
        for expr in ("img[alt]", "meta + title"):
            result = html2_root.cssselect(expr, translator="html")
            reveal_type(result)
            assert len(result) > 0
            selector = CSSSelector(expr, translator="html")
            assert result == selector(html2_root)


class MyElement(ElementBase):
    pass


class TestElementSubclass:
    def test_subclass(self, svg_filepath: Path) -> None:
        parser = XMLParser()
        lookup = ElementDefaultClassLookup(element=MyElement)
        if TYPE_CHECKING:
            parser = cast(XMLParser[MyElement], parser)
        else:
            parser.set_element_class_lookup(lookup)
        tree = parse(svg_filepath, parser=parser)
        result = tree.getroot().cssselect("g > circle")
        reveal_type(result)
        assert len(result) > 0
