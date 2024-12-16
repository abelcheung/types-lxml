from __future__ import annotations

import sys
from copy import deepcopy
from inspect import Parameter
from random import randrange
from types import MappingProxyType
from typing import Any, BinaryIO, cast

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

from . import _testutils

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


# See mypy.ini in testsuite for explanation
TC_HONORS_REVERSED = True


class TestBasicBehavior:
    def test_sequence_read(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)

        reveal_type(len(elem))
        length = len(elem)
        reveal_type(elem[randrange(length)])
        reveal_type(elem[: 2])  # fmt: skip  # ast: why the space???

        itr = iter(elem)
        reveal_type(itr)
        item = next(itr)
        reveal_type(item)
        assert elem.index(item) == 0
        del itr, item

        if TC_HONORS_REVERSED:
            rev = reversed(elem)
        else:
            rev = elem.__reversed__()
        reveal_type(rev)
        item = next(rev)
        reveal_type(item)
        assert elem.index(item) == length - 1
        del rev, item

        for sub in elem:
            reveal_type(sub)

        subelem = elem[3]
        reveal_type(subelem in elem)
        o = object()
        reveal_type(o in elem)

        with pytest.raises(TypeError, match="cannot be interpreted as an integer"):
            _ = elem[cast(int, "0")]

        del elem, subelem

    def test_sequence_modify(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)

        subelem = elem[3]
        del elem[0]
        assert elem.index(subelem) == 2
        del elem[0:2]
        assert elem.index(subelem) == 0

        comment = etree.Comment("comment")
        comment2 = etree.Comment("foo")
        entity = etree.Entity("foo")
        pi = etree.ProcessingInstruction("target", "text")
        div = h_Element("div")

        elem[1] = comment
        assert len(elem) == 2
        elem[2:4] = (entity, pi)
        assert len(elem) == 4
        # Actually permitted, just that elements are
        # added in random order. This is undesirable so
        # not supported in stub.
        elem[4:] = {div, comment2}  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]
        assert len(elem) == 6

        for obj in (object(), 0, "", (subelem,), {subelem}):
            with pytest.raises(TypeError, match=r"Cannot convert \w+ to .+\._Element"):
                elem[0] = cast(Any, obj)
        with pytest.raises(ValueError, match="cannot assign None"):
            elem[0] = cast(Any, None)
        with pytest.raises(ValueError, match="cannot assign None"):
            elem[:] = cast(Any, None)

        # test broken behavior: elem[slice] = single_elem
        # It returns successfully, just that elements are
        # silently discarded without adding new ones
        elem[:] = comment  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]
        assert len(elem) == 0

        del subelem, comment, comment2, entity, pi, div, elem

    @_testutils.signature_tester(_Element.index, (
        ("child", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("start", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("stop" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_index(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)
        subelem = elem[3]

        pos = elem.index(subelem)
        reveal_type(pos)
        del pos
        with pytest.raises(ValueError, match="x not in slice"):
            _ = elem.index(subelem, len(elem) - 1, len(elem) - 1)

        for obj in (0, None, "", object(), (elem[-1],)):
            with pytest.raises(TypeError, match="Argument 'child' has incorrect type"):
                _ = elem.index(cast(Any, obj))

        for obj in ("1", (0,), object()):
            if etree.LXML_VERSION >= (5, 1):
                match_re = "Argument 'start' has incorrect type"
            else:
                match_re = "cannot be interpreted as an integer"
            with pytest.raises(TypeError, match=match_re):
                _ = elem.index(subelem, cast(Any, obj))

            if etree.LXML_VERSION >= (5, 1):
                match_re = "Argument 'stop' has incorrect type"
            else:
                match_re = "cannot be interpreted as an integer"
            with pytest.raises(TypeError, match=match_re):
                _ = elem.index(subelem, None, cast(Any, obj))

        del elem, subelem

    @_testutils.signature_tester(_Element.append, (
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_append(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)
        subelem = deepcopy(elem[-1])
        length = len(elem)

        assert elem.append(subelem) is None
        assert len(elem) == length + 1

        for obj in (0, None, "", object(), (elem[-1],)):
            with pytest.raises(
                TypeError, match="Argument 'element' has incorrect type"
            ):
                elem.append(cast(Any, obj))

        del elem, subelem

    @_testutils.signature_tester(_Element.insert, (
        ("index"  , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_insert(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)
        comment = etree.Comment("comment")
        pos = randrange(len(elem))
        assert elem.insert(pos, comment) is None
        assert elem.index(comment) == pos

        for obj in (0, None, "", object(), (elem[-1],)):
            with pytest.raises(
                TypeError, match="Argument 'element' has incorrect type"
            ):
                elem.insert(pos, cast(Any, obj))

        for obj in (None, "1", (0,), object()):
            if etree.LXML_VERSION >= (5, 1):
                match_re = "Argument 'index' has incorrect type"
            else:
                match_re = "cannot be interpreted as an integer"
            with pytest.raises(TypeError, match=match_re):
                elem.insert(cast(Any, obj), comment)

        del elem, comment

    @_testutils.signature_tester(_Element.remove, (
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_remove(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)
        assert elem.remove(elem[-1]) is None

        # Can construct a new node and fail removing it, but that is
        # pure runtime behavior and doesn't violate method annotation
        for obj in (0, None, "", object(), (elem[-1],)):
            with pytest.raises(
                TypeError, match="Argument 'element' has incorrect type"
            ):
                elem.remove(cast(Any, obj))

        del elem

    @_testutils.signature_tester(_Element.replace, (
        ("old_element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("new_element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_replace(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)
        subelem = elem[-1]
        new_elem = deepcopy(subelem)
        new_elem.tag = "foo"
        assert elem.replace(subelem, new_elem) is None

        for obj in (0, None, "", object(), (elem[-1],)):
            with pytest.raises(
                TypeError, match="Argument 'old_element' has incorrect type"
            ):
                elem.replace(cast(Any, obj), elem[-1])
            with pytest.raises(
                TypeError, match="Argument 'new_element' has incorrect type"
            ):
                elem.replace(elem[-1], cast(Any, obj))

        del new_elem, subelem, elem

    @_testutils.signature_tester(_Element.extend, (
        ("elements", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_extend(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)
        new_elem1 = etree.Comment("foo")
        new_elem2 = etree.Entity("foo")
        assert elem.extend([new_elem1]) is None

        elem.extend([new_elem1, new_elem2])
        elem.extend((new_elem1, new_elem2))

        # test broken behavior (but no exception though)
        elem.extend(elem[0])  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]

        for obj in (None, 0):
            with pytest.raises(TypeError, match="is not iterable"):
                elem.extend(cast(Any, obj))

        for obj2 in ("abc", (0,)):
            with pytest.raises(TypeError, match=r"Cannot convert \w+ to .+\._Element"):
                elem.extend(cast(Any, obj2))

    @_testutils.signature_tester(_Element.clear, (
        ("keep_tail", Parameter.POSITIONAL_OR_KEYWORD, False),
    ))  # fmt: skip
    def test_method_clear(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)
        elem.clear()
        assert len(elem) == 0
        del elem

        elem = deepcopy(xml2_root)
        elem.tail = "junk"
        elem.clear(keep_tail=True)
        assert len(elem) == 0


class TestProperties:
    def test_ro_properties(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)

        for subelem in elem:
            if type(subelem) is not _Element:
                continue
            reveal_type(subelem.attrib)
            reveal_type(subelem.prefix)
            reveal_type(subelem.nsmap)
            reveal_type(subelem.sourceline)

        with pytest.raises(AttributeError, match="objects is not writable"):
            elem.attrib = cast(Any, elem.attrib)  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]

        with pytest.raises(AttributeError, match="objects is not writable"):
            elem.prefix = cast(Any, elem.prefix)  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]

        with pytest.raises(AttributeError, match="objects is not writable"):
            elem.nsmap = cast(Any, elem.nsmap)  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]

        # Not performing test for .sourceline ! We pretend it is not
        # changeable in stub, but actually it is read-write

        del elem

    def test_rw_properties(self, xml2_root: _Element) -> None:
        elem = deepcopy(xml2_root)

        for subelem in elem:
            if type(subelem) is not _Element:
                continue
            reveal_type(subelem.base)
            reveal_type(subelem.tag)
            reveal_type(subelem.text)
            reveal_type(subelem.tail)

        cdata = etree.CDATA("foo")
        qname = QName("dummyns", "dummytext")

        elem.base = "http://dummy.site/"
        elem.base = None
        elem.base = b"http://dummy.site/"
        for data1 in (1, cdata, qname):
            with pytest.raises(TypeError, match="must be string or unicode"):
                elem.base = cast(Any, data1)

        elem.tag = "foo"
        elem.tag = b"foo"
        elem.tag = qname
        for data2 in (None, 1, cdata):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                elem.tag = cast(Any, data2)

        elem.text = "sometext"
        elem.text = None
        elem.text = b"sometext"
        elem.text = cdata
        elem.text = qname
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            elem.text = cast(Any, 1)

        elem.tail = "sometail"
        elem.tail = None
        elem.tail = b"sometail"
        elem.tail = cdata
        for data in (1, qname):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                elem.tail = cast(Any, data)

        del elem


class TestContentOnlyElement:
    @_testutils.signature_tester(etree.Comment, (
        ("text", Parameter.POSITIONAL_OR_KEYWORD, None),
    ))  # fmt: skip
    def test_construct_comment(self) -> None:
        comm = etree.Comment()
        reveal_type(comm)
        del comm

        for text in (None, "foo", b"foo"):
            comm = etree.Comment(text)
            reveal_type(comm)
            del comm

        for data in (1, ["foo"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = etree.Comment(cast(Any, data))

    @_testutils.signature_tester(etree.Entity, (
        ("name", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_construct_entity(self) -> None:
        for name in ("foo", b"foo"):
            ent = etree.Entity(name)
            reveal_type(ent)
            del ent

        for data in (None, 1, ["foo"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = etree.Entity(cast(Any, data))

    @_testutils.signature_tester(etree.ProcessingInstruction, (
        ("target", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("text"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_construct_pi(self) -> None:
        for target in ("foo", b"foo"):
            pi = etree.ProcessingInstruction(target)
            reveal_type(pi)
            del pi

        for data in (None, 1, ["foo"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = etree.ProcessingInstruction(cast(Any, data))

        for text in ("bar", b"bar"):
            pi = etree.ProcessingInstruction("foo", text)
            reveal_type(pi)
            del pi

        for data in (1, ["bar"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = etree.ProcessingInstruction("foo", cast(Any, data))


class TestAttribAccessMethods:
    @_testutils.empty_signature_tester(
        _Element.keys,
        _Element.values,
        _Element.items,
    )
    def test_method_keyval(self, bightml_bin_fp: BinaryIO) -> None:
        parser = etree.HTMLParser()
        with bightml_bin_fp as f:
            doc = etree.parse(f, parser=parser)
        for elem in doc.iter():
            if type(elem) is not _Element:
                continue
            reveal_type(elem.keys())
            reveal_type(elem.values())
            reveal_type(elem.items())

    @_testutils.signature_tester(_Element.get, (
        ("key"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_get(self, svg_root: _Element) -> None:
        root = svg_root

        reveal_type(root.get("width"))
        reveal_type(root.get("somejunk"))
        reveal_type(root.get(b"width"))
        # Not meaningful to use QName here, but still
        qname = QName(None, "width")
        reveal_type(root.get(qname))

        for arg in (1, object(), ["width"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = root.get(cast(Any, arg))

        reveal_type(root.get("width", 0))
        reveal_type(root.get("somejunk", (0, "foo")))

    @_testutils.signature_tester(_Element.set, (
        ("key"  , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("value", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_set(self, xml2_root: _Element) -> None:
        root = deepcopy(xml2_root)

        assert root.set("foo", "bar") is None

        qname = QName("foo")
        for arg1 in ("foo", b"foo", qname):
            root.set(arg1, "bar")
        for arg2 in (None, 1, object(), ["foo"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                root.set(cast(Any, arg2), "bar")

        qname = QName("bar")
        for arg3 in ("bar", b"bar", qname):
            root.set("foo", arg3)
        for arg4 in (None, 1, object(), ["bar"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                root.set("foo", cast(Any, arg4))


# The find*() methods of _Element are all derivations of
# iterfind(). So they almost have same arguments, and even
# the other test contents look very similar.
class TestFindMethods:
    @_testutils.signature_tester(_Element.iterfind, (
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

    @_testutils.signature_tester(_Element.find, (
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

    @_testutils.signature_tester(_Element.findall, (
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

    @_testutils.signature_tester(_Element.findtext, (
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
    @_testutils.signature_tester(
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

    @_testutils.signature_tester(
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
    @_testutils.empty_signature_tester(
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
    @_testutils.signature_tester(_Element.iter, (
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

    @_testutils.signature_tester(_Element.iterancestors, (
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
    @_testutils.signature_tester(_Element.iterdescendants, (
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

    @_testutils.signature_tester(_Element.itersiblings, (
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

    @_testutils.signature_tester(_Element.iterchildren, (
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

    @_testutils.signature_tester(_Element.itertext, (
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
