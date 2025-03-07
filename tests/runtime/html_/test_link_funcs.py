from __future__ import annotations

import inspect
import sys
from collections.abc import (
    Callable,
    Iterable,
)
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from types import NoneType, NotImplementedType
from typing import (
    Any,
    cast,
)

import pytest
from hypothesis import (
    HealthCheck,
    given,
    settings,
)
from lxml.etree import (
    LXML_VERSION,
    XPathResultError,
    _Element,
    _ElementTree,
    _ElementUnicodeResult,
    tostring,
)
from lxml.html import (
    Element,
    HtmlElement,
    find_class,
    find_rel_links,
    iterlinks,
    make_links_absolute,
    parse,
    resolve_base_href,
    rewrite_links,
)

from .._testutils import strategy as _st
from .._testutils.common import attr_value_types

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


byte_bug_marker = pytest.mark.xfail(
    LXML_VERSION[:3] == (5, 1, 0),
    reason="lxml 5.1.0 has bug in bytes support of html processing functions",
)

_BASE_HREF = "http://dummy.base"

# Can't casually test html link function signatures as they are wrapped within
# _MethodFunc, which mangles corresponding HtmlMixin methods with a generic
# signature.


def _get_elementtree_from_file(filepath: Path) -> _ElementTree[HtmlElement]:
    with filepath.open("rb") as fp:
        return parse(fp)


