from __future__ import annotations

import io
import sys
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest
from lxml.etree import _Element as _Element, _ElementTree, iterparse, iterwalk
from lxml.html import HtmlElement

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


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
    def test_input_arg(
        self,
        svg_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterator[Any]],
    ) -> None:
        for input in generate_input_file_arguments(svg_filepath):
            should_support = False
            if isinstance(input, (str, bytes, Path)):
                should_support = True
            elif hasattr(input, "read"):
                if hasattr(input, "status"):
                    # Assume this is HTTP response, which is not seekable
                    should_support = True
                else:
                    # check SupportsRead[bytes]
                    data = input.read(1)
                    if isinstance(data, bytes):
                        should_support = True
                    input.seek(0, io.SEEK_SET)
            else:
                raise ValueError(f"Unhandled input type: {type(input)}")

            walker = iterparse(input)
            if should_support:
                print(f"Good input being tested: {input!r}")
                reveal_type(walker)
                for event, elem in walker:
                    reveal_type(event)
                    reveal_type(elem)
            else:  # Exception only after accessing iterator
                with pytest.raises(
                    TypeError, match="reading file objects must return bytes objects"
                ):
                    _ = next(walker)

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
