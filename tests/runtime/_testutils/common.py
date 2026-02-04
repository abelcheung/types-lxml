from __future__ import annotations

import sys
from collections.abc import Iterable
from dataclasses import dataclass
from types import NoneType
from typing import (
    Any,
    cast,
    get_args,
    get_type_hints,
)

from lxml.etree import LXML_VERSION, QName

from . import strategy as _st

if sys.version_info >= (3, 12):
    from collections.abc import Buffer
else:
    from typing_extensions import Buffer

# Intended for multi subclass patch
is_multi_subclass_build = False


class FuncSignatureError(Exception):
    def __init__(self, message: str, funcname: str) -> None:
        super().__init__(message)
        self._func = funcname

    def __str__(self) -> str:
        return "{}(): {}".format(self._func, self.args[0])


def hashable_elem_if_is_set(iterable_of: object, elem: object) -> bool:
    if getattr(iterable_of, "type") not in {set, frozenset}:
        return True
    try:
        hash(elem)
    except Exception:
        return False
    return True

# In PyPy, some objects can practically perform iter operation
# without __iter__() by using __getitem__(), so isinstance is
# usesless there
def can_practically_iter(thing: object) -> bool:
    try:
        _ = [n for n in cast(Any, thing)]
    except Exception:
        return False
    else:
        return True


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

tag_name_types = attr_name_types

text_document_types = ArgumentTypes(
    (str, Buffer) if LXML_VERSION >= (6, 0) else (str, bytes),
    (),
)

tag_selector_types = ArgumentTypes(
    (str, bytes, QName, NoneType),
    (Iterable,),
)
