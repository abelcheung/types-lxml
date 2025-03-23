from __future__ import annotations

import copy
import sys
from collections.abc import Callable, Iterable
from inspect import Parameter
from pathlib import Path
from types import NoneType
from typing import Any

import pytest
from hypothesis import HealthCheck, given, settings
from lxml.etree import (
    DTD,
    LXML_VERSION,
    DocumentInvalid,
    DTDParseError,
    _Element,
    _ElementTree,
    _ListErrorLog as _ListErrorLog,
)

from ._testutils import (
    empty_signature_tester,
    signature_tester,
    strategy as _st,
)
from ._testutils.errors import (
    raise_attr_not_writable,
    raise_invalid_lxml_type,
    raise_invalid_utf8_type,
    raise_wrong_pos_arg_count,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestProperties:
    def test_properties(self, dtd: DTD) -> None:
        reveal_type(dtd.external_id)
        reveal_type(dtd.name)
        reveal_type(dtd.system_url)
        for prop in ("external_id", "name", "system_url"):
            with raise_attr_not_writable:
                setattr(dtd, prop, getattr(dtd, prop))
            with raise_attr_not_writable:
                delattr(dtd, prop)

    def test_errorlog(self, dtd: DTD, xml2_root: _Element) -> None:
        reveal_type(dtd.error_log)
        with raise_attr_not_writable:
            dtd.error_log = dtd.error_log  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with raise_attr_not_writable:
            del dtd.error_log  # pyright: ignore[reportAttributeAccessIssue]
        new_root = copy.deepcopy(xml2_root)
        new_root.tag = "bad"
        dtd(new_root)
        assert len(dtd.error_log) > 0


class TestDtdInput:
    # Generic Cython signature
    @pytest.mark.parametrize(
        ("args", "kw"),
        [
            ((), {}),
            ((None,), {}),
            ((None, None), {}),
            ((None,), {"external_id": None}),
            ((), {"external_id": None}),
        ],
    )
    def test_none_input_arg(self, args: Any, kw: Any) -> None:
        if len(args) < 2:
            raise_cm = pytest.raises(
                DTDParseError, match=r"either filename or external ID required"
            )
        else:
            raise_cm = raise_wrong_pos_arg_count
        with raise_cm:
            _ = DTD(*args, **kw)

    def test_file_arg_ok(
        self,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
        dtd_path: Path,
    ) -> None:
        for input in generate_input_file_arguments(dtd_path):
            dtd = DTD(file=input)
            reveal_type(dtd)
            del dtd

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_file_arg_bad(
        self,
        dtd_path: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
        iterable_of: Any,
    ) -> None:
        for input in generate_input_file_arguments(dtd_path):
            with pytest.raises(
                DTDParseError,
                match=r"file must be a filename, file-like or path-like object",
            ):
                _ = DTD(file=iterable_of(input))

    # Testing external_id properly requires setup of
    # DTD catalog in test environment, so we stop at
    # DTDParseError and call it a day.

    def test_external_id_arg_ok(self) -> None:
        input: list[Any] = [b"test", bytearray(b"test")]
        if LXML_VERSION >= (5, 3, 1):
            input.append("test")
        for i in input:
            with pytest.raises(DTDParseError, match=r"error parsing DTD"):
                _ = DTD(external_id=i)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray, NoneType))
    @pytest.mark.slow
    def test_external_id_arg_bad_1(self, thing: Any) -> None:
        if LXML_VERSION >= (5, 3, 1):
            raise_cm = raise_invalid_utf8_type
        else:
            raise_cm = pytest.raises(TypeError, match=r"expected bytes, .+ found")
        with raise_cm:
            _ = DTD(external_id=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_external_id_arg_bad_2(self, iterable_of: Any) -> None:
        if LXML_VERSION >= (5, 3, 1):
            raise_cm = raise_invalid_utf8_type
        else:
            raise_cm = pytest.raises(TypeError, match=r"expected bytes, .+ found")
        with raise_cm:
            _ = DTD(external_id=iterable_of("test"))


class TestDtdValidate:
    @signature_tester(
        DTD.validate,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_call_arg_ok(
        self,
        dtd: DTD,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        reveal_type(dtd.validate(xml2_root))
        reveal_type(dtd.validate(xml2_tree))
        reveal_type(dtd(xml2_root))
        reveal_type(dtd(xml2_tree))

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        reveal_type(dtd(faulty_root))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_call_arg_bad_1(self, dtd: DTD, thing: Any) -> None:
        with raise_invalid_lxml_type:
            _ = dtd.validate(thing)
        with raise_invalid_lxml_type:
            _ = dtd(thing)

    @pytest.mark.parametrize(["funcname"], (["validate"], ["__call__"]))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_arg_bad_2(
        self,
        dtd: DTD,
        iterable_of: Any,
        funcname: str,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        func = getattr(dtd, funcname)
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_root))
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_tree))

    @signature_tester(
        DTD.assert_,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    @signature_tester(
        DTD.assertValid,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_assert_arg_ok(
        self,
        dtd: DTD,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        assert dtd.assertValid(xml2_root) is None
        assert dtd.assertValid(xml2_tree) is None
        assert dtd.assert_(xml2_root) is None
        assert dtd.assert_(xml2_tree) is None

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        with pytest.raises(DocumentInvalid):
            dtd.assertValid(faulty_root)

        with pytest.raises(AssertionError):
            dtd.assert_(faulty_root)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_assert_arg_bad_1(self, dtd: DTD, thing: Any) -> None:
        with raise_invalid_lxml_type:
            _ = dtd.assertValid(thing)
        with raise_invalid_lxml_type:
            _ = dtd.assert_(thing)

    @pytest.mark.parametrize(["funcname"], (["assertValid"], ["assert_"]))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_assert_arg_bad_2(
        self,
        dtd: DTD,
        iterable_of: Any,
        funcname: str,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        func = getattr(dtd, funcname)
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_root))
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_tree))


