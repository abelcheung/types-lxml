from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from . import _testutils
import pytest
from lxml.etree import _Element as _Element, _ElementTree, iterparse, iterwalk
from lxml.html import HtmlElement

INJECT_REVEAL_TYPE = True
if INJECT_REVEAL_TYPE:
    reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestIterwalk:
    def test_xml_default_event(self, xml2_tree: _ElementTree) -> None:
        walker = iterwalk(xml2_tree)
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_xml_more_event(self, xml2_tree: _ElementTree) -> None:
        walker = iterwalk(xml2_tree, ["start", "end", "start-ns", "end-ns", "comment"])
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

    @pytest.mark.slow
    def test_html_default_event(self, bightml_tree: _ElementTree[HtmlElement]) -> None:
        walker = iterwalk(bightml_tree, tag=("div", "span"))
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    @pytest.mark.slow
    def test_html_more_event(self, bightml_tree: _ElementTree[HtmlElement]) -> None:
        # Since HtmlComment is pretended as HtmlElement subclass
        # in stub but not runtime, adding 'comment' event would fail
        walker = iterwalk(bightml_tree, ("start", "end", "start-ns", "end-ns"), "div")
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
    def test_xml_default_event(self, svg_filepath: Path) -> None:
        walker = iterparse(svg_filepath)
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_xml_more_event(self, svg_filepath: Path) -> None:
        walker = iterparse(
            svg_filepath, ["start", "end", "start-ns", "end-ns", "comment"]
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

    @pytest.mark.filterwarnings("ignore:.* 'strip_cdata' option .*:DeprecationWarning")
    def test_html_mode(self, svg_filepath: Path) -> None:
        walker = iterparse(
            source=svg_filepath,
            html=True,
            events=("start", "end", "start-ns", "end-ns", "comment"),
        )
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_plain_filename(self, svg_filepath: Path) -> None:
        walker = iterparse(str(svg_filepath))
        reveal_type(walker)
        for event, elem in walker:
            reveal_type(event)
            reveal_type(elem)

    def test_binary_io(self, svg_filepath: Path) -> None:
        with open(svg_filepath, "rb") as f:
            walker = iterparse(f)
            reveal_type(walker)
            for event, elem in walker:
                reveal_type(event)
                reveal_type(elem)

    def test_text_io(self, svg_filepath: Path) -> None:
        with pytest.raises(
            TypeError, match="reading file objects must return bytes objects"
        ):
            with open(svg_filepath, "r") as f:
                walker = iterparse(cast(Any, f))
                _ = next(walker)  # Exception only after accessing iterator
