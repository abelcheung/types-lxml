from __future__ import annotations

import pathlib
import sys
from typing import TYPE_CHECKING, cast

import lxml.etree as _e
import pytest
from lxml.etree import (
    ElementBase,
    XMLParser,
    _Element as _Element,
    _ElementTree as _ElementTree,
)
from lxml.objectify import ObjectifiedElement, ObjectifyElementClassLookup
from typeguard import TypeCheckError

from .._testutils import is_multi_subclass_build

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


def test_manual_objectify_parser(xml2_filepath: pathlib.Path) -> None:
    parser = XMLParser()
    reveal_type(parser)
    if TYPE_CHECKING:
        parser = cast("XMLParser[ObjectifiedElement]", parser)
    else:
        parser.set_element_class_lookup(ObjectifyElementClassLookup())
    reveal_type(parser)
    tree = _e.parse(xml2_filepath, parser)
    reveal_type(tree)
    reveal_type(tree.getroot())


class TestDefaultLookup:
    def test_single_subclass(self, xml2_filepath: pathlib.Path) -> None:
        class MyBaseElement(ElementBase):
            pass

        lookup = _e.ElementDefaultClassLookup(element=MyBaseElement)
        parser = XMLParser()
        if TYPE_CHECKING:
            parser = cast("XMLParser[MyBaseElement]", parser)
        else:
            parser.set_element_class_lookup(lookup=lookup)
        reveal_type(parser)
        tree = _e.parse(xml2_filepath, parser)
        reveal_type(tree)
        reveal_type(tree.getroot())


class TestNamespaceLookup:
    FOONS = "http://example.org/myfoo"

    def test_single_ns_all_tag_1(self, svg_filepath: pathlib.Path) -> None:
        """Class lookup that creates my single element type
        for all nodes under specific namespace"""
        lookup = _e.ElementNamespaceClassLookup()
        ns = lookup.get_namespace(self.FOONS)

        @ns(None)
        class MyBaseElement(ElementBase):
            pass

        parser = XMLParser()
        # Not replacing parser type subscript since
        # most elements still remain as basic one
        # Next test shows how it would fail if it
        # were replaced
        parser.set_element_class_lookup(lookup)

        tree = _e.parse(svg_filepath, parser=parser)
        root = tree.getroot()

        count = 0
        for e in root.iter():
            reveal_type(e)
            if isinstance(e, MyBaseElement):
                count += 1
        assert count == 7

    def test_single_ns_all_tag_2(self, svg_filepath: pathlib.Path) -> None:
        """Class lookup that creates my single element type
        for all nodes under specific namespace, while proving
        that parser subscript type can't be modified"""
        lookup = _e.ElementNamespaceClassLookup()
        ns = lookup.get_namespace(self.FOONS)

        @ns(None)
        class MyBaseElement(ElementBase):
            pass

        parser = XMLParser()
        # Contrast with previous test; this shows how
        # test would fail if parser type subscript
        # is replaced
        if TYPE_CHECKING:
            parser = cast("XMLParser[MyBaseElement]", parser)
        else:
            parser.set_element_class_lookup(lookup)

        tree = _e.parse(svg_filepath, parser=parser)
        root = tree.getroot()

        if is_multi_subclass_build:
            # For multiclass build, .iter() is hardcoded to return _Element,
            # and author is expected to do method / annotation overrides
            # in their classes
            for e in root.iter():
                reveal_type(e)
        else:
            with pytest.raises(
                TypeCheckError, match="not an instance of .*MyBaseElement"
            ):
                for e in root.iter():
                    reveal_type(e)

    def test_single_ns_single_tag_1(self, svg_filepath: pathlib.Path) -> None:
        """Decorator and non-decorator ways of adding per-tag
        class to registry, where tag name equals class name
        """
        lookup = _e.ElementNamespaceClassLookup()
        ns = lookup.get_namespace(self.FOONS)

        @ns
        class title(ElementBase):  # pyright: ignore[reportUnusedClass]
            pass

        class descr(ElementBase):
            pass

        # mypy error: Cannot assign to a type
        descr = ns(descr)  # type: ignore[misc]

        class emph(ElementBase):
            pass

        ns["emph"] = emph

        parser = XMLParser()
        parser.set_element_class_lookup(lookup)

        tree = _e.parse(svg_filepath, parser=parser)
        root = tree.getroot()

        count = 0
        for e in root.iter():
            reveal_type(e)
            if issubclass(type(e), ElementBase):
                count += 1
        assert count == 3

    def test_single_ns_single_tag_2(self, svg_filepath: pathlib.Path) -> None:
        """Decorator and non-decorator ways of adding per-tag
        class to registry, where tag name and class name
        are different"""
        lookup = _e.ElementNamespaceClassLookup()
        ns = lookup.get_namespace(self.FOONS)

        @ns("title")
        class _TitleClass(ElementBase):  # pyright: ignore[reportUnusedClass]
            pass

        class _DescClass(ElementBase):
            pass

        # mypy error: Cannot assign to a type
        _DescClass = ns("descr")(_DescClass)  # type: ignore[misc]

        class _EmphClass(ElementBase):
            pass

        ns["emph"] = _EmphClass

        parser = XMLParser()
        parser.set_element_class_lookup(lookup)

        tree = _e.parse(svg_filepath, parser=parser)
        root = tree.getroot()

        count = 0
        for e in root.iter():
            reveal_type(e)
            if issubclass(type(e), ElementBase):
                count += 1
        assert count == 3

    def test_default_ns(self, svg_filepath: pathlib.Path) -> None:
        """Class lookup that creates my single element type
        for all nodes under all namespaces, behaving like
        ElementDefaultClassLookup"""
        lookup = _e.ElementNamespaceClassLookup()
        ns = lookup.get_namespace(None)

        @ns(None)
        class MyBaseElement(ElementBase):
            pass

        parser = XMLParser()
        # Shouldn't have been casted for real life code, since
        # ONLY default namespace is covered
        if TYPE_CHECKING:
            parser = cast("XMLParser[MyBaseElement]", parser)
        else:
            parser.set_element_class_lookup(lookup)

        tree = _e.parse(svg_filepath, parser=parser)
        root = tree.getroot()
        reveal_type(root)

        if is_multi_subclass_build:
            # See test_single_ns_all_tag_2 test
            for e in root.iter():
                reveal_type(e)
        else:
            with pytest.raises(
                TypeCheckError, match="not an instance of .*MyBaseElement"
            ):
                for e in root.iter():
                    reveal_type(e)
