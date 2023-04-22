from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import _testutils
import pytest
from lxml.html import (
    HtmlElement as HtmlElement,
    find_class,
    find_rel_links,
    iterlinks,
    make_links_absolute,
    parse,
    resolve_base_href,
    rewrite_links,
)

reveal_type = getattr(_testutils, "reveal_type_wrapper")


def test_input_content_type(h_filepath: Path) -> None:
    fio = open(h_filepath, "rb")
    tree = parse(h_filepath)
    for bad_input in [h_filepath, fio, tree]:
        with pytest.raises(
            AttributeError, match="object has no attribute 'find_rel_links'"
        ):
            _ = find_rel_links(cast(Any, bad_input), "stylesheet")
    fio.close()

    links = find_rel_links(str(h_filepath), "stylesheet")
    reveal_type(links)
    assert links == find_rel_links(tree.getroot(), "stylesheet")
    assert links == find_rel_links(h_filepath.read_text(), "stylesheet")
    assert links == find_rel_links(h_filepath.read_bytes(), "stylesheet")


def test_find_class(h_filepath: Path) -> None:
    elems = find_class(h_filepath.read_text(), "single")
    reveal_type(elems)
    for e in elems:
        reveal_type(e)


def test_iterlinks(h_filepath: Path) -> None:
    results = iterlinks(h_filepath.read_text())
    reveal_type(results)
    for r in results:
        assert len(r) == 4
        reveal_type(r[0])
        reveal_type(r[1])
        reveal_type(r[2])
        reveal_type(r[3])


class TestOutputType:
    BASE = "http://dummy.link"

    def test_make_links_absolute(self, h_filepath: Path) -> None:
        in_data1 = h_filepath.read_bytes()
        with pytest.raises(
            TypeError, match="No base_url given, and the document has no base_url"
        ):
            out_data1 = make_links_absolute(in_data1)
        out_data1 = make_links_absolute(in_data1, self.BASE)
        assert type(in_data1) == type(out_data1)
        in_data2 = h_filepath.read_text()
        with pytest.raises(TypeError, match="Cannot mix str and non-str"):
            out_data2 = make_links_absolute(
                in_data2, cast(Any, self.BASE.encode("ascii"))
            )
        out_data2 = make_links_absolute(in_data2, self.BASE)
        assert type(in_data2) == type(out_data2)
        tree = parse(h_filepath)
        in_data3 = tree.getroot()
        out_data3 = make_links_absolute(in_data3, self.BASE)
        assert type(in_data3) == type(out_data3)

    def test_resolve_base_href(self, h_filepath: Path) -> None:
        in_data1 = h_filepath.read_bytes()
        out_data1 = resolve_base_href(in_data1)
        assert type(in_data1) == type(out_data1)
        in_data2 = h_filepath.read_text()
        out_data2 = resolve_base_href(in_data2)
        assert type(in_data2) == type(out_data2)
        tree = parse(h_filepath)
        in_data3 = tree.getroot()
        out_data3 = resolve_base_href(in_data3)
        assert type(in_data3) == type(out_data3)

    def test_rewrite_links(self, h_filepath: Path) -> None:
        in_data1 = h_filepath.read_bytes()
        out_data1 = rewrite_links(in_data1, lambda _: self.BASE)
        assert type(in_data1) == type(out_data1)
        in_data2 = h_filepath.read_text()
        with pytest.raises(TypeError, match="can only concatenate str"):
            out_data2 = rewrite_links(
                in_data2, lambda _: cast(Any, self.BASE.encode("ASCII"))
            )
        out_data2 = rewrite_links(in_data2, lambda _: self.BASE)
        assert type(in_data2) == type(out_data2)
        tree = parse(h_filepath)
        in_data3 = tree.getroot()
        out_data3 = rewrite_links(in_data3, lambda _: None)
        assert type(in_data3) == type(out_data3)
