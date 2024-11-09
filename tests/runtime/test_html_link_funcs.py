from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Sequence, cast

from . import _testutils
import pytest
from lxml.etree import __version__ as _lxml_ver, _ElementTree
from lxml.html import (
    HtmlElement,
    find_class,
    find_rel_links,
    iterlinks,
    make_links_absolute,
    resolve_base_href,
    rewrite_links,
)

INJECT_REVEAL_TYPE = True
if INJECT_REVEAL_TYPE:
    reveal_type = getattr(_testutils, "reveal_type_wrapper")

_BASE_HREF = "http://dummy"


def _has_bytes_support() -> bool:
    # See https://github.com/lxml/lxml/commit/6619dfd4c446b3a813ab380b22ddd583d32b9a29
    return _lxml_ver != "5.1.0"


class TestInputType:
    # Some funcs perform deepcopy of origin data, which requires original
    # data to be pickleable, and IO buffer can't be pickled.
    def test_bad_input_without_copy(
        self,
        html2_filepath: Path,
        html2_tree: _ElementTree[HtmlElement],
    ) -> None:
        buffer = open(html2_filepath, "rb")
        for bad_input in (html2_filepath, buffer, html2_tree):
            with pytest.raises(
                AttributeError, match="object has no attribute 'find_rel_links'"
            ):
                _ = find_rel_links(cast(Any, bad_input), "nofollow noopener noreferrer")
            with pytest.raises(
                AttributeError, match="object has no attribute 'find_class'"
            ):
                _ = find_class(cast(Any, bad_input), "single")
            with pytest.raises(
                AttributeError, match="object has no attribute 'iterlinks'"
            ):
                _ = iterlinks(cast(Any, bad_input))
        buffer.close()

    def test_bad_input_with_copy(
        self,
        html2_filepath: Path,
        html2_tree: _ElementTree[HtmlElement],
    ) -> None:
        for bad_input in (html2_filepath, html2_tree):
            with pytest.raises(
                AttributeError, match="object has no attribute 'make_links_absolute'"
            ):
                _ = make_links_absolute(cast(Any, bad_input), _BASE_HREF)
            with pytest.raises(
                AttributeError, match="object has no attribute 'resolve_base_href'"
            ):
                _ = resolve_base_href(cast(Any, bad_input))
            with pytest.raises(
                AttributeError, match="object has no attribute 'rewrite_links'"
            ):
                _ = rewrite_links(cast(Any, bad_input), lambda _: None)

    def test_find_rel_links(
        self,
        html2_filepath: Path,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        if _has_bytes_support():
            links = find_rel_links(html2_bytes, "nofollow noopener noreferrer")
            reveal_type(links)
            del links
        links = find_rel_links(str(html2_filepath), "nofollow noopener noreferrer")
        reveal_type(links)
        del links
        links = find_rel_links(html2_str, "nofollow noopener noreferrer")
        reveal_type(links)
        del links

        links = find_rel_links(bightml_root, "nofollow noopener noreferrer")
        reveal_type(links)
        for link in links:
            reveal_type(link)

    def test_find_class(
        self,
        html2_filepath: Path,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        if _has_bytes_support():
            elems = find_class(html2_bytes, "single")
            reveal_type(elems)
            del elems
        elems = find_class(str(html2_filepath), "single")
        reveal_type(elems)
        del elems
        elems = find_class(html2_str, "single")
        reveal_type(elems)
        del elems
        elems = find_class(bightml_root, "single")
        reveal_type(elems)
        for e in elems:
            reveal_type(e)

    def test_iterlinks(
        self,
        html2_filepath: Path,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        if _has_bytes_support():
            results = iterlinks(html2_bytes)
            reveal_type(results)
            del results
        results = iterlinks(str(html2_filepath))
        reveal_type(results)
        del results
        results = iterlinks(html2_str)
        reveal_type(results)
        del results
        results = iterlinks(bightml_root)
        reveal_type(results)
        for r in results:
            assert len(r) == 4
            reveal_type(r[0])
            reveal_type(r[1])
            reveal_type(r[2])
            reveal_type(r[3])


@pytest.mark.parametrize(
    ("func", "args"),
    [
        pytest.param(find_rel_links, ()),
        pytest.param(find_class, ()),
    ],
)
def test_missing_pos_arg(
    html2_str: str,
    func: Callable[..., Any],
    args: Sequence[Any],
) -> None:
    with pytest.raises(TypeError, match="missing 1 required positional argument"):
        _ = func(html2_str, *args)


@pytest.mark.parametrize(
    ("func", "args"),
    [
        pytest.param(find_rel_links, ("", None)),
        pytest.param(find_class, ("", None)),
        pytest.param(iterlinks, (None,)),
    ],
)
def test_too_many_pos_arg(
    html2_str: str,
    func: Callable[..., Any],
    args: Sequence[Any],
) -> None:
    length = len(args)
    match = f"takes {length} positional arguments? but {length + 1} were given"
    with pytest.raises(TypeError, match=match):
        _ = func(html2_str, *args)


# Keyword arguments are not tested here, see TestKeywordArgs below for detail
class TestBadArgs:
    def test_find_rel_links(self, bightml_str: str) -> None:
        links = find_rel_links(bightml_str, "nofollow noopener noreferrer")
        assert len(links) > 0
        del links
        # XPath selection result always generate str, never match bytes
        links = find_rel_links(bightml_str, cast(Any, b"nofollow noopener noreferrer"))
        assert len(links) == 0
        del links
        with pytest.raises(AttributeError, match="object has no attribute 'lower'"):
            _ = find_rel_links(bightml_str, cast(Any, None))

    def test_find_class(self, bightml_str: str) -> None:
        elems1 = find_class(bightml_str, "single")
        reveal_type(elems1)
        assert len(elems1) > 0
        elems2 = find_class(bightml_str, b"single")
        assert len(elems1) == len(elems2)
        # XPath stringify input args so they don't fail,
        # but guaranteed to not produce any result
        result = find_class(bightml_str, cast(Any, None))
        assert len(result) == 0
        del result
        result = find_class(bightml_str, cast(Any, 1))
        assert len(result) == 0

    def test_make_links_absolute(self, html2_str: str) -> None:
        # Arguments below are not tested
        # base_url: behavior depends on document .base_url property
        # resolve_base_href: use bool for easier understanding, but
        #                    anything truthy and falsy works in runtime
        with pytest.raises(
            ValueError, match="unexpected value for handle_failures: 'junk'"
        ):
            _ = make_links_absolute(html2_str, "", True, cast(Any, "junk"))

    def test_resolve_base_href(self, bightml_str: str) -> None:
        with pytest.raises(
            ValueError, match="unexpected value for handle_failures: 'junk'"
        ):
            _ = resolve_base_href(bightml_str, cast(Any, "junk"))

    def test_rewrite_links(self, html2_str: str) -> None:
        with pytest.raises(TypeError, match="'NoneType' object is not callable"):
            _ = rewrite_links(html2_str, cast(Any, None))
        with pytest.raises(
            TypeError, match="takes 0 positional arguments but 1 was given"
        ):
            _ = rewrite_links(html2_str, cast(Any, lambda: _BASE_HREF))
        with pytest.raises(
            TypeError, match="Argument must be bytes or unicode, got 'int'"
        ):
            _ = rewrite_links(html2_str, cast(Any, lambda _: 1))  # pyright: ignore[reportUnknownLambdaType]

        def repl_func(orig: bytes) -> bytes:
            return orig.replace(b"http", b"ftp")

        with pytest.raises(TypeError, match="argument 1 must be str, not bytes"):
            _ = rewrite_links(html2_str, cast(Any, repl_func))

    #
    # non-Element input + keyword args = Exception
    # See comment on module level functions in html/_funcs.pyi
    #

    def test_bad_methodfunc(
        self,
        html2_str: str,
        html2_bytes: bytes,
        html2_filepath: Path,
        bightml_root: HtmlElement,
    ) -> None:
        sources = [html2_str, str(html2_filepath), html2_bytes]
        if _has_bytes_support():
            sources.pop()
        for input in sources:
            with pytest.raises(
                TypeError, match="got an unexpected keyword argument 'handle_failures'"
            ):
                _ = make_links_absolute(
                    doc=cast(Any, input), base_url=None, handle_failures=None
                )
        with pytest.raises(
            TypeError, match="got an unexpected keyword argument 'class_name'"
        ):
            _ = find_class(cast(Any, html2_str), class_name="something")
        # kw are fine for Element input
        result = make_links_absolute(bightml_root, "", handle_failures=None)
        reveal_type(result)


class TestOutputType:
    BASE = "http://dummy.link"

    def test_make_links_absolute(
        self,
        bightml_str: str,
        bightml_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        if _has_bytes_support():
            with pytest.raises(
                TypeError, match="No base_url given, and the document has no base_url"
            ):
                _ = make_links_absolute(bightml_bytes)
            result = make_links_absolute(bightml_bytes, _BASE_HREF)
            reveal_type(result)
            del result
        with pytest.raises(TypeError, match="Cannot mix str and non-str"):
            _ = make_links_absolute(bightml_str, cast(Any, _BASE_HREF.encode("ascii")))
        result1 = make_links_absolute(bightml_str, _BASE_HREF)
        reveal_type(result1)
        del result1
        result2 = make_links_absolute(bightml_root, _BASE_HREF)
        reveal_type(result2)

    def test_resolve_base_href(
        self,
        bightml_str: str,
        bightml_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        if _has_bytes_support():
            result = resolve_base_href(bightml_bytes)
            reveal_type(result)
            del result
        result1 = resolve_base_href(bightml_str)
        reveal_type(result1)
        del result1
        result2 = resolve_base_href(bightml_root)
        reveal_type(result2)

    def test_rewrite_links(
        self,
        bightml_str: str,
        bightml_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        if _has_bytes_support():
            result = rewrite_links(bightml_bytes, lambda _: _BASE_HREF)
            reveal_type(result)
            del result
        with pytest.raises(TypeError, match="can only concatenate str"):
            _ = rewrite_links(
                bightml_str, lambda _: cast(Any, _BASE_HREF.encode("ASCII"))
            )
        result2 = rewrite_links(bightml_str, lambda _: _BASE_HREF)
        reveal_type(result2)
        del result2
        result3 = rewrite_links(bightml_root, lambda _: None)
        reveal_type(result3)
