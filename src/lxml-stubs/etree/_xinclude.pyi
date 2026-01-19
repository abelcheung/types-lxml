from typing_extensions import disjoint_base

from ._element import _Element
from ._module_misc import LxmlError
from ._xmlerror import _ListErrorLog

class XIncludeError(LxmlError): ...

@disjoint_base
class XInclude:
    """XInclude processor for applying XInclude directives to a tree.

    See Also
    --------
    - [API Documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XInclude)
    """
    def __init__(self) -> None: ...
    @property
    def error_log(self) -> _ListErrorLog: ...
    def __call__(self, node: _Element) -> None: ...
