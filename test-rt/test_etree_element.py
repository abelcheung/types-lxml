from __future__ import annotations

from copy import deepcopy
from inspect import Parameter
from random import randrange
from typing import Any, cast

import _testutils
import pytest
from lxml.etree import (
    LXML_VERSION,
    Comment,
    Entity,
    ProcessingInstruction,
    _Element,
    _ElementTree,
)
from lxml.html import Element as h_Element

reveal_type = getattr(_testutils, "reveal_type_wrapper")


class TestBasicBehavior:
    def test_sequence_read(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())

        reveal_type(len(elem))
        length = len(elem)
        reveal_type(elem[randrange(length)])
        # fmt: off
        reveal_type(elem[: 2])  # ast: why the space???
        # fmt: on

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

        del elem[0]
        assert elem.index(subelem) == 2
        del elem[0:2]
        assert elem.index(subelem) == 0

        with pytest.raises(TypeError, match="cannot be interpreted as an integer"):
            _ = elem["0"]  # pyright: ignore

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

    # fmt: off
    @_testutils.signature_tester(_Element.index, (
        None,
        ("child", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("start", Parameter.POSITIONAL_OR_KEYWORD,
            None if LXML_VERSION >= (5, 0) else Parameter.empty),
        ("stop" , Parameter.POSITIONAL_OR_KEYWORD,
            None if LXML_VERSION >= (5, 0) else Parameter.empty),
    ))
    # fmt: on
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

    # fmt: off
    @_testutils.signature_tester(_Element.append, (
        None,
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))
    # fmt: on
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

    # fmt: off
    @_testutils.signature_tester(_Element.insert, (
        None,
        ("index"  , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))
    # fmt: on
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

    # fmt: off
    @_testutils.signature_tester(_Element.remove, (
        None,
        ("element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))
    # fmt: on
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

    # fmt: off
    @_testutils.signature_tester(_Element.replace, (
        None,
        ("old_element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("new_element", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))
    # fmt: on
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

    # fmt: off
    @_testutils.signature_tester(_Element.extend, (
        None,
        ("elements", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))
    # fmt: on
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

    # fmt: off
    @_testutils.signature_tester(_Element.clear, (
        None,
        ("keep_tail", Parameter.POSITIONAL_OR_KEYWORD,
            False if LXML_VERSION >= (5, 0) else Parameter.empty),
    ))
    # fmt: on
    def test_method_clear(self, xml_tree: _ElementTree) -> None:
        elem = deepcopy(xml_tree.getroot())
        elem.clear()
        assert len(elem) == 0
        del elem

        elem = deepcopy(xml_tree.getroot())
        elem.tail = "junk"
        elem.clear(keep_tail=True)
        assert len(elem) == 0
