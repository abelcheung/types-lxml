import functools
from inspect import _ParameterKind, signature
from typing import Any, Callable, ParamSpec, Sequence

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
