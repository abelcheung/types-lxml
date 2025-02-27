from __future__ import annotations

import copy
import io
import sys
from collections.abc import Callable, Iterator
from inspect import Parameter
from pathlib import Path
from types import NoneType
from typing import Any

import pytest
from hypothesis import HealthCheck, given, settings
from lxml.etree import (
    DocumentInvalid,
    XMLSchema,
    XMLSchemaParseError,
    _Element,
    _ElementTree,
)

from ._testutils import signature_tester, strategy as _st

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestXMLSchemaInput:
    # Generic Cython signature
    def test_none(self) -> None:
        with pytest.raises(XMLSchemaParseError, match="No tree or file given"):
            _ = XMLSchema()  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue]

        with pytest.raises(XMLSchemaParseError, match="No tree or file given"):
            _ = XMLSchema(None)  # type: ignore[call-overload]  # pyright: ignore[reportArgumentType]

        with pytest.raises(TypeError, match="at most 1 positional argument"):
            _ = XMLSchema(None, None)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue]

        with pytest.raises(XMLSchemaParseError, match="No tree or file given"):
            _ = XMLSchema(None, file=None)  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]

        with pytest.raises(XMLSchemaParseError, match="No tree or file given"):
            _ = XMLSchema(file=None)  # type: ignore[call-overload]  # pyright: ignore[reportArgumentType]

    @given(etree=_st.all_instances_except_of_type(NoneType))
    def test_etree_bad(self, etree: Any) -> None:
        with pytest.raises((XMLSchemaParseError, ValueError, TypeError)):
            _ = XMLSchema(etree)

    def test_etree_ok(self, xmlschema_root: _Element) -> None:
        schema = XMLSchema(xmlschema_root)
        reveal_type(schema)
        del schema

        schema = XMLSchema(etree=xmlschema_root.getroottree())
        reveal_type(schema)

    def test_file_ok(
        self,
        generate_input_file_arguments: Callable[..., Iterator[Any]],
        xmlschema_path: Path,
    ) -> None:
        for file in generate_input_file_arguments(
            xmlschema_path, exclude_type=(io.StringIO,)
        ):
            schema = XMLSchema(file=file)
            reveal_type(schema)
            del schema

    # TODO How to annotate this situation where TextIOWrapper works but
    # not for StringIO?
    def test_file_bad(self, xmlschema_path: Path) -> None:
        sio = io.StringIO(xmlschema_path.read_text())
        # Unicode strings with encoding declaration are not supported.
        with pytest.raises(ValueError, match="encoding declaration are not supported"):
            _ = XMLSchema(file=sio)

    # TODO test attribute_defaults argument


class TestXMLSchemaValidate:
    @signature_tester(
        XMLSchema.validate,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_call_arg_ok(
        self,
        xmlschema: XMLSchema,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        result = xmlschema.validate(xml2_root)
        reveal_type(result)

        result = xmlschema.validate(xml2_tree)
        reveal_type(result)

        result = xmlschema(xml2_root)
        reveal_type(result)

        result = xmlschema(xml2_tree)
        reveal_type(result)

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        result = xmlschema(faulty_root)
        reveal_type(result)

    @settings(suppress_health_check=[HealthCheck.too_slow])
    @given(etree=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_call_arg_bad(self, xmlschema: XMLSchema, etree: Any) -> None:
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.validate(etree)

        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema(etree)

    @signature_tester(
        XMLSchema.assert_,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    @signature_tester(
        XMLSchema.assertValid,
        (("etree", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_assert_arg_ok(
        self,
        xmlschema: XMLSchema,
        xml2_root: _Element,
        xml2_tree: _ElementTree[_Element],
    ) -> None:
        assert xmlschema.assertValid(xml2_root) is None
        assert xmlschema.assertValid(xml2_tree) is None
        assert xmlschema.assert_(xml2_root) is None
        assert xmlschema.assert_(xml2_tree) is None

        faulty_root = copy.deepcopy(xml2_root)
        faulty_root[0].tag = "faulty"
        with pytest.raises(DocumentInvalid):
            xmlschema.assertValid(faulty_root)

        with pytest.raises(AssertionError):
            xmlschema.assert_(faulty_root)

    @settings(suppress_health_check=[HealthCheck.too_slow])
    @given(etree=_st.all_instances_except_of_type(_Element, _ElementTree))
    @pytest.mark.slow
    def test_assert_arg_bad(self, xmlschema: XMLSchema, etree: Any) -> None:
        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.assertValid(etree)

        with pytest.raises(TypeError, match=r"Invalid input object"):
            _ = xmlschema.assert_(etree)
