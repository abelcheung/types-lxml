import ast
import inspect
import logging
import typing as _t
from pathlib import Path

from typeguard import TypeCheckMemo, check_type_internal

from . import pyright_adapter as adapter
from .common import FilePos, TypeCheckerError

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


def _get_var_name(frame: inspect.FrameInfo) -> str | None:
    ctxt, idx = frame.code_context, frame.index
    assert ctxt is not None and idx is not None
    code = ctxt[idx].strip()

    walker = RevealTypeExtractor()
    walker.visit(ast.parse(code, mode="eval"))
    assert walker.target is not None
    return ast.get_source_segment(code, walker.target)


def reveal_type_wrapper(var: _T) -> _T:
    """Replacement of `reveal_type()` that matches static
    type checker result with typeguard runtime result

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
    TypeCheckerError
        If static type checker failed to get inferred type
        for variable
    typeguard.TypeCheckError
        If type checker result doesn't match runtime result
    """
    caller = inspect.stack()[1]
    pos = FilePos(Path(caller.filename).name, caller.lineno)
    typechecker_result = adapter.get_result(caller.filename)
    try:
        result = typechecker_result[pos]
    except KeyError as e:
        raise TypeCheckerError('No inferred type', pos.file, pos.lineno) from e

    if result.var:  # mypy output doesn't have this extra protection
        var_name = _get_var_name(caller)
        if result.var != var_name:
            raise TypeCheckerError(
                f'Variable name should be "{result.var}", but got "{var_name}"',
                pos.file, pos.lineno
            )

    # Since this is a wrapper of typeguard.check_type(),
    # get globals and locals from my caller, not mine
    globalns = caller.frame.f_globals
    localns = caller.frame.f_locals

    ref_arg = result.type.__forward_arg__
    type_ast = ast.parse(ref_arg, mode="eval")
    walker = adapter.NameCollector(globalns, localns)
    walker.visit(type_ast)
    memo = TypeCheckMemo(globalns, localns | walker.collected)
    try:
        check_type_internal(var, result.type, memo)
    except TypeError as e:
        if "is not subscriptable" not in e.args[0]:
            raise
        if not isinstance(type_ast.body, ast.Subscript):
            raise TypeCheckerError(
                f'{ref_arg} should be parsed as Subscript, '
                f'but got {type(type_ast.body).__name__}',
                pos.file,
                pos.lineno
            ) from e
        # Have to concede by verifying unsubscripted type
        # Specialized classes is a stub-only thing here, and
        # all classes in lxml do not support __class_getitem__
        bare_type = ast.get_source_segment(ref_arg, type_ast.body.value)
        assert bare_type is not None
        check_type_internal(var, _t.ForwardRef(bare_type), memo)

    del caller
    return var
