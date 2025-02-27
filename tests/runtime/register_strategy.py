# Register hypothesis strategies for generating lxml
# elements and various auxiliary types.

from __future__ import annotations

import hypothesis.strategies as st
import lxml.etree as _e
import lxml.html as _h
import pytest

from ._testutils import strategy as _st


# Need to register early, before any tests are collected.
def pytest_configure(config: pytest.Config) -> None:
    st.register_type_strategy(_e._Comment, _st.comment())
    st.register_type_strategy(_e._Entity, _st.entity())
    st.register_type_strategy(_e._ProcessingInstruction, _st.processing_instruction())
    st.register_type_strategy(_e.CDATA, _st.cdata())
    st.register_type_strategy(_e.QName, _st.qname())
    st.register_type_strategy(_e._Element, _st.single_simple_element())
    st.register_type_strategy(_e._ElementTree, _st.simple_elementtree())
    st.register_type_strategy(_h.HtmlElement, _st.simple_html_element())
