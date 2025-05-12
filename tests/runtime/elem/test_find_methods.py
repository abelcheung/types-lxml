# The find*() methods of _Element are all derivations of
# iterfind(). So they almost have same arguments, and even
# the other test contents look very similar.


from __future__ import annotations

import sys
from collections.abc import Mapping
from inspect import Parameter
from types import (
    MappingProxyType,
    NoneType,
)
from typing import Any, cast

import pytest
from hypothesis import HealthCheck, assume, example, given, settings
from lxml.etree import (
    QName,
    _Attrib as _Attrib,
    _Comment as _Comment,
    _Element,
    _ElementTree as _ElementTree,
    _Entity as _Entity,
    _ProcessingInstruction as _ProcessingInstruction,
    iselement,
)

from .._testutils import signature_tester, strategy as _st
from .._testutils.errors import (
    raise_no_attribute,
    raise_non_iterable,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestIterfind:
    @signature_tester(_Element.iterfind, (
        ("path"      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("namespaces", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    def test_path_arg_ok(self, svg_root: _Element) -> None:
        tag = "desc"
        itr = reveal_type(svg_root.iterfind(tag))
        result = reveal_type(list(itr))
        del itr

        qname = QName(None, tag)
        itr = reveal_type(svg_root.iterfind(qname))
        assert result == list(itr)
        del itr

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, QName, bytes, bytearray))
    @example(thing=b"desc")
    @example(thing=bytearray(b"desc"))
    @pytest.mark.slow
    def test_path_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with pytest.raises(Exception):  # very diversed
            _ = disposable_element.iterfind(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_path_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with pytest.raises(TypeError):
            _ = disposable_element.iterfind(iterable_of("desc"))

    # Invalid entries in namespace mapping wouldn't be fatal; those with wrong
    # keys / values only silently fail to select useful elements. Therefore no
    # key/val type check is performed, only the type of namespaces argument
    # itself is checked as a whole. Same applies to all find*() methods below.

    def test_namespaces_arg_ok(self, svg_root: _Element) -> None:
        url = "http://example.org/myapp"
        prefix = "m"
        nsdict = {prefix: url}
        tag = "piechart"
        qname = QName(url, tag)

        itr = reveal_type(svg_root.iterfind(f"{{{url}}}{tag}"))
        reveal_type(itr)
        result = reveal_type(list(itr))
        del itr

        itr = svg_root.iterfind(qname, namespaces=None)
        assert result == list(itr)
        del itr

        itr = svg_root.iterfind(f"{prefix}:{tag}", namespaces=nsdict)
        assert result == list(itr)
        del itr

        itr = svg_root.iterfind(f"{prefix}:{tag}", namespaces=MappingProxyType(nsdict))
        assert result == list(itr)
        del itr

    # range objects can cause indefinite hang
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(Mapping, NoneType, range))
    @pytest.mark.slow
    def test_namespaces_arg_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        assume(thing is NotImplemented or bool(thing))
        if not hasattr(thing, "__iter__"):
            raise_cm = raise_non_iterable
        else:
            raise_cm = pytest.raises((TypeError, AttributeError))  # type: ignore[arg-type]
        with raise_cm:
            _ = disposable_element.iterfind("foo", namespaces=thing)

    # prove ns prefix/url tuple pair won't do
    def test_namespaces_arg_bad_2(self, svg_root: _Element) -> None:
        with raise_no_attribute:
            _ = svg_root.iterfind(
                "m:piechart", namespaces=cast(Any, [("m", "http://example.org/myapp")])
            )


class TestFind:
    @signature_tester(_Element.find, (
        ("path"      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("namespaces", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    def test_path_arg_ok(self, svg_root: _Element) -> None:
        tag = "desc"
        result = reveal_type(svg_root.find(tag))
        qname = QName(None, tag)
        assert result == svg_root.find(qname)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, QName, bytes, bytearray))
    @example(thing=b"desc")
    @example(thing=bytearray(b"desc"))
    @pytest.mark.slow
    def test_path_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with pytest.raises(Exception):  # very diversed
            _ = disposable_element.find(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_path_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with pytest.raises(TypeError):
            _ = disposable_element.find(iterable_of("desc"))

    def test_namespaces_arg_ok(self, svg_root: _Element) -> None:
        url = "http://example.org/myapp"
        prefix = "m"
        nsdict = {prefix: url}
        tag = "piechart"
        qname = QName(url, tag)

        result = reveal_type(svg_root.find(f"{{{url}}}{tag}"))
        assert result == svg_root.find(qname, namespaces=None)
        assert result == svg_root.find(f"{prefix}:{tag}", namespaces=nsdict)
        assert result == svg_root.find(
            f"{prefix}:{tag}", namespaces=MappingProxyType(nsdict)
        )

    # range objects can cause indefinite hang
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(Mapping, NoneType, range))
    @pytest.mark.slow
    def test_namespaces_arg_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        assume(thing is NotImplemented or bool(thing))
        if not hasattr(thing, "__iter__"):
            raise_cm = raise_non_iterable
        else:
            raise_cm = pytest.raises((TypeError, AttributeError))  # type: ignore[arg-type]
        with raise_cm:
            _ = disposable_element.find("foo", namespaces=thing)

    # prove ns prefix/url tuple pair won't do
    def test_namespaces_arg_bad_2(self, svg_root: _Element) -> None:
        with raise_no_attribute:
            _ = svg_root.find(
                "m:piechart", namespaces=cast(Any, [("m", "http://example.org/myapp")])
            )


class TestFindall:
    @signature_tester(_Element.findall, (
        ("path"      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("namespaces", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    def test_path_arg_ok(self, svg_root: _Element) -> None:
        tag = "desc"
        result = reveal_type(svg_root.findall(tag))
        qname = QName(None, tag)
        assert result == svg_root.findall(qname)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, QName, bytes, bytearray))
    @example(thing=b"desc")
    @example(thing=bytearray(b"desc"))
    @pytest.mark.slow
    def test_path_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with pytest.raises(Exception):  # very diversed
            _ = disposable_element.findall(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_path_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with pytest.raises(TypeError):
            _ = disposable_element.findall(iterable_of("desc"))

    def test_namespaces_arg_ok(self, svg_root: _Element) -> None:
        url = "http://example.org/myapp"
        prefix = "m"
        nsdict = {prefix: url}
        tag = "piechart"
        qname = QName(url, tag)

        result = reveal_type(svg_root.findall(f"{{{url}}}{tag}"))
        assert result == svg_root.findall(qname, namespaces=None)
        assert result == svg_root.findall(f"{prefix}:{tag}", namespaces=nsdict)
        assert result == svg_root.findall(
            f"{prefix}:{tag}", namespaces=MappingProxyType(nsdict)
        )

    # range objects can cause indefinite hang
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(Mapping, NoneType, range))
    @pytest.mark.slow
    def test_namespaces_arg_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        assume(thing is NotImplemented or bool(thing))
        if not hasattr(thing, "__iter__"):
            raise_cm = raise_non_iterable
        else:
            raise_cm = pytest.raises((TypeError, AttributeError))  # type: ignore[arg-type]
        with raise_cm:
            _ = disposable_element.findall("foo", namespaces=thing)

    # prove ns prefix/url tuple pair won't do
    def test_namespaces_arg_bad_2(self, svg_root: _Element) -> None:
        with raise_no_attribute:
            _ = svg_root.findall(
                "m:piechart", namespaces=cast(Any, [("m", "http://example.org/myapp")])
            )


class TestFindtext:
    @signature_tester(_Element.findtext, (
        ("path"      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default"   , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("namespaces", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    def test_path_arg_ok(self, svg_root: _Element) -> None:
        tag = "desc"
        result = reveal_type(svg_root.findtext(tag))
        assert result and result.startswith("This chart")
        qname = QName(None, tag)
        assert result == svg_root.findtext(qname)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, QName, bytes, bytearray))
    @example(thing=b"desc")
    @example(thing=bytearray(b"desc"))
    @pytest.mark.slow
    def test_path_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        with pytest.raises(Exception):  # very diversed
            _ = disposable_element.findtext(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_path_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with pytest.raises(TypeError):
            _ = disposable_element.findtext(iterable_of("desc"))

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=5
    )
    @given(thing=_st.all_instances_except_of_type(str, NoneType))
    def test_path_hit(self, svg_root: _Element, thing: Any) -> None:
        result = svg_root.findtext("desc", default=thing)
        assert type(result) is not type(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=5
    )
    @given(thing=_st.all_instances_except_of_type(str, NoneType))
    def test_path_miss(self, svg_root: _Element, thing: Any) -> None:
        result = svg_root.findtext("foo", default=thing)
        assert type(result) is type(thing)

    def test_namespaces_arg_ok(self, svg_root: _Element) -> None:
        url = "http://example.org/myfoo"
        prefix = "m"
        nsdict = {prefix: url}
        tag = "title"
        qname = QName(url, tag)

        # get the parent node first
        xpath = f'//{prefix}:{tag}[namespace-uri()="{url}"]/..'
        parent = svg_root.xpath(xpath, namespaces=nsdict)[0]
        assert iselement(parent)
        result = reveal_type(parent.findtext(f"{{{url}}}{tag}"))
        assert result and result.endswith("report")
        assert result == parent.findtext(qname, namespaces=None)
        assert result == parent.findtext(f"{prefix}:{tag}", namespaces=nsdict)
        assert result == parent.findtext(
            f"{prefix}:{tag}", namespaces=MappingProxyType(nsdict)
        )

    # range objects can cause indefinite hang
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(Mapping, NoneType, range))
    @pytest.mark.slow
    def test_namespaces_arg_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        assume(thing is NotImplemented or bool(thing))
        if not hasattr(thing, "__iter__"):
            raise_cm = raise_non_iterable
        else:
            raise_cm = pytest.raises((TypeError, AttributeError))  # type: ignore[arg-type]
        with raise_cm:
            _ = disposable_element.findtext("foo", namespaces=thing)

    # prove ns prefix/url tuple pair won't do
    def test_namespaces_arg_bad_2(self, svg_root: _Element) -> None:
        with raise_no_attribute:
            _ = svg_root.findtext(
                "m:title", namespaces=cast(Any, [("m", "http://example.org/myfoo")])
            )