class TestDtdMethods:
    @empty_signature_tester(
        DTD.iterelements,
        DTD.elements,
        DTD.iterentities,
        DTD.entities,
    )
    def test_signature(self) -> None:
        pass

    # reveal_type() unusable for some properties, because the private classes
    # are not exposed by lxml.etree, thus not resolvable.
    def test_elements(self, dtd: DTD) -> None:
        itr = dtd.iterelements()
        elems = dtd.elements()
        assert len(elems) == len(list(itr))
        for el in elems:
            reveal_type(el.name)
            reveal_type(el.prefix)
            reveal_type(el.type)
            assert el.content is not None
            reveal_type(el.content.name)
            reveal_type(el.content.type)
            reveal_type(el.content.occur)
            assert el.content.left is None or type(el.content.left) is type(el.content)
            assert el.content.right is None or type(el.content.right) is type(
                el.content
            )
            attrs = el.attributes()
            assert len(attrs) == len(list(el.iterattributes()))
            for a in attrs:
                reveal_type(a.name)
                reveal_type(a.elemname)
                reveal_type(a.prefix)
                reveal_type(a.type)
                reveal_type(a.default)
                reveal_type(a.default_value)
                vals = reveal_type(a.values())
                assert len(vals) == len(list(a.itervalues()))

        el = elems[0]
        for attr in ("name", "prefix", "type", "content"):
            with raise_attr_not_writable:
                setattr(el, attr, getattr(el, attr))
            with raise_attr_not_writable:
                delattr(el, attr)
        c = el.content
        for attr in ("name", "type", "occur"):
            with raise_attr_not_writable:
                setattr(c, attr, getattr(c, attr))
            with raise_attr_not_writable:
                delattr(c, attr)

    def test_entities(self, dtd: DTD) -> None:
        itr = dtd.iterentities()
        ents = dtd.entities()
        assert len(ents) == len(list(itr))
        for ent in ents:
            reveal_type(ent.name)
            reveal_type(ent.orig)
            reveal_type(ent.content)
            reveal_type(ent.system_url)

        ent = ents[0]
        for attr in ("name", "orig", "content", "system_url"):
            with raise_attr_not_writable:
                setattr(ent, attr, getattr(ent, attr))
            with raise_attr_not_writable:
                delattr(ent, attr)
