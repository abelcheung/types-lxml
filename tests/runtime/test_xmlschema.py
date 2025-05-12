from __future__ import annotations

import copy
import io
import sys
from collections.abc import Callable, Iterable
from inspect import Parameter
from pathlib import Path
from types import NoneType
from typing import Any

import pytest
from hypothesis import HealthCheck, given, settings
from lxml.etree import (
    DocumentInvalid,
    XMLSchema,
    XMLSchemaParseError,
    _Element,
    _ElementTree,
)

from ._testutils import signature_tester, strategy as _st
from ._testutils.errors import raise_wrong_pos_arg_count

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type

exc_wrong_obj = pytest.raises(TypeError, match=r"Invalid input object:")


class TestXMLSchemaInput:
    # Generic Cython signature
    @pytest.mark.parametrize(
        ("args", "kw"),
        [
            ((), {}),
            ((None,), {}),
            ((None, None), {}),
            ((None,), {"file": None}),
            ((), {"file": None}),
        ],
    )
    def test_none_input_arg(self, args: Any, kw: Any) -> None:
        if len(args) < 2:
            raise_cm = pytest.raises(
                XMLSchemaParseError, match=r"No tree or file given"
            )
        else:
            raise_cm = raise_wrong_pos_arg_count
        with raise_cm:
            _ = XMLSchema(*args, **kw)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType, _Element, _ElementTree))
    @pytest.mark.slow
    def test_etree_arg_bad_1(self, thing: Any) -> None:
        with exc_wrong_obj:
            _ = XMLSchema(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_etree_arg_bad_2(self, xmlschema_root: _Element, iterable_of: Any) -> None:
        with exc_wrong_obj:
            _ = XMLSchema(iterable_of(xmlschema_root))

    def test_etree_arg_ok(self, xmlschema_root: _Element) -> None:
        schema = XMLSchema(xmlschema_root)
        reveal_type(schema)
        del schema

        schema = XMLSchema(etree=xmlschema_root.getroottree())
        reveal_type(schema)

    def test_file_arg_ok(
        self,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
        xmlschema_path: Path,
    ) -> None:
        # For StringIO, input content needs tweaking
        # (remove encoding declaration)
        def _tweak_sio_content(file: Path) -> io.StringIO:
            return io.StringIO(file.read_text().replace('encoding="UTF-8"', ""))

        for file in generate_input_file_arguments(
            xmlschema_path,
            exclude_type=(io.StringIO,),
            include=[_tweak_sio_content],
        ):
            schema = XMLSchema(file=file)
            reveal_type(schema)
            del schema

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterator_of=_st.fixed_item_iterables())
    def test_file_arg_bad(
        self,
        xmlschema_path: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
        iterator_of: Any,
    ) -> None:
        for input in generate_input_file_arguments(xmlschema_path):
            with pytest.raises(TypeError, match=r"cannot parse from"):
                _ = XMLSchema(file=iterator_of(input))

    # TODO test attribute_defaults argument


class TestXMLSchemaValidate:
    @signature_tester(
        XMLSchema.validate,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_call_arg_ok(
        self,
        xmlschema: XMLSchema,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        reveal_type(xmlschema.validate(xml2_root))
        reveal_type(xmlschema.validate(xml2_tree))
        reveal_type(xmlschema(xml2_root))
        reveal_type(xmlschema(xml2_tree))

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        reveal_type(xmlschema(faulty_root))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_call_arg_bad_1(self, xmlschema: XMLSchema, thing: Any) -> None:
        with exc_wrong_obj:
            _ = xmlschema.validate(thing)
        with exc_wrong_obj:
            _ = xmlschema(thing)

    @pytest.mark.parametrize(["funcname"], (["validate"], ["__call__"]))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_arg_bad_2(
        self,
        xmlschema: XMLSchema,
        iterable_of: Any,
        funcname: str,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        func = getattr(xmlschema, funcname)
        with exc_wrong_obj:
            _ = func(iterable_of(xml2_root))
        with exc_wrong_obj:
            _ = func(iterable_of(xml2_tree))

    @signature_tester(
        XMLSchema.assert_,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    @signature_tester(
        XMLSchema.assertValid,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_assert_arg_ok(
        self,
        xmlschema: XMLSchema,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        assert xmlschema.assertValid(xml2_root) is None
        assert xmlschema.assertValid(xml2_tree) is None
        assert xmlschema.assert_(xml2_root) is None
        assert xmlschema.assert_(xml2_tree) is None

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        with pytest.raises(DocumentInvalid):
            xmlschema.assertValid(faulty_root)

        with pytest.raises(AssertionError):
            xmlschema.assert_(faulty_root)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_assert_arg_bad_1(self, xmlschema: XMLSchema, thing: Any) -> None:
        with exc_wrong_obj:
            _ = xmlschema.assertValid(thing)
        with exc_wrong_obj:
            _ = xmlschema.assert_(thing)

    @pytest.mark.parametrize(["funcname"], (["assertValid"], ["assert_"]))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_assert_arg_bad_2(
        self,
        xmlschema: XMLSchema,
        iterable_of: Any,
        funcname: str,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        func = getattr(xmlschema, funcname)
        with exc_wrong_obj:
            _ = func(iterable_of(xml2_root))
        with exc_wrong_obj:
            _ = func(iterable_of(xml2_tree))
