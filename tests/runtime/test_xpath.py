from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from inspect import Parameter
from io import BytesIO, StringIO
from types import NoneType
from typing import Any, cast

import pytest
from hypothesis import HealthCheck, given, settings
from lxml.etree import (
    ETXPath,
    XPath,
    XPathDocumentEvaluator,
    XPathElementEvaluator,
    XPathEvalError,
    XPathEvaluator,
    XPathSyntaxError,
    _Element,
    _ElementTree,
    _ElementUnicodeResult,
    _ListErrorLog as _ListErrorLog,
    iselement,
)

from ._testutils import signature_tester, strategy as _st
from ._testutils.common import (
    can_practically_iter,
    is_iterator_of_nothing,
)
from ._testutils.errors import (
    raise_attr_not_writable,
    raise_invalid_lxml_type,
    raise_invalid_utf8_type,
    raise_non_iterable,
    raise_unexpected_type,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


# -- _Element.xpath method tests --


class TestElementXPathSignature:
    @signature_tester(_Element.xpath, (
        ('_path'         , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ('namespaces'    , Parameter.KEYWORD_ONLY      , None           ),
        ('extensions'    , Parameter.KEYWORD_ONLY      , None           ),
        ('smart_strings' , Parameter.KEYWORD_ONLY      , True           ),
        ('_variables'    , Parameter.VAR_KEYWORD       , Parameter.empty),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass


class TestElementXPathPath:
    def test_path_str_ok(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item")
        assert len(result) == 3
        for elem in result:
            assert iselement(elem)

    def test_path_bytes_ok(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath(b"//item")
        assert len(result) == 3

    def test_path_bytearray_ok(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath(bytearray(b"//item"))
        assert len(result) == 3

    def test_path_returns_string(self, xml2_root: _Element) -> None:
        assert xml2_root.xpath("string(//orderperson)") == "John Smith"

    def test_path_returns_float(self, xml2_root: _Element) -> None:
        assert xml2_root.xpath("count(//item)") == 3.0

    def test_path_returns_bool(self, xml2_root: _Element) -> None:
        assert xml2_root.xpath("boolean(//item)") is True

    def test_path_returns_attribute(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item/@id")
        assert len(result) == 3
        for r in result:
            assert isinstance(r, str)

    def test_invalid_xpath_expr(self, xml2_root: _Element) -> None:
        with pytest.raises(XPathEvalError):
            xml2_root.xpath("///invalid[")

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_path_arg_bad_1(self, disposable_element: _Element, thing: Any) -> None:
        # pyrefly: ignore[no-matching-overload]
        with pytest.raises((TypeError, XPathSyntaxError)):
            disposable_element.xpath(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_path_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with pytest.raises(TypeError):
            disposable_element.xpath(iterable_of("//item"))


class TestElementXPathNamespaces:
    def test_namespaces_none(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item", namespaces=None)
        assert len(result) == 3

    def test_namespaces_str_dict(self, svg_root: _Element) -> None:
        ns = {"m": "http://example.org/myapp"}
        result = svg_root.xpath("//m:piechart", namespaces=ns)
        assert len(result) > 0

    def test_namespaces_bytes_dict(self, svg_root: _Element) -> None:
        ns = {b"m": b"http://example.org/myapp"}
        result = svg_root.xpath(b"//m:piechart", namespaces=ns)
        assert len(result) > 0

    def test_namespaces_tuple_iterable(self, svg_root: _Element) -> None:
        ns = iter([("m", "http://example.org/myapp")])
        result = svg_root.xpath("//m:piechart", namespaces=cast(Any, ns))
        assert len(result) > 0

    def test_namespaces_bytes_tuple_iterable(self, svg_root: _Element) -> None:
        ns = [(b"m", b"http://example.org/myapp")]
        result = svg_root.xpath(b"//m:piechart", namespaces=cast(Any, ns))
        assert len(result) > 0

    # StringIO and BytesIO can be iterated since their strings
    # can be unpacked into prefix/URI pairs
    @settings(
        suppress_health_check=[
            HealthCheck.function_scoped_fixture,
            HealthCheck.too_slow,
        ],
        max_examples=300,
    )
    @given(
        thing=_st
        .all_instances_except_of_type(dict, NoneType, StringIO, BytesIO)
        .filter(lambda x: x is not NotImplemented and bool(x))
        .filter(lambda x: not is_iterator_of_nothing(x))
    )
    @pytest.mark.slow
    def test_namespaces_arg_bad(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        if isinstance(thing, Iterable) or can_practically_iter(thing):
            # pyrefly: ignore[no-matching-overload]
            raise_cm = pytest.raises((TypeError, ValueError))
        else:
            raise_cm = raise_non_iterable
        with raise_cm:
            disposable_element.xpath(  # pyright: ignore[reportUnknownMemberType]
                "//foo", namespaces=cast(Any, thing)
            )


class TestElementXPathExtensions:
    def test_extensions_none(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item", extensions=None)
        assert len(result) == 3

    def test_extensions_dict_str_ns(self, xml2_root: _Element) -> None:
        def my_ext(context: Any, arg: Any) -> str:
            return "hello"

        ext: dict[tuple[str, str], Callable[..., Any]] = {
            ("http://myns", "myfunc"): my_ext
        }
        ns = {"my": "http://myns"}
        result = xml2_root.xpath(
            "my:myfunc(//orderperson)", namespaces=ns, extensions=ext
        )
        assert result == "hello"

    def test_extensions_dict_none_ns(self, xml2_root: _Element) -> None:
        def my_lower(context: Any, nodes: list[Any]) -> str:
            if len(nodes) > 0:
                return str(nodes[0].text).lower()
            return ""

        ext: dict[tuple[None, str], Callable[..., Any]] = {
            (None, "lower"): my_lower
        }
        result = xml2_root.xpath("lower(//orderperson)", extensions=ext)
        assert result == "john smith"

    def test_extensions_list_of_dicts(self, xml2_root: _Element) -> None:
        def ext_func(context: Any, arg: Any) -> int:
            return 42

        ext_list = [{("http://ns1", "func1"): ext_func}]
        ns = {"ns1": "http://ns1"}
        result = xml2_root.xpath(
            "ns1:func1('x')", namespaces=ns, extensions=ext_list
        )
        assert result == 42

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(
        thing=_st
        .all_instances_except_of_type(dict, list, tuple, NoneType)
        .filter(lambda x: x is not NotImplemented and bool(x))
        .filter(lambda x: not is_iterator_of_nothing(x))
    )
    @pytest.mark.slow
    def test_extensions_arg_bad(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        # pyrefly: ignore[no-matching-overload]
        with pytest.raises((TypeError, AttributeError)):
            disposable_element.xpath("//foo", extensions=thing)


class TestElementXPathSmartStrings:
    def test_smart_strings_true(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//orderperson/text()", smart_strings=True)
        result = cast(list[_ElementUnicodeResult], result)
        assert len(result) == 1
        val = result[0]
        assert isinstance(val, _ElementUnicodeResult)
        assert val.is_text is True
        assert val.is_tail is False
        assert val.is_attribute is False
        parent = val.getparent()
        assert parent is not None
        assert parent.tag == "orderperson"

    def test_smart_strings_false(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//orderperson/text()", smart_strings=False)
        assert len(result) == 1
        val = result[0]
        assert type(val) is str
        assert not isinstance(val, _ElementUnicodeResult)

    def test_smart_strings_attribute(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item/@id", smart_strings=True)
        assert len(result) == 3
        for val in result:
            assert isinstance(val, _ElementUnicodeResult)
            assert val.is_attribute is True
            assert val.is_text is False
            assert val.attrname == "id"

    def test_smart_strings_tail(self, xml2_root: _Element) -> None:
        # Comments have tail text in shiporder.xml
        result = xml2_root.xpath("//comment()/following-sibling::text()")
        for val in result:
            if isinstance(val, _ElementUnicodeResult):
                assert val.is_tail is True


class TestElementXPathVariables:
    def test_variable_str(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item[@id = $myid]", myid="b-001")
        assert len(result) == 1
        elem = result[0]
        assert iselement(elem)
        assert elem.attrib["id"] == "b-001"

    def test_variable_bytes(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item[@id = $myid]", myid=b"b-002")
        assert len(result) == 1

    def test_variable_int(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item[position() = $pos]", pos=2)
        assert len(result) == 1

    def test_variable_float(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item[price > $limit]", limit=10.0)
        assert len(result) == 1

    def test_variable_bool(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath("//item[$flag]", flag=True)
        assert len(result) == 3

        result = xml2_root.xpath("//item[$flag]", flag=False)
        assert len(result) == 0

    def test_variable_element(self, xml2_root: _Element) -> None:
        first_item = xml2_root.xpath("//item")[0]
        assert iselement(first_item)
        # Use element in xpath variable context
        result = xml2_root.xpath("$elem/@id", elem=first_item)
        assert len(result) == 1

    def test_variable_element_list(self, xml2_root: _Element) -> None:
        items: list[_Element] = xml2_root.xpath("//item")
        result = xml2_root.xpath("count($elems)", elems=items)
        assert result == 3.0

    def test_multiple_variables(self, xml2_root: _Element) -> None:
        result = xml2_root.xpath(
            "//item[@id = $myid and price > $limit]",
            myid="b-001",
            limit=10.0,
        )
        assert len(result) == 1


# -- XPath compiled expression tests --


class TestXPathInit:
    # XPath has generic __init__ signature

    def test_properties(self) -> None:
        xpath_obj = XPath("//item")
        reveal_type(xpath_obj)

        reveal_type(xpath_obj.path)
        assert xpath_obj.path == "//item"

        reveal_type(xpath_obj.error_log)
        assert len(xpath_obj.error_log) == 0

        for attr in ("path", "error_log"):
            with raise_attr_not_writable:
                setattr(xpath_obj, attr, getattr(xpath_obj, attr))

    def test_path_str(self) -> None:
        xpath_obj = XPath("//item")
        assert xpath_obj.path == "//item"

    def test_path_bytes(self) -> None:
        xpath_obj = XPath(b"//item")
        assert xpath_obj.path == "//item"

    def test_invalid_path(self) -> None:
        with pytest.raises(XPathSyntaxError):
            XPath("///invalid[")

    def test_no_positional_arg(self) -> None:
        with pytest.raises(TypeError):
            # pyrefly: ignore[missing-argument]
            XPath()  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

    def test_two_positional_args(self) -> None:
        with pytest.raises(TypeError):
            # pyrefly: ignore[bad-argument-count]
            XPath("//a", "//b")  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_path_arg_bad(self, thing: Any) -> None:
        # pyrefly: ignore[no-matching-overload]
        with pytest.raises((TypeError, XPathSyntaxError)):
            XPath(thing)


class TestXPathCall:
    def test_call_element(
        self, xml2_root: _Element
    ) -> None:
        xpath_obj = XPath("//item")
        assert len(xpath_obj(xml2_root)) == 3

    def test_call_tree(
        self, xml2_tree: _ElementTree
    ) -> None:
        xpath_obj = XPath("//item")
        assert len(xpath_obj(xml2_tree)) == 3

    def test_call_with_variables(self, xml2_root: _Element) -> None:
        xpath_obj = XPath("//item[@id = $myid]")
        result = xpath_obj(xml2_root, myid="b-001")
        assert len(result) == 1

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_call_arg_bad_1(self, thing: Any) -> None:
        xpath_obj = XPath("//item")
        with raise_invalid_lxml_type:
            xpath_obj(thing)  # pyright: ignore[reportUnknownVariableType]

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_arg_bad_2(
        self,
        iterable_of: Any,
        xml2_root: _Element,
        xml2_tree: _ElementTree,
    ) -> None:
        xpath_obj = XPath("//item")
        with raise_invalid_lxml_type:
            xpath_obj(iterable_of(xml2_root))  # pyright: ignore[reportUnknownVariableType]
        with raise_invalid_lxml_type:
            xpath_obj(iterable_of(xml2_tree))  # pyright: ignore[reportUnknownVariableType]


class TestXPathNamespaces:
    def test_namespaces_str_dict(self, svg_root: _Element) -> None:
        ns = {"m": "http://example.org/myapp"}
        xpath_obj = XPath("//m:piechart", namespaces=ns)
        result = xpath_obj(svg_root)
        assert len(result) > 0

    def test_namespaces_bytes_dict(self, svg_root: _Element) -> None:
        ns = {b"m": b"http://example.org/myapp"}
        xpath_obj = XPath(b"//m:piechart", namespaces=ns)
        result = xpath_obj(svg_root)
        assert len(result) > 0


class TestXPathExtensions:
    def test_extensions_dict(self, xml2_root: _Element) -> None:
        def my_ext(context: Any, arg: Any) -> str:
            return "ext_result"

        ext: dict[tuple[str, str], Callable[..., Any]] = {
            ("http://myns", "myfunc"): my_ext,
        }
        ns = {"my": "http://myns"}
        xpath_obj = XPath("my:myfunc('x')", namespaces=ns, extensions=ext)
        result = xpath_obj(xml2_root)
        assert result == "ext_result"


class TestXPathSmartStrings:
    def test_smart_strings_true(self, xml2_root: _Element) -> None:
        xpath_obj = XPath("//orderperson/text()", smart_strings=True)
        result = xpath_obj(xml2_root)
        assert len(result) == 1
        assert isinstance(result[0], _ElementUnicodeResult)

    def test_smart_strings_false(self, xml2_root: _Element) -> None:
        xpath_obj = XPath("//orderperson/text()", smart_strings=False)
        result = xpath_obj(xml2_root)
        assert len(result) == 1
        assert type(result[0]) is str
        assert not isinstance(result[0], _ElementUnicodeResult)


class TestXPathRegexp:
    def test_regexp_flag(self, xml2_root: _Element) -> None:
        # Only perform trivial test of regexp flag since:
        # - it doesn't affect the typing of result
        # - the flag is merely a truthy / falsy value
        xpath_obj = XPath("//item", regexp=True)
        result = xpath_obj(xml2_root)
        assert len(result) == 3

        xpath_obj_nr = XPath("//item", regexp=False)
        result_nr = xpath_obj_nr(xml2_root)
        assert len(result_nr) == 3


# -- ETXPath tests --


class TestETXPathInit:
    # ETXPath has generic __init__ signature

    def test_properties(self) -> None:
        xpath_obj = ETXPath("//item")
        reveal_type(xpath_obj)

        reveal_type(xpath_obj.path)
        assert xpath_obj.path == "//item"

        reveal_type(xpath_obj.error_log)

    def test_path_str(self) -> None:
        xpath_obj = ETXPath("//item")
        assert xpath_obj.path == "//item"

    def test_path_bytes(self) -> None:
        xpath_obj = ETXPath(b"//item")
        assert xpath_obj.path == "//item"

    def test_path_with_default_ns(self, svg_root: _Element) -> None:
        # ETXPath supports {uri}local syntax for default namespace
        xpath_obj = ETXPath("//{http://example.org/myapp}piechart")
        result = xpath_obj(svg_root)
        assert len(result) > 0

    def test_no_positional_arg(self) -> None:
        with pytest.raises(TypeError):
            # pyrefly: ignore[missing-argument]
            ETXPath()  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

    def test_two_positional_args(self) -> None:
        with pytest.raises(TypeError):
            # pyrefly: ignore[bad-argument-count]
            ETXPath("//a", "//b")  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_path_arg_bad(self, thing: Any) -> None:
        # pyrefly: ignore[no-matching-overload]
        with pytest.raises((TypeError, XPathSyntaxError)):
            ETXPath(thing)


class TestETXPathCall:
    def test_call_element(self, xml2_root: _Element) -> None:
        xpath_obj = ETXPath("//item")
        assert len(xpath_obj(xml2_root)) == 3

    def test_call_tree(self, xml2_tree: _ElementTree) -> None:
        xpath_obj = ETXPath("//item")
        assert len(xpath_obj(xml2_tree)) == 3

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_call_arg_bad_1(self, thing: Any) -> None:
        xpath_obj = ETXPath("//item")
        with raise_invalid_lxml_type:
            xpath_obj(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_arg_bad_2(
        self,
        iterable_of: Any,
        xml2_root: _Element,
        xml2_tree: _ElementTree,
    ) -> None:
        xpath_obj = ETXPath("//item")
        with raise_invalid_lxml_type:
            xpath_obj(iterable_of(xml2_root))
        with raise_invalid_lxml_type:
            xpath_obj(iterable_of(xml2_tree))


# -- XPathElementEvaluator tests --


class TestXPathElementEvaluatorInit:
    # XPathElementEvaluator has generic __init__ signature

    def test_properties(self, xml2_root: _Element) -> None:
        evaluator = XPathElementEvaluator(xml2_root)
        reveal_type(evaluator)

        reveal_type(evaluator.error_log)

    def test_no_positional_arg(self) -> None:
        with pytest.raises(TypeError):
            # pyrefly: ignore[missing-argument]
            XPathElementEvaluator()  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

    def test_two_positional_args(self, disposable_element: _Element) -> None:
        with pytest.raises(TypeError):
            # pyrefly: ignore[bad-argument-count]
            XPathElementEvaluator(disposable_element, disposable_element)  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element))
    @pytest.mark.slow
    def test_element_arg_bad_1(self, thing: Any) -> None:
        with pytest.raises(TypeError):
            XPathElementEvaluator(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_element_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with pytest.raises(TypeError):
            XPathElementEvaluator(iterable_of(disposable_element))


class TestXPathElementEvaluatorCall:
    def test_call_ok(self, xml2_root: _Element) -> None:
        evaluator = XPathElementEvaluator(xml2_root)
        for arg in ("//item", b"//item", bytearray(b"//item")):
            assert len(evaluator(arg)) == 3

    def test_call_with_variables(self, xml2_root: _Element) -> None:
        evaluator = XPathElementEvaluator(xml2_root)
        result = evaluator("//item[@id = $myid]", myid="b-001")
        assert len(result) == 1

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_call_path_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        evaluator = XPathElementEvaluator(disposable_element)
        with raise_unexpected_type:
            evaluator(thing)  # pyright: ignore[reportUnknownVariableType]

    def test_call_returns_string(self, xml2_root: _Element) -> None:
        evaluator = XPathElementEvaluator(xml2_root)
        result = evaluator("string(//orderperson)")
        assert result == "John Smith"

    def test_call_returns_float(self, xml2_root: _Element) -> None:
        evaluator = XPathElementEvaluator(xml2_root)
        result = evaluator("count(//item)")
        assert result == 3.0


class TestXPathElementEvaluatorRegisterNamespace:
    @signature_tester(XPathElementEvaluator.register_namespace, (
        ('prefix', Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ('uri'   , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_register_namespace_ok(self, svg_root: _Element) -> None:
        evaluator = XPathElementEvaluator(svg_root)
        evaluator.register_namespace("m", "http://example.org/myapp")
        result = evaluator("//m:piechart")
        assert len(result) > 0

    def test_register_namespace_bytes(self, svg_root: _Element) -> None:
        evaluator = XPathElementEvaluator(svg_root)
        evaluator.register_namespace(b"m", b"http://example.org/myapp")
        result = evaluator(b"//m:piechart")
        assert len(result) > 0

    @signature_tester(XPathElementEvaluator.register_namespaces, (
        ('namespaces', Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_register_namespaces_ok(self, svg_root: _Element) -> None:
        evaluator = XPathElementEvaluator(svg_root)
        evaluator.register_namespaces({"m": "http://example.org/myapp"})
        result = evaluator("//m:piechart")
        assert len(result) > 0

    # TODO Negative tests TBD

# -- XPathDocumentEvaluator tests --


class TestXPathDocumentEvaluatorInit:
    # XPathDocumentEvaluator has generic __init__ signature

    def test_properties(self, xml2_tree: _ElementTree) -> None:
        evaluator = XPathDocumentEvaluator(xml2_tree)
        reveal_type(evaluator)

        reveal_type(evaluator.error_log)

    def test_no_positional_arg(self) -> None:
        with pytest.raises(TypeError):
            # pyrefly: ignore[missing-argument]
            XPathDocumentEvaluator()  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

    def test_two_positional_args(self, xml2_tree: _ElementTree) -> None:
        with pytest.raises(TypeError):
            # pyrefly: ignore[bad-argument-count]
            XPathDocumentEvaluator(xml2_tree, xml2_tree)  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_ElementTree))
    @pytest.mark.slow
    def test_etree_arg_bad_1(self, thing: Any) -> None:
        with raise_unexpected_type:
            XPathDocumentEvaluator(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_etree_arg_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        with raise_unexpected_type:
            XPathDocumentEvaluator(iterable_of(disposable_element.getroottree()))


class TestXPathDocumentEvaluatorCall:
    def test_call_ok(self, xml2_tree: _ElementTree) -> None:
        evaluator = XPathDocumentEvaluator(xml2_tree)
        assert len(evaluator("//item")) == 3

    def test_call_with_variables(self, xml2_tree: _ElementTree) -> None:
        evaluator = XPathDocumentEvaluator(xml2_tree)
        result = evaluator("//item[@id = $myid]", myid="b-001")
        assert len(result) == 1

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_call_path_bad_1(
        self, disposable_element: _Element, thing: Any
    ) -> None:
        evaluator = XPathDocumentEvaluator(disposable_element.getroottree())
        with raise_invalid_utf8_type:
            evaluator(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_call_path_bad_2(
        self, disposable_element: _Element, iterable_of: Any
    ) -> None:
        evaluator = XPathDocumentEvaluator(disposable_element.getroottree())
        with raise_invalid_utf8_type:
            evaluator(iterable_of("//item"))


# -- XPathEvaluator factory function tests --


class TestXPathEvaluatorFactory:
    def test_element_input(self, xml2_root: _Element) -> None:
        evaluator = XPathEvaluator(xml2_root)
        reveal_type(evaluator)
        assert isinstance(evaluator, XPathElementEvaluator)

    def test_tree_input(self, xml2_tree: _ElementTree) -> None:
        evaluator = XPathEvaluator(xml2_tree)
        reveal_type(evaluator)
        assert isinstance(evaluator, XPathDocumentEvaluator)

    def test_element_with_kwargs(self, svg_root: _Element) -> None:
        ns = {"m": "http://example.org/myapp"}
        evaluator = XPathEvaluator(
            svg_root,
            namespaces=ns,
            regexp=True,
            smart_strings=True,
        )
        result = evaluator("//m:piechart")
        assert len(result) > 0

    def test_tree_with_kwargs(self, svg_tree: _ElementTree) -> None:
        ns = {"m": "http://example.org/myapp"}
        evaluator = XPathEvaluator(
            svg_tree,
            namespaces=ns,
            regexp=True,
            smart_strings=True,
        )
        result = evaluator("//m:piechart")
        assert len(result) > 0

    def test_with_extensions(self, xml2_root: _Element) -> None:
        def my_ext(context: Any, arg: Any) -> str:
            return "value"

        ext: dict[tuple[str, str], Callable[..., Any]] = {
            ("http://myns", "func"): my_ext
        }
        ns = {"ns": "http://myns"}
        evaluator = XPathEvaluator(xml2_root, namespaces=ns, extensions=ext)
        result = evaluator("ns:func('x')")
        assert result == "value"

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_input_arg_bad_1(self, thing: Any) -> None:
        with raise_unexpected_type:
            XPathEvaluator(thing)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        max_examples=5,
    )
    @given(iterable_of=_st.fixed_item_iterables())
    def test_input_arg_bad_2(
        self,
        iterable_of: Any,
        xml2_root: _Element,
        xml2_tree: _ElementTree,
    ) -> None:
        with raise_unexpected_type:
            XPathEvaluator(iterable_of(xml2_root))
        with raise_unexpected_type:
            XPathEvaluator(iterable_of(xml2_tree))
