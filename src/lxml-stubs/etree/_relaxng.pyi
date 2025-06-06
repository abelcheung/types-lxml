from typing import overload

from .._types import _ElementOrTree, _FileReadSource
from ._module_misc import LxmlError, _Validator

class RelaxNGError(LxmlError): ...
class RelaxNGParseError(RelaxNGError): ...
class RelaxNGValidateError(RelaxNGError): ...

class RelaxNG(_Validator):
    @overload
    def __init__(self, etree: _ElementOrTree) -> None: ...
    @overload
    def __init__(
        self,
        etree: None = None,
        *,
        file: _FileReadSource,
    ) -> None: ...
    def __call__(self, etree: _ElementOrTree) -> bool: ...
    @classmethod
    def from_rnc_string(
        cls, src: str, base_url: str | bytes | None = None
    ) -> RelaxNG: ...
