from __future__ import annotations

from collections import ChainMap, defaultdict
from collections.abc import Mapping
from inspect import Parameter
from types import MappingProxyType
from typing import Any, Iterable, cast

import pytest
from hypothesis import assume, example, given, settings, strategies as st
from lxml.etree import Element, QName, _Attrib, _Element

from . import _testutils
from ._testutils import (
    empty_signature_tester,
    signature_tester,
    strategy as _st,
)

INJECT_REVEAL_TYPE = True
if INJECT_REVEAL_TYPE:
    reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestAttrib:
    def test_basic_behavior(self, xml2_root: _Element) -> None:
        attrib = xml2_root.attrib
        reveal_type(len(attrib))
        reveal_type(bool(attrib))
        reveal_type("foo" in attrib)

        for k1 in attrib:
            reveal_type(k1)

    @given(k=_st.all_instances_except_of_type(str, bytes, bytearray, QName))
    def test_wrong_key_type(self, disposable_attrib: _Attrib, k: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = disposable_attrib[k]

    @given(k=_st.xml_name_arg())
    def test_valid_key_type(
        self, disposable_attrib: _Attrib, k: str | bytes | bytearray | QName
    ) -> None:
        disposable_attrib[k] = "bar"
        del disposable_attrib[k]

    @given(v=_st.all_instances_except_of_type(str, bytes, bytearray, QName))
    def test_wrong_value_type(self, disposable_attrib: _Attrib, v: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            disposable_attrib["foo"] = v

    @given(v=_st.xml_attr_value_arg())
    def test_valid_value_type(
        self, disposable_attrib: _Attrib, v: str | bytes | bytearray | QName
    ) -> None:
        disposable_attrib["foo"] = v
        reveal_type(disposable_attrib["foo"])

    @empty_signature_tester(_Attrib.clear)
    def test_method_clear(self, disposable_attrib: _Attrib) -> None:
        assert disposable_attrib.clear() is None
        assert len(disposable_attrib) == 0

    @empty_signature_tester(
        _Attrib.keys,
        _Attrib.values,
        _Attrib.items,
        _Attrib.iterkeys,
        _Attrib.itervalues,
        _Attrib.iteritems,
    )
    def test_method_keyval(self, xml2_root: _Element) -> None:
        attrib = xml2_root.attrib

        ks = attrib.keys()
        reveal_type(ks)
        for k in ks:
            reveal_type(k)

        vs = attrib.values()
        reveal_type(vs)
        for v in vs:
            reveal_type(v)

        items = attrib.items()
        reveal_type(items)
        for i in items:
            reveal_type(i)

        ik = attrib.iterkeys()
        reveal_type(ik)
        for k in ik:
            reveal_type(k)

        iv = attrib.itervalues()
        reveal_type(iv)
        for v in iv:
            reveal_type(v)

        ii = attrib.iteritems()
        reveal_type(ii)
        for i in ii:
            reveal_type(i)


class TestMethodHasKey:
    @signature_tester(_Attrib.has_key, (
        ("key", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    @given(k=_st.all_instances_except_of_type(str, bytes, bytearray, QName))
    def test_wrong_key_type(self, disposable_attrib: _Attrib, k: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = disposable_attrib.has_key(k)

    @given(k=_st.xml_name_arg())
    @example(k="date")
    def test_valid_key_type(
        self, disposable_attrib: _Attrib, k: str | bytes | bytearray | QName
    ) -> None:
        reveal_type(disposable_attrib.has_key(k))


class TestMethodGet:
    @signature_tester(_Attrib.get, (
        ("key"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    @given(k=_st.all_instances_except_of_type(str, bytes, bytearray, QName))
    def test_wrong_key_type(self, disposable_attrib: _Attrib, k: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = disposable_attrib.get(k)

    @given(k=_st.xml_name_arg())
    @example(k="date")
    def test_valid_key_type(
        self, disposable_attrib: _Attrib, k: str | bytes | bytearray | QName
    ) -> None:
        reveal_type(disposable_attrib.get(k))

    @given(default=_st.all_instances_except_of_type())
    def test_default_value(self, disposable_attrib: _Attrib, default: object) -> None:
        val = disposable_attrib.get("id", default=default)
        reveal_type(val)  # Not useful for typeguard, too generic
        assert type(val) == str
        assert type(disposable_attrib.get("foo", default)) == type(default)


class TestMethodPop:
    @signature_tester(_Attrib.pop, (
        ("key"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_signature(self, xml2_root: _Element) -> None:
        # Verify 'default' parameter being VAR_POSITIONAL is actually
        # superfluous, as only one 'default' parameter is expected.
        with pytest.raises(TypeError, match="pop expected at most 2 arguments"):
            xml2_root.attrib.pop("foo", 0, 1)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue]

    @given(k=_st.all_instances_except_of_type(str, bytes, bytearray, QName))
    def test_wrong_key_type(self, disposable_attrib: _Attrib, k: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = disposable_attrib.pop(k)

    @given(k=_st.xml_name_arg(), v=_st.xml_attr_value_arg())
    def test_valid_key_type(
        self,
        disposable_attrib: _Attrib,
        k: str | bytes | bytearray | QName,
        v: str | bytes | bytearray | QName,
    ) -> None:
        assume(k not in disposable_attrib)
        disposable_attrib[k] = v
        reveal_type(disposable_attrib.pop(k))

    @settings(max_examples=5)
    @given(default=_st.all_instances_except_of_type())
    def test_default_with_key_hit(
        self, disposable_attrib: _Attrib, default: object
    ) -> None:
        with pytest.MonkeyPatch().context() as m:
            m.setitem(disposable_attrib, "fakekey", "fakevalue")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
            val = disposable_attrib.pop("fakekey", default)
            reveal_type(val)  # Not useful for typeguard too generic
            assert type(val) == str

    @settings(max_examples=5)
    @given(default=_st.all_instances_except_of_type())
    def test_default_with_key_miss(
        self, disposable_attrib: _Attrib, default: object
    ) -> None:
        val = disposable_attrib.pop("foo", default)
        reveal_type(val)  # Not useful for typeguard, too generic
        assert type(val) == type(default)


# Note that monkeypatch is useless here. _Attrib merely provides an
# interface to the underlying _Element which is not patched
#
class TestMethodUpdate:
    def _normalized_value(self, v: str | bytes | bytearray | QName) -> str:
        if isinstance(v, QName):
            return v.text
        elif isinstance(v, (bytes, bytearray)):
            # str(b'') == "b''"
            return v.decode("utf-8")
        else:
            return str(v)

    def _toggle_empty_ns(self, k: str | bytes | bytearray | QName) -> str:
        norm = self._normalized_value(k)
        return norm[2:] if norm.startswith("{}") else "{}" + norm

    def _verify_key_val_present(self, test_object: _Attrib, inserted: Any) -> None:
        test_object.update(inserted)

        # This is bad. update() with random mapping might actually
        # succeed, if mapping keys are simple str or bytes of
        # len > 1, or is itself a 2-item tuple. The key is split
        # into 2 and added to the attrib as key/value pair.
        # Rigorously verify key / value pairs inserted into Attrib,
        # but there are still exceptions. See below.
        if isinstance(inserted, Mapping):
            normalized_data = inserted.items()  # pyright: ignore[reportUnknownVariableType]
        else:
            normalized_data = inserted  # pyright: ignore[reportUnknownVariableType]
        normalized_data = cast(Iterable[tuple[Any, Any]], normalized_data)
        try:
            for k, v in normalized_data:
                assert k in test_object
                # Things become dirty here.
                #
                # Counter example 1: {'k': 'v1', '{}k': 'v2'}
                # Keys are normalized before insertion, so
                # 'k' and '{}k' are both inserted as 'k',
                # therefore end result becomes {'k': 'v2'}.
                tk = self._toggle_empty_ns(k)
                if k != tk and tk in [_k for _k, _ in normalized_data]:
                    continue

                # Counter example 2: {'k': QName('{n}v')}
                # When QName is supplied as value, it is transformed
                # into ns0:v format.
                if isinstance(v, QName):
                    assert test_object[k].split(":")[-1] == v.localname
                else:
                    assert test_object[k] == self._normalized_value(v)
        except AssertionError:
            test_object.clear()
            raise

    @signature_tester(_Attrib.update, (
        ("sequence_or_dict", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_signature(self, disposable_attrib: _Attrib) -> None:
        assert disposable_attrib.update({"foo": "bar"}) is None
        disposable_attrib.clear()

    # TODO register_type_strategy for element, QName, CDATA etc

    @given(
        atts=st.dictionaries(
            # Can't use mutable bytearray as Mapping key
            keys=_st.xml_name_arg().filter(lambda x: not isinstance(x, bytearray)),
            values=_st.xml_attr_value_arg(),
            max_size=3,
        )
    )
    def test_input_dict_ok(
        self, disposable_attrib: _Attrib, atts: dict[Any, Any]
    ) -> None:
        self._verify_key_val_present(disposable_attrib, atts)
        self._verify_key_val_present(disposable_attrib, atts.items())

    @given(
        atts=st.dictionaries(
            # Can't use mutable bytearray as Mapping key
            keys=_st.xml_name_arg().filter(lambda x: not isinstance(x, bytearray)),
            values=_st.xml_attr_value_arg(),
            max_size=3,
        )
    )
    def test_input_dict_subclass(
        self, disposable_attrib: _Attrib, atts: dict[Any, Any]
    ) -> None:
        self._verify_key_val_present(disposable_attrib, defaultdict(str, atts))

    # Prove that non-dict Mapping won't do
    @settings(max_examples=5)
    @given(
        atts=st.dictionaries(
            # Can't use mutable bytearray as Mapping key
            keys=_st.xml_name_arg().filter(lambda x: not isinstance(x, bytearray)),
            values=_st.xml_attr_value_arg(),
            min_size=1,
            max_size=3,
        )
    )
    def test_input_other_mapping_1(
        self, disposable_attrib: _Attrib, atts: dict[Any, Any]
    ) -> None:
        with pytest.raises((TypeError, ValueError, AssertionError)):
            self._verify_key_val_present(disposable_attrib, MappingProxyType(atts))

    @given(
        atts=st.dictionaries(
            # Can't use mutable bytearray as dict key
            keys=_st.xml_name_arg().filter(lambda x: not isinstance(x, bytearray)),
            values=_st.xml_attr_value_arg(),
            min_size=1,
            max_size=3,
        )
    )
    def test_input_other_mapping_2(
        self, disposable_attrib: _Attrib, atts: dict[Any, Any]
    ) -> None:
        with pytest.raises((TypeError, ValueError, AssertionError)):
            self._verify_key_val_present(disposable_attrib, ChainMap(atts))

    @given(atts=st.iterables(
        st.tuples(_st.xml_name_arg(), _st.xml_attr_value_arg()), max_size=3
    ))  # fmt: skip
    def test_input_sequence_ok(
        self, disposable_attrib: _Attrib, atts: list[tuple[Any, Any]]
    ) -> None:
        self._verify_key_val_present(disposable_attrib, atts)

    @given(atts=st.iterables(
        st.tuples(_st.xml_name_arg(), _st.xml_attr_value_arg()), max_size=3
    ))  # fmt: skip
    def test_input_attrib(
        self, disposable_attrib: _Attrib, atts: list[tuple[Any, Any]]
    ) -> None:
        # generate a temp element with supplied iterable as attributes,
        # then extract the attributes and insert into disposable_attrib
        new_elem = Element("foo")
        new_elem.attrib.update(atts)
        self._verify_key_val_present(disposable_attrib, new_elem.attrib)

    # TODO Need negative tests for _Attrib.update()
