import functools
from inspect import Parameter, Signature, _ParameterKind, signature, isclass
from typing import Any, Callable, ParamSpec, Sequence

import pytest
from .common import is_lxml_4x

_P = ParamSpec("_P")


# Very crude and probably won't work on many corner cases,
# but enough for here so far
def is_cython_class_method(func: Callable[..., Any]) -> bool:
    glob = getattr(func, 'func_globals', None)
    if not glob:
        return False
    parent = func.__qualname__.rsplit('.', 1)[0]
    return isclass(glob[parent])


def signature_tester(
    func_to_check: Callable[..., Any],
    param_data: Sequence[tuple[str, _ParameterKind, Any] | None],
) -> Callable[[Callable[_P, None]], Callable[_P, None]]:
    def decorator(f: Callable[_P, None]) -> Callable[_P, None]:
        @functools.wraps(f)
        def wrapped(*args: _P.args, **kw: _P.kwargs) -> None:
            sig = signature(func_to_check)
            param = list(sig.parameters.values())

            if param[0].name == 'self':
                _ = param.pop(0)

            assert len(param) == len(param_data)

            # For lxml < 5, args in class methods never contain
            # default values (.__defaults__ property is empty).
            # This is probably due to older cython
            # compiler which doesn't support that yet
            no_default = False
            if is_lxml_4x and is_cython_class_method(func_to_check):
                no_default = True

            for i in range(len(param_data)):
                if (p := param_data[i]) is None:
                    continue
                assert param[i].name == p[0]
                assert param[i].kind == p[1]
                if no_default:
                    assert param[i].default == Parameter.empty
                else:
                    assert param[i].default == p[2]
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
