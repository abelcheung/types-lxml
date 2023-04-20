from __future__ import annotations

from pathlib import Path

import _testutils
import pytest
from lxml.etree import _Element, _ElementTree, iterparse, iterwalk
from lxml.html import HtmlElement

try:
    _testutils.run_pyright_on(__file__)
except FileNotFoundError as e:
    _ = pytest.mark.skip(" ".join([str(a) for a in e.args]))

reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestIterwalk:
    def test_xml_default_event(self, xml_tree: _ElementTree[_Element]) -> None:
        walker = iterwalk(xml_tree)
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)


    def test_xml_more_event(self, xml_tree: _ElementTree[_Element]) -> None:
        walker = iterwalk(xml_tree, ["start", "end", "start-ns", "end-ns", "comment"])
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)


    def test_html_default_event(self, html_tree: _ElementTree[HtmlElement]) -> None:
        walker = iterwalk(html_tree)
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)


    def test_html_more_event(self, html_tree: _ElementTree[HtmlElement]) -> None:
        # BUG Since HtmlComment is pretended as HtmlElement subclass
        # in stub but not runtime, adding 'comment' event would fail
        walker = iterwalk(html_tree, ["start", "end", "start-ns", "end-ns"], "div")
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

class TestIterparse:
    def test_default_event(self, x_filepath: Path) -> None:
        walker = iterparse(x_filepath)
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_html_mode(self, x_filepath: Path) -> None:
        walker = iterparse(source=str(x_filepath), html=True)
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_custom_event(self, x_filepath: Path) -> None:
        with open(x_filepath, 'rb') as f:
            walker = iterparse(f, ['start', 'end', 'start-ns', 'end-ns'])
            reveal_type(walker)
            for event, elem in walker:
                reveal_type(event)
                reveal_type(elem)
