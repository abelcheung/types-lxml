from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from inspect import Parameter
from pathlib import Path
from types import NoneType
from typing import Any

import pytest
from hypothesis import (
    HealthCheck,
    assume,
    given,
    settings,
)
from lxml.etree import (
    LXML_VERSION,
    XMLDTDID,
    XMLID,
    XMLParser,
    _Element as _Element,
    _IDDict as _IDDict,
)
from lxml.html import (
    HtmlElement as HtmlElement,
    XHTMLParser,
    xhtml_parser,
)
from lxml.objectify import (
    ObjectifiedElement as ObjectifiedElement,
    makeparser,
)

from ._testutils import signature_tester, strategy as _st
from ._testutils.common import text_document_types
from ._testutils.errors import (
    raise_invalid_filename_type,
    raise_wrong_arg_type,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestXmlid:
    @signature_tester(XMLID, (
        ("text"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("parser"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("base_url", Parameter.KEYWORD_ONLY         , None           ),
    ))  # fmt: skip
    def test_basic(self, xml2_bytes: bytes) -> None:
        root, xmlids = XMLID(xml2_bytes)
        reveal_type(root)
        reveal_type(xmlids)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    def test_text_arg_ok(self) -> None:
        content = b'<root id="1"/>'
        src: list[Any] = [content.decode(), content]
        if LXML_VERSION >= (6, 0):
            src.extend([bytearray(content), memoryview(content)])
        for text in src:
            _, xmlids = XMLID(text)
            assert len(xmlids) == 1

    def test_text_arg_bad(
        self,
        xml2_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        if LXML_VERSION >= (6, 0):
            exc, match = TypeError, r"bytes-like object is required"
        else:
            exc, match = ValueError, r"can only parse strings"
        for input in generate_input_file_arguments(
            xml2_filepath,
            exclude_type=(
                *text_document_types.allow,
                *text_document_types.skip,
            ),
        ):
            with pytest.raises(exc, match=match):
                _ = XMLID(input)

    def test_parser_basic(self, xml2_bytes: bytes) -> None:
        root, xmlids = XMLID(xml2_bytes, parser=None)
        reveal_type(root)
        reveal_type(xmlids)
        assert len(xmlids) == len(root.xpath("//*[@id]"))
        del root, xmlids

        root, xmlids = XMLID(xml2_bytes, parser=XMLParser())
        reveal_type(root)
        reveal_type(xmlids)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    def test_parser_subclass_1(self, xml2_bytes: bytes) -> None:
        root, xmlids = XMLID(xml2_bytes, parser=makeparser())
        reveal_type(root)
        reveal_type(xmlids)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    def test_parser_subclass_2(self, xml2_bytes: bytes) -> None:
        root, xmlids = XMLID(xml2_bytes, parser=xhtml_parser)
        reveal_type(root)
        reveal_type(xmlids)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_parser_arg_bad_1(self, xml2_bytes: bytes, thing: Any) -> None:
        with raise_wrong_arg_type:
            _ = XMLID(xml2_bytes, parser=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_parser_arg_bad_2(self, xml2_bytes: bytes, iterable_of: Any) -> None:
        with raise_wrong_arg_type:
            _ = XMLID(xml2_bytes, parser=iterable_of(XMLParser()))

    def test_baseurl_arg_ok(self, xml2_bytes: bytes) -> None:
        url = b"http://example.com"
        for base_url in (url.decode(), url):
            root, xmlids = XMLID(xml2_bytes, base_url=base_url)
            reveal_type(root)
            reveal_type(xmlids)
            assert len(xmlids) == len(root.xpath("//*[@id]"))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, NoneType))
    @pytest.mark.slow
    def test_baseurl_arg_bad_1(self, xml2_bytes: bytes, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_invalid_filename_type:
            _ = XMLID(xml2_bytes, base_url=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_baseurl_arg_bad_2(self, xml2_bytes: bytes, iterable_of: Any) -> None:
        with raise_invalid_filename_type:
            _ = XMLID(xml2_bytes, base_url=iterable_of("http://example.com"))


# Note that XMLDTDID() doesn't work with default parser.
# Custom parser is required to enable DTD parsing.
class TestXmldtdid:
    @signature_tester(XMLDTDID, (
        ("text"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("parser"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("base_url", Parameter.KEYWORD_ONLY         , None           ),
    ))  # fmt: skip
    def test_basic(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser
    ) -> None:
        root, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        reveal_type(root)
        reveal_type(xmlids)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    def test_text_arg_ok(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser
    ) -> None:
        str_content = xml2_bytes_with_dtd.decode().replace('encoding="UTF-8"', "")
        # ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
        src: list[Any] = [
            xml2_bytes_with_dtd,
            str_content,
        ]
        if LXML_VERSION >= (6, 0):
            src.extend([
                bytearray(xml2_bytes_with_dtd),
                memoryview(xml2_bytes_with_dtd),
            ])
        for text in src:
            _, xmlids = XMLDTDID(text, parser=dtd_enabled_parser)
            assert len(xmlids) > 0

    def test_text_arg_bad(
        self,
        xml2_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        if LXML_VERSION >= (6, 0):
            exc, match = TypeError, r"bytes-like object is required"
        else:
            exc, match = ValueError, r"can only parse strings"
        for input in generate_input_file_arguments(
            xml2_filepath,
            exclude_type=(
                *text_document_types.allow,
                *text_document_types.skip,
            ),
        ):
            with pytest.raises(exc, match=match):
                _ = XMLDTDID(input)

    def test_parser_basic(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser
    ) -> None:
        root, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=None)
        reveal_type(root)
        reveal_type(xmlids)
        assert len(xmlids) == 0
        del root, xmlids

        root, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=XMLParser())
        reveal_type(root)
        reveal_type(xmlids)
        assert len(xmlids) == 0
        del root, xmlids

        root, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        reveal_type(root)
        reveal_type(xmlids)
        for i in xmlids.items():
            reveal_type(i)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    # Though failure poses no concern in terms of typing, but why?
    @pytest.mark.xfail
    def test_parser_subclass_1(self, xml2_bytes: bytes) -> None:
        root, xmlids = XMLDTDID(
            xml2_bytes, parser=makeparser(dtd_validation=True, load_dtd=True)
        )
        reveal_type(root)
        reveal_type(xmlids)
        for i in xmlids.items():
            reveal_type(i)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    @pytest.mark.xfail
    def test_parser_subclass_2(self, xml2_bytes: bytes) -> None:
        parser = XHTMLParser(dtd_validation=True, load_dtd=True)
        root, xmlids = XMLDTDID(xml2_bytes, parser=parser)
        reveal_type(root)
        reveal_type(xmlids)
        for i in xmlids.items():
            reveal_type(i)
        assert len(xmlids) == len(root.xpath("//*[@id]"))
