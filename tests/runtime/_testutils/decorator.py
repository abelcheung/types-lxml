from __future__ import annotations

import functools
from collections.abc import Callable, Sequence
from inspect import Parameter, Signature, _ParameterKind, isclass, signature
from typing import Any, ParamSpec

from lxml.etree import LXML_VERSION

from .common import FuncSignatureError

_P = ParamSpec("_P")


# Very crude and probably won't work on many corner cases,
# but enough for here so far
def is_cython_class_method(func: Callable[..., Any]) -> bool:
    glob = getattr(func, "func_globals", None)
    if not glob:
        return False
    parent = func.__qualname__.rsplit(".", 1)[0]
    return isclass(glob[parent])


def signature_tester(
    func_to_check: Callable[..., Any],
    expect_param: Sequence[tuple[str, _ParameterKind, Any] | None],
) -> Callable[[Callable[_P, None]], Callable[_P, None]]:
    def decorator(f: Callable[_P, None]) -> Callable[_P, None]:
        @functools.wraps(f)
        def wrapped(*args: _P.args, **kw: _P.kwargs) -> None:
            sig = signature(func_to_check)
            param = list(sig.parameters.values())
            funcname = func_to_check.__qualname__

            has_self = False
            if param[0].name == "self":
                has_self = True
                _ = param.pop(0)

            if len(param) != len(expect_param):
                raise FuncSignatureError(
                    "Parameter count{}don't match, expected {} but got {}".format(
                        " (excluding Self) " if has_self else " ",
                        len(expect_param),
                        len(param),
                    ),
                    funcname,
                )

            # For lxml < 5, args in class methods never contain
            # default values (.__defaults__ property is empty).
            # This is probably due to older cython
            # compiler which doesn't support that yet
            no_default = False
            if LXML_VERSION < (5, 0) and is_cython_class_method(func_to_check):
                no_default = True

            for i in range(len(expect_param)):
                if (p := expect_param[i]) is None:
                    continue
                if param[i].name != p[0]:
                    raise FuncSignatureError(
                        "Name of parameter {} don't match, "
                        "expected {} but got {}".format(i + 1, p[0], param[i].name),
                        funcname,
                    )
                if param[i].kind != p[1]:
                    raise FuncSignatureError(
                        "Type of '{}' parameter don't match, "
                        "expected {} but got {}".format(
                            p[0], p[1].name, param[i].kind.name
                        ),
                        funcname,
                    )
                def_val = Parameter.empty if no_default else p[2]
                if param[i].default != def_val:
                    raise FuncSignatureError(
                        "Default value of '{}' parameter don't match, "
                        "expected {} but got {}".format(
                            p[0],
                            "no default" if def_val is Parameter.empty else def_val,
                            "no default"
                            if param[i].default is Parameter.empty
                            else param[i].default,
                        ),
                        funcname,
                    )
            f(*args, **kw)

        return wrapped

    return decorator


def empty_signature_tester(
    *_funcs: Callable[..., Any],
) -> Callable[[Callable[_P, None]], Callable[_P, None]]:
    def decorator(f: Callable[_P, None]) -> Callable[_P, None]:
        @functools.wraps(f)
        def wrapped(*args: _P.args, **kw: _P.kwargs) -> None:
            for func in _funcs:
                sig = signature(func)
                if sig == Signature():
                    continue
                param = list(sig.parameters.values())
                if param[0].name == "self":
                    _ = param.pop(0)
                if param:
                    raise FuncSignatureError(
                        "Signature expected to be empty but actually is not",
                        func.__qualname__,
                    )
            f(*args, **kw)

        return wrapped

    return decorator
