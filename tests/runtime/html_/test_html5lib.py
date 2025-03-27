from __future__ import annotations

import io
import sys
from collections.abc import Callable, Iterable
from inspect import Parameter
from itertools import product
from pathlib import Path
from typing import Any, cast

import html5lib.html5parser
import lxml.etree as _e
import lxml.html.html5parser as h5
import pytest
from hypothesis import HealthCheck, assume, given, settings
from lxml.etree import (
    _Element as _Element,
    _ElementTree as _ElementTree,
)
from lxml.html.html5parser import HTMLParser as HTMLParser

from .._testutils import signature_tester, strategy as _st
from .._testutils.errors import (
    raise_no_attribute,
    raise_unexpected_kwarg,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type

if sys.version_info >= (3, 12):
    from collections.abc import Buffer
else:
    from typing_extensions import Buffer


class TestParserConstruct:
    def test_default_parser(self) -> None:
        reveal_type(h5.html_parser)

    # `tree` param is dropped in stub
    @signature_tester(h5.HTMLParser.__init__, (
        ("strict", Parameter.POSITIONAL_OR_KEYWORD, False          ),
        ("kwargs", Parameter.VAR_KEYWORD          , Parameter.empty),
    ))  # fmt: skip
    @signature_tester(html5lib.html5parser.HTMLParser.__init__, (
        ("tree"                 , Parameter.POSITIONAL_OR_KEYWORD, None ),
        ("strict"               , Parameter.POSITIONAL_OR_KEYWORD, False),
        ("namespaceHTMLElements", Parameter.POSITIONAL_OR_KEYWORD, True ),
        ("debug"                , Parameter.POSITIONAL_OR_KEYWORD, False),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    # Stub signature is pretty strict in order to promote cleaner code; but the
    # params are just truthy/falsy values in runtime. No hypothesis testing is
    # imposed on the parameters.
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
        reveal_type(h5.HTMLParser(*args, **kw))


# Misc arguments are not tested, they are just truthy/falsy values
# - no_leading_text from fragments_fromstring()
# - create_parent from fragment_fromstring()
class TestSignature:
    @signature_tester(h5.document_fromstring, (
        ("html"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("guess_charset", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_document_fromstring(self) -> None:
        pass

    @signature_tester(h5.fragments_fromstring, (
        ("html"           , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("no_leading_text", Parameter.POSITIONAL_OR_KEYWORD, False          ),
        ("guess_charset"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"         , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_fragments_fromstring(self) -> None:
        pass

    @signature_tester(h5.fragment_fromstring, (
        ("html"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("create_parent", Parameter.POSITIONAL_OR_KEYWORD, False          ),
        ("guess_charset", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_fragment_fromstring(self) -> None:
        pass

    @signature_tester(h5.fromstring, (
        ("html"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("guess_charset", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_fromstring(self) -> None:
        pass

    @signature_tester(h5.parse, (
        ("filename_url_or_file", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("guess_charset"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parser"              , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_parse(self) -> None:
        pass


class TestInputArg:
    def test_document_fromstring(self, html2_str: str, html2_bytes: bytes) -> None:
        reveal_type(h5.document_fromstring(html2_str))
        reveal_type(h5.document_fromstring(html=html2_bytes))

    def test_fragments_fromstring(self) -> None:
        src = '<div><img src=""/></div><span>nothing</span>'
        reveal_type(h5.fragments_fromstring(src))
        reveal_type(h5.fragments_fromstring(html=src.encode()))
        reveal_type(h5.fragments_fromstring(src, no_leading_text=True))

    def test_fragment_fromstring(self) -> None:
        src: str = "<span>nothing</span>"
        reveal_type(h5.fragment_fromstring(src))
        reveal_type(h5.fragment_fromstring(src.encode()))

    def test_fromstring(self, html2_str: str, html2_bytes: bytes) -> None:
        reveal_type(h5.fromstring(html2_str))
        reveal_type(h5.fromstring(html2_bytes))

    @pytest.mark.parametrize(
        ("funcname",),
        [
            ("document_fromstring",),
            ("fragments_fromstring",),
            ("fragment_fromstring",),
            ("fromstring",),
        ],
    )
    def test_invalid_src_1(
        self,
        funcname: str,
        html2_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        for src in generate_input_file_arguments(
            html2_filepath, exclude_type=(str, bytes)
        ):
            with pytest.raises(TypeError, match="string required"):
                func = getattr(h5, funcname)
                _ = func(html=src)

    @pytest.mark.parametrize(
        ("funcname",),
        [
            ("document_fromstring",),
            ("fragments_fromstring",),
            ("fragment_fromstring",),
            ("fromstring",),
        ],
    )
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(src=_st.all_instances_except_of_type(str, bytes))
    def test_invalid_src_2(self, funcname: str, src: Any) -> None:
        func = getattr(h5, funcname)
        with pytest.raises(TypeError, match="string required"):
            _ = func(src)

    @pytest.mark.parametrize(
        ("funcname",),
        [
            ("document_fromstring",),
            ("fragments_fromstring",),
            ("fragment_fromstring",),
            ("fromstring",),
        ],
    )
    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_invalid_src_3(
        self,
        funcname: str,
        html2_str: str,
        iterable_of: Any,
    ) -> None:
        func = getattr(h5, funcname)
        with pytest.raises(TypeError, match="string required"):
            _ = func(iterable_of(html2_str))

    def test_parse_src_ok(
        self,
        html2_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        if sys.platform == "win32":
            # html.html5parser _looks_like_uri() util func has bug
            excluded = (Path, bytes)
        else:
            excluded = (Path,)
        for src in generate_input_file_arguments(html2_filepath, exclude_type=excluded):
            tree = h5.parse(src)
            reveal_type(tree)
            reveal_type(tree.getroot())
            del tree

        with pytest.raises(TypeError, match="bytes-like object is required"):
            _ = h5.parse(cast(Any, html2_filepath))

    # `parse()` has some very odd quirks in that it unexpectedly accepts:
    # - None or other structs that evaluate to None, which results in
    #   empty html document (<html><body/></html>)
    # - buffer-like objects, in which html content is directly taken from
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, io.BytesIO, io.StringIO, Buffer))
    @pytest.mark.slow
    def test_parse_src_bad(self, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with pytest.raises((TypeError, AssertionError)):
            _ = h5.parse(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_parse_src_bad_2(self, html2_filepath: Path, iterable_of: Any) -> None:
        with pytest.raises(TypeError, match="bytes-like object is required"):
            _ = h5.parse(iterable_of(str(html2_filepath)))


class TestParserArg:
    class MyParser(h5.HTMLParser):
        pass

    # Not just any html5lib parser, requires those
    # using etree_lxml as treebuilder
    def test_subclass(self, html2_str: str, html2_filepath: Path) -> None:
        parser = self.MyParser()

        reveal_type(h5.document_fromstring(html2_str, parser=parser))
        reveal_type(h5.fragments_fromstring(html2_str, parser=parser))
        reveal_type(h5.fragment_fromstring(html2_str, parser=parser, create_parent=True))  # fmt: skip  # noqa: E501
        reveal_type(h5.fromstring(html2_str, parser=parser))

        tree = h5.parse(str(html2_filepath), parser=parser)
        reveal_type(tree)

    @pytest.mark.parametrize(
        ("funcname",),
        [
            ("document_fromstring",),
            ("fragments_fromstring",),
            ("fragment_fromstring",),
            ("fromstring",),
            ("parse",),
        ],
    )
    def test_incompatible(
        self, html2_str: str, html2_filepath: Path, funcname: str
    ) -> None:
        src = str(html2_filepath) if funcname == "parse" else html2_str
        func = getattr(h5, funcname)
        keywords: dict[str, Any] = {"parser": _e.HTMLParser()}
        if funcname == "fragment_fromstring":
            keywords["create_parent"] = True
        with raise_no_attribute:
            _ = func(src, **keywords)


# guess_charset is a truthy/falsy value, thus no arg type test
class TestCharsetArg:
    @pytest.mark.parametrize(("chardet",), [(True,), (False,)])
    def test_bytes_input_ok(self, html2_bytes: bytes, chardet: bool) -> None:
        reveal_type(h5.document_fromstring(html2_bytes, chardet))
        reveal_type(h5.fragments_fromstring(html2_bytes, guess_charset=chardet))
        reveal_type(h5.fragment_fromstring(html2_bytes, create_parent=True, guess_charset=chardet))  # fmt: skip
        reveal_type(h5.fromstring(html2_bytes, guess_charset=chardet))

    @pytest.mark.parametrize(
        ("funcname", "chardet"),
        product(
            [
                "document_fromstring",
                "fragments_fromstring",
                "fragment_fromstring",
                "fromstring",
            ],
            [True, False],
        ),
    )
    def test_str_input_conflict(
        self, html2_str: str, funcname: str, chardet: bool
    ) -> None:
        func = getattr(h5, funcname)
        with raise_unexpected_kwarg:
            _ = func(html2_str, guess_charset=chardet)

    @pytest.mark.parametrize(("chardet",), [(True,), (False,)])
    def test_parse_bytes_input_ok(
        self,
        html2_filepath: Path,
        chardet: bool,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        if sys.platform == "win32":
            # html.html5parser _looks_like_uri() util func has bug
            excluded = (Path, bytes)
        else:
            excluded = (Path,)

        for input in generate_input_file_arguments(
            html2_filepath, exclude_type=excluded
        ):
            has_conflict = False
            # local file object
            if hasattr(input, "read") and not hasattr(input, "status"):
                data = input.read(1)
                # SupportsRead[str] + guess_charset = boom
                if isinstance(data, str) and chardet:
                    has_conflict = True
                input.seek(0, io.SEEK_SET)

            if has_conflict:
                with raise_unexpected_kwarg:
                    _ = h5.parse(input, guess_charset=chardet)
            else:
                tree = h5.parse(input, guess_charset=chardet)
                reveal_type(tree)
                reveal_type(tree.getroot())
                del tree
