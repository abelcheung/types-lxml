from __future__ import annotations

import typing as typing
from pathlib import Path

import pytest
import typeguard
from lxml.etree import _Element, _ElementTree
from lxml.html import HtmlElement, parse
from _testutils import run_pyright_on

typeguard.config.forward_ref_policy = typeguard.ForwardRefPolicy.ERROR

def pytest_collection_finish(session: pytest.Session) -> None:
    files = {i.path for i in session.items}
    run_pyright_on(files)


@pytest.fixture
def h_filepath() -> Path:
    # hand edited to chop off many inline script blocks
    return Path(__file__).parent / "data" / "sample.html"


@pytest.fixture
def x_filepath() -> Path:
    return Path(__file__).parent / "data" / "w3c-example.svg"


@pytest.fixture
def html_tree(h_filepath: Path) -> _ElementTree[HtmlElement]:
    with open(h_filepath, "r", encoding="utf-8") as f:
        tree = parse(f, base_url="https://example.com/some/url/")
    return tree


@pytest.fixture
def xml_tree(x_filepath: Path) -> _ElementTree[_Element]:
    with open(x_filepath, "r", encoding="ascii") as f:
        tree = parse(f)
    return tree
