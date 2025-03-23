from __future__ import annotations

import bz2
import gzip
import io
import logging
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
import urllib3
from lxml import etree as _e, html as _h
from lxml.isoschematron import Schematron

pytest_plugins = [
    "typeguard",
    "hypothesis",
    "pytest-revealtype-injector",
    "runtime.register_strategy",
]

http_pool = urllib3.PoolManager()

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


typeguard.config.forward_ref_policy = typeguard.ForwardRefPolicy.ERROR
typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS


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


@pytest.fixture(scope="session")
def xml2_str(xml2_filepath: Path) -> str:
    return xml2_filepath.read_text()


@pytest.fixture(scope="session")
def xml2_bytes_with_dtd(xml2_filepath: Path) -> bytes:
    result = xml2_filepath.read_bytes()
    dtd_path = xml2_filepath.parent / "shiporder.dtd"
    result = result.replace(
        b"?>",
        # python/cpython#103631 or expect this on Windows py3.11
        # "C:\\/Users/..." --> fails loading DTD
        '?><!DOCTYPE shiporder SYSTEM "file:///{}">'.format(
            dtd_path.as_posix()
        ).encode(),
        1,
    )
    return result


@pytest.fixture(scope="session")
def xml2_bytes(xml2_filepath: Path) -> bytes:
    return xml2_filepath.read_bytes()


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


@pytest.fixture(scope="session")
def xmlschema_path() -> Path:
    return Path(__file__).resolve().parent / "_data" / "shiporder.xsd"


@pytest.fixture(scope="session")
def xmlschema_root(xmlschema_path: Path) -> _e._Element:
    return _e.fromstring(xmlschema_path.read_bytes())


@pytest.fixture(scope="session")
def xmlschema(xmlschema_path: Path) -> _e.XMLSchema:
    return _e.XMLSchema(file=str(xmlschema_path))


@pytest.fixture(scope="session")
def rnc_path() -> Path:
    return Path(__file__).resolve().parent / "_data" / "shiporder.rnc"


@pytest.fixture(scope="session")
def rnc_str(rnc_path: Path) -> str:
    return rnc_path.read_text()


@pytest.fixture(scope="session")
def relaxng_path() -> Path:
    return Path(__file__).resolve().parent / "_data" / "shiporder.rng"


@pytest.fixture(scope="session")
def relaxng_root(relaxng_path: Path) -> _e._Element:
    return _e.fromstring(relaxng_path.read_bytes())


@pytest.fixture(scope="session")
def relaxng(relaxng_path: Path) -> _e.RelaxNG:
    return _e.RelaxNG(file=relaxng_path)


@pytest.fixture(scope="session")
def schematron_path() -> Path:
    return Path(__file__).resolve().parent / "_data" / "shiporder.sch"


@pytest.fixture(scope="session")
def schematron_root(schematron_path: Path) -> _e._Element:
    return _e.fromstring(schematron_path.read_bytes())


@pytest.fixture(scope="session")
def schematron(schematron_path: Path) -> Schematron:
    return Schematron(file=schematron_path)


@pytest.fixture(scope="session")
def dtd_path() -> Path:
    return Path(__file__).resolve().parent / "_data" / "shiporder.dtd"


@pytest.fixture(scope="session")
def dtd_root(dtd_path: Path) -> _e._Element:
    return _e.fromstring(dtd_path.read_bytes())


@pytest.fixture(scope="session")
def dtd(dtd_path: Path) -> _e.DTD:
    return _e.DTD(file=dtd_path)


@pytest.fixture(scope="session")
def dtd_enabled_parser() -> _e.XMLParser:
    return _e.XMLParser(dtd_validation=True, load_dtd=True)


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


@pytest.fixture(scope="class")
def pylog() -> _e.PyErrorLog:
    result = _e.PyErrorLog()
    _e.use_global_python_log(result)
    bad_data = "<bad><a><b></a>&qwerty;</bad>"
    try:
        _ = _e.fromstring(bad_data)
    except _e.XMLSyntaxError:
        pass
    else:
        raise RuntimeError("Unknown error when creating pylog fixture")
    return result


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

        buffer.seek(0, io.SEEK_SET)
        return comp_type(**{param: buffer, "mode": "rb"})  # pyright: ignore

    return _wrapped


# It's too much to create protocol signature just for this thing
@pytest.fixture
def generate_input_file_arguments(
    pytestconfig: pytest.Config,
    pook: Any,
) -> Callable[..., Iterator[Any]]:
    def _wrapped(
        path: Path,
        *,
        exclude_type: tuple[type[Any]] = tuple(),
        include: Collection[Callable[[Path], Any]] = tuple(),
    ) -> Iterator[Any]:
        assert path.is_file()

        match path.suffix.lower():
            case ".htm" | ".html":
                content_type = "text/html"
            case ".svg":
                content_type = "image/svg+xml"
            case _:
                content_type = "application/xml"
        pook.get(
            "http://example.com/" + path.name,
            response_type=content_type,
            response_body=path.read_text(),
            persist=True,
        )
        mock_http_response = http_pool.request("GET", "http://example.com/" + path.name)

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
            mock_http_response,
        ]

        for func in include:
            items.append(func)
        for i in items:
            if isinstance(i, exclude_type):
                continue
            if callable(i):
                i = i(path)
            if pytestconfig.get_verbosity() >= 2:
                _logger.debug(f"Testing file input {i!r}")
            if isinstance(i, AbstractContextManager) and not isinstance(i, Path):
                cm = i
            else:
                cm = nullcontext(i)
            with cm as f:
                yield f

    return _wrapped
