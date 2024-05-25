from __future__ import annotations

import copy
from inspect import Parameter, _ParameterKind
from io import StringIO
from pathlib import Path
from typing import Any, Literal, cast, overload

import _testutils
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

reveal_type = getattr(_testutils, "reveal_type_wrapper")


# XInclude only works on ElementTree as method,
# and only on Element when used as function.
# In both cases, no return value is expected,
# and source data type is preserved


class TestXInclude:
    def test_init_and_prop(self) -> None:
        with pytest.raises(TypeError, match="takes exactly 0 positional arguments"):
            xinc = XInclude(None)  # pyright: ignore
        xinc = XInclude()
        reveal_type(xinc.error_log)

    def test_xinclude_as_method(self, xinc_sample_data: str) -> None:
        elem = fromstring(xinc_sample_data)
        tree = elem.getroottree()
        result = tree.xinclude()
        reveal_type(tree)
        reveal_type(result)

    def test_xinclude_as_func(self, xinc_sample_data: str) -> None:
        xinc = XInclude()
        with pytest.raises(TypeError, match="Argument 'node' has incorrect type"):
            xinc(cast(Any, xinc_sample_data))

        iodata = StringIO(xinc_sample_data)
        with pytest.raises(TypeError, match="Argument 'node' has incorrect type"):
            xinc(cast(Any, iodata))

        elem = fromstring(xinc_sample_data)
        tree = elem.getroottree()
        with pytest.raises(TypeError, match="Argument 'node' has incorrect type"):
            xinc(cast(Any, tree))

        result = xinc(elem)
        reveal_type(elem)
        reveal_type(result)


@overload
def good_loader(
    href: str, mode: Literal["xml"], encoding: str | None = None
) -> _Element:
    ...


@overload
def good_loader(href: str, mode: Literal["text"], encoding: str | None = None) -> str:
    ...


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


def bad_loader_3(href: str, mode: str, _) -> _Element:
    return parse(href).getroot()


class TestElementInclude:
    @_testutils.signature_tester(EI.include, (
        ('elem'     , _ParameterKind.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ('loader'   , _ParameterKind.POSITIONAL_OR_KEYWORD, None           ),
        ('base_url' , _ParameterKind.POSITIONAL_OR_KEYWORD, None           ),
        ('max_depth', _ParameterKind.POSITIONAL_OR_KEYWORD, 6              ),
    ))  # fmt: skip
    def test_func_sig(self) -> None:
        pass

    def test_input_type(self, xinc_sample_data: str) -> None:
        elem = fromstring(xinc_sample_data)
        result = EI.include(elem)
        reveal_type(result)
        del elem, result

        sio = StringIO(xinc_sample_data)
        tree = parse(sio)
        EI.include(tree)
        del tree

        with pytest.raises(AttributeError, match="no attribute 'getroottree'"):
            EI.include(cast(Any, xinc_sample_data))

        with pytest.raises(AttributeError, match="no attribute 'getroottree'"):
            EI.include(cast(Any, sio))

        sio.close()

    def test_loader(self, xinc_sample_data: str) -> None:
        elem = fromstring(xinc_sample_data)

        temp_el = copy.copy(elem)
        EI.include(temp_el, good_loader)
        del temp_el

        # It's actually ok to ignore 3rd param in XML mode
        temp_el = copy.copy(elem)
        EI.include(temp_el, cast(Any, bad_loader_3))
        del temp_el

        temp_el = copy.copy(elem)
        with pytest.raises(AttributeError, match="no attribute 'getroottree'"):
            EI.include(temp_el, cast(Any, bad_loader_1))
        del temp_el

        temp_el = copy.copy(elem)
        with pytest.raises(
            TypeError, match="takes 1 positional argument but 3 were given"
        ):
            EI.include(temp_el, cast(Any, bad_loader_2))
        del temp_el

        temp_el = copy.copy(elem)
        # Coerce loader into text mode, this is REALLY artificial though
        temp_el[1].attrib["parse"] = "text"
        with pytest.raises(TypeError, match="can only concatenate str"):
            EI.include(temp_el, cast(Any, bad_loader_3))
        del temp_el
