import ast
import inspect
import logging
import pathlib
import typing as _t

from typeguard import TypeCheckError, TypeCheckMemo, check_type_internal

from . import mypy_adapter, pyright_adapter
from .common import FilePos, TypeCheckerError, VarType

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
    and runtime result

    This function is intended as a drop-in replacement of
    `reveal_type()`, replacing official one from Python 3.11
    or `typing_extensions` module. Under the hook, it uses
    `typeguard` to get runtime variable type, and compare it
    with static type checker results for coherence.

    Usage
    -----
    This function needs special boiler plate to fool command
    line type checkers. Add following fragment to any python
    source using `reveal_type()` function:

    ```python
        INJECT_REVEAL_TYPE = True
        if INJECT_REVEAL_TYPE:
            reveal_type = getattr(_testutils, "reveal_type_wrapper")
    ```

    Mypy needs extra configuration; add
    `INJECT_REVEAL_TYPE` to `always_false` setting.
    No configuration needed for pyright.
    Such maneuver is designed to circumvent type checkers'
    ability to resolve `reveal_type()`'s origin. Otherwise,
    when type checkers managed to detect `reveal_type()` is
    somehow overridden, they refuse to print any output.

    Its calling behavior is identical to official
    `reveal_type()`: returns input argument unchanged.

    Raises
    ------
    `TypeCheckerError`
        If static type checker failed to get inferred type
        for variable
    `typeguard.TypeCheckError`
        If type checker result doesn't match runtime result
    """
    caller = inspect.stack()[1]
    var_name = _get_var_name(caller)
    pos = FilePos(pathlib.Path(caller.filename).name, caller.lineno)

    # Since this routine is a wrapper of typeguard.check_type(),
    # get globals and locals from my caller, not mine
    globalns = caller.frame.f_globals
    localns = caller.frame.f_locals

    for adapter in (pyright_adapter.adapter, mypy_adapter.adapter):
        try:
            tc_result = adapter.typechecker_result[pos]
        except KeyError as e:
            raise TypeCheckerError(
                f"No inferred type from {adapter.id}", pos.file, pos.lineno
            ) from e

        if tc_result.var:  # Only pyright has this extra protection
            if tc_result.var != var_name:
                raise TypeCheckerError(
                    f'Variable name should be "{tc_result.var}", but got "{var_name}"',
                    pos.file,
                    pos.lineno,
                )
        else:
            adapter.typechecker_result[pos] = VarType(var_name, tc_result.type)

        ref = tc_result.type
        try:
            _ = eval(ref.__forward_arg__, globalns, localns)
        except:
            ref_ast = ast.parse(ref.__forward_arg__, mode="eval")
            walker = adapter.create_collector(globalns, localns)
            new_ast = walker.visit(ref_ast)
            if walker.modified:
                ref = _t.ForwardRef(ast.unparse(new_ast))
            memo = TypeCheckMemo(globalns, localns | walker.collected)
        else:
            memo = TypeCheckMemo(globalns, localns)

        try:
            check_type_internal(var, ref, memo)
        except TypeCheckError as e:
            e.args = (f"({adapter.id}) " + e.args[0],) + e.args[1:]
            raise

    return var
