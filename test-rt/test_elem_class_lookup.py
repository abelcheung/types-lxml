from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

import _testutils
from lxml.etree import (
    ElementBase,
    ElementDefaultClassLookup,
    XMLParser,
    _Element as _Element,
    _ElementTree as _ElementTree,
    parse,
)
from lxml.objectify import ObjectifiedElement, ObjectifyElementClassLookup

reveal_type = getattr(_testutils, "reveal_type_wrapper")


def test_manual_objectify_parser(x2_filepath: Path) -> None:
    parser = XMLParser()
    reveal_type(parser)
    if TYPE_CHECKING:
        parser = cast("XMLParser[ObjectifiedElement]", parser)
    else:
        parser.set_element_class_lookup(ObjectifyElementClassLookup())
    reveal_type(parser)
    tree = parse(x2_filepath, parser)
    reveal_type(tree)
    reveal_type(tree.getroot())


def test_my_default_element(x2_filepath: Path) -> None:
    class MyElement(ElementBase):
        pass

    lookup = ElementDefaultClassLookup(element=MyElement)
    parser = XMLParser()
    if TYPE_CHECKING:
        parser = cast("XMLParser[MyElement]", parser)
    else:
        parser.set_element_class_lookup(lookup=lookup)
    reveal_type(parser)
    tree = parse(str(x2_filepath).encode("ascii"), parser)
    reveal_type(tree)
    reveal_type(tree.getroot())
