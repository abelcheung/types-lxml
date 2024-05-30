from __future__ import annotations

from inspect import Parameter
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, cast

import _testutils
import lxml.html.html5parser as h5
import pytest
from lxml.etree import (
    HTMLParser as WrongParser,
    _Element as _Element,
    _ElementTree as _ElementTree,
)
from lxml.html.html5parser import HTMLParser

reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestParserConstruct:
    def test_default_parser(self) -> None:
        reveal_type(h5.html_parser)

    @_testutils.signature_tester(HTMLParser.__init__, (
        ("strict", Parameter.POSITIONAL_OR_KEYWORD, False          ),
        ("kwargs", Parameter.VAR_KEYWORD          , Parameter.empty),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    @pytest.mark.parametrize(
        ("args", "kw"),
        [
            pytest.param((), {}),
            pytest.param((False,), {}),
            pytest.param((), {"strict": True, "debug": True}),
            pytest.param((True,), {"namespaceHTMLElements": True}),
        ],
    )
    def test_good_args(self, args: tuple[Any], kw: dict[str, Any]) -> None:
        p = HTMLParser(*args, **kw)
        reveal_type(p)

    # Stub signature is pretty strict in order to promote cleaner code;
    # but the params are just truthy/falsy values in runtime, so no test
    # is imposed on them
    @pytest.mark.parametrize(
        ("args", "kw"),
        [
            pytest.param((True, True), {}),
            pytest.param((), {"badarg": 1}),
        ],
    )
    def test_bad_args(self, args: tuple[Any], kw: dict[str, Any]) -> None:
        with pytest.raises(TypeError):
            _ = HTMLParser(*args, **kw)


class TestFromstringFamily:
    @_testutils.signature_tester(h5.document_fromstring, (
        ("html"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("guess_charset", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_d_fs_sig(self) -> None:
        pass

    def test_d_fs_src(self, h2_str: str, h2_bytes: bytes) -> None:
        elem = h5.document_fromstring(h2_str)
        reveal_type(elem)
        del elem

        elem = h5.document_fromstring(h2_bytes)
        reveal_type(elem)
        del elem

    @_testutils.signature_tester(h5.fragments_fromstring, (
        ("html"           , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("no_leading_text", Parameter.POSITIONAL_OR_KEYWORD, False          ),
        ("guess_charset"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"         , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_fs_fs_sig(self) -> None:
        pass

    def test_fs_fs_src(self) -> None:
        src_s: str = '<div><img src=""/></div><span>nothing</span>'
        src_b: bytes = src_s.encode()

        elems = h5.fragments_fromstring(src_s)
        reveal_type(elems)
        for elem in elems:
            reveal_type(elem)
        del elems

        elems = h5.fragments_fromstring(src_b)
        reveal_type(elems)
        for elem in elems:
            reveal_type(elem)
        del elems

        elems = h5.fragments_fromstring(src_b, no_leading_text=True)
        reveal_type(elems)
        for elem in elems:
            reveal_type(elem)
        del elems

    @_testutils.signature_tester(h5.fragment_fromstring, (
        ("html"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("create_parent", Parameter.POSITIONAL_OR_KEYWORD, False          ),
        ("guess_charset", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_f_fs_sig(self) -> None:
        pass

    def test_f_fs_src(self) -> None:
        src_s: str = "<span>nothing</span>"
        src_b: bytes = src_s.encode()

        elem = h5.fragment_fromstring(src_s)
        reveal_type(elem)
        del elem

        elem = h5.fragment_fromstring(src_b)
        reveal_type(elem)
        del elem

    @_testutils.signature_tester(h5.fromstring, (
        ("html"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("guess_charset", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_fs_sig(self) -> None:
        pass


    def test_fs_src(self, h2_str: str, h2_bytes: bytes) -> None:
        elem = h5.fromstring(h2_str)
        reveal_type(elem)
        del elem

        elem = h5.fromstring(h2_bytes)
        reveal_type(elem)
        del elem

    @pytest.mark.parametrize(
        ("funcname",),
        [
            ("document_fromstring",),
            ("fragments_fromstring",),
            ("fragment_fromstring",),
            ("fromstring",),
        ],
    )
    def test_invalid_src(self, h2_str: str, h2_filepath: Path, funcname: str) -> None:
        sio = StringIO(h2_str)
        fh = open(h2_filepath, "rb")
        for src in (None, sio, fh):
            with pytest.raises(TypeError, match="string required"):
                func = getattr(h5, funcname)
                _ = func(cast(Any, src))
        fh.close()

    @_testutils.signature_tester(h5.parse, (
        ("filename_url_or_file", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("guess_charset"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"              , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_parse_sig(self) -> None:
        pass


    def test_parse_src(self, h2_filepath: Path) -> None:
        with open(h2_filepath, "rb") as fh:
            tree = h5.parse(fh)
        reveal_type(tree)
        reveal_type(tree.getroot())
        del tree

        b_io = BytesIO(h2_filepath.read_bytes())
        tree = h5.parse(b_io)
        reveal_type(tree)
        del tree

        s_io = StringIO(h2_filepath.read_text())
        tree = h5.parse(s_io)
        reveal_type(tree)
        del tree

        with pytest.raises(TypeError, match="bytes-like object is required"):
            _ = h5.parse(cast(Any, h2_filepath))

        tree = h5.parse(str(h2_filepath))
        reveal_type(tree)
        del tree


class MyParser(h5.HTMLParser):
    pass


class TestParserArg:
    # Not just any html5lib parser, requires those
    # using etree_lxml as treebuilder
    def test_subclass(self, h2_str: str) -> None:
        parser = MyParser()

        elem = h5.document_fromstring(h2_str, parser=parser)
        reveal_type(elem)
        del elem

        elems = h5.fragments_fromstring(h2_str, parser=parser)
        reveal_type(elems)
        for elem in elems:
            reveal_type(elem)
        del elems

        elem = h5.fragment_fromstring(h2_str, parser=parser, create_parent=True)
        reveal_type(elem)
        del elem

        elem = h5.fromstring(h2_str, parser=parser)
        reveal_type(elem)
        del elem

        s_io = StringIO(h2_str)
        tree = h5.parse(s_io, parser=parser)
        reveal_type(tree)
        del tree

    def test_incompatible(self, h2_str: str) -> None:
        parser = WrongParser()

        with pytest.raises(AttributeError, match="has no attribute 'parse'"):
            _ = h5.document_fromstring(h2_str, parser=cast(Any, parser))

        with pytest.raises(AttributeError, match="has no attribute 'parseFragment'"):
            _ = h5.fragments_fromstring(h2_str, parser=cast(Any, parser))

        with pytest.raises(AttributeError, match="has no attribute 'parseFragment'"):
            _ = h5.fragment_fromstring(
                h2_str, parser=cast(Any, parser), create_parent=True
            )

        with pytest.raises(AttributeError, match="has no attribute 'parse'"):
            _ = h5.fromstring(h2_str, parser=cast(Any, parser))

        s_io = StringIO(h2_str)
        with pytest.raises(AttributeError, match="has no attribute 'parse'"):
            _ = h5.parse(s_io, parser=cast(Any, parser))


# guess_charset is a truthy/falsy value, thus no arg type test
class TestCharsetArg:
    def test_bool(self, h2_bytes: bytes) -> None:
        elem = h5.document_fromstring(h2_bytes, True)
        reveal_type(elem)
        del elem

        elems = h5.fragments_fromstring(h2_bytes, guess_charset=True)
        reveal_type(elems)
        for elem in elems:
            reveal_type(elem)
        del elems

        elem = h5.fragment_fromstring(
            h2_bytes, create_parent=b"article", guess_charset=False
        )
        reveal_type(elem)
        del elem

        elem = h5.fromstring(h2_bytes, guess_charset=False)
        reveal_type(elem)
        del elem

        b_io = BytesIO(h2_bytes)
        tree = h5.parse(b_io, guess_charset=False)
        reveal_type(tree)
        del tree

    def test_conflict(self, h2_str: str) -> None:
        with pytest.raises(TypeError, match="unexpected keyword argument"):
            _ = h5.document_fromstring(h2_str, guess_charset=True)  # type: ignore

        with pytest.raises(TypeError, match="unexpected keyword argument"):
            _ = h5.fragments_fromstring(h2_str, guess_charset=False)  # type: ignore

        with pytest.raises(TypeError, match="unexpected keyword argument"):
            _ = h5.fragment_fromstring(h2_str, guess_charset=False)  # type: ignore

        with pytest.raises(TypeError, match="unexpected keyword argument"):
            _ = h5.fromstring(h2_str, False)  # type: ignore

        s_io = StringIO(h2_str)
        with pytest.raises(TypeError, match="unexpected keyword argument"):
            _ = h5.parse(s_io, True)  # type: ignore
