from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import pytest
from _pytest.fixtures import FixtureRequest
from lxml.html import Element, HtmlElement


@pytest.fixture(scope="class")
def disposable_html_element(request: FixtureRequest) -> HtmlElement:
    input_args: Sequence[Any] = getattr(request, "param", ["div", {"class": "disposable"}])
    if isinstance(input_args, str):
        input_args = [input_args]
    return Element(*input_args)


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
