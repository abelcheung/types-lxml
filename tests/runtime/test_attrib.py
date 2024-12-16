from __future__ import annotations

import sys
from collections import ChainMap, Counter, defaultdict
from collections.abc import Iterable, Mapping
from inspect import Parameter
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    cast,
)

import pytest
from hypothesis import (
    HealthCheck,
    assume,
    example,
    given,
    settings,
    strategies as st,
)
from lxml.etree import Element, QName, _Attrib, _Element

from ._testutils import (
    empty_signature_tester,
    signature_tester,
    strategy as _st,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type
from ._testutils.common import attr_name_types, attr_value_types

if TYPE_CHECKING:
    from lxml._types import (  # pyright: ignore[reportMissingModuleSource]
        _AttrName,
        _AttrVal,
    )


class TestAttrib:
    def test_basic_behavior(self, xml2_root: _Element) -> None:
        attrib = xml2_root.attrib
        reveal_type(len(attrib))
        reveal_type(bool(attrib))
        reveal_type("foo" in attrib)

        for k1 in attrib:
            reveal_type(k1)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        k=_st.all_instances_except_of_type(
            *attr_name_types.allow, *attr_name_types.skip
        )
    )
    @pytest.mark.slow
    def test_wrong_key_type(self, disposable_attrib: _Attrib, k: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = disposable_attrib[k]

    @given(k=_st.xml_name_arg())
    def test_valid_key_type(self, disposable_attrib: _Attrib, k: _AttrName) -> None:
        disposable_attrib[k] = "bar"
        del disposable_attrib[k]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        v=_st.all_instances_except_of_type(
            *attr_value_types.allow, *attr_value_types.skip
        )
    )
    @pytest.mark.slow
    def test_wrong_value_type(self, disposable_attrib: _Attrib, v: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            disposable_attrib["foo"] = v

    @given(v=_st.xml_attr_value_arg())
    def test_valid_value_type(self, disposable_attrib: _Attrib, v: _AttrVal) -> None:
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

        reveal_type(attrib.keys())
        reveal_type(attrib.values())
        reveal_type(attrib.items())

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

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        k=_st.all_instances_except_of_type(
            *attr_name_types.allow, *attr_name_types.skip
        )
    )
    @pytest.mark.slow
    def test_wrong_key_type(self, disposable_attrib: _Attrib, k: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = disposable_attrib.has_key(k)

    @given(k=_st.xml_name_arg())
    @example(k="date")
    def test_valid_key_type(self, disposable_attrib: _Attrib, k: _AttrName) -> None:
        reveal_type(disposable_attrib.has_key(k))


class TestMethodGet:
    @signature_tester(_Attrib.get, (
        ("key"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        k=_st.all_instances_except_of_type(
            *attr_name_types.allow, *attr_name_types.skip
        )
    )
    @pytest.mark.slow
    def test_wrong_key_type(self, disposable_attrib: _Attrib, k: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = disposable_attrib.get(k)

    @given(k=_st.xml_name_arg())
    @example(k="date")
    def test_valid_key_type(self, disposable_attrib: _Attrib, k: _AttrName) -> None:
        reveal_type(disposable_attrib.get(k))

    @settings(max_examples=5)
    @given(default=_st.all_instances_except_of_type())
    def test_default_value(self, disposable_attrib: _Attrib, default: object) -> None:
        val = disposable_attrib.get("id", default=default)
        reveal_type(val)  # Not useful for typeguard, too generic
        assert type(val) is str
        assert type(disposable_attrib.get("foo", default)) is type(default)


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

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        k=_st.all_instances_except_of_type(
            *attr_name_types.allow, *attr_name_types.skip
        )
    )
    @pytest.mark.slow
    def test_wrong_key_type(self, disposable_attrib: _Attrib, k: Any) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = disposable_attrib.pop(k)

    @given(k=_st.xml_name_arg(), v=_st.xml_attr_value_arg())
    def test_valid_key_type(
        self,
        disposable_attrib: _Attrib,
        k: _AttrName,
        v: _AttrVal,
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
            assert type(val) is str

    @settings(max_examples=5)
    @given(default=_st.all_instances_except_of_type())
    def test_default_with_key_miss(
        self, disposable_attrib: _Attrib, default: object
    ) -> None:
        val = disposable_attrib.pop("foo", default)
        reveal_type(val)  # Not useful for typeguard, too generic
        assert type(val) is type(default)


# Beware that monkeypatch is useless here. _Attrib merely provides an
# interface to the underlying _Element which is not patched
class TestMethodUpdate:
    # HACK Using _AttrName instead of _AttrVal to play safe, as attribute names
    # use this routine as well
    def _normalized_value(self, v: _AttrName) -> str:
        if isinstance(v, QName):
            return v.text
        elif isinstance(v, (bytes, bytearray)):
            # str(b'') == "b''"
            return v.decode("utf-8")
        else:
            return str(v)

    # HACK Merely an attempted external reproduction of how lxml
    # normalize keys before insertion into _Attrib.
    def _normalized_key(self, k: _AttrName) -> str:
        norm = self._normalized_value(k)
        return norm[2:] if norm.startswith("{}") else norm

    def _verify_key_val_present(self, test_object: _Attrib, inserted: Any) -> None:
        test_object.update(inserted)

        # This is bad. update() with random mapping might actually
        # succeed, if mapping keys are simple str or bytes of
        # len > 1, or is itself a 2-item tuple. The key is split
        # into 2 and added to the attrib as key/value pair.
        # Rigorously verify key / value pairs inserted into Attrib,
        # but there are still exceptions. See below.
        if isinstance(inserted, Mapping):
            iterable_pairs = inserted.items()  # pyright: ignore[reportUnknownVariableType]
        else:
            iterable_pairs = inserted  # pyright: ignore[reportUnknownVariableType]
        iterable_pairs = cast(Iterable[tuple[Any, Any]], iterable_pairs)
        all_norm_keys = [self._normalized_key(k) for k, _ in iterable_pairs]
        blacklist_keys = {k for k, c in Counter(all_norm_keys).items() if c > 1}
        try:
            for k, v in iterable_pairs:
                assert k in test_object
                # Things become dirty here.
                #
                # Counter example 1: {'k': 'v1', b'{}k': 'v2'}
                # Keys are normalized before insertion, so
                # end result becomes {'k': 'v2'}. Dict key
                # uniqueness is broken in this case and we can
                # no longer guarantee value equality.
                if self._normalized_key(k) in blacklist_keys:
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
            keys=_st.xml_name_key_arg(),
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
            keys=_st.xml_name_key_arg(),
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
            keys=_st.xml_name_key_arg(),
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
            keys=_st.xml_name_key_arg(),
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
