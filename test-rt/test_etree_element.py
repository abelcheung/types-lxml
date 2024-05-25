from __future__ import annotations

from copy import deepcopy
from inspect import Parameter
from pathlib import Path
from random import randrange
from typing import Any, cast

import _testutils
import pytest
from lxml.etree import (
    CDATA,
    LXML_VERSION,
    Comment,
    Entity,
    HTMLParser,
    ProcessingInstruction,
    QName,
    _Attrib as _Attrib,
    _Comment as _Comment,
    _Element,
    _ElementTree,
    _Entity as _Entity,
    _ProcessingInstruction as _ProcessingInstruction,
    parse,
)
from lxml.html import Element as h_Element

reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestBasicBehavior:
    def test_sequence_read(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())

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

        rev = reversed(elem)
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

    def test_sequence_modify(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())

        subelem = elem[3]
        del elem[0]
        assert elem.index(subelem) == 2
        del elem[0:2]
        assert elem.index(subelem) == 0

        comment = Comment("comment")
        comment2 = Comment("foo")
        entity = Entity("foo")
        pi = ProcessingInstruction("target", "text")
        div = h_Element("div")

        elem[1] = comment
        assert len(elem) == 2
        elem[2:4] = (entity, pi)
        assert len(elem) == 4
        # Actually permitted, just that elements are
        # added in random order. This is undesirable so
        # not supported in stub.
        elem[4:] = {div, comment2}  # pyright: ignore
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
        elem[:] = comment  # pyright: ignore
        assert len(elem) == 0

        del subelem, comment, comment2, entity, pi, div, elem

    @_testutils.signature_tester(_Element.index, (
        ("child", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("start", Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("stop" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_index(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())
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
            if LXML_VERSION >= (5, 1):
                match_re = "Argument 'start' has incorrect type"
            else:
                match_re = "cannot be interpreted as an integer"
            with pytest.raises(TypeError, match=match_re):
                _ = elem.index(subelem, cast(Any, obj))

            if LXML_VERSION >= (5, 1):
                match_re = "Argument 'stop' has incorrect type"
            else:
                match_re = "cannot be interpreted as an integer"
            with pytest.raises(TypeError, match=match_re):
                _ = elem.index(subelem, None, cast(Any, obj))

        del elem, subelem

    @_testutils.signature_tester(_Element.append, (
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_append(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())
        subelem = deepcopy(elem[-1])
        length = len(elem)

        result = elem.append(subelem)
        reveal_type(result)
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
    def test_method_insert(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())
        comment = Comment("comment")
        pos = randrange(len(elem))
        result = elem.insert(pos, comment)
        reveal_type(result)
        assert elem.index(comment) == pos

        for obj in (0, None, "", object(), (elem[-1],)):
            with pytest.raises(
                TypeError, match="Argument 'element' has incorrect type"
            ):
                elem.insert(pos, cast(Any, obj))

        for obj in (None, "1", (0,), object()):
            if LXML_VERSION >= (5, 1):
                match_re = "Argument 'index' has incorrect type"
            else:
                match_re = "cannot be interpreted as an integer"
            with pytest.raises(TypeError, match=match_re):
                elem.insert(cast(Any, obj), comment)

        del elem, comment

    @_testutils.signature_tester(_Element.remove, (
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_remove(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())
        result = elem.remove(elem[-1])
        reveal_type(result)

        # Can construct a new node and fail removing it, but that is
        # pure runtime behavior and doesn't violate method annotation
        for obj in (0, None, "", object(), (elem[-1],)):
            with pytest.raises(
                TypeError, match="Argument 'element' has incorrect type"
            ):
                _ = elem.remove(cast(Any, obj))

        del elem

    @_testutils.signature_tester(_Element.replace, (
        ("old_element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("new_element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_method_replace(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())
        subelem = elem[-1]
        new_elem = deepcopy(subelem)
        new_elem.tag = "foo"
        result = elem.replace(subelem, new_elem)
        reveal_type(result)

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
    def test_method_extend(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())
        new_elem1 = Comment("foo")
        new_elem2 = Entity("foo")
        result = elem.extend([new_elem1])
        reveal_type(result)

        elem.extend([new_elem1, new_elem2])
        elem.extend((new_elem1, new_elem2))

        # test broken behavior (but no exception though)
        elem.extend(elem[0])  # pyright: ignore

        for obj in (None, 0):
            with pytest.raises(TypeError, match="is not iterable"):
                elem.extend(cast(Any, obj))

        for obj in ("abc", (0,)):
            with pytest.raises(TypeError, match=r"Cannot convert \w+ to .+\._Element"):
                elem.extend(cast(Any, obj))

    @_testutils.signature_tester(_Element.clear, (
        ("keep_tail", Parameter.POSITIONAL_OR_KEYWORD, False),
    ))  # fmt: skip
    def test_method_clear(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())
        elem.clear()
        assert len(elem) == 0
        del elem

        elem = deepcopy(xml_tree.getroot())
        elem.tail = "junk"
        elem.clear(keep_tail=True)
        assert len(elem) == 0


class TestProperties:
    def test_ro_properties(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())

        for subelem in elem:
            if type(subelem) != _Element:
                continue
            reveal_type(subelem.attrib)
            reveal_type(subelem.prefix)
            reveal_type(subelem.nsmap)
            reveal_type(subelem.sourceline)

        with pytest.raises(AttributeError, match="objects is not writable"):
            elem.attrib = elem.attrib  # pyright: ignore

        with pytest.raises(AttributeError, match="objects is not writable"):
            elem.prefix = elem.prefix  # pyright: ignore

        with pytest.raises(AttributeError, match="objects is not writable"):
            elem.nsmap = elem.nsmap  # pyright: ignore

        # Not performing test for .sourceline ! We pretend it is not
        # changeable in stub, but actually it is read-write

        del elem

    def test_rw_properties(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())

        for subelem in elem:
            if type(subelem) != _Element:
                continue
            reveal_type(subelem.base)
            reveal_type(subelem.tag)
            reveal_type(subelem.text)
            reveal_type(subelem.tail)

        cdata = CDATA("foo")
        qname = QName("dummyns", "dummytext")

        elem.base = b"http://dummy.site/"
        elem.base = "http://dummy.site/"
        elem.base = None
        for data in (1, cdata, qname):
            with pytest.raises(TypeError, match="must be string or unicode"):
                elem.base = cast(Any, data)

        elem.tag = b"foo"
        elem.tag = "foo"
        elem.tag = qname
        for data in (None, 1, cdata):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                elem.tag = cast(Any, data)

        elem.text = b"sometext"
        elem.text = "sometext"
        elem.text = None
        elem.text = cdata
        elem.text = qname
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            elem.text = cast(Any, 1)

        elem.tail = b"sometail"
        elem.tail = "sometail"
        elem.tail = None
        elem.tail = cdata
        for data in (1, qname):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                elem.tail = cast(Any, data)

        del elem


class TestContentOnlyElement:
    @_testutils.signature_tester(Comment, (
        ("text", Parameter.POSITIONAL_OR_KEYWORD, None),
    ))  # fmt: skip
    def test_construct_comment(self) -> None:
        comm = Comment()
        reveal_type(comm)
        del comm

        for text in (None, "foo", b"foo"):
            comm = Comment(text)
            reveal_type(comm)
            del comm

        for data in (1, ["foo"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = Comment(cast(Any, data))

    @_testutils.signature_tester(Entity, (
        ("name", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_construct_entity(self) -> None:
        for name in ("foo", b"foo"):
            ent = Entity(name)
            reveal_type(ent)
            del ent

        for data in (None, 1, ["foo"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = Entity(cast(Any, data))

    @_testutils.signature_tester(ProcessingInstruction, (
        ("target", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("text"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_construct_pi(self) -> None:
        for target in ("foo", b"foo"):
            pi = ProcessingInstruction(target)
            reveal_type(pi)
            del pi

        for data in (None, 1, ["foo"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = ProcessingInstruction(cast(Any, data))

        for text in ("bar", b"bar"):
            pi = ProcessingInstruction("foo", text)
            reveal_type(pi)
            del pi

        for data in (1, ["bar"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                _ = ProcessingInstruction("foo", cast(Any, data))


class TestAttribAccessMethods:
    @_testutils.empty_signature_tester(
        _Element.keys,
        _Element.values,
        _Element.items,
    )
    def test_method_keyval(self, h1_filepath: Path) -> None:
        parser = HTMLParser()
        doc = parse(h1_filepath, parser=parser)
        for elem in doc.iter():
            if type(elem) != _Element:
                continue
            reveal_type(elem.keys())
            reveal_type(elem.values())
            reveal_type(elem.items())

    @_testutils.signature_tester(_Element.get, (
        ("key"    , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("default", Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_method_get(self, x1_filepath: Path) -> None:
        tree = parse(x1_filepath)
        root = tree.getroot()

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
    def test_method_set(self, xml_tree: _ElementTree) -> None:
        root = deepcopy(xml_tree.getroot())

        result = root.set("foo", "bar")
        reveal_type(result)

        qname = QName("foo")
        for arg in ("foo", b"foo", qname):
            root.set(arg, "bar")
        for arg in (None, 1, object(), ["foo"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                root.set(cast(Any, arg), "bar")

        qname = QName("bar")
        for arg in ("bar", b"bar", qname):
            root.set("foo", arg)
        for arg in (None, 1, object(), ["bar"]):
            with pytest.raises(TypeError, match="must be bytes or unicode"):
                root.set("foo", cast(Any, arg))
