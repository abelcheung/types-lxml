import sys
from typing import Any, ClassVar, overload

if sys.version_info >= (3, 11):
    from typing import LiteralString
else:
    from typing_extensions import LiteralString

from . import etree as _e
from ._types import _ElementOrTree, _FileReadSource
from .etree._xslt import _Stylesheet_Param

__all__ = (
    # Official exports
    "extract_xsd",
    "extract_rng",
    "iso_dsdl_include",
    "iso_abstract_expand",
    "iso_svrl_for_xslt1",
    "svrl_validation_errors",
    "schematron_schema_valid",
    "stylesheet_params",
    "Schematron",
    # Namespace constants
    "XML_SCHEMA_NS",
    "RELAXNG_NS",
    "SCHEMATRON_NS",
    "SVRL_NS",
)

XML_SCHEMA_NS: LiteralString
RELAXNG_NS: LiteralString
SCHEMATRON_NS: LiteralString
SVRL_NS: LiteralString

extract_xsd: _e.XSLT
extract_rng: _e.XSLT
iso_dsdl_include: _e.XSLT
iso_abstract_expand: _e.XSLT
iso_svrl_for_xslt1: _e.XSLT
svrl_validation_errors: _e.XPath
schematron_schema_valid: _e.RelaxNG

def stylesheet_params(**__kw: str | _e.XPath | Any) -> dict[str, _Stylesheet_Param]: ...

class Schematron(_e._Validator):
    _domain: ClassVar[_e.ErrorDomains]
    _level: ClassVar[_e.ErrorLevels]
    _error_type: ClassVar[_e.ErrorTypes]
    ASSERTS_ONLY: ClassVar[_e.XPath]
    ASSERTS_AND_REPORTS: ClassVar[_e.XPath]
    _extract_xsd: ClassVar[_e.XSLT]
    _extract_rng: ClassVar[_e.XSLT]
    _include: ClassVar[_e.XSLT]
    _expand: ClassVar[_e.XSLT]
    _compile: ClassVar[_e.XSLT]
    _validation_errors: ClassVar[_e.XPath]
    # _extract() can be a mean of customisation like some of the vars above
    def _extract(self, element: _e._Element) -> _e._ElementTree[_e._Element] | None: ...

    # The overload arg matrix is daunting (3 * 2**3) without much benefit:
    # - etree / file
    # - include / include_params
    # - expand / expand_params
    # - compile_params / phase
    # Following other validators, just distinguish etree and file arg.
    @overload
    def __init__(
        self,
        etree: _ElementOrTree,
        file: None = ...,
        include: bool = ...,
        expand: bool = ...,
        include_params: dict[str, _Stylesheet_Param] = ...,
        expand_params: dict[str, _Stylesheet_Param] = ...,
        compile_params: dict[str, _Stylesheet_Param] = ...,
        store_schematron: bool = ...,
        store_xslt: bool = ...,
        store_report: bool = ...,
        phase: str | None = ...,
        error_finder: _e.XPath = ...,
        validate_schema: bool = ...,
    ) -> None: ...
    @overload
    def __init__(
        self,
        etree: None,
        file: _FileReadSource,
        include: bool = ...,
        expand: bool = ...,
        include_params: dict[str, _Stylesheet_Param] = ...,
        expand_params: dict[str, _Stylesheet_Param] = ...,
        compile_params: dict[str, _Stylesheet_Param] = ...,
        store_schematron: bool = ...,
        store_xslt: bool = ...,
        store_report: bool = ...,
        phase: str | None = ...,
        error_finder: _e.XPath = ...,
        validate_schema: bool = ...,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        file: _FileReadSource,
        include: bool = ...,
        expand: bool = ...,
        include_params: dict[str, _Stylesheet_Param] = ...,
        expand_params: dict[str, _Stylesheet_Param] = ...,
        compile_params: dict[str, _Stylesheet_Param] = ...,
        store_schematron: bool = ...,
        store_xslt: bool = ...,
        store_report: bool = ...,
        phase: str | None = ...,
        error_finder: _e.XPath = ...,
        validate_schema: bool = ...,
    ) -> None: ...
    def __call__(self, etree: _ElementOrTree) -> bool: ...
    @property
    def schematron(self) -> _e._XSLTResultTree | None: ...
    @property
    def validator_xslt(self) -> _e._XSLTResultTree | None: ...
    @property
    def validation_report(self) -> _e._XSLTResultTree | None: ...