# COMPLETED
class TestInputOutputType:
    def test_bad_input_arg(
        self,
        html2_filepath: Path,
        generate_input_file_arguments: Callable[..., Iterable[Any]],
    ) -> None:
        for bad_input in generate_input_file_arguments(
            html2_filepath,
            include=(_get_elementtree_from_file,),
            # lxml permits str and bytes *as input data*, but we can't
            # distinguish data from file name in terms of typing
            exclude_type=(str, bytes),
        ):
            with pytest.raises(AttributeError):
                _ = find_rel_links(bad_input, "nofollow")
            with pytest.raises(AttributeError):
                _ = find_class(bad_input, "single")
            with pytest.raises(AttributeError):
                _ = iterlinks(bad_input)
            # _MethodFunc performs deepcopy on input for following functions,
            # which raises TypeError on non-pickerable objects
            with pytest.raises((AttributeError, TypeError)):
                _ = make_links_absolute(bad_input, _BASE_HREF)
            with pytest.raises((AttributeError, TypeError)):
                _ = resolve_base_href(bad_input)
            with pytest.raises((AttributeError, TypeError)):
                _ = rewrite_links(bad_input, lambda _: None)

    @byte_bug_marker
    def test_find_rel_links(
        self,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        for data in (html2_bytes, html2_str, bightml_root):
            result = find_rel_links(data, "nofollow noopener noreferrer")
            reveal_type(result)

    @byte_bug_marker
    def test_find_class(
        self,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        for data in (html2_bytes, html2_str, bightml_root):
            result = find_class(data, "single")
            reveal_type(result)

    @byte_bug_marker
    def test_iterlinks(
        self,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        for data in (html2_bytes, html2_str, bightml_root):
            itr = iterlinks(data)  # type: ignore[type-var]
            reveal_type(itr)
            for link in itr:
                reveal_type(link)
            del itr

    # Unroll loops for remaining test functions, as union of input types
    # is considered incompatible to TypeVars

    @byte_bug_marker
    def test_make_links_absolute(
        self,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        # Already beyond the scope of typing. Let it stay nonetheless,
        # in case some idea pops up on how to improve this.
        with pytest.raises(
            TypeError, match="No base_url given, and the document has no base_url"
        ):
            _ = make_links_absolute(html2_bytes)
        reveal_type(make_links_absolute(html2_str, _BASE_HREF))
        reveal_type(make_links_absolute(html2_bytes, _BASE_HREF))
        reveal_type(make_links_absolute(bightml_root, _BASE_HREF))

    @byte_bug_marker
    def test_resolve_base_href(
        self,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        reveal_type(resolve_base_href(html2_str))
        reveal_type(resolve_base_href(html2_bytes))
        reveal_type(resolve_base_href(bightml_root))

    @byte_bug_marker
    def test_rewrite_links(
        self,
        html2_str: str,
        html2_bytes: bytes,
        bightml_root: HtmlElement,
    ) -> None:
        reveal_type(rewrite_links(html2_str, lambda _: _BASE_HREF))
        reveal_type(rewrite_links(html2_bytes, lambda _: _BASE_HREF))
        reveal_type(rewrite_links(bightml_root, lambda _: _BASE_HREF))


# COMPLETED
class TestFindRelLinksArg:
    # XPath selection result always generate str, never match other
    # string-like types. So bytes and bytearray are banned in stub
    # despite the fact that they don't raise exception
    def test_wrong_type_no_raise(self, bightml_root: HtmlElement) -> None:
        attributes = "nofollow noopener noreferrer"
        links = find_rel_links(bightml_root, attributes)
        assert len(links) > 0
        del links
        b = attributes.encode("utf-8")
        links = find_rel_links(bightml_root, cast(Any, b))
        assert len(links) == 0
        links = find_rel_links(bightml_root, cast(Any, bytearray(b)))
        assert len(links) == 0

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(t=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_wrong_type_raises(
        self, disposable_html_element: HtmlElement, t: Any
    ) -> None:
        # Besides instances of str, bytes and bytearray, the aforementioned
        # types themselves also has 'lower' attribute, so using them as
        # input raises TypeError instead (unbound method needs argument)
        with pytest.raises((AttributeError, TypeError)):
            _ = find_rel_links(disposable_html_element, t)


# COMPLETED
class TestFindClassArg:
    def test_valid_type(self, bightml_str: str) -> None:
        elems1 = find_class(bightml_str, "single")
        reveal_type(elems1)
        assert len(elems1) > 0
        elems2 = find_class(bightml_str, b"single")
        assert len(elems1) == len(elems2)

    @staticmethod
    def _non_xpathobject_filter(x: Any) -> bool:
        if inspect.isclass(x):
            return True
        if not hasattr(x, "__len__"):
            return True
        # range objects are moody, ranging from no exception
        # to XPathResultError then to OverflowError
        if not isinstance(x, range):
            return len(x) > 0
        return (x.stop - x.start) / x.step > 0

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        t=_st.all_instances_except_of_type(
            str,
            bytes,
            bytearray,
            NoneType,
            bool,
            int,
            float,
            Fraction,
            _Element,
            Decimal,
        ).filter(_non_xpathobject_filter)
    )
    @pytest.mark.slow
    def test_wrong_type_raises(
        self, disposable_html_element: HtmlElement, t: Any
    ) -> None:
        # _wrapXPathObject can produce different exceptions
        with pytest.raises((XPathResultError, TypeError)):
            _ = find_class(disposable_html_element, t)

    # Several basic types are acceptable as XPathObject and thus stringified,
    # yet they will never ever match class names
    def test_wrong_type_no_raise(self, disposable_html_element: HtmlElement) -> None:
        arg: Any
        for arg in (  # pyright: ignore[reportAssignmentType]
            None,
            tuple(),
            True,
            3,
            2.0,
            Element("foo"),
            Fraction(1, 2),
            range(1, 1),  # degenerates to nothing
            Decimal(1),
        ):
            elems = find_class(disposable_html_element, arg)
            assert len(elems) == 0


# COMPLETED
class TestResolveBaseHrefArg:
    def test_handle_failures_valid_type(
        self, disposable_html_with_base_href: HtmlElement
    ) -> None:
        old_links = [
            cast(_ElementUnicodeResult, link)
            for link in disposable_html_with_base_href.xpath("//a/@href")
        ]
        for arg in ("discard", "ignore", None):
            new_root = resolve_base_href(
                disposable_html_with_base_href,
                arg,  # type: ignore[arg-type,call-overload]
            )
            new_links = [
                cast(_ElementUnicodeResult, link)
                for link in new_root.xpath("//a/@href")
            ]
            for old, new in zip(old_links, new_links):
                if old.startswith("http"):
                    assert old == new
                else:
                    assert old != new

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        t=_st.all_instances_except_of_type().filter(
            lambda x: x not in ("discard", "ignore", None)
        )
    )
    @pytest.mark.slow
    def test_handle_failures_wrong_type(
        self, disposable_html_with_base_href: HtmlElement, t: Any
    ) -> None:
        # collection raises TypeError instead
        # because of error in constructing exception
        with pytest.raises((ValueError, TypeError)):
            _ = resolve_base_href(disposable_html_with_base_href, handle_failures=t)


class TestMakeLinksAbsoluteArg:
    def test_handle_failures_valid_type(
        self, disposable_html_with_base_href: HtmlElement
    ) -> None:
        old_links = [
            cast(_ElementUnicodeResult, link)
            for link in disposable_html_with_base_href.xpath("//a/@href")
        ]
        for arg in ("discard", "ignore", None):
            new_root = make_links_absolute(
                disposable_html_with_base_href,
                _BASE_HREF,
                handle_failures=arg,  # type: ignore[arg-type,call-overload]
            )
            new_links = [
                cast(_ElementUnicodeResult, link)
                for link in new_root.xpath("//a/@href")
            ]
            for old, new in zip(old_links, new_links):
                if old.startswith("http"):
                    assert old == new
                else:
                    assert old != new

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        t=_st.all_instances_except_of_type().filter(
            lambda _: _ not in ("ignore", "discard", None)
        )
    )
    @pytest.mark.slow
    def test_handle_failures_wrong_type(
        self, disposable_html_with_base_href: HtmlElement, t: Any
    ) -> None:
        with pytest.raises((ValueError, TypeError)):
            _ = make_links_absolute(
                disposable_html_with_base_href, _BASE_HREF, handle_failures=t
            )

    # Not testing resolve_base_href type, as it is a truthy/falsy argument
    # that can be anything

    # Falsy values got short circuited by urljoin() and never raises
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(t=_st.all_instances_except_of_type(str, NoneType, NotImplementedType).filter(bool))
    @pytest.mark.slow
    def test_base_href(
        self, disposable_html_with_base_href: HtmlElement, t: Any
    ) -> None:
        with pytest.raises(TypeError, match="Cannot mix str and non-str arguments"):
            _ = make_links_absolute(disposable_html_with_base_href, base_url=t)


# COMPLETED
# Need HTML fixtures that really contains link, otherwise
# iterlinks() is a no-op and most tests won't fail
class TestRewriteLinksArg:
    @given(t=_st.all_instances_except_of_type().filter(lambda x: not callable(x)))
    def test_link_repl_func_is_callable(
        self, disposable_html_with_base_href: HtmlElement, t: Any
    ) -> None:
        with pytest.raises(TypeError, match="object is not callable"):
            _ = rewrite_links(disposable_html_with_base_href, t)

    # QName has the unintended consequence of doing tag name check while
    # replaced link is an attribute value, thus raising ValueError instead
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(
        t=_st.all_instances_except_of_type(
            *attr_value_types.allow,
            *attr_value_types.skip,
            NoneType,
        )
    )
    @pytest.mark.slow
    def test_link_repl_func_output_type(
        self, disposable_html_with_base_href: HtmlElement, t: Any
    ) -> None:
        with pytest.raises(TypeError, match="Argument must be bytes or unicode"):
            _ = rewrite_links(disposable_html_with_base_href, lambda _: t)

    def test_link_repl_func_input_arg(
        self, disposable_html_with_base_href: HtmlElement
    ) -> None:
        with pytest.raises(
            TypeError, match="takes 0 positional arguments but 1 was given"
        ):
            _ = rewrite_links(
                disposable_html_with_base_href, cast(Any, lambda: _BASE_HREF)
            )
        # Induce it into revealing feeded data type by supplying wrong function
        with pytest.raises(
            TypeError, match="'str' object cannot be interpreted as an integer"
        ):
            _ = rewrite_links(disposable_html_with_base_href, cast(Any, range))

    # Not testing resolve_base_href type, as it is a truthy/falsy argument
    # that can be anything

    # Falsy values got short circuited by urljoin() and never raises
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=500)
    @given(t=_st.all_instances_except_of_type(str, NoneType, NotImplementedType).filter(bool))
    @pytest.mark.slow
    def test_base_href(
        self, disposable_html_with_base_href: HtmlElement, t: Any
    ) -> None:
        with pytest.raises(TypeError, match="Cannot mix str and non-str arguments"):
            _ = rewrite_links(disposable_html_with_base_href, str, base_href=t)


# COMPLETED
# non-Element input + keyword args = Exception
# See comment on module level functions in html/_funcs.pyi
# Not just for pytest, we want to make sure they show
# warnings in IDE too.
@byte_bug_marker
class TestMethodFuncBug:
    def test_find_rel_links(self, disposable_html_with_base_href: HtmlElement) -> None:
        for encoding in ("utf-8", str):
            content = tostring(disposable_html_with_base_href, encoding=encoding)
            with pytest.raises(TypeError, match="got an unexpected keyword argument"):
                _ = find_rel_links(content, rel="nofollow")
        _ = find_rel_links(disposable_html_with_base_href, rel="nofollow")

    def test_find_class(self, disposable_html_with_base_href: HtmlElement) -> None:
        for encoding in ("utf-8", str):
            content = tostring(disposable_html_with_base_href, encoding=encoding)
            with pytest.raises(TypeError, match="got an unexpected keyword argument"):
                _ = find_class(content, class_name="single")
        _ = find_class(disposable_html_with_base_href, class_name="single")

    def test_make_links_absolute(
        self, disposable_html_with_base_href: HtmlElement
    ) -> None:
        str_content = tostring(disposable_html_with_base_href, encoding=str)
        bytes_content = tostring(disposable_html_with_base_href, encoding="utf-8")

        _ = make_links_absolute(str_content, base_url=_BASE_HREF)
        _ = make_links_absolute(bytes_content, base_url=_BASE_HREF)

        for input in (str_content, bytes_content):
            with pytest.raises(TypeError, match="got an unexpected keyword argument"):
                _ = make_links_absolute(  # type: ignore[call-overload]
                    input, _BASE_HREF, resolve_base_href=True
                )
        _ = make_links_absolute(
            disposable_html_with_base_href, _BASE_HREF, resolve_base_href=True
        )

        for input in (str_content, bytes_content):
            with pytest.raises(TypeError, match="got an unexpected keyword argument"):
                _ = make_links_absolute(  # type: ignore[call-overload]
                    input, _BASE_HREF, handle_failures=None
                )
        _ = make_links_absolute(
            disposable_html_with_base_href, _BASE_HREF, handle_failures=None
        )

    def test_resolve_base_href(
        self,
        disposable_html_with_base_href: HtmlElement,
    ) -> None:
        for encoding in ("utf-8", str):
            content = tostring(disposable_html_with_base_href, encoding=encoding)
            with pytest.raises(TypeError, match="got an unexpected keyword argument"):
                _ = resolve_base_href(  # type: ignore[call-overload]
                    content, handle_failures=None
                )
        _ = resolve_base_href(disposable_html_with_base_href, handle_failures=None)

    def test_rewrite_links(
        self,
        disposable_html_with_base_href: HtmlElement,
    ) -> None:
        str_content = tostring(disposable_html_with_base_href, encoding=str)
        byte_content = tostring(disposable_html_with_base_href, encoding="utf-8")

        for input in (str_content, byte_content):
            with pytest.raises(TypeError, match="got an unexpected keyword argument"):
                _ = rewrite_links(  # type: ignore[call-overload]
                    input, link_repl_func=str
                )
        _ = rewrite_links(disposable_html_with_base_href, link_repl_func=str)

        for input in (str_content, byte_content):
            with pytest.raises(TypeError, match="got an unexpected keyword argument"):
                _ = rewrite_links(  # type: ignore[call-overload]
                    input, str, resolve_base_href=False
                )
        _ = rewrite_links(disposable_html_with_base_href, str, resolve_base_href=False)

        for input in (str_content, byte_content):
            with pytest.raises(TypeError, match="got an unexpected keyword argument"):
                _ = rewrite_links(  # type: ignore[call-overload]
                    input, str, base_href=_BASE_HREF
                )
        _ = rewrite_links(disposable_html_with_base_href, str, base_href=_BASE_HREF)
