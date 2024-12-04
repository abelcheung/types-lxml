from __future__ import annotations

import pytest
from lxml.html import Element, HtmlElement


@pytest.fixture(scope="class")
def disposable_html_element() -> HtmlElement:
    return Element("div", {"class": "disposable"})


# HTML link replacement functions need <base href="...">,
# otherwise they short circuit and ignore invalid args
@pytest.fixture(scope="class")
def disposable_html_with_base_href() -> HtmlElement:
    import lxml.html.builder as b

    return b.HTML(
        b.HEAD(
            # urljoin is too robust (?)
            b.BASE(href="?foo?<")
        ),
        b.BODY(
            b.A("Anchor", href="#id1", id="id1"),
            b.A("Relative Link", href="./relative"),
            b.A("Full Link", href="http://example.org"),
        ),
    )
