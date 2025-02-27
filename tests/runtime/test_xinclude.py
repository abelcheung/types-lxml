from __future__ import annotations

import copy
import sys
from collections.abc import Callable, Iterator
from inspect import Parameter
from pathlib import Path
from typing import Any, Literal, cast, overload

import lxml.ElementInclude as EI
import pytest
from lxml.etree import (
    XInclude,
    _Element,
    _ElementTree as _ElementTree,
    _ListErrorLog as _ListErrorLog,
    fromstring,
    parse,
)

from ._testutils import signature_tester

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type

# XInclude only works on ElementTree as method,
# and only on Element when used as standalone class.
# In both cases, no return value is expected,
# and source data type is preserved


class TestXInclude:
    def test_init_and_prop(self) -> None:
        # Cython generic signature
        with pytest.raises(TypeError, match="takes exactly 0 positional arguments"):
            xinc = XInclude(None)  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]
        xinc = XInclude()
        reveal_type(xinc)
        reveal_type(xinc.error_log)

    def test_xinclude_as_method(self, xinc_sample_data: str) -> None:
        elem = fromstring(xinc_sample_data)
        tree = elem.getroottree()
        assert tree.xinclude() is None

    def test_xinclude_as_func(
        self,
        xinc_sample_data: str,
        tmp_path: Path,
        generate_input_file_arguments: Callable[..., Iterator[Any]],
    ) -> None:
        tmp_file = tmp_path / "xinc_sample_data.xml"
        tmp_file.write_text(xinc_sample_data)
        tree = parse(tmp_file)

        xinc = XInclude()
        for input in generate_input_file_arguments(tmp_file, include=(tree,)):
            with pytest.raises(TypeError, match="Argument 'node' has incorrect type"):
                xinc(input)

        elem = fromstring(xinc_sample_data)
        assert xinc(elem) is None


@overload
def good_loader(
    href: str, mode: Literal["xml"], encoding: str | None = None
) -> _Element: ...


@overload
def good_loader(
    href: str, mode: Literal["text"], encoding: str | None = None
) -> str: ...


def good_loader(href: str, mode: str, encoding: str | None = None) -> Any:
    # Over simplified version of _lxml_default_loader without network
    if mode == "xml":
        return parse(href).getroot()
    else:
        return Path(href).read_text()


def bad_loader_1(href: str, mode: str, encoding: str | None = None) -> str:
    return href


def bad_loader_2(href: str) -> str:
    return href


def bad_loader_3(href: str, mode: str, _: Any) -> _Element:
    return parse(href).getroot()


class TestElementInclude:
    @signature_tester(EI.include, (
        ('elem'     , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ('loader'   , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ('base_url' , Parameter.POSITIONAL_OR_KEYWORD, None           ),
        ('max_depth', Parameter.POSITIONAL_OR_KEYWORD, 6              ),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    def test_input_type(
        self,
        xinc_sample_data: str,
        tmp_path: Path,
        generate_input_file_arguments: Callable[..., Iterator[Any]],
    ) -> None:
        tmp_file = tmp_path / "xinc_sample_data.xml"
        tmp_file.write_text(xinc_sample_data)

        for input in generate_input_file_arguments(tmp_file):
            with pytest.raises(AttributeError, match="no attribute 'getroottree'"):
                EI.include(input)

        elem = fromstring(xinc_sample_data)
        elem2 = copy.deepcopy(elem)
        assert EI.include(elem) is None
        tree = elem2.getroottree()
        EI.include(tree)

    def test_loader(self, xinc_sample_data: str) -> None:
        elem = fromstring(xinc_sample_data)

        temp_el = copy.deepcopy(elem)
        EI.include(temp_el, good_loader)
        del temp_el

        # It's actually ok to ignore 3rd param in XML mode
        temp_el = copy.deepcopy(elem)
        EI.include(temp_el, cast(Any, bad_loader_3))
        del temp_el

        temp_el = copy.deepcopy(elem)
        with pytest.raises(AttributeError, match="no attribute 'getroottree'"):
            EI.include(temp_el, cast(Any, bad_loader_1))
        del temp_el

        temp_el = copy.deepcopy(elem)
        with pytest.raises(
            TypeError, match="takes 1 positional argument but 3 were given"
        ):
            EI.include(temp_el, cast(Any, bad_loader_2))
        del temp_el

        temp_el = copy.deepcopy(elem)
        # Coerce loader into text mode, this is REALLY artificial though
        temp_el[1].attrib["parse"] = "text"
        with pytest.raises(TypeError, match="can only concatenate str"):
            EI.include(temp_el, cast(Any, bad_loader_3))
        del temp_el
