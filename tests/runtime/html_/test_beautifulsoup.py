from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from inspect import Parameter
from pathlib import Path
from types import NoneType
from typing import Any, cast
from urllib.request import urlopen

import pytest
from bs4 import BeautifulSoup
from hypothesis import HealthCheck, assume, given, settings
from lxml.etree import (
    Element,
    _Element as _Element,
    _ElementTree as _ElementTree,
)
from lxml.html import (
    HtmlElement as HtmlElement,
    soupparser as _soup,
    xhtml_parser,
)

from .._testutils import signature_tester, strategy as _st
from .._testutils.errors import (
    raise_unexpected_kwarg,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestFromstring:
    @signature_tester(_soup.fromstring, (
        ("data"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("beautifulsoup", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("makeelement"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("bsargs"       , Parameter.VAR_KEYWORD          , Parameter.empty),
    ))  # fmt: skip
    @signature_tester(BeautifulSoup.__init__, (
        ("markup"           , Parameter.POSITIONAL_OR_KEYWORD, ""             ),
        ("features"         , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("builder"          , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("parse_only"       , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("from_encoding"    , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("exclude_encodings", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("element_classes"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("kwargs"           , Parameter.VAR_KEYWORD          , Parameter.empty),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    # Even though input content could be invalid, it is still correct
    # with respect to typing (str)
    @pytest.mark.filterwarnings(
        "ignore:The input passed in on this line .*:bs4.MarkupResemblesLocatorWarning"
    )
    def test_dubious_input(self, html2_filepath: Path) -> None:
        result = _soup.fromstring(str(html2_filepath))
        reveal_type(result)

    def test_input_arg_ok(
        self,
        html2_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        for input in generate_input_file_arguments(
            html2_filepath, exclude_type=(str, bytes, Path)
        ):
            result = _soup.fromstring(input)
            reveal_type(result)
            del result

        result = _soup.fromstring(html2_filepath.read_bytes())
        reveal_type(result)
        del result

        result = _soup.fromstring(html2_filepath.read_text())
        reveal_type(result)
        del result

    def test_beautifulsoup_arg_ok(self, html2_str: str) -> None:
        result1 = _soup.fromstring(html2_str, BeautifulSoup)
        reveal_type(result1)
        del result1

        result2 = _soup.fromstring(html2_str, None)
        reveal_type(result2)
        del result2

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_beautifulsoup_arg_bad_1(self, html2_str: str, thing: Any) -> None:
        assume(thing is not NoneType)
        if not callable(thing):
            with pytest.raises(TypeError, match=r"object is not callable"):
                _ = _soup.fromstring(html2_str, thing)
        else:
            with pytest.raises(Exception):  # Very diversified
                _ = _soup.fromstring(html2_str, cast(Any, thing))

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_beautifulsoup_arg_bad_2(self, html2_str: str, iterable_of: Any) -> None:
        with pytest.raises(TypeError, match=r"object is not callable"):
            _ = _soup.fromstring(html2_str, iterable_of(BeautifulSoup))

    def test_makeelement_arg_ok(self, html2_str: str) -> None:
        result1 = _soup.fromstring(html2_str, makeelement=xhtml_parser.makeelement)
        reveal_type(result1)
        del result1

        result2 = _soup.fromstring(html2_str, None, Element)
        reveal_type(result2)
        del result2

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_makeelement_arg_bad_1(self, html2_str: str, thing: Any) -> None:
        with pytest.raises((TypeError, ValueError)):
            _ = _soup.fromstring(html2_str, makeelement=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_makeelement_arg_bad_2(self, html2_str: str, iterable_of: Any) -> None:
        with pytest.raises(TypeError):
            _ = _soup.fromstring(html2_str, makeelement=iterable_of(Element))

    # Just test capability to pass extra keywords to beautifulsoup
    # no intention to cover all keyword arguments supported by bs
    def test_bs_args(self, html2_bytes: bytes) -> None:
        result = _soup.fromstring(html2_bytes, exclude_encodings=["ascii"])
        reveal_type(result)
        del result

        result = _soup.fromstring(html2_bytes, from_encoding="ascii")
        reveal_type(result)
        del result

        with raise_unexpected_kwarg:
            _ = _soup.fromstring(html2_bytes, badarg=None)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportUnknownVariableType]


class TestParse:
    @signature_tester(_soup.parse, (
        ("file"         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("beautifulsoup", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("makeelement"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("bsargs"       , Parameter.VAR_KEYWORD          , Parameter.empty),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    def test_input_arg_ok(
        self,
        html2_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        # expects filename/io, not html data
        with pytest.raises(OSError):
            _ = _soup.parse(html2_filepath.read_text())
        with pytest.raises(OSError):
            _ = _soup.parse(html2_filepath.read_bytes())

        for input in generate_input_file_arguments(html2_filepath):
            reveal_type(_soup.parse(input))

    def test_beautifulsoup_arg_ok(self, html2_filepath: Path) -> None:
        result1 = _soup.parse(html2_filepath, BeautifulSoup)
        reveal_type(result1)
        del result1

        result2 = _soup.parse(html2_filepath, None)
        reveal_type(result2)
        del result2

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_beautifulsoup_arg_bad_1(self, html2_filepath: Path, thing: Any) -> None:
        if not callable(thing):
            with pytest.raises(TypeError, match=r"object is not callable"):
                _ = _soup.parse(html2_filepath, thing)
        else:
            with pytest.raises(Exception):  # Very diversified
                _ = _soup.parse(html2_filepath, cast(Any, thing))

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_beautifulsoup_arg_bad_2(
        self, html2_filepath: Path, iterable_of: Any
    ) -> None:
        with pytest.raises(TypeError, match=r"object is not callable"):
            _ = _soup.parse(html2_filepath, beautifulsoup=iterable_of(BeautifulSoup))

    def test_makeelement_arg_ok(self, html2_filepath: Path) -> None:
        result1 = _soup.parse(html2_filepath, makeelement=xhtml_parser.makeelement)
        reveal_type(result1)
        reveal_type(result1.getroot())
        del result1

        result2 = _soup.parse(html2_filepath, None, Element)
        reveal_type(result2)
        reveal_type(result2.getroot())
        del result2

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_makeelement_arg_bad_1(self, html2_filepath: Path, thing: Any) -> None:
        with pytest.raises((TypeError, ValueError)):
            _ = _soup.parse(html2_filepath, makeelement=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_makeelement_arg_bad_2(
        self, html2_filepath: Path, iterable_of: Any
    ) -> None:
        with pytest.raises(TypeError):
            _ = _soup.parse(html2_filepath, makeelement=iterable_of(Element))

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

        with raise_unexpected_kwarg:
            _ = _soup.parse(fh, badarg=None)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportUnknownVariableType]

        fh.close()


class TestConvertTree:
    @signature_tester(_soup.convert_tree, (
        ("beautiful_soup_tree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("makeelement"        , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    def test_input_arg_ok(self, html2_filepath: Path) -> None:
        for feat in ("lxml-html", "html.parser"):
            soup = BeautifulSoup(html2_filepath.read_text(), features=feat)
            reveal_type(_soup.convert_tree(soup))

    def test_input_arg_bad(
        self,
        html2_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        # Using lxml _Element/_ElementTree as input has very bad effect;
        # it generates TypeError uncatchable by pytest.raises.
        # Thus not included in the test.
        for input in generate_input_file_arguments(html2_filepath):
            with pytest.raises((TypeError, AttributeError)):
                _ = _soup.convert_tree(input)

    def test_makeelement_arg_ok(self, html2_str: str) -> None:
        soup = BeautifulSoup(html2_str, features="html.parser")

        result1 = _soup.convert_tree(soup, makeelement=xhtml_parser.makeelement)
        reveal_type(result1)
        del result1

        result2 = _soup.convert_tree(soup, makeelement=Element)
        reveal_type(result2)
        del result2

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_makeelement_arg_bad_1(self, html2_str: str, thing: Any) -> None:
        soup = BeautifulSoup(html2_str, features="html.parser")
        assume(thing is not NoneType)
        if not callable(thing):
            with pytest.raises(TypeError, match=r"object is not callable"):
                _ = _soup.convert_tree(soup, makeelement=thing)
        else:
            with pytest.raises(TypeError):
                _ = _soup.convert_tree(soup, makeelement=cast(Any, thing))

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_makeelement_arg_bad_2(self, html2_str: str, iterable_of: Any) -> None:
        soup = BeautifulSoup(html2_str, features="html.parser")
        with pytest.raises(TypeError, match=r"object is not callable"):
            _ = _soup.convert_tree(soup, makeelement=iterable_of(Element))
