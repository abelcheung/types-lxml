from __future__ import annotations

import sys
from inspect import Parameter
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, cast
from urllib.request import urlopen

import pytest
from bs4 import BeautifulSoup
from lxml import (
    etree as _e,
    html as _h,
)
from lxml.etree import _Element as _Element, _ElementTree as _ElementTree
from lxml.html import HtmlElement as HtmlElement, soupparser as _soup

from . import _testutils

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestFromstring:
    @_testutils.signature_tester(_soup.fromstring, (
        ("data"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("beautifulsoup", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("makeelement"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("bsargs"       , Parameter.VAR_KEYWORD          , Parameter.empty),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    # Even though input content could be invalid, it is still correct
    # with respect to typing (str)
    @pytest.mark.filterwarnings(
        "ignore:.* input looks more like a filename .*:"
        "bs4.MarkupResemblesLocatorWarning"
    )
    def test_dubious_input(self, html2_filepath: Path) -> None:
        result = _soup.fromstring(str(html2_filepath))
        reveal_type(result)

    @pytest.mark.filterwarnings("ignore:.* 'strip_cdata' option .*:DeprecationWarning")
    def test_input_type(self, html2_filepath: Path, html2_fileuri: str) -> None:
        s = html2_filepath.read_text()
        result = _soup.fromstring(s)
        reveal_type(result)
        del result

        b = html2_filepath.read_bytes()
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

        with open(html2_filepath, "r") as f:
            result = _soup.fromstring(f)
        reveal_type(result)
        del result

        with open(html2_filepath, "rb") as f:
            result = _soup.fromstring(f)
        reveal_type(result)
        del result

        with urlopen(html2_fileuri) as f:
            result = _soup.fromstring(f)
        reveal_type(result)
        del result

        for arg in (1, None, html2_filepath):
            with pytest.raises(TypeError, match=r"object of type '\w+' has no len\(\)"):
                _ = _soup.fromstring(cast(Any, arg))

            with pytest.raises(TypeError, match=r"object is not subscriptable"):
                _ = _soup.fromstring(cast(Any, {s}))

        for arg2 in ([s, b], (s, b)):
            with pytest.raises(
                TypeError, match=r"expected string or bytes-like object"
            ):
                _ = _soup.fromstring(cast(Any, arg2))

    def test_makeelement(self, html2_str: str) -> None:
        result1 = _soup.fromstring(html2_str, makeelement=_h.xhtml_parser.makeelement)
        reveal_type(result1)
        del result1

        result2 = _soup.fromstring(html2_str, None, _e.Element)
        reveal_type(result2)
        del result2

        with pytest.raises(TypeError, match="object is not callable"):
            _ = _soup.fromstring(html2_str, makeelement=cast(Any, 1))

        with pytest.raises(TypeError, match="unexpected keyword argument 'attrib"):
            _ = _soup.fromstring(html2_str, makeelement=cast(Any, _e.CommentBase))

    # Just test capability to pass extra keywords to beautifulsoup
    # no intention to cover all keyword arguments supported by bs
    def test_bs_args(self, html2_bytes: bytes) -> None:
        result = _soup.fromstring(html2_bytes, exclude_encodings=["ascii"])
        reveal_type(result)
        del result

        result = _soup.fromstring(html2_bytes, from_encoding="ascii")
        reveal_type(result)
        del result

        with pytest.raises(TypeError, match="unexpected keyword argument 'badarg'"):
            _ = _soup.fromstring(html2_bytes, badarg=None)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportUnknownVariableType]


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
        html2_filepath: Path,
        html2_fileuri: str,
    ) -> None:
        # expects filename/io, not html data
        s = html2_filepath.read_text()
        with pytest.raises(OSError):
            _ = _soup.parse(s)

        b = html2_filepath.read_bytes()
        with pytest.raises(OSError):
            _ = _soup.parse(b)

        result = _soup.parse(str(html2_filepath))
        reveal_type(result)
        root = result.getroot()
        reveal_type(root)
        del result

        result = _soup.parse(html2_filepath)
        reveal_type(result)
        root2 = result.getroot()
        assert root.tag == root2.tag
        assert root.attrib == root2.attrib
        del root, root2, result

        s_io = StringIO(s)
        result = _soup.parse(s_io)
        reveal_type(result)
        del result

        b_io = BytesIO(b)
        result = _soup.parse(b_io)
        reveal_type(result)
        del result

        with open(html2_filepath, "r") as f:
            result = _soup.parse(f)
        reveal_type(result)
        del result

        with open(html2_filepath, "rb") as f:
            result = _soup.parse(f)
        reveal_type(result)
        del result

        with urlopen(html2_fileuri) as f:
            result = _soup.parse(f)
        reveal_type(result)
        del result

        # Don't test integers, which are treated as file descriptor int

        for arg in (None, [html2_filepath, html2_filepath]):
            with pytest.raises(
                TypeError, match=r"expected str, bytes or os\.PathLike object"
            ):
                _ = _soup.parse(cast(Any, arg))

    def test_makeelement(self, html2_filepath: Path) -> None:
        result1 = _soup.parse(html2_filepath, makeelement=_h.xhtml_parser.makeelement)
        reveal_type(result1.getroot())
        del result1

        result2 = _soup.parse(html2_filepath, None, _e.Element)
        reveal_type(result2.getroot())
        del result2

        with pytest.raises(TypeError, match="object is not callable"):
            _ = _soup.parse(html2_filepath, makeelement=cast(Any, 1))

        with pytest.raises(TypeError, match="unexpected keyword argument 'attrib"):
            _ = _soup.parse(html2_filepath, makeelement=cast(Any, _e.CommentBase))

    # Just test capability to pass extra keywords to beautifulsoup
    # no intention to cover all keyword arguments supported by bs
    def test_bs_args(self, html2_fileuri: str) -> None:
        fh = urlopen(html2_fileuri)
        result = _soup.parse(fh, exclude_encodings=["ascii"])
        reveal_type(result)
        del result

        result = _soup.parse(fh, from_encoding="ascii")
        reveal_type(result)
        del result

        with pytest.raises(TypeError, match="unexpected keyword argument 'badarg'"):
            _ = _soup.parse(fh, badarg=None)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportUnknownVariableType]

        fh.close()


class TestConvertTree:
    @_testutils.signature_tester(
        _soup.convert_tree,
        (
            ("beautiful_soup_tree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
            ("makeelement"        , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ),
    )  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    @pytest.mark.filterwarnings("ignore:.* 'strip_cdata' option .*:DeprecationWarning")
    def test_input_type(self, html2_filepath: Path) -> None:
        for feat in ("lxml-html", "html.parser"):
            soup = BeautifulSoup(html2_filepath.read_text(), features=feat)
            result = _soup.convert_tree(soup)
            reveal_type(result)
            for item in result:
                reveal_type(item)
            del soup, result

        tree = _h.parse(html2_filepath)
        s_io = StringIO(html2_filepath.read_text())

        for src1 in (tree, html2_filepath):
            with pytest.raises(TypeError, match="object is not iterable"):
                _ = _soup.convert_tree(cast(Any, src1))

        for src2 in (tree.getroot(), s_io):
            with pytest.raises(
                AttributeError, match="object has no attribute 'contents'"
            ):
                _ = _soup.convert_tree(cast(Any, src2))

        s_io.close()
        del tree

    def test_makeelement(self, html2_str: str) -> None:
        soup = BeautifulSoup(html2_str, features="html.parser")

        result1 = _soup.convert_tree(soup, makeelement=_h.xhtml_parser.makeelement)
        reveal_type(result1)
        del result1

        result2 = _soup.convert_tree(soup, makeelement=_e.Element)
        reveal_type(result2)
        del result2

        with pytest.raises(TypeError, match="object is not callable"):
            _ = _soup.convert_tree(soup, makeelement=cast(Any, 1))

        with pytest.raises(TypeError, match="unexpected keyword argument 'attrib"):
            _ = _soup.convert_tree(soup, makeelement=cast(Any, _e.CommentBase))
