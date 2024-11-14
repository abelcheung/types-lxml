# Register hypothesis strategies for generating lxml
# elements and various auxiliary types.

from __future__ import annotations

import hypothesis.strategies as st
import lxml.etree as _e
import pytest

from ._testutils import strategy as _st


def pytest_collection_finish(session: pytest.Session) -> None:
    pluginmanager = session.config.pluginmanager
    if not pluginmanager.has_plugin("hypothesis"):
        return

    st.register_type_strategy(_e.CDATA, _st.cdata())
    st.register_type_strategy(_e._ProcessingInstruction, _st.processing_instruction())
    st.register_type_strategy(_e._Comment, _st.comment())
    st.register_type_strategy(_e._Entity, _st.entity())
