from __future__ import annotations

import typing as typing
from pathlib import Path, PurePosixPath

import pytest
import typeguard
from _testutils import run_pyright_on
from lxml import etree as _e, html as _h

typeguard.config.forward_ref_policy = typeguard.ForwardRefPolicy.ERROR


def pytest_collection_finish(session: pytest.Session) -> None:
    files = {i.path for i in session.items}
    run_pyright_on(files)


@pytest.fixture
def h1_filepath() -> Path:
    # hand edited to chop off many inline script blocks
    return Path(__file__).parent / "data" / "sample.html"


@pytest.fixture
def h1_str(h1_filepath: Path) -> str:
    return h1_filepath.read_text()


@pytest.fixture
def h1_bytes(h1_filepath: Path) -> bytes:
    return h1_filepath.read_bytes()


@pytest.fixture
def h2_filepath() -> Path:
    return Path(__file__).parent / "data" / "mdn-sample.html"


@pytest.fixture
def h2_fileuri(h2_filepath: Path) -> str:
    return "file:///" + str(h2_filepath)


@pytest.fixture
def h2_str(h2_filepath: Path) -> str:
    return h2_filepath.read_text()


@pytest.fixture
def h2_bytes(h2_filepath: Path) -> bytes:
    return h2_filepath.read_bytes()


@pytest.fixture
def x1_filepath() -> Path:
    return Path(__file__).parent / "data" / "w3c-example.svg"


@pytest.fixture
def x2_filepath() -> Path:
    return Path(__file__).parent / "data" / "shiporder.xml"


@pytest.fixture
def html_tree(h1_filepath: Path) -> _e._ElementTree[_h.HtmlElement]:
    with open(h1_filepath, "r", encoding="utf-8") as f:
        tree = _h.parse(f)
    return tree


@pytest.fixture
def xml_tree(x2_filepath: Path) -> _e._ElementTree:
    with open(x2_filepath, "r", encoding="ascii") as f:
        tree = _e.parse(f)
    return tree


@pytest.fixture
def xinc_sample_data(x2_filepath: Path) -> str:
    purepath = PurePosixPath(x2_filepath.relative_to(Path(__file__).parent.parent))
    return """<doc xmlns:xi="http://www.w3.org/2001/XInclude">
        <foo/><xi:include href="{}" /></doc>""".format(
        purepath
    )


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
