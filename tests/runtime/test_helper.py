from __future__ import annotations

import re
import sys
from contextlib import nullcontext
from itertools import product
from types import NoneType
from typing import Any

import pytest
from hypothesis import example, given, settings
from lxml.etree import Element, QName, _Element

from ._testutils import strategy as _st
from ._testutils.errors import (
    raise_attr_not_writable,
    raise_invalid_utf8_type,
    raise_too_few_pos_arg,
    raise_too_many_pos_arg,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


def param_type_ident(val: Any) -> str:
    return type(val).__name__


class TestQName:
    arg1_choice = [
        "foo",
        b"foo",
        # bytearray(b"foo"),
        QName("{http://dummy.ns}foo"),
        Element("{http://dummy.ns}foo"),
    ]

    arg2_choice = [
        "bar",
        b"bar",
        bytearray(b"bar"),
        QName("{http://another.ns}bar"),
        Element("{http://another.ns}bar"),
    ]

    # Generic cython signature

    @pytest.mark.parametrize(
        ("args", "kw", "raise_cm"),
        [
            ([], {}, raise_too_few_pos_arg),
            ([1, 2, 3], {}, raise_too_many_pos_arg),
            ([None], {}, pytest.raises(ValueError, match=r"Invalid input tag of type")),
            ([], {"tag": None}, raise_too_few_pos_arg),
            (
                [],
                {"text_or_uri_or_element": None},
                pytest.raises(ValueError, match=r"Invalid input tag of type"),
            ),
            (
                [],
                {"text_or_uri_or_element": None, "tag": None},
                pytest.raises(ValueError, match=r"Invalid input tag of type"),
            ),
        ],
    )
    def test_signature(self, args: Any, kw: Any, raise_cm: Any) -> None:
        with raise_cm:
            _ = QName(*args, **kw)

    # When only one argument is passed, first or second arg is interchangeable
    @pytest.mark.parametrize(("arg",), [[c] for c in arg1_choice])
    def test_single_arg_ok(self, arg: Any) -> None:
        qn = reveal_type(QName(text_or_uri_or_element=arg))
        assert qn == QName(None, tag=arg)
        reveal_type(qn.localname)
        reveal_type(qn.namespace)
        reveal_type(qn.text)
        # only do it once
        if isinstance(arg, str):
            for attr in "localname", "namespace", "text":
                with raise_attr_not_writable:
                    setattr(qn, attr, getattr(qn, attr))
                with raise_attr_not_writable:
                    delattr(qn, attr)

    @settings(max_examples=300)
    @given(
        thing=_st.all_instances_except_of_type(str, bytes, QName, _Element, NoneType)
    )
    @example(thing=bytearray(b"foo"))
    def test_single_arg_bad(self, thing: Any) -> None:
        if len(str(thing)) == 0 or str(thing).endswith("}"):
            raise_cm = pytest.raises(ValueError, match=r"Empty tag name")
        elif re.match(r"^[A-Za-z_]([\w\.-])*$", str(thing)):
            # QName creation really succeed with quite a few unexpected
            # types like UUID, timezones, literal constants etc
            raise_cm = nullcontext()
        else:
            raise_cm = pytest.raises(
                ValueError,
                match=r"(Invalid tag name|All strings must be XML compatible)",
            )
        with raise_cm:
            _ = QName(thing)
        with raise_cm:
            _ = QName(None, thing)

    # Proves following rules:
    # - 2nd arg can't be QName or _Element if 1st non-empty
    # - Only 2nd arg can be bytearray when 1st is non-empty
    @pytest.mark.parametrize(
        ("arg1", "arg2"),
        product(arg1_choice, arg2_choice),
        ids=param_type_ident,
    )
    def test_second_arg_ok(self, arg1: Any, arg2: Any) -> None:
        if isinstance(arg2, (QName, _Element)):
            raise_cm = raise_invalid_utf8_type
        else:
            raise_cm = nullcontext()
        with raise_cm:
            _ = reveal_type(QName(arg1, arg2))

    @settings(max_examples=300)
    @given(
        thing=_st.all_instances_except_of_type(
            str, bytes, bytearray, QName, _Element, NoneType
        )
    )
    def test_second_arg_bad(self, thing: Any) -> None:
        with raise_invalid_utf8_type:
            _ = QName("foo", thing)

    # Forget richcmp tests, seems pointless
