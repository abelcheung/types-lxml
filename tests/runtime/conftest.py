from __future__ import annotations

import lzma
import typing as _t
from pathlib import Path, PurePosixPath

import pytest
import typeguard
from lxml import etree as _e, html as _h

from ._testutils import mypy_adapter, pyright_adapter

pytest_plugins = ["typeguard"]
typeguard.config.forward_ref_policy = typeguard.ForwardRefPolicy.ERROR


def pytest_collection_finish(session: pytest.Session) -> None:
    files = {i.path for i in session.items}
    for adapter in (pyright_adapter.adapter, mypy_adapter.adapter):
        adapter.run_typechecker_on(files)


def pytest_configure(config: pytest.Config) -> None:
    # "normal" or "multiclass"
    setattr(config, "types_lxml_build", "normal")


def _bightml_filepath() -> Path:
    return Path(__file__).resolve().parent / "data" / "sample.html.xz"


# To fool test functions that use this fixture,
# specify argument type as typing.BinaryIO
# and don't include Iterator/Generator
@pytest.fixture
def bightml_bin_fp() -> _t.Iterator[lzma.LZMAFile]:
    fp = lzma.open(_bightml_filepath(), "rb")
    yield fp
    if not fp.closed:
        fp.close()


# To fool test functions that use this fixture,
# specify argument type as typing.TextIO
# and don't include Iterator/Generator
@pytest.fixture
def bightml_txt_fp() -> _t.Iterator[_t.TextIO]:
    fp = lzma.open(_bightml_filepath(), "rt", encoding="utf-8")
    yield fp
    if not fp.closed:
        fp.close()


@pytest.fixture(scope="session")
def bightml_str() -> str:
    with lzma.open(_bightml_filepath(), "rt", encoding="utf-8") as f:
        result = f.read()
    return result


@pytest.fixture(scope="session")
def bightml_bytes() -> bytes:
    with lzma.open(_bightml_filepath(), "rb") as f:
        result = f.read()
    return result


@pytest.fixture(scope="session")
def html2_filepath() -> Path:
    return Path(__file__).resolve().parent / "data" / "mdn-sample.html"


@pytest.fixture(scope="session")
def html2_fileuri(html2_filepath: Path) -> str:
    return "file:///" + str(html2_filepath)


@pytest.fixture(scope="session")
def html2_str(html2_filepath: Path) -> str:
    return html2_filepath.read_text()


@pytest.fixture(scope="session")
def html2_bytes(html2_filepath: Path) -> bytes:
    return html2_filepath.read_bytes()


@pytest.fixture(scope="session")
def svg_filepath() -> Path:
    return Path(__file__).resolve().parent / "data" / "w3c-example.svg"


@pytest.fixture(scope="session")
def xml2_filepath() -> Path:
    return Path(__file__).resolve().parent / "data" / "shiporder.xml"


@pytest.fixture
def bightml_tree(bightml_bin_fp: _t.BinaryIO) -> _e._ElementTree[_h.HtmlElement]:
    with bightml_bin_fp as f:
        tree = _h.parse(f)
    return tree


@pytest.fixture
def bightml_root(bightml_tree: _e._ElementTree[_h.HtmlElement]) -> _h.HtmlElement:
    return bightml_tree.getroot()


@pytest.fixture
def html2_tree(html2_filepath: Path) -> _e._ElementTree[_h.HtmlElement]:
    with open(html2_filepath, "r", encoding="utf-8") as f:
        tree = _h.parse(f)
    return tree


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


@pytest.fixture(scope="session")
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
