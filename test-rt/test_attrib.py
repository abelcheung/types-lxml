from __future__ import annotations

from copy import deepcopy
from inspect import Parameter
from typing import Any, cast
from types import MappingProxyType

import _testutils
import pytest
from lxml.etree import QName, _Attrib, _ElementTree

reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestXmlAttrib:
    def test_basic_behavior(self, xml_tree: _ElementTree) -> None:
        root = deepcopy(xml_tree.getroot())
        attrib = root.attrib
        reveal_type(len(attrib))
        reveal_type(bool(attrib))
        reveal_type("foo" in attrib)

        for k in attrib:
            reveal_type(k)
            reveal_type(attrib[k])

        qn = QName(None, "foo")
        for k in ("foo", b"foo", qn):
            attrib[k] = "bar"
            del attrib[k]
        for k in (None, 1, object(), ["foo"]):
            with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
                attrib[cast(Any, k)] = "bar"

        qn = QName(None, "bar")
        for v in ("bar", b"bar", qn):
            attrib["foo"] = v
        for v in (None, 1, object(), ["bar"]):
            with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
                attrib["foo"] = cast(Any, v)

    @_testutils.empty_signature_tester(_Attrib.clear)
    def test_method_clear(self, xml_tree: _ElementTree) -> None:
        root = deepcopy(xml_tree.getroot())
        attrib = root.attrib
        reveal_type(attrib.clear())
        assert len(attrib) == 0

    @_testutils.signature_tester(_Attrib.get, (
        ("key"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_get(self, xml_tree: _ElementTree) -> None:
        root = deepcopy(xml_tree.getroot())
        attrib = root.attrib

        key = "orderid"
        result = attrib.get(key)
        reveal_type(result)
        qname = QName(None, key)
        for arg in (key, key.encode(), qname):
            assert attrib.get(arg) == result
        for arg in (None, 1, object(), [key]):
            with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
                _ = attrib.get(cast(Any, arg))

        reveal_type(attrib.get("dummy"))
        reveal_type(attrib.get("dummy", 0))
        reveal_type(attrib.get("dummy", (1, "dummy")))

    @_testutils.signature_tester(_Attrib.update, (
        ("sequence_or_dict", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_update(self, xml_tree: _ElementTree) -> None:
        root = deepcopy(xml_tree.getroot())
        attrib = root.attrib
        result = attrib.update({"foo": "bar"})
        reveal_type(result)

        attrib.update({
            "foo": b"bar",
            b"foo": QName(None, "bar"),
            QName(None, "foo"): "bar",
        })

        attrib.update([
            (b"foo", "bar"),
            ("foo", QName(None, "bar")),
            (QName(None, "foo"), b"bar"),
        ])

        attrib_copy = deepcopy(attrib)
        attrib.clear()
        assert len(attrib) == 0
        attrib.update(attrib_copy)
        assert len(attrib) > 0

        for data in (None, 1):
            with pytest.raises(TypeError, match="object is not iterable"):
                attrib.update(cast(Any, data))

        for data in ({"foo", "bar"}, MappingProxyType({"foo": "bar"})):
            with pytest.raises(ValueError, match="too many values to unpack"):
                attrib.update(cast(Any, data))

    @_testutils.signature_tester(_Attrib.pop, (
        ("key"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_method_pop(self, xml_tree: _ElementTree) -> None:
        root = deepcopy(xml_tree.getroot())
        attrib = deepcopy(root.attrib)
        result = attrib.pop("dummy", 0)
        reveal_type(result)
        assert result == 0
        with pytest.raises(TypeError, match="expected at most 2 arguments"):
            _ = attrib.pop("dummy", 0, 0)  # type: ignore
        del result, root

        for arg in ("orderid", b"orderid", QName(None, "orderid")):
            root = deepcopy(xml_tree.getroot())
            attrib = root.attrib
            result = attrib.pop(arg)
            reveal_type(result)
            del result, root

    @_testutils.signature_tester(_Attrib.has_key, (
        ("key", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_haskey(self, xml_tree: _ElementTree) -> None:
        root = deepcopy(xml_tree.getroot())
        attrib = root.attrib
        result = attrib.has_key("orderid")
        reveal_type(result)
        for k in (b"orderid", QName(None, "orderid")):
            assert attrib.has_key(k) == result

        for k in (None, 1, object(), ["orderid"]):
            with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
                _ = attrib.has_key(cast(Any, k))

    @_testutils.empty_signature_tester(
        _Attrib.keys,
        _Attrib.values,
        _Attrib.items,
        _Attrib.iterkeys,
        _Attrib.itervalues,
        _Attrib.iteritems,
    )
    def test_method_keyval(self, xml_tree: _ElementTree) -> None:
        root = deepcopy(xml_tree.getroot())
        attrib = root.attrib

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
