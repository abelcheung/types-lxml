from __future__ import annotations

import bz2
import gzip
import io
import lzma
from collections.abc import (
    Callable,
    Collection,
    Iterator,
)
from contextlib import AbstractContextManager, nullcontext
from pathlib import Path, PurePosixPath
from typing import (
    Any,
    BinaryIO,
    Literal,
    TextIO,
    cast,
    overload,
)
from urllib.request import urlopen
from urllib.response import addinfourl

import pytest
import typeguard
from lxml import etree as _e, html as _h

pytest_plugins = [
    "typeguard",
    "hypothesis",
    "pytest-revealtype-injector",
    "runtime.register_strategy",
]

typeguard.config.forward_ref_policy = typeguard.ForwardRefPolicy.ERROR

is_multi_subclass_build = pytest.StashKey[bool]()


def pytest_configure(config: pytest.Config) -> None:
    config.stash[is_multi_subclass_build] = False


def _bightml_filepath() -> Path:
    return Path(__file__).resolve().parent / "_data" / "sample.html.xz"


# To fool test functions that use this fixture,
# specify argument type as typing.BinaryIO
# and don't include Iterator/Generator
@pytest.fixture
def bightml_bin_fp() -> Iterator[lzma.LZMAFile]:
    fp = lzma.open(_bightml_filepath(), "rb")
    yield fp
    if not fp.closed:
        fp.close()


# To fool test functions that use this fixture,
# specify argument type as typing.TextIO
# and don't include Iterator/Generator
@pytest.fixture
def bightml_txt_fp() -> Iterator[TextIO]:
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
    return Path(__file__).resolve().parent / "_data" / "mdn-sample.html"


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
    return Path(__file__).resolve().parent / "_data" / "w3c-example.svg"


@pytest.fixture(scope="session")
def xml2_filepath() -> Path:
    return Path(__file__).resolve().parent / "_data" / "shiporder.xml"


@pytest.fixture
def bightml_tree(bightml_bin_fp: BinaryIO) -> _e._ElementTree[_h.HtmlElement]:
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
def html2_root(html2_tree: _e._ElementTree[_h.HtmlElement]) -> _h.HtmlElement:
    return html2_tree.getroot()


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


# For hypothesis tests, parsing valid document spends too much
# time and raises HealthCheck warning, use simple stuff instead
@pytest.fixture(scope="class")
def disposable_element() -> _e._Element:
    return _e.Element("order", date="1900-01-01", id="123")


@pytest.fixture(scope="class")
def disposable_attrib(disposable_element: _e._Element) -> _e._Attrib:
    return disposable_element.attrib


@overload
def _get_compressed_fp_from(
    zmode: Literal["gz"],
) -> Callable[[Path], gzip.GzipFile]: ...
@overload
def _get_compressed_fp_from(
    zmode: Literal["bz2"],
) -> Callable[[Path], bz2.BZ2File]: ...
@overload
def _get_compressed_fp_from(
    zmode: Literal["xz"],
) -> Callable[[Path], lzma.LZMAFile]: ...
def _get_compressed_fp_from(zmode: str) -> Any:
    param_name = {
        "gz": (gzip.GzipFile, "fileobj"),
        "bz2": (bz2.BZ2File, "filename"),
        "xz": (lzma.LZMAFile, "filename"),
    }

    def _wrapped(path: Path, /) -> Any:
        buffer = io.BytesIO()
        comp_type, param = param_name[zmode]
        with path.open("rb") as f, comp_type(**{param: buffer, "mode": "wb"}) as z:  # pyright: ignore
            z.write(f.read())

        return comp_type(**{param: buffer, "mode": "rb"})  # pyright: ignore

    return _wrapped


# It's too much to create protocol signature just for this thing
@pytest.fixture
def generate_input_file_arguments() -> Callable[..., Iterator[Any]]:
    def _wrapped(
        path: Path,
        *,
        exclude_type: tuple[type[Any]] = tuple(),
        include: Collection[Callable[[Path], Any]] = tuple(),
    ) -> Iterator[Any]:
        assert path.is_file()
        items = [
            path,
            str(path),
            str(path).encode("utf-8"),
            path.open("rb"),
            path.open("rt", encoding="utf-8"),
            io.BytesIO(path.read_bytes()),
            io.StringIO(path.read_text()),
            # Just because typeshed doesn't have typing for urlopen!
            cast(
                AbstractContextManager[addinfourl],
                urlopen("file:///" + str(path)),
            ),
            _get_compressed_fp_from("gz"),
            _get_compressed_fp_from("bz2"),
            _get_compressed_fp_from("xz"),
        ]
        for func in include:
            items.append(func)
        for i in items:
            if isinstance(i, exclude_type):
                continue
            if callable(i):
                i = i(path)
            if isinstance(i, AbstractContextManager):
                cm = i
            else:
                cm = nullcontext(i)
            with cm as f:
                yield f

    return _wrapped
