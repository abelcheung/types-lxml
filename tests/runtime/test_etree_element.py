from __future__ import annotations

import sys
from inspect import Parameter
from typing import Any, cast

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

from ._testutils import signature_tester
from ._testutils.errors import (
    raise_non_iterable,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


# See mypy.ini in testsuite for explanation
TC_HONORS_REVERSED = True


class TestIterMethods:
    @signature_tester(_Element.iter, (
        ("tag" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_iter_method(self, xml2_root: _Element) -> None:
        itr = reveal_type(xml2_root.iter())
        result = reveal_type([e for e in itr])
        del itr

        itr = reveal_type(xml2_root.iter(None))
        assert result == [e for e in itr]
        del itr

        itr = reveal_type(xml2_root.iter("title"))
        result = [e for e in itr if e.tag == "title"]
        del itr

        itr = reveal_type(xml2_root.iter(tag=b"title"))
        result = [e for e in itr if e.tag == "title"]
        del itr, result

        itr = reveal_type(xml2_root.iter(QName("price", None)))
        result = [e for e in itr if e.tag == "price"]
        del itr

        itr = reveal_type(xml2_root.iter("quantity", etree.Comment))
        result = [e for e in itr if e.tag in {"quantity", etree.Comment}]
        del itr

        itr = xml2_root.iter({"quantity", etree.Comment})
        assert result == [e for e in itr if e.tag in {"quantity", etree.Comment}]
        del itr, result

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with raise_non_iterable:
                _ = xml2_root.iter(cast(Any, arg))

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
            with raise_non_iterable:
                _ = child.iterancestors(cast(Any, arg))

    # iterdescendants() is iter() sans root node, so the
    # test is identical
    @signature_tester(_Element.iterdescendants, (
        ("tag" , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ("tags", Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_iterdescendants_method(self, xml2_root: _Element) -> None:
        itr = reveal_type(xml2_root.iterdescendants())
        result = [e for e in itr]
        reveal_type(result)
        del itr

        itr = reveal_type(xml2_root.iterdescendants(None))
        assert result == [e for e in itr]
        del itr

        itr = reveal_type(xml2_root.iterdescendants("title"))
        assert [e for e in itr] == [e for e in result if e.tag == "title"]
        del itr

        itr = reveal_type(xml2_root.iterdescendants(tag=b"title"))
        assert [e for e in itr] == [e for e in result if e.tag == "title"]
        del itr

        itr = reveal_type(xml2_root.iterdescendants(QName("price", None)))
        assert [e for e in itr] == [e for e in result if e.tag == "price"]
        del itr

        itr = reveal_type(xml2_root.iterdescendants("quantity", etree.Comment))
        assert [e for e in itr] == [
            e for e in result if e.tag in {"quantity", etree.Comment}
        ]
        del itr

        # FIXME Bug in AST parser, set braces disappeared
        itr = xml2_root.iterdescendants({"quantity", etree.Comment})
        reveal_type(itr)
        assert [e for e in itr] == [
            e for e in result if e.tag in {"quantity", etree.Comment}
        ]
        del itr, result

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with raise_non_iterable:
                _ = xml2_root.iterdescendants(cast(Any, arg))

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
            with raise_non_iterable:
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
        assert result[-3:] == [e for e in itr]
        del itr

        itr = root.iterchildren(etree.Comment)
        reveal_type(itr)
        assert result[1] == next(itr)
        del itr

        itr = root.iterchildren(qn, etree.Comment)
        reveal_type(itr)
        assert len([e for e in itr]) == 4
        del itr

        itr = root.iterchildren({str(root[0].tag), etree.Comment}, reversed=True)
        reveal_type(itr)
        assert next(itr) == result[1]
        assert next(itr) == result[0]
        del itr, result

        for arg in (1, object(), etree.iselement, ["foo", 1]):
            with raise_non_iterable:
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
            with raise_non_iterable:
                _ = root.itertext(cast(Any, arg))
