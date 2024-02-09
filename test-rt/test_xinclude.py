from __future__ import annotations

from io import StringIO
from typing import Any, cast

import _testutils
import pytest

# import pytest
from lxml.etree import (
    XInclude,
    _Element as _Element,
    _ElementTree as _ElementTree,
    _ListErrorLog as _ListErrorLog,
    fromstring,
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
