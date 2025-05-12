from __future__ import annotations

import io
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
    _ElementTree as _ElementTree,
    _IDDict as _IDDict,
    parseid,
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

from ._testutils import empty_signature_tester, signature_tester, strategy as _st
from ._testutils.common import text_document_types
from ._testutils.errors import (
    raise_invalid_filename_type,
    raise_invalid_utf8_type,
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


# Beware that XMLDTDID() doesn't work with default parser.
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

    def test_parser_subclass_1(self, xml2_bytes_with_dtd: bytes) -> None:
        parser = makeparser(dtd_validation=True, load_dtd=True)
        root, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=parser)
        reveal_type(root)
        reveal_type(xmlids)
        for i in xmlids.items():
            reveal_type(i)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    def test_parser_subclass_2(self, xml2_bytes_with_dtd: bytes) -> None:
        parser = XHTMLParser(dtd_validation=True, load_dtd=True)
        root, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=parser)
        reveal_type(root)
        reveal_type(xmlids)
        for i in xmlids.items():
            reveal_type(i)
        assert len(xmlids) == len(root.xpath("//*[@id]"))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_parser_arg_bad_1(self, xml2_bytes: bytes, thing: Any) -> None:
        with raise_wrong_arg_type:
            _ = XMLDTDID(xml2_bytes, parser=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_parser_arg_bad_2(self, xml2_bytes: bytes, iterable_of: Any) -> None:
        with raise_wrong_arg_type:
            _ = XMLDTDID(xml2_bytes, parser=iterable_of(XMLParser()))

    def test_baseurl_arg_ok(self, xml2_bytes_with_dtd: bytes) -> None:
        url = b"http://example.com"
        for base_url in (url.decode(), url):
            root, xmlids = XMLDTDID(xml2_bytes_with_dtd, base_url=base_url)
            reveal_type(root)
            reveal_type(xmlids)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, NoneType))
    @pytest.mark.slow
    def test_baseurl_arg_bad_1(self, xml2_bytes: bytes, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_invalid_filename_type:
            _ = XMLDTDID(xml2_bytes, base_url=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_baseurl_arg_bad_2(self, xml2_bytes: bytes, iterable_of: Any) -> None:
        with raise_invalid_filename_type:
            _ = XMLDTDID(xml2_bytes, base_url=iterable_of("http://example.com"))


class TestParseid:
    @signature_tester(parseid, (
        ("source"  , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("parser"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("base_url", Parameter.KEYWORD_ONLY         , None           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    def test_source_arg_ok(
        self,
        xml2_bytes_with_dtd: bytes,
        tmp_path: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        tmp_file = tmp_path / "sample.xml"
        tmp_file.write_bytes(xml2_bytes_with_dtd)
        for input in generate_input_file_arguments(
            tmp_file,
            exclude_type=io.StringIO,
        ):
            tree, xmlids = parseid(source=input)
            reveal_type(tree)
            reveal_type(xmlids)
            assert len(xmlids) == 0  # need custom parser

    def test_source_arg_bad_1(self, xml2_bytes_with_dtd: bytes) -> None:
        data: list[tuple[Any, type[Exception], str]] = [
            (xml2_bytes_with_dtd.decode(), OSError, r"Error reading file"),
            (xml2_bytes_with_dtd, OSError, r"Error reading file"),
            (bytearray(xml2_bytes_with_dtd), TypeError, r"cannot parse from"),
            (memoryview(xml2_bytes_with_dtd), TypeError, r"cannot parse from"),
        ]
        for input in data:
            with pytest.raises(input[1], match=input[2]):
                _ = parseid(source=input[0])

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_source_arg_bad_2(self, xml2_filepath: Path, iterable_of: Any) -> None:
        with pytest.raises(TypeError, match=r"cannot parse from"):
            _ = parseid(source=iterable_of(xml2_filepath))

    def test_parser_basic(
        self,
        tmp_path: Path,
        xml2_bytes_with_dtd: bytes,
        dtd_enabled_parser: XMLParser,
    ) -> None:
        tmp_file = tmp_path / "sample.xml"
        tmp_file.write_bytes(xml2_bytes_with_dtd)

        tree, xmlids = parseid(tmp_file, parser=None)
        reveal_type(tree)
        reveal_type(xmlids)
        assert len(xmlids) == 0
        del tree, xmlids

        tree, xmlids = parseid(tmp_file, parser=XMLParser())
        reveal_type(tree)
        reveal_type(xmlids)
        assert len(xmlids) == 0
        del tree, xmlids

        tree, xmlids = parseid(tmp_file, parser=dtd_enabled_parser)
        reveal_type(tree)
        reveal_type(xmlids)
        for i in xmlids.items():
            reveal_type(i)
        assert len(xmlids) == len(tree.xpath("//*[@id]"))

    def test_parser_subclass_1(
        self,
        tmp_path: Path,
        xml2_bytes_with_dtd: bytes,
    ) -> None:
        tmp_file = tmp_path / "sample.xml"
        tmp_file.write_bytes(xml2_bytes_with_dtd)
        parser = makeparser(dtd_validation=True, load_dtd=True)
        tree, xmlids = parseid(tmp_file, parser=parser)
        reveal_type(tree)
        reveal_type(xmlids)
        for i in xmlids.items():
            reveal_type(i)
        assert len(xmlids) == len(tree.xpath("//*[@id]"))

    def test_parser_subclass_2(
        self,
        tmp_path: Path,
        xml2_bytes_with_dtd: bytes,
    ) -> None:
        tmp_file = tmp_path / "sample.xml"
        tmp_file.write_bytes(xml2_bytes_with_dtd)
        parser = XHTMLParser(dtd_validation=True, load_dtd=True)
        tree, xmlids = parseid(tmp_file, parser=parser)
        reveal_type(tree)
        reveal_type(xmlids)
        for i in xmlids.items():
            reveal_type(i)
        assert len(xmlids) == len(tree.xpath("//*[@id]"))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_parser_arg_bad_1(
        self,
        xml2_filepath: Path,
        thing: Any,
    ) -> None:
        with pytest.raises(TypeError, match=r"Cannot convert .+ to .+\._BaseParser"):
            _ = parseid(xml2_filepath, parser=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_parser_arg_bad_2(
        self,
        xml2_filepath: Path,
        iterable_of: Any,
    ) -> None:
        with pytest.raises(TypeError, match=r"Cannot convert .+ to .+\._BaseParser"):
            _ = parseid(xml2_filepath, parser=iterable_of(XMLParser()))

    def test_baseurl_arg_ok(self, xml2_filepath: Path) -> None:
        url = b"http://example.com"
        for base_url in (url.decode(), url):
            tree, xmlids = parseid(xml2_filepath, base_url=base_url)
            reveal_type(tree)
            reveal_type(xmlids)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, NoneType))
    @pytest.mark.slow
    def test_baseurl_arg_bad_1(self, xml2_filepath: Path, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with raise_invalid_filename_type:
            _ = parseid(xml2_filepath, base_url=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_baseurl_arg_bad_2(self, xml2_filepath: Path, iterable_of: Any) -> None:
        with raise_invalid_filename_type:
            _ = parseid(xml2_filepath, base_url=iterable_of("http://example.com"))


class TestIddict:
    def test_basic(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser
    ) -> None:
        root, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        reveal_type(xmlids)
        assert len(xmlids) == len(root.xpath("//*[@id]"))
        assert "cd-001" in xmlids
        for k in xmlids:
            reveal_type(k)
            reveal_type(xmlids[k])

    @empty_signature_tester(
        _IDDict.keys,
        _IDDict.values,
        _IDDict.items,
        _IDDict.iterkeys,
        _IDDict.itervalues,
        _IDDict.iteritems,
    )
    def test_keyval_methods(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser
    ) -> None:
        _, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        keys = xmlids.keys()
        values = xmlids.values()
        items = xmlids.items()
        assert keys == list(xmlids.iterkeys())
        assert values == list(xmlids.itervalues())
        assert items == list(xmlids.iteritems())

    @signature_tester(_IDDict.get, (
        ("id_name", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_get_method_ok(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser
    ) -> None:
        _, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        result = reveal_type(xmlids.get("b-001"))
        for k in (b"b-001", bytearray(b"b-001")):
            assert result == xmlids.get(k) == xmlids[k]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_get_method_bad_1(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser, thing: Any
    ) -> None:
        _, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        with raise_invalid_utf8_type:
            _ = xmlids.get(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_get_method_bad_2(
        self,
        xml2_bytes_with_dtd: bytes,
        dtd_enabled_parser: XMLParser,
        iterable_of: Any,
    ) -> None:
        _, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        with raise_invalid_utf8_type:
            _ = xmlids.get(iterable_of("b-001"))

    @signature_tester(_IDDict.has_key, (
        ("id_name", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_has_key_method_ok(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser
    ) -> None:
        _, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        for k in ("b-001", b"b-001", bytearray(b"b-001")):
            assert reveal_type(xmlids.has_key(k))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_has_key_method_bad_1(
        self, xml2_bytes_with_dtd: bytes, dtd_enabled_parser: XMLParser, thing: Any
    ) -> None:
        _, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        with raise_invalid_utf8_type:
            _ = xmlids.has_key(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_has_key_method_bad_2(
        self,
        xml2_bytes_with_dtd: bytes,
        dtd_enabled_parser: XMLParser,
        iterable_of: Any,
    ) -> None:
        _, xmlids = XMLDTDID(xml2_bytes_with_dtd, parser=dtd_enabled_parser)
        with raise_invalid_utf8_type:
            _ = xmlids.has_key(iterable_of("b-001"))
