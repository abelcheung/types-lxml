from __future__ import annotations

import copy
import sys
from collections.abc import Callable, Iterable
from inspect import Parameter
from pathlib import Path
from types import NoneType
from typing import Any, cast

import pytest
from hypothesis import HealthCheck, assume, example, given, settings
from lxml.etree import (
    DocumentInvalid,
    RelaxNG,
    RelaxNGParseError,
    _Element,
    _ElementTree,
)

from ._testutils import signature_tester, strategy as _st
from ._testutils.errors import (
    raise_invalid_filename_type,
    raise_invalid_lxml_type,
    raise_no_attribute,
    raise_wrong_pos_arg_count,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestRelaxNGInput:
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
            raise_cm = pytest.raises(RelaxNGParseError, match=r"No tree or file given")
        else:
            raise_cm = raise_wrong_pos_arg_count
        with raise_cm:
            _ = RelaxNG(*args, **kw)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType, _Element, _ElementTree))
    @pytest.mark.slow
    def test_etree_arg_bad_1(self, thing: Any) -> None:
        with raise_invalid_lxml_type:
            _ = RelaxNG(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_etree_arg_bad_2(self, relaxng_root: _Element, iterable_of: Any) -> None:
        with raise_invalid_lxml_type:
            _ = RelaxNG(iterable_of(relaxng_root))

    def test_etree_arg_ok(self, relaxng_root: _Element) -> None:
        rng = RelaxNG(relaxng_root)
        reveal_type(rng)
        del rng

        rng = RelaxNG(etree=relaxng_root.getroottree())
        reveal_type(rng)

    def test_file_arg_ok(
        self,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
        relaxng_path: Path,
    ) -> None:
        for input in generate_input_file_arguments(relaxng_path):
            rng = RelaxNG(file=input)
            reveal_type(rng)
            del rng

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_file_arg_bad(
        self,
        relaxng_path: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
        iterable_of: Any,
    ) -> None:
        for input in generate_input_file_arguments(relaxng_path):
            with pytest.raises(TypeError, match=r"cannot parse from"):
                _ = RelaxNG(file=iterable_of(input))

    @signature_tester(RelaxNG.from_rnc_string, (
        ("src"     , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("base_url", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_from_rnc_signature(self) -> None:
        pass

    def test_from_rnc_input_ok(self, rnc_str: str, xml2_root: _Element) -> None:
        rng = RelaxNG.from_rnc_string(src=rnc_str)
        reveal_type(rng)
        assert rng(xml2_root) is True

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str))
    @pytest.mark.slow
    @example(thing=b"start = element shiporder {}")
    def test_from_rnc_input_bad_1(self, thing: Any) -> None:
        if isinstance(thing, (bytes, bytearray)) and not thing:
            raise_cm = pytest.raises(
                RelaxNGParseError, match=r"grammar has no children"
            )
        else:
            # too diversified
            raise_cm = pytest.raises((TypeError, AttributeError))  # type: ignore[arg-type]
        with raise_cm:
            _ = RelaxNG.from_rnc_string(src=cast(Any, thing))

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_from_rnc_input_bad_2(self, rnc_str: str, iterable_of: Any) -> None:
        with raise_no_attribute:
            _ = RelaxNG.from_rnc_string(src=iterable_of(rnc_str))

    def test_from_rnc_baseurl_ok(self, rnc_str: str, xml2_root: _Element) -> None:
        for url in (None, "http://example.org/", b"http://example.org/"):
            rng = RelaxNG.from_rnc_string(rnc_str, base_url=url)
            reveal_type(rng)
            assert rng(xml2_root) is True

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, NoneType))
    @pytest.mark.slow
    def test_from_rnc_baseurl_bad_1(self, rnc_str: str, thing: Any) -> None:
        # Falsy values evaluated as None in _parseDocFromFileLike
        assume(thing is NotImplemented or bool(thing))
        with raise_invalid_filename_type:
            _ = RelaxNG.from_rnc_string(rnc_str, base_url=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_from_rnc_baseurl_bad_2(self, rnc_str: str, iterable_of: Any) -> None:
        with raise_invalid_filename_type:
            _ = RelaxNG.from_rnc_string(rnc_str, base_url=iterable_of("foo"))


class TestRelaxNGValidate:
    @signature_tester(
        RelaxNG.validate,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_call_arg_ok(
        self,
        relaxng: RelaxNG,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        reveal_type(relaxng.validate(xml2_root))
        reveal_type(relaxng.validate(xml2_tree))
        reveal_type(relaxng(xml2_root))
        reveal_type(relaxng(xml2_tree))

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        reveal_type(relaxng(faulty_root))

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_call_arg_bad_1(self, relaxng: RelaxNG, thing: Any) -> None:
        with raise_invalid_lxml_type:
            _ = relaxng.validate(thing)
        with raise_invalid_lxml_type:
            _ = relaxng(thing)

    @pytest.mark.parametrize(["funcname"], (["validate"], ["__call__"]))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_arg_bad_2(
        self,
        relaxng: RelaxNG,
        iterable_of: Any,
        funcname: str,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        func = getattr(relaxng, funcname)
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_root))
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_tree))

    @signature_tester(
        RelaxNG.assert_,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    @signature_tester(
        RelaxNG.assertValid,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_assert_arg_ok(
        self,
        relaxng: RelaxNG,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        assert relaxng.assertValid(xml2_root) is None
        assert relaxng.assertValid(xml2_tree) is None
        assert relaxng.assert_(xml2_root) is None
        assert relaxng.assert_(xml2_tree) is None

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        with pytest.raises(DocumentInvalid):
            relaxng.assertValid(faulty_root)

        with pytest.raises(AssertionError):
            relaxng.assert_(faulty_root)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_assert_arg_bad_1(self, relaxng: RelaxNG, thing: Any) -> None:
        with raise_invalid_lxml_type:
            _ = relaxng.assertValid(thing)
        with raise_invalid_lxml_type:
            _ = relaxng.assert_(thing)

    @pytest.mark.parametrize(["funcname"], (["assertValid"], ["assert_"]))
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_assert_arg_bad_2(
        self,
        relaxng: RelaxNG,
        iterable_of: Any,
        funcname: str,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        func = getattr(relaxng, funcname)
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_root))
        with raise_invalid_lxml_type:
            _ = func(iterable_of(xml2_tree))
