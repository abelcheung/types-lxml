from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import _testutils
import pytest
from lxml.etree import _Element, _ElementTree, iterparse, iterwalk
from lxml.html import HtmlElement

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
        # Generated values are not unpacked here to test type narrowing
        # See issue #19 for more info
        for item in walker:
            if item[0] == "start-ns":
                reveal_type(item[1])
            elif item[0] == "end-ns":
                reveal_type(item[1])
            else:
                reveal_type(item[1])

    def test_html_default_event(self, html_tree: _ElementTree[HtmlElement]) -> None:
        walker = iterwalk(html_tree, tag=("div", "span"))
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_html_more_event(self, html_tree: _ElementTree[HtmlElement]) -> None:
        # Since HtmlComment is pretended as HtmlElement subclass
        # in stub but not runtime, adding 'comment' event would fail
        walker = iterwalk(html_tree, ("start", "end", "start-ns", "end-ns"), "div")
        reveal_type(walker)
        # Unlike iterparse(), iterwalk behaves the same with HTML
        for item in walker:
            if item[0] == "start-ns":
                reveal_type(item[1])
            elif item[0] == "end-ns":
                reveal_type(item[1])
            else:
                reveal_type(item[1])


class TestIterparse:
    def test_xml_default_event(self, x1_filepath: Path) -> None:
        walker = iterparse(x1_filepath)
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_xml_more_event(self, x1_filepath: Path) -> None:
        walker = iterparse(
            x1_filepath, ["start", "end", "start-ns", "end-ns", "comment"]
        )
        reveal_type(walker)
        # Generated values are not unpacked here to test type narrowing
        # See issue #19 for more info
        for item in walker:
            if item[0] == "start-ns":
                reveal_type(item[1])
            elif item[0] == "end-ns":
                reveal_type(item[1])
            else:
                reveal_type(item[1])

    def test_html_mode(self, x1_filepath: Path) -> None:
        walker = iterparse(
            source=x1_filepath,
            html=True,
            events=("start", "end", "start-ns", "end-ns", "comment"),
        )
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_plain_filename(self, x1_filepath: Path) -> None:
        walker = iterparse(str(x1_filepath))
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_binary_io(self, x1_filepath: Path) -> None:
        with open(x1_filepath, "rb") as f:
            walker = iterparse(f)
            reveal_type(walker)
            for event, elem in walker:
                reveal_type(event)
                reveal_type(elem)

    def test_text_io(self, x1_filepath: Path) -> None:
        with pytest.raises(
            TypeError, match="reading file objects must return bytes objects"
        ):
            with open(x1_filepath, "r") as f:
                walker = iterparse(cast(Any, f))
                _ = next(walker)  # Exception only after accessing iterator
