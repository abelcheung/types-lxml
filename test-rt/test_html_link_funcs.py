from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Sequence, cast

import _testutils
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
        h1_filepath: Path,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        buffer = open(h1_filepath, "rb")
        for bad_input in (h1_filepath, buffer, html_tree):
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
        h1_filepath: Path,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        for bad_input in (h1_filepath, html_tree):
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
        h1_filepath: Path,
        h1_str: str,
        h1_bytes: bytes,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        if _has_bytes_support():
            links = find_rel_links(h1_bytes, "nofollow noopener noreferrer")
            reveal_type(links)
            del links
        links = find_rel_links(str(h1_filepath), "nofollow noopener noreferrer")
        reveal_type(links)
        del links
        links = find_rel_links(html_tree.getroot(), "nofollow noopener noreferrer")
        reveal_type(links)
        del links
        links = find_rel_links(h1_str, "nofollow noopener noreferrer")
        reveal_type(links)

        for link in links:
            reveal_type(link)

    def test_find_class(
        self,
        h1_filepath: Path,
        h1_str: str,
        h1_bytes: bytes,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        if _has_bytes_support():
            elems = find_class(h1_bytes, "single")
            reveal_type(elems)
            del elems
        elems = find_class(str(h1_filepath), "single")
        reveal_type(elems)
        del elems
        elems = find_class(h1_str, "single")
        reveal_type(elems)
        del elems
        elems = find_class(html_tree.getroot(), "single")
        reveal_type(elems)
        for e in elems:
            reveal_type(e)

    def test_iterlinks(
        self,
        h1_filepath: Path,
        h1_str: str,
        h1_bytes: bytes,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        if _has_bytes_support():
            results = iterlinks(h1_bytes)
            reveal_type(results)
            del results
        results = iterlinks(str(h1_filepath))
        reveal_type(results)
        del results
        results = iterlinks(h1_str)
        reveal_type(results)
        del results
        results = iterlinks(html_tree.getroot())
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
    h1_str: str,
    func: Callable[..., Any],
    args: Sequence[Any],
) -> None:
    with pytest.raises(TypeError, match="missing 1 required positional argument"):
        _ = func(h1_str, *args)


@pytest.mark.parametrize(
    ("func", "args"),
    [
        pytest.param(find_rel_links, ("", None)),
        pytest.param(find_class, ("", None)),
        pytest.param(iterlinks, (None,)),
    ],
)
def test_too_many_pos_arg(
    h1_str: str,
    func: Callable[..., Any],
    args: Sequence[Any],
) -> None:
    length = len(args)
    match = f"takes {length} positional arguments? but {length + 1} were given"
    with pytest.raises(TypeError, match=match):
        _ = func(h1_str, *args)


# Keyword arguments are not tested here, see TestKeywordArgs below for detail
class TestBadArgs:
    def test_find_rel_links(self, h1_str: str) -> None:
        links = find_rel_links(h1_str, "nofollow noopener noreferrer")
        assert len(links) > 0
        del links
        # XPath selection result always generate str, never match bytes
        links = find_rel_links(h1_str, cast(Any, b"nofollow noopener noreferrer"))
        assert len(links) == 0
        del links
        with pytest.raises(AttributeError, match="object has no attribute 'lower'"):
            _ = find_rel_links(h1_str, cast(Any, None))

    def test_find_class(self, h1_str: str) -> None:
        elems1 = find_class(h1_str, "single")
        reveal_type(elems1)
        assert len(elems1) > 0
        elems2 = find_class(h1_str, b"single")
        assert len(elems1) == len(elems2)
        # XPath stringify input args so they don't fail,
        # but guaranteed to not produce any result
        result = find_class(h1_str, cast(Any, None))
        assert len(result) == 0
        del result
        result = find_class(h1_str, cast(Any, 1))
        assert len(result) == 0

    def test_make_links_absolute(self, h1_str: str) -> None:
        # Arguments below are not tested
        # base_url: behavior depends on document .base_url property
        # resolve_base_href: use bool for easier understanding, but
        #                    anything truthy and falsy works in runtime
        with pytest.raises(
            ValueError, match="unexpected value for handle_failures: 'junk'"
        ):
            _ = make_links_absolute(h1_str, "", True, cast(Any, "junk"))

    def test_resolve_base_href(self, h1_str: str) -> None:
        with pytest.raises(
            ValueError, match="unexpected value for handle_failures: 'junk'"
        ):
            _ = resolve_base_href(h1_str, cast(Any, "junk"))

    def test_rewrite_links(self, h1_str: str) -> None:
        with pytest.raises(TypeError, match="'NoneType' object is not callable"):
            _ = rewrite_links(h1_str, cast(Any, None))
        with pytest.raises(
            TypeError, match="takes 0 positional arguments but 1 was given"
        ):
            _ = rewrite_links(h1_str, cast(Any, lambda: _BASE_HREF))
        with pytest.raises(
            TypeError, match="Argument must be bytes or unicode, got 'int'"
        ):
            _ = rewrite_links(h1_str, lambda _: 1)  # pyright: ignore

        def repl_func(orig: bytes) -> bytes:
            return orig.replace(b"http", b"ftp")

        with pytest.raises(TypeError, match="argument 1 must be str, not bytes"):
            _ = rewrite_links(h1_str, cast(Any, repl_func))

    #
    # XXX lxml bug
    # For standalone link funcs,
    # non-Element input + keyword args = Exception
    # See html/_funcs.pyi for detail
    #

    def test_bad_methodfunc(
        self,
        h1_str: str,
        h1_bytes: bytes,
        h1_filepath: Path,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        sources: list[Any] = [h1_str, str(h1_filepath)]
        if _has_bytes_support():
            sources.append(h1_bytes)
        for input in sources:
            with pytest.raises(
                TypeError, match="got an unexpected keyword argument 'handle_failures'"
            ):
                _ = make_links_absolute(doc=input, base_url=None, handle_failures=None)
        with pytest.raises(
            TypeError, match="got an unexpected keyword argument 'class_name'"
        ):
            _ = find_class(cast(Any, h1_str), class_name="something")
        # kw are fine for Element input
        result = make_links_absolute(html_tree.getroot(), "", handle_failures=None)
        reveal_type(result)


class TestOutputType:
    BASE = "http://dummy.link"

    def test_make_links_absolute(
        self,
        h1_str: str,
        h1_bytes: bytes,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        if _has_bytes_support():
            with pytest.raises(
                TypeError, match="No base_url given, and the document has no base_url"
            ):
                _ = make_links_absolute(h1_bytes)
            result = make_links_absolute(h1_bytes, _BASE_HREF)
            reveal_type(result)
            del result
        with pytest.raises(TypeError, match="Cannot mix str and non-str"):
            _ = make_links_absolute(h1_str, cast(Any, _BASE_HREF.encode("ascii")))
        result = make_links_absolute(h1_str, _BASE_HREF)
        reveal_type(result)
        del result
        root = html_tree.getroot()
        result = make_links_absolute(root, _BASE_HREF)
        reveal_type(result)

    def test_resolve_base_href(
        self,
        h1_str: str,
        h1_bytes: bytes,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        if _has_bytes_support():
            result = resolve_base_href(h1_bytes)
            reveal_type(result)
            del result
        result = resolve_base_href(h1_str)
        reveal_type(result)
        del result
        root = html_tree.getroot()
        result = resolve_base_href(root)
        reveal_type(result)

    def test_rewrite_links(
        self,
        h1_str: str,
        h1_bytes: bytes,
        html_tree: _ElementTree[HtmlElement],
    ) -> None:
        if _has_bytes_support():
            result = rewrite_links(h1_bytes, lambda _: _BASE_HREF)
            reveal_type(result)
            del result
        with pytest.raises(TypeError, match="can only concatenate str"):
            _ = rewrite_links(h1_str, lambda _: cast(Any, _BASE_HREF.encode("ASCII")))
        result = rewrite_links(h1_str, lambda _: _BASE_HREF)
        reveal_type(result)
        del result
        root = html_tree.getroot()
        result = rewrite_links(root, lambda _: None)
        reveal_type(result)
