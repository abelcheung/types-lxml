import functools
from inspect import Signature, _ParameterKind, signature
from typing import Any, Callable, ParamSpec, Sequence

import pytest

_P = ParamSpec("_P")


def signature_tester(
    func_to_check: Callable[..., Any],
    param_data: Sequence[tuple[str, _ParameterKind, Any] | None],
) -> Callable[[Callable[_P, None]], Callable[_P, None]]:
    def decorator(f: Callable[_P, None]) -> Callable[_P, None]:
        @functools.wraps(f)
        def wrapped(*args: _P.args, **kw: _P.kwargs) -> None:
            sig = signature(func_to_check)
            param = list(sig.parameters.values())
            assert len(param) == len(param_data)
            for i in range(len(param_data)):
                if param_data[i] is None:
                    continue
                # fmt: off
                assert (
                    param[i].name,
                    param[i].kind,
                    param[i].default
                ) == param_data[i]
                # fmt: on
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
                    pytest.fail(f"Signature of {func.__qualname__} is non-empty")
            f(*args, **kw)

        return wrapped

    return decorator
