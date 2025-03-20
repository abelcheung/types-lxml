from __future__ import annotations

import copy
import sys
from collections.abc import Callable, Iterable
from inspect import Parameter, _ParameterKind
from pathlib import Path
from types import NoneType
from typing import Any

import pytest
from hypothesis import HealthCheck, given, settings
from lxml.etree import (
    LXML_VERSION,
    DocumentInvalid,
    SchematronParseError,
    _Element,
    _ElementTree,
)
from lxml.isoschematron import (
    Schematron,
)

from ._testutils import signature_tester, strategy as _st
from ._testutils.errors import (
    raise_invalid_lxml_type,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


_init_args: list[tuple[str, _ParameterKind, Any]] = [
    ("etree"           , Parameter.POSITIONAL_OR_KEYWORD, None),
    ("file"            , Parameter.POSITIONAL_OR_KEYWORD, None),
    ("include"         , Parameter.POSITIONAL_OR_KEYWORD, True),
    ("expand"          , Parameter.POSITIONAL_OR_KEYWORD, True),
    ("include_params"  , Parameter.POSITIONAL_OR_KEYWORD, {}),
    ("expand_params"   , Parameter.POSITIONAL_OR_KEYWORD, {}),
    ("compile_params"  , Parameter.POSITIONAL_OR_KEYWORD, {}),
    ("store_schematron", Parameter.POSITIONAL_OR_KEYWORD, False),
    ("store_xslt"      , Parameter.POSITIONAL_OR_KEYWORD, False),
    ("store_report"    , Parameter.POSITIONAL_OR_KEYWORD, False),
    ("phase"           , Parameter.POSITIONAL_OR_KEYWORD, None),
    ("error_finder"    , Parameter.POSITIONAL_OR_KEYWORD, Schematron.ASSERTS_ONLY),
]  # fmt: skip
if LXML_VERSION >= (5, 0):
    from lxml.isoschematron import schematron_schema_valid_supported

    _init_args.append(
        (
            "validate_schema",
            Parameter.POSITIONAL_OR_KEYWORD,
            schematron_schema_valid_supported,
        ),
    )


# TODO Everything except basic validation is not tested yet
class TestSchematronInput:
    @signature_tester(Schematron.__init__, _init_args)
    def test_init_signature(self) -> None:
        pass

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
        with pytest.raises(ValueError, match=r"Empty tree"):
            _ = Schematron(*args, **kw)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType, _Element, _ElementTree))
    @pytest.mark.slow
    def test_etree_arg_bad_1(self, thing: Any) -> None:
        with pytest.raises(SchematronParseError, match=r"No tree or file given"):
            _ = Schematron(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_etree_arg_bad_2(self, schematron_root: _Element, iterable_of: Any) -> None:
        with pytest.raises(SchematronParseError, match=r"No tree or file given"):
            _ = Schematron(iterable_of(schematron_root))

    def test_etree_arg_ok(self, schematron_root: _Element) -> None:
        schematron = Schematron(schematron_root)
        reveal_type(schematron)
        del schematron

        schematron = Schematron(etree=schematron_root.getroottree())
        reveal_type(schematron)

    def test_file_arg_ok(
        self,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
        schematron_path: Path,
    ) -> None:
        for input in generate_input_file_arguments(schematron_path):
            schematron = Schematron(file=input)
            reveal_type(schematron)
            del schematron

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_file_arg_bad(
        self,
        schematron_path: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
        iterable_of: Any,
    ) -> None:
        for input in generate_input_file_arguments(schematron_path):
            with pytest.raises(SchematronParseError, match=r"No tree or file given"):
                _ = Schematron(file=iterable_of(input))


class TestSchematronValidate:
    @signature_tester(
        Schematron.validate,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_call_arg_ok(
        self,
        schematron: Schematron,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        reveal_type(schematron.validate(xml2_root))
        reveal_type(schematron.validate(xml2_tree))
        reveal_type(schematron(xml2_root))
        reveal_type(schematron(xml2_tree))

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        reveal_type(schematron(faulty_root))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_call_arg_bad_1(self, schematron: Schematron, thing: Any) -> None:
        with raise_invalid_lxml_type:
            _ = schematron.validate(thing)
        with raise_invalid_lxml_type:
            _ = schematron(thing)

    @pytest.mark.parametrize(["funcname"], (["validate"], ["__call__"]))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_arg_bad_2(
        self,
        schematron: Schematron,
        iterable_of: Any,
        funcname: str,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        func = getattr(schematron, funcname)
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_root))
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_tree))

    @signature_tester(
        Schematron.assert_,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    @signature_tester(
        Schematron.assertValid,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_assert_arg_ok(
        self,
        schematron: Schematron,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        assert schematron.assertValid(xml2_root) is None
        assert schematron.assertValid(xml2_tree) is None
        assert schematron.assert_(xml2_root) is None
        assert schematron.assert_(xml2_tree) is None

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        with pytest.raises(DocumentInvalid):
            schematron.assertValid(faulty_root)

        with pytest.raises(AssertionError):
            schematron.assert_(faulty_root)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_assert_arg_bad_1(self, schematron: Schematron, thing: Any) -> None:
        with raise_invalid_lxml_type:
            _ = schematron.assertValid(thing)
        with raise_invalid_lxml_type:
            _ = schematron.assert_(thing)

    @pytest.mark.parametrize(["funcname"], (["assertValid"], ["assert_"]))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_assert_arg_bad_2(
        self,
        schematron: Schematron,
        iterable_of: Any,
        funcname: str,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        func = getattr(schematron, funcname)
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_root))
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_tree))
