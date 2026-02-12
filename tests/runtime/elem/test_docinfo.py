from __future__ import annotations

import pathlib
import sys
from types import NoneType
from typing import (
    Any,
    cast,
    no_type_check,
)

import pook  # pyright: ignore[reportMissingTypeStubs]
import pytest
from hypothesis import given, settings
from lxml.etree import (
    DTD as DTD,
    DocInfo as DocInfo,
    _Element,
    fromstring,
    parse,
)

from .._testutils import strategy as _st
from .._testutils.errors import (
    raise_attr_not_writable,
    raise_invalid_filename_type,
    raise_invalid_utf8_type,
    raise_unexpected_type,
)
from ..conftest import http_pool

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type

if sys.version_info >= (3, 12):
    from collections.abc import Buffer
else:
    from typing_extensions import Buffer


class TestSource:
    def test_from_local_str(self, xml2_bytes_with_dtd: bytes) -> None:
        root = fromstring(xml2_bytes_with_dtd)
        docinfo = root.getroottree().docinfo
        reveal_type(docinfo)
        reveal_type(docinfo.root_name)
        reveal_type(docinfo.xml_version)
        reveal_type(docinfo.encoding)
        reveal_type(docinfo.standalone)
        reveal_type(docinfo.doctype)
        reveal_type(docinfo.internalDTD)
        reveal_type(docinfo.externalDTD)
        reveal_type(docinfo.public_id)
        reveal_type(docinfo.system_url)
        reveal_type(docinfo.URL)

    def test_from_local_file(self, xml2_filepath: pathlib.Path) -> None:
        tree = parse(source=xml2_filepath)
        docinfo = tree.docinfo
        reveal_type(docinfo)
        reveal_type(docinfo.root_name)
        reveal_type(docinfo.xml_version)
        reveal_type(docinfo.encoding)
        reveal_type(docinfo.standalone)
        reveal_type(docinfo.doctype)
        reveal_type(docinfo.internalDTD)
        reveal_type(docinfo.externalDTD)
        reveal_type(docinfo.public_id)
        reveal_type(docinfo.system_url)
        reveal_type(docinfo.URL)

    def test_from_remote_url(self, xml2_bytes_with_dtd: bytes) -> None:
        with pook.get(  # pyright: ignore[reportUnknownMemberType]
            "https://example.com/test.xml",
            reply=200,
            response_type="xml",
            response_body=xml2_bytes_with_dtd,
        ):
            http_response = http_pool.request("GET", "https://example.com/test.xml")
            tree = parse(source=http_response)
            docinfo = tree.docinfo
            reveal_type(docinfo)
            reveal_type(docinfo.root_name)
            reveal_type(docinfo.xml_version)
            reveal_type(docinfo.encoding)
            reveal_type(docinfo.standalone)
            reveal_type(docinfo.doctype)
            reveal_type(docinfo.internalDTD)
            reveal_type(docinfo.externalDTD)
            reveal_type(docinfo.public_id)
            reveal_type(docinfo.system_url)
            reveal_type(docinfo.URL)


class TestProperties:
    @no_type_check
    def test_ro_properties(self, xml2_bytes_with_dtd: bytes) -> None:
        root = fromstring(xml2_bytes_with_dtd)
        docinfo = root.getroottree().docinfo

        with raise_attr_not_writable:
            docinfo.root_name = docinfo.root_name
        with raise_attr_not_writable:
            docinfo.xml_version = docinfo.xml_version
        with raise_attr_not_writable:
            docinfo.encoding = docinfo.encoding
        with raise_attr_not_writable:
            docinfo.standalone = docinfo.standalone
        with raise_attr_not_writable:
            docinfo.doctype = docinfo.doctype
        with raise_attr_not_writable:
            docinfo.internalDTD = docinfo.internalDTD
        with raise_attr_not_writable:
            docinfo.externalDTD = docinfo.externalDTD

    def test_rw_properties_ok(self, xml2_bytes_with_dtd: bytes) -> None:
        root = fromstring(xml2_bytes_with_dtd)
        docinfo = root.getroottree().docinfo

        old_public_id = docinfo.public_id or "PUBLIC_ID"
        docinfo.public_id = None
        docinfo.public_id = old_public_id
        reveal_type(docinfo.public_id)

        old_system_url = docinfo.system_url or "SYSTEM_URL"
        docinfo.system_url = None
        docinfo.system_url = old_system_url
        docinfo.system_url = old_system_url.encode()
        docinfo.system_url = bytearray(old_system_url.encode())
        reveal_type(docinfo.system_url)

        old_URL = docinfo.URL or "URL"
        docinfo.URL = None
        docinfo.URL = old_URL
        docinfo.URL = old_URL.encode()
        reveal_type(docinfo.URL)

    @settings(max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, NoneType))
    def test_rw_properties_bad_public_id(
        self,
        disposable_element: _Element,
        thing: Any,
    ) -> None:
        docinfo = disposable_element.getroottree().docinfo
        if isinstance(thing, (bytes, Buffer)):
            raise_cm = pytest.raises(
                TypeError, match=r"string pattern on a bytes-like object"
            )
        else:
            raise_cm = raise_unexpected_type
        with raise_cm:
            docinfo.public_id = cast(Any, thing)

    @settings(max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, Buffer, NoneType))
    def test_rw_properties_bad_system_url(
        self,
        disposable_element: _Element,
        thing: Any,
    ) -> None:
        docinfo = disposable_element.getroottree().docinfo
        with raise_invalid_utf8_type:
            docinfo.system_url = thing

    @settings(max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, NoneType))
    def test_rw_properties_bad_URL(
        self,
        disposable_element: _Element,
        thing: Any,
    ) -> None:
        docinfo = disposable_element.getroottree().docinfo
        with raise_invalid_filename_type:
            docinfo.URL = thing


class TestMethods:
    def test_clear(self, xml2_bytes_with_dtd: bytes) -> None:
        root = fromstring(xml2_bytes_with_dtd)
        docinfo = root.getroottree().docinfo
        reveal_type(docinfo.clear())
