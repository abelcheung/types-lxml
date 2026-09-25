from __future__ import annotations

import math
import sys

import pytest
from lxml import objectify
from lxml.objectify import (
    BoolElement,
    FloatElement,
    IntElement,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


@pytest.fixture
def ie() -> IntElement:
    elem = objectify.fromstring("<root><i>5</i></root>").i
    assert isinstance(elem, IntElement)
    return elem


@pytest.fixture
def neg_ie() -> IntElement:
    elem = objectify.fromstring("<root><i>-8</i></root>").i
    assert isinstance(elem, IntElement)
    return elem


@pytest.fixture
def fe() -> FloatElement:
    elem = objectify.fromstring("<root><f>2.5</f></root>").f
    assert isinstance(elem, FloatElement)
    return elem


@pytest.fixture
def be() -> BoolElement:
    elem = objectify.fromstring("<root><b>true</b></root>").b
    assert isinstance(elem, BoolElement)
    return elem


class TestNotNativeNumber:
    def test_mro(self, ie: IntElement, fe: FloatElement, be: BoolElement) -> None:
        assert int not in type(ie).__mro__
        assert float not in type(fe).__mro__
        assert int not in type(be).__mro__

    def test_attribute_is_child_lookup(self, ie: IntElement, fe: FloatElement) -> None:
        # int / float attributes don't exist, they are child lookups
        with pytest.raises(AttributeError, match="no such child: real"):
            _ = ie.real
        with pytest.raises(AttributeError, match="no such child: bit_length"):
            _ = ie.bit_length
        with pytest.raises(AttributeError, match="no such child: is_integer"):
            _ = fe.is_integer


class TestConversion:
    def test_int_elem(self, ie: IntElement) -> None:
        reveal_type(int(ie))
        reveal_type(float(ie))
        reveal_type(complex(ie))
        reveal_type(bool(ie))
        reveal_type(hash(ie))
        assert hash(ie) == hash(5)
        reveal_type(ie.__index__())
        assert list(range(ie)) == [0, 1, 2, 3, 4]
        assert [0] * ie == [0] * 5
        reveal_type(hex(ie))

    def test_float_elem(self, fe: FloatElement) -> None:
        reveal_type(int(fe))
        reveal_type(float(fe))
        reveal_type(complex(fe))
        reveal_type(bool(fe))
        reveal_type(hash(fe))
        reveal_type(math.floor(fe))


class TestIntElemOperators:
    def test_add_sub_mul(self, ie: IntElement, fe: FloatElement) -> None:
        for result in (ie + 1, 1 + ie, ie + ie, ie - 1, 1 - ie, ie * 2, 2 * ie):
            reveal_type(result)
        reveal_type(ie + 1.5)
        reveal_type(1.5 + ie)
        reveal_type(ie - fe)
        reveal_type(ie * fe)
        reveal_type(ie + 1j)
        reveal_type(1j * ie)

    def test_division(self, ie: IntElement, fe: FloatElement) -> None:
        reveal_type(ie / 2)
        reveal_type(2 / ie)
        reveal_type(ie / ie)
        reveal_type(ie / 1j)
        reveal_type(ie // 2)
        reveal_type(7 // ie)
        reveal_type(ie // fe)
        reveal_type(ie % 2)
        reveal_type(7.5 % ie)
        reveal_type(divmod(ie, 2))
        reveal_type(divmod(7, ie))
        reveal_type(divmod(ie, fe))

    def test_pow(self, ie: IntElement, neg_ie: IntElement, fe: FloatElement) -> None:
        # Like typeshed's int and float, results depending on the value of
        # the exponent are typed Any, so only check them at runtime
        reveal_type(ie ** 0)  # fmt: skip
        reveal_type(ie ** 2)  # fmt: skip
        reveal_type(ie ** -1)  # fmt: skip
        assert ie**ie == 3125
        reveal_type(pow(ie, 2, 3))
        assert ie**fe == 5**2.5
        assert isinstance(neg_ie**0.5, complex)
        reveal_type(ie ** 1j)  # fmt: skip
        assert 2**ie == 32
        reveal_type(2.5 ** ie)  # fmt: skip
        reveal_type(1j ** ie)  # fmt: skip

    def test_bitwise(self, ie: IntElement) -> None:
        for result in (
            ie & 1, 1 & ie, ie | 2, 2 | ie, ie ^ ie, 3 ^ ie,
            ie << 1, 1 << ie, ie >> 1, 64 >> ie,
        ):  # fmt: skip
            reveal_type(result)

    def test_unary(self, ie: IntElement) -> None:
        reveal_type(-ie)
        reveal_type(+ie)
        reveal_type(abs(ie))
        reveal_type(~ie)

    def test_compare(self, ie: IntElement, fe: FloatElement) -> None:
        reveal_type(ie < 6)
        reveal_type(6 > ie)
        reveal_type(ie >= 4.5)
        reveal_type(ie <= fe)
        reveal_type(ie == 5)
        assert ie == 5 and ie > fe


class TestFloatElemOperators:
    def test_arith(self, ie: IntElement, fe: FloatElement) -> None:
        for result in (fe + 1, 1 + fe, fe + 0.5, fe - ie, fe * fe, 2 * fe):
            reveal_type(result)
        reveal_type(fe / 2)
        reveal_type(1 / fe)
        reveal_type(fe // 1)
        reveal_type(5 // fe)
        reveal_type(fe % ie)
        reveal_type(divmod(fe, 1))
        reveal_type(divmod(5, fe))
        reveal_type(fe + 1j)
        reveal_type(1j - fe)

    def test_pow(self, ie: IntElement, fe: FloatElement) -> None:
        reveal_type(fe ** 2)  # fmt: skip
        reveal_type(fe ** ie)  # fmt: skip
        assert fe**0.5 == 2.5**0.5
        reveal_type(fe ** 1j)  # fmt: skip
        reveal_type(2 ** fe)  # fmt: skip
        reveal_type((-2) ** fe)
        assert 2.5**fe == 2.5**2.5

    def test_unary_compare(self, fe: FloatElement) -> None:
        reveal_type(-fe)
        reveal_type(+fe)
        reveal_type(abs(fe))
        reveal_type(fe < 3)
        reveal_type(3.5 > fe)


class TestBoolElemOperators:
    def test_logical(self, be: BoolElement) -> None:
        for result in (
            be & True,
            True & be,
            be | be,
            False | be,
            be ^ False,
            True ^ be,
        ):
            reveal_type(result)
        reveal_type(be & 1)
        reveal_type(1 | be)
        reveal_type(be ^ 3)

    def test_arith(self, be: BoolElement, ie: IntElement) -> None:
        reveal_type(be + be)
        reveal_type(be + ie)
        reveal_type(1 - be)
        reveal_type(be ** 2)  # fmt: skip
        reveal_type(-be)
        reveal_type(be < 2)
        assert be == True  # noqa: E712
