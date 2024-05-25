from __future__ import annotations

from inspect import Parameter
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, cast
from urllib.request import urlopen

import _testutils
import lxml.etree as etree
import lxml.html as _html
import pytest
from bs4 import BeautifulSoup
from lxml.etree import _Element as _Element, _ElementTree as _ElementTree
from lxml.html import HtmlElement as HtmlElement, soupparser as _soup

reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestFromstring:
    @_testutils.signature_tester(_soup.fromstring, (
        ("data"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("beautifulsoup", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("makeelement"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("bsargs"       , Parameter.VAR_KEYWORD          , Parameter.empty),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    def test_input_type(self, h2_filepath: Path, h2_fileuri: str) -> None:
        result = _soup.fromstring(str(h2_filepath))
        del result

        s = h2_filepath.read_text()
        result = _soup.fromstring(s)
        reveal_type(result)
        del result

        b = h2_filepath.read_bytes()
        result = _soup.fromstring(b)
        reveal_type(result)
        del result

        s_io = StringIO(s)
        result = _soup.fromstring(s_io)
        reveal_type(result)
        del result

        b_io = BytesIO(b)
        result = _soup.fromstring(b_io)
        reveal_type(result)
        del result

        with open(h2_filepath, "r") as f:
            result = _soup.fromstring(f)
        reveal_type(result)
        del result

        with open(h2_filepath, "rb") as f:
            result = _soup.fromstring(f)
        reveal_type(result)
        del result

        with urlopen(h2_fileuri) as f:
            result = _soup.fromstring(f)
        reveal_type(result)
        del result

        with pytest.raises(TypeError, match=r"object of type '\w+' has no len\(\)"):
            _ = _soup.fromstring(cast(Any, None))

        with pytest.raises(TypeError, match=r"object of type '\w+' has no len\(\)"):
            _ = _soup.fromstring(cast(Any, h2_filepath))

    def test_makeelement(self, h2_str: str) -> None:
        result = _soup.fromstring(h2_str, makeelement=_html.xhtml_parser.makeelement)
        reveal_type(result)
        del result

        result = _soup.fromstring(h2_str, None, etree.Element)
        reveal_type(result)
        del result

        with pytest.raises(TypeError, match="object is not callable"):
            _ = _soup.fromstring(h2_str, makeelement=cast(Any, 1))

        with pytest.raises(TypeError, match="unexpected keyword argument 'attrib"):
            _ = _soup.fromstring(h2_str, makeelement=cast(Any, etree.CommentBase))

    # Just test capability to pass extra keywords to beautifulsoup
    # no intention to cover all keyword arguments supported by bs
    def test_bs_args(self, h2_bytes: bytes) -> None:
        result = _soup.fromstring(h2_bytes, exclude_encodings=["ascii"])
        reveal_type(result)
        del result

        result = _soup.fromstring(h2_bytes, from_encoding="ascii")
        reveal_type(result)
        del result

        with pytest.raises(TypeError, match="unexpected keyword argument 'badarg'"):
            _ = _soup.fromstring(h2_bytes, badarg=None)  # pyright: ignore


class TestParse:
    @_testutils.signature_tester(_soup.parse, (
        ("file"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("beautifulsoup", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("makeelement"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("bsargs"       , Parameter.VAR_KEYWORD          , Parameter.empty),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    def test_input_type(
        self,
        h2_filepath: Path,
        h2_fileuri: str,
    ) -> None:
        # expects filename/io, not html data
        s = h2_filepath.read_text()
        with pytest.raises(OSError):
            _ = _soup.parse(s)

        b = h2_filepath.read_bytes()
        with pytest.raises(OSError):
            _ = _soup.parse(b)

        result = _soup.parse(str(h2_filepath))
        reveal_type(result)
        root = result.getroot()
        reveal_type(root)
        del root, result

        s_io = StringIO(s)
        result = _soup.parse(s_io)
        reveal_type(result)
        del result

        b_io = BytesIO(b)
        result = _soup.parse(b_io)
        reveal_type(result)
        del result

        with open(h2_filepath, "r") as f:
            result = _soup.parse(f)
        reveal_type(result)
        del result

        with open(h2_filepath, "rb") as f:
            result = _soup.parse(f)
        reveal_type(result)
        del result

        with urlopen(h2_fileuri) as f:
            result = _soup.parse(f)
        reveal_type(result)
        del result

        with pytest.raises(
            TypeError, match=r"expected str, bytes or os\.PathLike object"
        ):
            _ = _soup.parse(cast(Any, None))

        # recwarn fixture, pytest.warns() and warnings.catch_warnings()
        # all fail to catch this warning:
        # MarkupResemblesLocatorWarning: The input looks more like a
        # filename than markup. You may want to open this file and
        # pass the filehandle into Beautiful Soup.
        result = _soup.parse(cast(Any, h2_filepath))
        reveal_type(result)
        del result

    def test_makeelement(self, h2_filepath: Path) -> None:
        result = _soup.parse(
            str(h2_filepath), makeelement=_html.xhtml_parser.makeelement
        )
        reveal_type(result.getroot())
        del result

        result = _soup.parse(str(h2_filepath), None, etree.Element)
        reveal_type(result.getroot())
        del result

        with pytest.raises(TypeError, match="object is not callable"):
            _ = _soup.parse(str(h2_filepath), makeelement=cast(Any, 1))

        with pytest.raises(TypeError, match="unexpected keyword argument 'attrib"):
            _ = _soup.parse(str(h2_filepath), makeelement=cast(Any, etree.CommentBase))

    # Just test capability to pass extra keywords to beautifulsoup
    # no intention to cover all keyword arguments supported by bs
    def test_bs_args(self, h2_fileuri: str) -> None:
        fh = urlopen(h2_fileuri)
        result = _soup.parse(fh, exclude_encodings=["ascii"])
        reveal_type(result)
        del result

        result = _soup.parse(fh, from_encoding="ascii")
        reveal_type(result)
        del result

        with pytest.raises(TypeError, match="unexpected keyword argument 'badarg'"):
            _ = _soup.parse(fh, badarg=None)  # pyright: ignore

        fh.close()


class TestConvertTree:
    @_testutils.signature_tester(
        _soup.convert_tree,
        (
            ("beautiful_soup_tree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
            ("makeelement", Parameter.POSITIONAL_OR_KEYWORD, None),
        ),
    )  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    def test_input_type(self, h2_filepath: Path) -> None:
        for feat in ("lxml-html", "html.parser"):
            soup = BeautifulSoup(h2_filepath.read_text(), features=feat)
            result = _soup.convert_tree(soup)
            reveal_type(result)
            for item in result:
                reveal_type(item)
            del soup, result

        tree = _html.parse(h2_filepath)
        s_io = StringIO(h2_filepath.read_text())

        for src in (tree, h2_filepath):
            with pytest.raises(TypeError, match="object is not iterable"):
                _ = _soup.convert_tree(cast(Any, src))

        for src in (tree.getroot(), s_io):
            with pytest.raises(
                AttributeError, match="object has no attribute 'contents'"
            ):
                _ = _soup.convert_tree(cast(Any, src))

        s_io.close()
        del tree

    def test_makeelement(self, h2_str: str) -> None:
        soup = BeautifulSoup(h2_str, features="html.parser")

        result = _soup.convert_tree(soup, makeelement=_html.xhtml_parser.makeelement)
        reveal_type(result)
        del result

        result = _soup.convert_tree(soup, makeelement=etree.Element)
        reveal_type(result)
        del result

        with pytest.raises(TypeError, match="object is not callable"):
            _ = _soup.convert_tree(soup, makeelement=cast(Any, 1))

        with pytest.raises(TypeError, match="unexpected keyword argument 'attrib"):
            _ = _soup.convert_tree(soup, makeelement=cast(Any, etree.CommentBase))
