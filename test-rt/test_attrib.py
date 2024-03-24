from __future__ import annotations

import copy
from typing import Any, cast

import _testutils
import pytest
from lxml.etree import _Element, _ElementTree

reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestXmlAttrib:
    def test_behavior(self, xml_tree: _ElementTree[_Element]) -> None:
        e = copy.deepcopy(xml_tree.getroot())
        attrib = e.attrib
        reveal_type(len(attrib))
        attrib.update([("foo", "foo"), (b"bar", b"bar")])
        attrib.update({"foo": "foo", b"bar": b"bar"})
        for k in attrib:
            reveal_type(k)
            reveal_type(attrib[k])
        attrib[b"bar"] = "foo"
        del attrib["bar"]
        reveal_type(attrib.get("bar"))
        reveal_type(attrib.get("bar", 0))
        reveal_type(attrib.get("orderid"))
        reveal_type(attrib.has_key("whatever"))
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            attrib["x"] = cast(Any, 1)
        # Will fail, possibly got evaluated twice
        # v1 = attrib.pop('orderid')
        # reveal_type(v1)
        reveal_type(attrib.pop("whatever", 0))
        for k in attrib.keys():
            reveal_type(k)
        for v in attrib.values():
            reveal_type(v)
        for k, v in attrib.items():
            reveal_type(k)
            reveal_type(v)

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
