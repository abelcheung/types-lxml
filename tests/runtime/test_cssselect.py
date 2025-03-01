from __future__ import annotations

import copy
import sys
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

        with pytest.raises(AttributeError, match=r"objects is not writable"):
            selector.path = selector.path  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with pytest.raises(AttributeError, match=r"objects is not writable"):
            selector.error_log = selector.error_log  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
            # not checking .css properties because it is actually writable;
            # we lie to users about it being read-only.

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
    @given(css=_st.all_instances_except_of_type(str))
    def test_css_arg_bad(self, css: Any) -> None:
        with pytest.raises(TypeError, match=r"bytes-like object"):
            _ = CSSSelector(css)

    def test_namespaces_arg_ok(self, svg_root: _Element) -> None:
        rdfns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        selector = CSSSelector("rdf|Bag > rdf|li", namespaces={"rdf": rdfns})
        result = selector(svg_root)
        reveal_type(result)
        assert len(result) > 0

        foons = b"http://example.org/myfoo"
        appns = "http://example.org/myapp"
        ns = iter([("rdf", rdfns), ("myfoo", foons), (b"myapp", appns)])
        selector = CSSSelector("myfoo|what", namespaces=cast(Any, ns))
        result = selector(svg_root)
        reveal_type(result)
        assert len(result) > 0

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
        max_examples=500,
    )
    @given(ns=_st.all_instances_except_of_type(dict, NoneType, StringIO, BytesIO).filter(
        _namespace_aux_filter
    ))  # fmt: skip
    @pytest.mark.slow
    def test_namespaces_arg_bad(self, svg_root: _Element, ns: Any) -> None:
        with pytest.raises((TypeError, ValueError)):
            _ = CSSSelector("li", namespaces=ns)

    # Translator argument not tested, it just become a noop if required
    # values are not matched, not raising or doing anything.

    @given(etree=_st.all_instances_except_of_type(_Element, _ElementTree))
    def test_call_arg_bad(self, etree: Any) -> None:
        selector = CSSSelector("#id")
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = selector(etree)  # pyright: ignore[reportUnknownVariableType]


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
