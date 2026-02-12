#
# This test file attempts to verify function / method annotations are
# correct, so try NOT to add any type-ignores to this file.
#

import sys

import pytest
import typeguard
from lxml.etree import (
    LXML_VERSION,
    Comment,
    Element,
    ElementTree,
    QName as QName,
    _Element,
    _ElementTree,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestElementFactory:
    # lxml.etree.is_element() exists, but we want to test the
    # then-factory Element class instead of _Element
    def _is_element_check(self, el: Element) -> None:
        reveal_type(el)
        if LXML_VERSION >= (6, 0, 0):
            assert isinstance(el, Element)
        else:
            assert isinstance(el, _Element)
        if type(el) is not _Element:
            # TODO revealtype injector needs to support functiontype
            with pytest.raises(typeguard.TypeCheckError):
                reveal_type(el.tag)
        else:
            reveal_type(el.tag)

    def test_normal_element(self) -> None:
        el = Element("test")
        self._is_element_check(el)

    def test_comment_element(self) -> None:
        comm = Comment("test")
        self._is_element_check(comm)


class TestElementTreeGeneric:
    def test_normal_tree(self, xml2_tree: ElementTree) -> None:
        reveal_type(xml2_tree)
        if LXML_VERSION >= (6, 0, 0):
            assert isinstance(xml2_tree, ElementTree)
        else:
            assert isinstance(xml2_tree, _ElementTree)
        # TODO need to write a typeguard plugin to support
        # checking elements within ElementTree

    # TODO write test to check that ElementTree[int] or other
    # non-element types are rejected by typeguard
