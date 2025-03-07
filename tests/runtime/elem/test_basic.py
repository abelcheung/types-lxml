from __future__ import annotations

import sys
from copy import deepcopy
from random import randrange
from types import NoneType
from typing import Any, cast

import pytest
from hypothesis import (
    HealthCheck,
    given,
    settings,
)
from lxml import etree
from lxml.etree import (
    QName,
    _Attrib as _Attrib,
    _Comment as _Comment,
    _Element,
    _ElementTree as _ElementTree,
    _Entity as _Entity,
    _ProcessingInstruction as _ProcessingInstruction,
)
from lxml.html import Element as h_Element

from .._testutils import strategy as _st

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type

# See mypy.ini in testsuite for explanation
TC_HONORS_REVERSED = True


class TestBasicBehavior:
    def test_sequence_read(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)

        reveal_type(len(elem))
        length = len(elem)
        reveal_type(elem[randrange(length)])
        reveal_type(elem[: 2])  # fmt: skip  # ast: why the space???

        itr = iter(elem)
        reveal_type(itr)
        item = next(itr)
        reveal_type(item)
        assert elem.index(item) == 0
        del itr, item

        if TC_HONORS_REVERSED:
            rev = reversed(elem)
        else:
            rev = elem.__reversed__()
        reveal_type(rev)
        item = next(rev)
        reveal_type(item)
        assert elem.index(item) == length - 1
        del rev, item

        for sub in elem:
            reveal_type(sub)

        subelem = elem[3]
        reveal_type(subelem in elem)
        o = object()
        reveal_type(o in elem)

        with pytest.raises(TypeError, match="cannot be interpreted as an integer"):
            _ = elem[cast(int, "0")]

        del elem, subelem

    def test_sequence_modify(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)

        subelem = elem[3]
        del elem[0]
        assert elem.index(subelem) == 2
        del elem[0:2]
        assert elem.index(subelem) == 0

        comment = etree.Comment("comment")
        comment2 = etree.Comment("foo")
        entity = etree.Entity("foo")
        pi = etree.ProcessingInstruction("target", "text")
        div = h_Element("div")

        elem[1] = comment
        assert len(elem) == 2
        elem[2:4] = (entity, pi)
        assert len(elem) == 4
        # Actually permitted, just that elements are added in random order
        elem[4:] = {div, comment2}
        assert len(elem) == 6

        with pytest.raises(ValueError, match="cannot assign None"):
            elem[0] = cast(Any, None)
        with pytest.raises(ValueError, match="cannot assign None"):
            elem[:] = cast(Any, None)

        # test broken behavior: elem[slice] = single_elem
        # It returns successfully, just that elements are
        # silently discarded without adding new ones
        elem[:] = comment
        assert len(elem) == 0

    @settings(suppress_health_check=[HealthCheck.too_slow])
    @given(obj=_st.all_instances_except_of_type(NoneType, _Element))
    @pytest.mark.slow
    def test_insert_bad_elem(self, disposable_element: _Element, obj: Any) -> None:
        with pytest.raises(
            TypeError, match=r"Cannot convert \w+(\.\w+)* to .+\._Element"
        ):
            disposable_element[0] = obj


class TestProperties:
    def test_basic_stuff(self, xml2_root: _Element) -> None:
        for subelem in xml2_root:
            if type(subelem) is not _Element:
                continue
            reveal_type(subelem.attrib)
            reveal_type(subelem.prefix)
            reveal_type(subelem.nsmap)
            reveal_type(subelem.sourceline)
            reveal_type(subelem.base)
            reveal_type(subelem.tag)
            reveal_type(subelem.text)
            reveal_type(subelem.tail)

        for attr in (
            "attrib",
            "prefix",
            "nsmap",
            "sourceline",
            "base",
            "tag",
            "text",
            "tail",
        ):
            with pytest.raises((AttributeError, NotImplementedError)):
                delattr(xml2_root, attr)

    def test_ro_properties(self, xml2_root: _Element) -> None:
        with pytest.raises(AttributeError, match="objects is not writable"):
            xml2_root.attrib = xml2_root.attrib  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]

        with pytest.raises(AttributeError, match="objects is not writable"):
            xml2_root.prefix = xml2_root.prefix  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]

        with pytest.raises(AttributeError, match="objects is not writable"):
            xml2_root.nsmap = xml2_root.nsmap  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]

        # Not performing test for .sourceline ! We pretend it is not
        # changeable in stub, but actually it is read-write

    def test_base_rw_ok(self, disposable_element: _Element) -> None:
        for v in (
            "http://dummy.site/",
            None,
            b"http://dummy.site/",
        ):
            disposable_element.base = v
            # None is transformed to empty string, so no assert test
            reveal_type(disposable_element.base)

    @given(value=_st.all_instances_except_of_type(str, bytes, NoneType))
    def test_base_rw_bad(self, disposable_element: _Element, value: Any) -> None:
        with pytest.raises(TypeError, match="must be string or unicode"):
            disposable_element.base = value

    def test_tag_rw_ok(self, disposable_element: _Element) -> None:
        for v in (
            "foo",
            b"foo",
            bytearray(b"foo"),
            QName("foo", "bar"),
        ):
            disposable_element.tag = v
            reveal_type(disposable_element.tag)

    @given(value=_st.all_instances_except_of_type(str, bytes, bytearray, QName))
    def test_tag_rw_bad(self, disposable_element: _Element, value: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            disposable_element.tag = value

    def test_text_rw_ok(self, disposable_element: _Element) -> None:
        for v in (
            "foo",
            b"foo",
            bytearray(b"foo"),
            etree.CDATA("foo"),
            QName("foo", "bar"),
            None,
        ):
            disposable_element.text = v
            reveal_type(disposable_element.text)

    @given(value=_st.all_instances_except_of_type(
        str, bytes, bytearray, etree.CDATA, QName, NoneType
    ))  # fmt: skip
    def test_text_rw_bad(self, disposable_element: _Element, value: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            disposable_element.text = value

    def test_tail_rw_ok(self, disposable_element: _Element) -> None:
        for v in (
            "foo",
            b"foo",
            bytearray(b"foo"),
            etree.CDATA("foo"),
            None,
        ):
            disposable_element.tail = v
            reveal_type(disposable_element.tail)

    @given(value=_st.all_instances_except_of_type(
        str, bytes, bytearray, etree.CDATA, NoneType
    ))  # fmt: skip
    def test_tail_rw_bad(self, disposable_element: _Element, value: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            disposable_element.tail = value
