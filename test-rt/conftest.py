from __future__ import annotations

import typing as typing
from pathlib import Path, PurePosixPath

import pytest
import typeguard
from _testutils import mypy_adapter, pyright_adapter
from lxml import etree as _e, html as _h

typeguard.config.forward_ref_policy = typeguard.ForwardRefPolicy.ERROR


def pytest_collection_finish(session: pytest.Session) -> None:
    files = {i.path for i in session.items}
    for adapter in (pyright_adapter.adapter, mypy_adapter.adapter):
        adapter.run_typechecker_on(files)


@pytest.fixture
def bightml_filepath() -> Path:
    return Path(__file__).resolve().parent / "data" / "sample.html"


@pytest.fixture
def bightml_str(bightml_filepath: Path) -> str:
    return bightml_filepath.read_text()


@pytest.fixture
def bightml_bytes(bightml_filepath: Path) -> bytes:
    return bightml_filepath.read_bytes()


@pytest.fixture
def html2_filepath() -> Path:
    return Path(__file__).resolve().parent / "data" / "mdn-sample.html"


@pytest.fixture
def html2_fileuri(html2_filepath: Path) -> str:
    return "file:///" + str(html2_filepath)


@pytest.fixture
def html2_str(html2_filepath: Path) -> str:
    return html2_filepath.read_text()


@pytest.fixture
def html2_bytes(html2_filepath: Path) -> bytes:
    return html2_filepath.read_bytes()


@pytest.fixture
def svg_filepath() -> Path:
    return Path(__file__).resolve().parent / "data" / "w3c-example.svg"


@pytest.fixture
def xml2_filepath() -> Path:
    return Path(__file__).resolve().parent / "data" / "shiporder.xml"


@pytest.fixture
def bightml_tree(bightml_filepath: Path) -> _e._ElementTree[_h.HtmlElement]:
    with open(bightml_filepath, "r", encoding="utf-8") as f:
        tree = _h.parse(f)
    return tree


@pytest.fixture
def bightml_root(bightml_tree: _e._ElementTree[_h.HtmlElement]) -> _h.HtmlElement:
    return bightml_tree.getroot()


@pytest.fixture
def svg_tree(svg_filepath: Path) -> _e._ElementTree:
    with open(svg_filepath, "r", encoding="utf-8") as f:
        tree = _e.parse(f)
    return tree


@pytest.fixture
def svg_root(svg_tree: _e._ElementTree) -> _e._Element:
    return svg_tree.getroot()


@pytest.fixture
def xml2_tree(xml2_filepath: Path) -> _e._ElementTree:
    with open(xml2_filepath, "r", encoding="utf-8") as f:
        tree = _e.parse(f)
    return tree


@pytest.fixture
def xml2_root(xml2_tree: _e._ElementTree) -> _e._Element:
    return xml2_tree.getroot()


@pytest.fixture
def xinc_sample_data(xml2_filepath: Path) -> str:
    inc_href = PurePosixPath(xml2_filepath.resolve().relative_to(Path.cwd()))
    return """<doc xmlns:xi="http://www.w3.org/2001/XInclude">
        <foo/><xi:include href="{}" /></doc>""".format(inc_href)


@pytest.fixture
def list_log() -> _e._ListErrorLog:
    bad_data = "<bad><a><b></a>&qwerty;</bad>"
    p = _e.XMLParser()
    try:
        _ = _e.fromstring(bad_data, parser=p)
    except _e.XMLSyntaxError:
        err = p.error_log
    else:
        raise RuntimeError("Unknown error when creating error_log fixture")

    return err
