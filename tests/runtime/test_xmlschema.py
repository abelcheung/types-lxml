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

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


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
            exc, match = XMLSchemaParseError, "No tree or file given"
        else:
            exc, match = TypeError, r"at most 1 positional argument"
        with pytest.raises(exc, match=match):
            _ = XMLSchema(*args, **kw)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_etree_arg_bad_1(self, thing: Any) -> None:
        with pytest.raises((XMLSchemaParseError, ValueError, TypeError)):
            _ = XMLSchema(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_etree_arg_bad_2(self, xmlschema_root: _Element, iterable_of: Any) -> None:
        with pytest.raises(TypeError, match="Invalid input object"):
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
        for file in generate_input_file_arguments(
            xmlschema_path, exclude_type=(io.StringIO,)
        ):
            schema = XMLSchema(file=file)
            reveal_type(schema)
            del schema

    # TODO How to annotate this situation where TextIOWrapper works but
    # not for StringIO?
    def test_file_arg_bad_1(self, xmlschema_path: Path) -> None:
        sio = io.StringIO(xmlschema_path.read_text())
        # Unicode strings with encoding declaration are not supported.
        with pytest.raises(ValueError, match="encoding declaration are not supported"):
            _ = XMLSchema(file=sio)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterator_of=_st.fixed_item_iterables())
    def test_file_arg_bad_2(
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
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.validate(thing)
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_arg_bad_2(
        self,
        xmlschema: XMLSchema,
        iterable_of: Any,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.validate(iterable_of(xml2_root))
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.validate(iterable_of(xml2_tree))
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema(iterable_of(xml2_root))
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema(iterable_of(xml2_tree))

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
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.assertValid(thing)
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.assert_(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_assert_arg_bad_2(
        self,
        xmlschema: XMLSchema,
        iterable_of: Any,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.assertValid(iterable_of(xml2_root))
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.assertValid(iterable_of(xml2_tree))
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.assert_(iterable_of(xml2_root))
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.assert_(iterable_of(xml2_tree))
