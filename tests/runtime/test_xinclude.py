from __future__ import annotations

import copy
import sys
from collections.abc import Callable, Iterable
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
from ._testutils.errors import (
    raise_attr_not_writable,
    raise_no_attribute,
    raise_wrong_arg_type,
    raise_wrong_pos_arg_count,
)

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
        with raise_wrong_pos_arg_count:
            xinc = XInclude(None)  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]
        xinc = XInclude()
        reveal_type(xinc)
        reveal_type(xinc.error_log)
        with raise_attr_not_writable:
            xinc.error_log = xinc.error_log  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]

    def test_xinclude_as_method(self, xinc_sample_data: str) -> None:
        elem = fromstring(xinc_sample_data)
        tree = elem.getroottree()
        assert tree.xinclude() is None

    def test_xinclude_as_func(
        self,
        xinc_sample_data: str,
        tmp_path: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        tmp_file = tmp_path / "xinc_sample_data.xml"
        tmp_file.write_text(xinc_sample_data)
        tree = parse(tmp_file)

        xinc = XInclude()
        for input in generate_input_file_arguments(tmp_file, include=(tree,)):
            with raise_wrong_arg_type:
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
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        tmp_file = tmp_path / "xinc_sample_data.xml"
        tmp_file.write_text(xinc_sample_data)

        for input in generate_input_file_arguments(tmp_file):
            with raise_no_attribute:
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
        with raise_no_attribute:
            EI.include(temp_el, cast(Any, bad_loader_1))
        del temp_el

        temp_el = copy.deepcopy(elem)
        with raise_wrong_pos_arg_count:
            EI.include(temp_el, cast(Any, bad_loader_2))
        del temp_el

        temp_el = copy.deepcopy(elem)
        # Coerce loader into text mode, this is REALLY artificial though
        temp_el[1].attrib["parse"] = "text"
        with pytest.raises(TypeError, match="can only concatenate str"):
            EI.include(temp_el, cast(Any, bad_loader_3))
        del temp_el
