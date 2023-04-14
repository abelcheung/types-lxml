from __future__ import annotations

import _testutils
import pytest
from lxml.etree import _Element, _ElementTree, iterwalk
from lxml.html import HtmlElement

try:
    _testutils.run_pyright_on(__file__)
except FileNotFoundError as e:
    _ = pytest.mark.skip(" ".join([str(a) for a in e.args]))

reveal_type = getattr(_testutils, "reveal_type_wrapper")


def test_iterwalk_xml_default_event(xml_tree: _ElementTree[_Element]) -> None:
    walker = iterwalk(xml_tree)
    # reveal_type(walker)  # BUG Runtime iterwalk can't be subscripted
    for event, elem in walker:
        reveal_type(event)
        reveal_type(elem)


def test_iterwalk_xml_more_event(xml_tree: _ElementTree[_Element]) -> None:
    walker = iterwalk(xml_tree, ["start", "end", "start-ns", "end-ns", "comment"])
    for event, elem in walker:
        reveal_type(event)
        reveal_type(elem)


def test_iterwalk_html_default_event(html_tree: _ElementTree[HtmlElement]) -> None:
    walker = iterwalk(html_tree)
    for event, elem in walker:
        reveal_type(event)
        reveal_type(elem)


def test_iterwalk_html_more_event(html_tree: _ElementTree[HtmlElement]) -> None:
    # BUG Since HtmlComment is pretended as HtmlElement in stub but
    # not runtime, adding 'comment' event would fail
    walker = iterwalk(html_tree, ["start", "end", "start-ns", "end-ns"], "div")
    for event, elem in walker:
        reveal_type(event)
        reveal_type(elem)
