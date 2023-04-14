import ast
import inspect
import logging
import typing as _t
from pathlib import Path

from typeguard import TypeCheckError, TypeCheckMemo, check_type_internal

from .common import FilePos
from .pyright_adapter import NameCollector, get_pyright_result

_T = _t.TypeVar("_T")

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARN)


class RevealTypeExtractor(ast.NodeVisitor):
    target = None

    def visit_Call(self, node: ast.Call) -> _t.Any:
        func_name = node.func
        if isinstance(func_name, ast.Name) and func_name.id == "reveal_type":
            self.target = node.args[0]
        return self.generic_visit(node)


def _get_var_name(frame: inspect.FrameInfo) -> str:
    code, idx = frame.code_context, frame.index
    assert code is not None and idx is not None
    code = code[idx].strip()

    walker = RevealTypeExtractor()
    walker.visit(ast.parse(code))
    try:
        return ast.get_source_segment(code, walker.target)  # type: ignore
    except:
        raise TypeCheckError("Failed to get variable name " f'from expression "{code}"')


def reveal_type_wrapper(var: _T) -> _T:
    """Wrapper for `reveal_type()` that matches static type checker
    result with typeguard runtime result

    This function is intended to be called as `reveal_type()`,
    replacing official `reveal_type()` from either Python 3.11
    or `typing_extensions` module.

    Such maneuver is designed to circumvent `pyright`'s ability
    to resolve `reveal_type()`'s origin. Otherwise, if pyright
    determines `reveal_type()` does not come from `typing` or
    `typing_extensions` module, it would not print any
    inferred variable types.

    Usage
    -----
    This function needs special usage in order to fool `pyright`.
    Use it like this:

    ```python
        import your_test_mod
        reveal_type = getattr(your_test_mod, 'reveal_type_wrapper')
    ```

    `Mypy` is much more dumb and happily print output upon
    encountering `reveal_type` without checking its origin,
    thus workaround is not needed, but using this wrapper
    doesn't hurt.

    Its basic behavior is identical to official `reveal_type()` --
    it returns input argument unchanged.

    Raises
    ------
    TypeCheckError
        If static type checker failed to get inferred type
        for variable, or the type doesn't match runtime result
    """
    caller = inspect.stack()[1]
    pos = FilePos(Path(caller.filename).name, caller.lineno)
    pyr_result = get_pyright_result(caller.filename)
    if pos not in pyr_result:
        raise TypeCheckError(
            "Pyright does not provide inferred type on "
            f'"{pos.file}" line {pos.lineno}'
        )
    result = pyr_result[pos]

    var_name = _get_var_name(caller)
    if result.var != var_name:
        raise TypeCheckError(
            "Pyright result should contain " f'"{var_name}", but got "{result.var}"'
        )

    ref = _t.ForwardRef(result.type)
    # Since this is a wrapper of typeguard.check_type(),
    # get globals and locals from my caller, not mine
    globals = caller.frame.f_globals
    locals = caller.frame.f_locals
    try:
        memo = TypeCheckMemo(globals, locals)
        check_type_internal(var, ref, memo)
    except NameError:
        # Collect resolved bare names and try again
        walker = NameCollector()
        walker.visit(ast.parse(result.type))
        locals |= walker.names
        memo = TypeCheckMemo(globals, locals)
        check_type_internal(var, ref, memo)

    del caller
    return var
