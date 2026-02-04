from __future__ import annotations

import ipaddress
import sys
from collections.abc import (
    Callable,
    Iterable,
    Iterator,
)
from copy import deepcopy
from random import randrange
from types import NoneType
from typing import (
    Any,
    cast,
)

import pytest
from hypothesis import (
    HealthCheck,
    assume,
    given,
    settings,
)
from lxml import etree
from lxml.etree import (
    Element,
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
from .._testutils.common import (
    can_practically_iter,
    hashable_elem_if_is_set,
    tag_name_types,
)
from .._testutils.errors import (
    raise_attr_not_writable,
    raise_cannot_convert,
    raise_invalid_filename_type,
    raise_invalid_utf8_type,
    raise_non_integer,
    raise_non_iterable,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestBasicBehavior:
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(int, slice))
    @pytest.mark.slow
    def test_sequence_read_bad(self, disposable_element: _Element, thing: Any) -> None:
        with raise_non_integer:
            _ = cast(Any, disposable_element[thing])

    def test_sequence_read_ok(self, xml2_root: _Element) -> None:
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

        for sub in elem:
            reveal_type(sub)

        subelem = elem[3]
        reveal_type(subelem in elem)
        o = object()
        reveal_type(o in elem)

        with raise_non_integer:
            _ = elem[cast(int, "0")]

        del elem, subelem

    # mypy and ty don't support magic method and always treat
    # reversed(...) as `reversed` object
    @pytest.mark.notypechecker("mypy", "ty")
    def test_reversed_seq_read_1(self, xml2_root: _Element) -> None:
        rev = reversed(xml2_root)
        reveal_type(rev)
        reveal_type(list(rev))

    @pytest.mark.onlytypechecker("mypy", "ty")
    def test_reversed_seq_read_2(self, xml2_root: _Element) -> None:
        rev = xml2_root.__reversed__()
        reveal_type(rev)
        reveal_type(list(rev))

    def test_sequence_modify_ok(self, xml2_root: _Element) -> None:
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

        length = len(elem)
        elem[1] = comment
        assert len(elem) == length
        elem[length - 1 :] = (entity, pi)
        assert len(elem) == length + 1
        length = length + 1
        # Actually permitted, just that elements are added in random order
        elem[length:] = {div, comment2}
        assert len(elem) == length + 2

        with pytest.raises(ValueError, match="cannot assign None"):
            elem[0] = cast(Any, None)
        with pytest.raises(ValueError, match="cannot assign None"):
            elem[:] = cast(Any, None)

        # test broken behavior: elem[slice] = single_elem
        # It returns successfully, just that elements are
        # silently discarded without adding new ones
        elem[:] = comment
        assert len(elem) == 0

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_sequence_modify_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        if thing is None:
            with pytest.raises(ValueError, match="cannot assign None"):
                disposable_element[0] = cast(Any, thing)  # pyright: ignore[reportUnnecessaryCast]
        else:
            with raise_cannot_convert:
                disposable_element[0] = thing

    # some iterables may cause indefinite hang when lxml diligently try inserting
    # items into element tree (e.g. huge ranges)
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(
        thing=_st.all_instances_except_of_type(
            _Element,
            Iterator,
            range,
            ipaddress.IPv4Network,
            ipaddress.IPv6Network,
        ).filter(lambda x: x is not NotImplemented and bool(x))
    )
    @pytest.mark.slow
    def test_sequence_modify_bad_2(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        if isinstance(thing, (Iterable)) or can_practically_iter(thing):
            with raise_cannot_convert:
                disposable_element[:] = cast(Any, thing)
        else:
            with raise_non_iterable:
                disposable_element[:] = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_sequence_modify_bad_3(
        self,
        disposable_element: _Element,
        iterable_of: Callable[[_Element], Iterable[_Element]],
    ) -> None:
        el = Element("foo")
        with raise_cannot_convert:
            disposable_element[0] = cast(Any, iterable_of(el))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(
        thing=_st.all_instances_except_of_type(_Element).filter(
            lambda x: x is not NotImplemented and bool(x)
        ),
        iterable_of=_st.fixed_item_iterables(),
    )
    @pytest.mark.slow
    def test_sequence_modify_bad_4(
        self,
        disposable_element: _Element,
        thing: Any,
        iterable_of: Callable[[Any], Iterable[Any]],
    ) -> None:
        assume(hashable_elem_if_is_set(iterable_of, thing))
        with raise_cannot_convert:
            disposable_element[:] = iterable_of(thing)


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
            "sourceline",
            "base",
            "tag",
            "text",
            "tail",
        ):
            with pytest.raises(NotImplementedError, match=r"__del__"):
                delattr(xml2_root, attr)

    def test_ro_properties(self, xml2_root: _Element) -> None:
        # Not performing test for .sourceline ! We pretend it is not
        # changeable in stub, but actually it is read-write
        for attr in ("attrib", "prefix", "nsmap"):
            with raise_attr_not_writable:
                setattr(xml2_root, attr, getattr(xml2_root, attr))
            with raise_attr_not_writable:
                delattr(xml2_root, attr)

    def test_base_rw_ok(self, disposable_element: _Element) -> None:
        for v in (
            "http://dummy.site/",
            None,
            b"http://dummy.site/",
        ):
            disposable_element.base = v
            # None is transformed to empty string, so no assert test
            reveal_type(disposable_element.base)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, NoneType))
    @pytest.mark.slow
    def test_base_rw_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with raise_invalid_filename_type:
            disposable_element.base = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_base_rw_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_invalid_filename_type:
            disposable_element.base = iterable_of("foo")

    def test_tag_rw_ok(self, disposable_element: _Element) -> None:
        for v in (
            "foo",
            b"foo",
            bytearray(b"foo"),
            QName("foo", "bar"),
        ):
            disposable_element.tag = v
            reveal_type(disposable_element.tag)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(value=_st.all_instances_except_of_type(*tag_name_types.allow))
    @pytest.mark.slow
    def test_tag_rw_bad_1(self, disposable_element: _Element, value: Any) -> None:
        with raise_invalid_utf8_type:
            disposable_element.tag = value

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_tag_rw_bad_2(self, disposable_element: _Element, iterable_of: Any) -> None:
        with raise_invalid_utf8_type:
            disposable_element.tag = iterable_of("foo")

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

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(
        str, bytes, bytearray, etree.CDATA, QName, NoneType
    ))  # fmt: skip
    @pytest.mark.slow
    def test_text_rw_bad(self, disposable_element: _Element, thing: Any) -> None:
        with raise_invalid_utf8_type:
            disposable_element.text = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_text_rw_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_invalid_utf8_type:
            disposable_element.text = iterable_of("foo")

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

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(
        str, bytes, bytearray, etree.CDATA, NoneType
    ))  # fmt: skip
    @pytest.mark.slow
    def test_tail_rw_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with raise_invalid_utf8_type:
            disposable_element.tail = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_tail_rw_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_invalid_utf8_type:
            disposable_element.tail = iterable_of("foo")
