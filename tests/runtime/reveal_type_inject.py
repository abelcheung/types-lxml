from __future__ import annotations

import pytest

from ._testutils import mypy_adapter, pyright_adapter
from ._testutils.rt_wrapper import reveal_type_wrapper


def pytest_pyfunc_call(pyfuncitem: pytest.Function) -> None:
    assert pyfuncitem.module is not None
    try:
        pyfuncitem.module.reveal_type = reveal_type_wrapper
    except AttributeError:
        pass
    # TODO If only typing is imported, monkeypatch it


def pytest_collection_finish(session: pytest.Session) -> None:
    files = {i.path for i in session.items}
    for adapter in (pyright_adapter.adapter, mypy_adapter.adapter):
        adapter.run_typechecker_on(files)
