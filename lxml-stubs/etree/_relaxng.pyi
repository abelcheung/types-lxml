from gzip import GzipFile
from io import FileIO
from typing import IO, overload

from .._types import SupportsGeturl, _AnyStr, _FileReadSource
from . import LxmlError, _ElementOrAnyTree, _ElementOrXMLTree, _Validator

class RelaxNGError(LxmlError): ...
class RelaxNGParseError(RelaxNGError): ...
class RelaxNGValidateError(RelaxNGError): ...

class RelaxNG(_Validator):
    @overload
    def __init__(self, etree: _ElementOrXMLTree) -> None: ...
    @overload
    def __init__(
        self,
        etree: None = ...,
        *,
        file: _ElementOrXMLTree | _FileReadSource | SupportsGeturl | FileIO | GzipFile
    ) -> None: ...
    def __call__(self, etree: _ElementOrAnyTree) -> bool: ...
    # No pathlike support
    @classmethod
    def from_rnc_string(
        cls, src: _AnyStr | IO[str] | IO[bytes], base_url: str | None = ...
    ) -> RelaxNG: ...
