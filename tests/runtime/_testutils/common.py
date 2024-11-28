from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    get_args,
    get_type_hints,
)

from . import strategy as _st


class FuncSignatureError(Exception):
    def __init__(self, message: str, funcname: str) -> None:
        super().__init__(message)
        self._func = funcname

    def __str__(self) -> str:
        return "{}(): {}".format(self._func, self.args[0])


@dataclass
class ArgumentTypes:
    allow: tuple[type[Any], ...]
    skip: tuple[type[Any], ...]


attr_name_types = ArgumentTypes(
    get_args(get_args(get_type_hints(_st.xml_name_arg)["return"])[0]),
    (),
)

attr_value_types = ArgumentTypes(
    get_args(get_args(get_type_hints(_st.xml_attr_value_arg)["return"])[0]),
    (),
)
