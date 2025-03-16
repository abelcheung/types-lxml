from __future__ import annotations

import sys
from copy import deepcopy
from inspect import Parameter
from types import (
    MappingProxyType,
)
from typing import Any, cast

import pytest
from lxml import etree
from lxml.etree import (
    QName,
    _Attrib as _Attrib,
    _Comment as _Comment,
    _Element,
    _ElementTree as _ElementTree,
    _Entity as _Entity,
    _ProcessingInstruction as _ProcessingInstruction,
)
from lxml.html import Element as h_Element

from ._testutils import empty_signature_tester, signature_tester

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


# See mypy.ini in testsuite for explanation
TC_HONORS_REVERSED = True


# The find*() methods of _Element are all derivations of
# iterfind(). So they almost have same arguments, and even
# the other test contents look very similar.
class TestFindMethods:
    @signature_tester(_Element.iterfind, (
        ("path"      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("namespaces", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_iterfind(self, svg_root: _Element) -> None:
        root = svg_root
        tag = "desc"

        iterator = root.iterfind(tag)
        reveal_type(iterator)
        del iterator

        iterator = root.iterfind(path="junk")
        reveal_type(iterator)
        del iterator

        iterator = root.iterfind("defs/{http://example.org/myapp}piechart")
        reveal_type(iterator)
        del iterator

        qn = QName(None, tag)
        reveal_type(root.iterfind(qn))

        with pytest.raises(TypeError, match="a string pattern on a bytes-like object"):
            _ = root.iterfind(cast(Any, tag.encode()))

        for data in (None, 1):
            with pytest.raises(TypeError, match="object is unsliceable"):
                _ = root.iterfind(cast(Any, data))

        with pytest.raises(TypeError, match="unhashable type:"):
            _ = root.iterfind(cast(Any, [tag]))

        with pytest.raises(TypeError, match="expected string or bytes-like object"):
            _ = root.iterfind(cast(Any, (tag,)))

        # Check QName and namespace support
        #
        # Invalid entries in namespace dict (those with invalid key or value
        # types) wouldn't be fatal; they only silently fail to select useful
        # elements. Therefore no key/val type check is performed. Same for all
        # find*() methods below.

        iterator = root.iterfind("defs")
        url = "http://example.org/myapp"
        nsdict = {"m": url}
        defs = next(iterator)
        del iterator

        qn = QName(url, "piechart")
        result = tuple(elem for elem in defs.iterfind(f"{{{url}}}piechart"))
        assert result == tuple(elem for elem in defs.iterfind(qn, None))
        assert result == tuple(
            elem for elem in defs.iterfind("m:piechart", namespaces=nsdict)
        )
        assert result == tuple(
            elem for elem in defs.iterfind("m:piechart", MappingProxyType(nsdict))
        )

        for arg in (1, object()):
            with pytest.raises(TypeError, match="is not iterable"):
                _ = defs.iterfind("m:piechart", cast(Any, arg))
        with pytest.raises(TypeError, match="requires string as left operand"):
            _ = defs.iterfind("m:piechart", cast(Any, "foo"))
        with pytest.raises(AttributeError, match="has no attribute 'items'"):
            _ = defs.iterfind("m:piechart", cast(Any, [("m", url)]))

        # NS dict with wrong val type won't raise exception, they just fail
        # to produce result silently
        # FIXME Something not quite right, raises SyntaxError if
        # following 2 identical sections are merged
        for badns1 in ({"m": 1}, {"m": url.encode()}):
            iterator = defs.iterfind("m:piechart", namespaces=cast(Any, badns1))
            assert 0 == len(tuple(elem for elem in iterator))
            del iterator

        for badns2 in ({b"m": url}, {1: url}):
            iterator = defs.iterfind("m.piechart", namespaces=cast(Any, badns2))
            assert 0 == len(tuple(elem for elem in iterator))
            del iterator

    @signature_tester(_Element.find, (
        ("path"      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("namespaces", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_find(self, svg_root: _Element) -> None:
        root = svg_root
        tag = "desc"
        reveal_type(root.find(tag))
        reveal_type(root.find(path="junk"))
        assert etree.iselement(root.find("defs/{http://example.org/myapp}piechart"))

        qn = QName(None, tag)
        reveal_type(root.find(qn))

        with pytest.raises(TypeError, match="a string pattern on a bytes-like object"):
            _ = root.find(cast(Any, tag.encode()))

        for data in (None, 1):
            with pytest.raises(TypeError, match="object is unsliceable"):
                _ = root.find(cast(Any, data))

        with pytest.raises(TypeError, match="unhashable type:"):
            _ = root.find(cast(Any, [tag]))

        with pytest.raises(TypeError, match="expected string or bytes-like object"):
            _ = root.find(cast(Any, (tag,)))

        # Check QName and NS support; see iterfind() comment above

        defs = root.find("defs")
        assert defs is not None
        url = "http://example.org/myapp"
        nsdict = {"m": url}

        result = defs.find(f"{{{url}}}piechart")
        qn = QName(url, "piechart")
        assert result == defs.find(qn, None)
        assert result == defs.find("m:piechart", namespaces=nsdict)
        assert result == defs.find("m:piechart", MappingProxyType(nsdict))

        for arg in (1, object()):
            with pytest.raises(TypeError, match="is not iterable"):
                _ = defs.find("m:piechart", cast(Any, arg))
        with pytest.raises(TypeError, match="requires string as left operand"):
            _ = defs.find("m:piechart", cast(Any, "foo"))
        with pytest.raises(AttributeError, match="has no attribute 'items'"):
            _ = defs.find("m:piechart", cast(Any, [("m", url)]))

    @signature_tester(_Element.findall, (
        ("path"      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("namespaces", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_findall(self, svg_root: _Element) -> None:
        root = svg_root
        reveal_type(root.findall(path="junk"))

        result = root.findall("defs/{http://example.org/myapp}piechart")
        reveal_type(result)
        del result

        tag = "desc"
        result = root.findall(tag)
        qn = QName(None, tag)
        assert result == root.findall(qn)
        del result

        with pytest.raises(TypeError, match="a string pattern on a bytes-like object"):
            _ = root.findall(cast(Any, tag.encode()))

        for data in (None, 1):
            with pytest.raises(TypeError, match="object is unsliceable"):
                _ = root.findall(cast(Any, data))

        with pytest.raises(TypeError, match="unhashable type:"):
            _ = root.findall(cast(Any, [tag]))

        with pytest.raises(TypeError, match="expected string or bytes-like object"):
            _ = root.findall(cast(Any, (tag,)))

        # Check QName and NS support; see iterfind() comment above

        result = root.findall("defs")
        assert len(result) == 1
        url = "http://example.org/myapp"
        nsdict = {"m": url}
        defs = result[0]

        result = defs.findall(f"{{{url}}}piechart")
        qn = QName(url, "piechart")
        assert result == defs.findall(qn, None)
        assert result == defs.findall("m:piechart", namespaces=nsdict)
        assert result == defs.findall("m:piechart", MappingProxyType(nsdict))

        for arg in (1, object()):
            with pytest.raises(TypeError, match="is not iterable"):
                _ = defs.findall("m:piechart", cast(Any, arg))
        with pytest.raises(TypeError, match="requires string as left operand"):
            _ = defs.findall("m:piechart", cast(Any, "foo"))
        with pytest.raises(AttributeError, match="has no attribute 'items'"):
            _ = defs.findall("m:piechart", cast(Any, [("m", url)]))

    @signature_tester(_Element.findtext, (
        ("path"      , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default"   , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("namespaces", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_findtext(self, svg_root: _Element) -> None:
        root = svg_root

        result = root.findtext(path="junk")
        reveal_type(result)
        assert result is None
        del result

        result2 = root.findtext("junk", 1)
        reveal_type(result2)
        assert result2 == 1
        del result2

        result3 = root.findtext("junk", object())
        reveal_type(result3)
        del result3

        result = root.findtext("junk", "foo")
        reveal_type(result)
        del result

        result4 = root.findtext("junk", ("foo", 1))
        reveal_type(result4)
        del result4

        tag = "desc"
        result = root.findtext(tag)
        reveal_type(result)
        assert result and result.startswith("This chart")
        qn = QName(None, tag)
        assert result == root.findtext(qn)
        del result

        with pytest.raises(TypeError, match="a string pattern on a bytes-like object"):
            _ = root.findtext(cast(Any, tag.encode()))

        for data in (None, 1):
            with pytest.raises(TypeError, match="object is unsliceable"):
                _ = root.findtext(cast(Any, data))

        with pytest.raises(TypeError, match="unhashable type:"):
            _ = root.findtext(cast(Any, [tag]))

        with pytest.raises(TypeError, match="expected string or bytes-like object"):
            _ = root.findtext(cast(Any, (tag,)))

        # Check QName and NS support; see iterfind() comment above

        url = "http://example.org/myfoo"
        nsdict = {"m": url}

        result = root.findtext(f"desc/{{{url}}}title")
        assert result and result.endswith("report")
        resultnode = root.find(f"desc/{{{url}}}title")
        assert etree.iselement(resultnode)
        parent = resultnode.getparent()
        assert etree.iselement(parent)

        qn = QName(url, "title")
        assert result == parent.findtext(qn, namespaces=None)
        assert result == parent.findtext("m:title", namespaces=nsdict)
        assert result == parent.findtext("m:title", namespaces=MappingProxyType(nsdict))

        for arg in (1, object()):
            with pytest.raises(TypeError, match="is not iterable"):
                _ = parent.findtext("m:title", namespaces=cast(Any, arg))
        with pytest.raises(TypeError, match="requires string as left operand"):
            _ = parent.findtext("m:title", namespaces=cast(Any, "foo"))
        with pytest.raises(AttributeError, match="has no attribute 'items'"):
            _ = parent.findtext("m:title", namespaces=cast(Any, [("m", url)]))


class TestAddMethods:
    @signature_tester(
        _Element.addnext,
        (("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_method_addnext(self, xml2_root: _Element) -> None:
        root = deepcopy(xml2_root)
        comm = etree.Comment("foo")

        assert root[0].addnext(comm) is None

        for arg in ("junk", 1, object(), ("a", 0), [comm, comm]):
            with pytest.raises(
                TypeError, match=r"Argument 'element' has incorrect type"
            ):
                root[0].addnext(cast(Any, arg))

        h_elem = h_Element("bar")
        root[1].addnext(h_elem)

    @signature_tester(
        _Element.addprevious,
        (("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_method_addprevious(self, xml2_root: _Element) -> None:
        root = deepcopy(xml2_root)
        comm = etree.Comment("foo")

        assert root[0].addprevious(comm) is None

        for arg in ("junk", 1, object(), ("a", 0), [comm, comm]):
            with pytest.raises(
                TypeError, match=r"Argument 'element' has incorrect type"
            ):
                root[0].addprevious(cast(Any, arg))

        h_elem = h_Element("bar")
        root[1].addprevious(h_elem)


class TestGetMethods:
    @empty_signature_tester(
        _Element.getparent,
        _Element.getprevious,
        _Element.getnext,
        _Element.getroottree,
    )
    def test_func_sig(self) -> None:
        pass

    def test_getparent_method(self, xml2_root: _Element) -> None:
        root = xml2_root

        nada = root.getparent()
        reveal_type(nada)
        assert nada is None

        elem = root[0].getparent()
        reveal_type(elem)
        assert elem is root

    def test_getprevious_method(self, xml2_root: _Element) -> None:
        root = xml2_root

        nada = root[0].getprevious()
        reveal_type(nada)
        assert nada is None

        elem = root[-1].getprevious()
        reveal_type(elem)

    def test_getnext_method(self, xml2_root: _Element) -> None:
        root = xml2_root

        elem = root[0].getnext()
        reveal_type(elem)

        nada = root[-1].getnext()
        reveal_type(nada)
        assert nada is None

    def test_getroottree_method(self, xml2_root: _Element) -> None:
        root = xml2_root

        tree2 = root.getroottree()
        reveal_type(tree2)


class TestIterMethods:
    @signature_tester(_Element.iter, (
        ("tag" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_iter_method(self, xml2_root: _Element) -> None:
        root = xml2_root

        itr = root.iter()
        reveal_type(itr)
        result: list[_Element] = []
        for e in itr:
            reveal_type(e)
            result.append(e)
        del itr

        itr = root.iter(None)
        reveal_type(itr)
        assert result == [e for e in itr]
        del itr, result

        itr = root.iter("title")
        reveal_type(itr)
        result = [e for e in itr]
        assert len(result) == 2
        del itr

        itr = root.iter(tag=b"title")
        reveal_type(itr)
        assert result == [e for e in itr]
        del itr, result

        itr = root.iter(QName("price", None))
        reveal_type(itr)
        assert len([e for e in itr]) == 2
        del itr

        itr = root.iter("quantity", etree.Comment)
        reveal_type(itr)
        result = [e for e in itr]
        assert len(result) == 3
        del itr

        itr = root.iter({"quantity", etree.Comment})
        assert result == [e for e in itr]
        del itr, result

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with pytest.raises(TypeError, match=r"object is not iterable"):
                _ = root.iter(cast(Any, arg))

    @signature_tester(_Element.iterancestors, (
        ("tag" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_iterancestors_method(self, svg_root: _Element) -> None:
        root = svg_root
        child = root[0]
        grandchild = child[0]

        itr = grandchild.iterancestors()
        reveal_type(itr)
        result: list[_Element] = []
        for e in itr:
            reveal_type(e)
            result.append(e)
        assert len(result) == 2
        del itr

        itr = grandchild.iterancestors(None)
        reveal_type(itr)
        assert result == [e for e in itr]
        del itr

        itr = child.iterancestors()
        reveal_type(itr)
        assert result[1:] == [e for e in itr]
        del itr

        itr = grandchild.iterancestors(tag=child.tag)
        reveal_type(itr)
        assert result[:1] == [e for e in itr]
        del itr

        itr = grandchild.iterancestors(str(child.tag).encode(), root.tag)
        reveal_type(itr)
        assert result == [e for e in itr]
        del itr, result

        itr = root.iter(etree.Comment)
        comm = next(itr)
        del itr
        itr = comm.iterancestors([QName(grandchild.tag), child.tag])
        reveal_type(itr)
        result = [e for e in itr]
        assert len(result) == 2
        del itr, result

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with pytest.raises(TypeError, match=r"object is not iterable"):
                _ = child.iterancestors(cast(Any, arg))

    # iterdescendants() is iter() sans root node, so the
    # test is identical
    @signature_tester(_Element.iterdescendants, (
        ("tag" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_iterdescendants_method(self, xml2_root: _Element) -> None:
        root = xml2_root

        itr = root.iterdescendants()
        reveal_type(itr)
        result: list[_Element] = []
        for e in itr:
            reveal_type(e)
            result.append(e)
        del itr

        itr = root.iterdescendants(None)
        reveal_type(itr)
        assert result == [e for e in itr]
        del itr, result

        itr = root.iterdescendants("title")
        reveal_type(itr)
        result = [e for e in itr]
        assert len(result) == 2
        del itr

        itr = root.iterdescendants(tag=b"title")
        reveal_type(itr)
        assert result == [e for e in itr]
        del itr, result

        itr = root.iterdescendants(QName("price", None))
        reveal_type(itr)
        assert len([e for e in itr]) == 2
        del itr

        itr = root.iterdescendants("quantity", etree.Comment)
        reveal_type(itr)
        result = [e for e in itr]
        assert len(result) == 3
        del itr

        itr = root.iterdescendants({"quantity", etree.Comment})
        assert result == [e for e in itr]
        del itr, result

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with pytest.raises(TypeError, match=r"object is not iterable"):
                _ = root.iterdescendants(cast(Any, arg))

    @signature_tester(_Element.itersiblings, (
        ("tag"      , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags"     , Parameter.VAR_POSITIONAL       , Parameter.empty),
        ("preceding", Parameter.KEYWORD_ONLY         , False          ),
    ))  # fmt: skip
    def test_itersiblings_method(self, svg_root: _Element) -> None:
        root = svg_root

        child = root[1]
        result: list[_Element] = []
        itr = child.itersiblings()
        reveal_type(itr)
        for e in itr:
            reveal_type(e)
            result.append(e)
        del itr

        itr = child.itersiblings(None)
        reveal_type(itr)
        assert result == [e for e in itr]
        del itr

        # Preceding param is a truthy/falsy value,
        # impossible to validate its accepted type.
        itr = child.itersiblings(preceding=True)
        reveal_type(itr)
        assert len([e for e in itr]) == 1
        del itr

        itr = child.itersiblings("metadata")
        reveal_type(itr)
        assert result[2:3] == [e for e in itr]
        del itr

        itr = child.itersiblings(tag=b"metadata")
        reveal_type(itr)
        assert result[2:3] == [e for e in itr]
        del itr

        qn = QName("desc")
        itr = child.itersiblings(qn)
        reveal_type(itr)
        assert result[1:2] == [e for e in itr]
        del itr

        itr = child.itersiblings(etree.Comment)
        reveal_type(itr)
        assert result[:1] == [e for e in itr]
        del itr

        itr = child.itersiblings("style", etree.Comment)
        reveal_type(itr)
        assert [e for e in itr] == [
            e for e in result if e.tag in {"style", etree.Comment}
        ]
        del itr

        itr = child.itersiblings({etree.Comment, "g"})
        reveal_type(itr)
        assert [e for e in itr] == [e for e in result if e.tag in {etree.Comment, "g"}]
        del itr, result

        itr = child.itersiblings("metadata", "g", preceding=True)
        reveal_type(itr)
        assert len([e for e in itr]) == 0
        del itr

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with pytest.raises(TypeError, match=r"object is not iterable"):
                _ = child.itersiblings(cast(Any, arg))

    @signature_tester(_Element.iterchildren, (
        ("tag"     , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags"    , Parameter.VAR_POSITIONAL       , Parameter.empty),
        ("reversed", Parameter.KEYWORD_ONLY         , False          ),
    ))  # fmt: skip
    def test_iterchildren_method(self, xml2_root: _Element) -> None:
        root = xml2_root

        itr = root.iterchildren()
        reveal_type(itr)
        result = [e for e in itr]
        del itr

        itr = root.iterchildren(None)
        reveal_type(itr)
        assert result == [e for e in itr]
        del itr

        # Reversed param is a truthy/falsy value,
        # impossible to validate its accepted type.
        itr = root.iterchildren(reversed=True)
        reveal_type(itr)
        assert list(reversed(result)) == [e for e in itr]
        del itr

        itr = root.iterchildren(root[2].tag)
        reveal_type(itr)
        assert result[2:3] == [e for e in itr]
        del itr

        itr = root.iterchildren(tag=str(root[2].tag).encode())
        reveal_type(itr)
        assert result[2:3] == [e for e in itr]
        del itr

        qn = QName(root[-1].tag)
        itr = root.iterchildren(qn)
        reveal_type(itr)
        assert result[-2:] == [e for e in itr]
        del itr

        itr = root.iterchildren(etree.Comment)
        reveal_type(itr)
        assert result[1] == next(itr)
        del itr

        itr = root.iterchildren(qn, etree.Comment)
        reveal_type(itr)
        assert len([e for e in itr]) == 3
        del itr

        itr = root.iterchildren({str(root[0].tag), etree.Comment}, reversed=True)
        reveal_type(itr)
        assert next(itr) == result[1]
        assert next(itr) == result[0]
        del itr, result

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with pytest.raises(TypeError, match=r"object is not iterable"):
                _ = root.iterchildren(cast(Any, arg))

    @signature_tester(_Element.itertext, (
        ("tag"      , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags"     , Parameter.VAR_POSITIONAL       , Parameter.empty),
        ("with_tail", Parameter.KEYWORD_ONLY         , True           ),
    ))  # fmt: skip
    def test_itertext_method(self, xml2_root: _Element) -> None:
        root = xml2_root

        itr = root.itertext()
        result: list[str] = []
        reveal_type(itr)
        for s in itr:
            reveal_type(s)
            result.append(s)
        del itr

        itr = root.itertext(None)
        reveal_type(itr)
        assert result == [s for s in itr]
        del itr

        # with_tail param is a truthy/falsy value,
        # impossible to validate its accepted type.
        itr = root.itertext(with_tail=False)
        reveal_type(itr)
        assert len(result) != len([s for s in itr])
        del itr, result

        itr = root.itertext("title")
        reveal_type(itr)
        result = [s for s in itr]
        del itr

        itr = root.itertext(tag=b"title")
        reveal_type(itr)
        assert result == [s for s in itr]
        del itr, result

        qn = QName("address")
        itr = root.itertext(qn)
        reveal_type(itr)
        reveal_type(next(itr))
        del itr

        itr = root.itertext(etree.Comment)
        reveal_type(itr)
        reveal_type(next(itr))
        del itr

        itr = root.itertext(qn, etree.Comment)
        reveal_type(itr)
        result = [s for s in itr]
        del itr

        itr = root.itertext({qn, etree.Comment})
        reveal_type(itr)
        assert result == [s for s in itr]
        del itr, result

        itr = root.itertext(tag={"quantity", "price"}, with_tail=False)
        reveal_type(itr)
        reveal_type(next(itr))
        del itr

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with pytest.raises(TypeError, match=r"object is not iterable"):
                _ = root.itertext(cast(Any, arg))
