from __future__ import annotations

import pytest
from lxml.html import Element, HtmlElement


@pytest.fixture(scope="class")
def disposable_html_element() -> HtmlElement:
    return Element("div", {"class": "disposable"})
