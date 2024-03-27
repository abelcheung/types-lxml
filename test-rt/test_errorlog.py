from __future__ import annotations

import inspect
from typing import Any, cast

import _testutils
import pytest
from lxml.etree import (
    LXML_VERSION,
    ErrorDomains,
    ErrorLevels,
    ErrorTypes as ErrorTypes,
    XMLSyntaxError,
    _ListErrorLog,
    _LogEntry as _LogEntry,
    fromstring,
)

reveal_type = getattr(_testutils, "reveal_type_wrapper")


def _method_no_kwarg() -> bool:
    # Param for some methods (filter_levels, receive)
    # is strictly positional in lxml 4.9.
    # Source code doesn't reveal anything abnormal,
    # is it some sort of problem with cython?
    return LXML_VERSION < (5, 0)


class TestListLog:
    def test_from_broken_string(self) -> None:
        src = "<bad><a><b></a>&qwerty;</bad>"
        try:
            _ = fromstring(src)
        except XMLSyntaxError as e:
            log = e.error_log
            reveal_type(log)
        else:
            pytest.fail(reason="Bad XML data should have failed parsing")

    def test_entry_properties(self, list_log: _ListErrorLog) -> None:
        e0 = list_log[0]
        reveal_type(e0)
        reveal_type(e0.domain_name)
        reveal_type(e0.type_name)
        reveal_type(e0.level_name)
        reveal_type(e0.line)
        reveal_type(e0.column)
        reveal_type(e0.message)
        reveal_type(e0.filename)
        reveal_type(e0.path)
        reveal_type(list_log.last_error)

        # types-lxml is lying below for following properties:
        # they are only present as int in runtime, but we want to
        # encourage symbolic comparisons, not whether they are int
        assert e0.domain == ErrorDomains.PARSER
        assert e0.level == ErrorLevels.FATAL
        # assert e0.type == ErrorTypes.ERR_TAG_NAME_MISMATCH

    def test_container_behavior(self, list_log: _ListErrorLog) -> None:
        e0 = list_log[0]
        reveal_type(len(list_log))
        reveal_type(e0)
        reveal_type(e0 in list_log)
        for e in list_log:
            reveal_type(e)

    def test_filter_domains(self, list_log: _ListErrorLog) -> None:
        sig = inspect.signature(list_log.filter_domains)
        param = list(sig.parameters.values())
        assert len(param) == 1
        assert param[0].name == "domains"
        assert param[0].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        del sig, param

        filtered = list_log.filter_domains([ErrorDomains.PARSER, ErrorDomains.DTD])
        reveal_type(filtered)
        del filtered

        filtered = list_log.filter_domains(ErrorDomains.PARSER)
        reveal_type(filtered)
        del filtered

        with pytest.raises(TypeError, match=r"argument .+ is not iterable"):
            _ = list_log.filter_domains(cast(Any, None))

    def test_filter_levels(self, list_log: _ListErrorLog) -> None:
        sig = inspect.signature(list_log.filter_levels)
        param = list(sig.parameters.values())
        assert len(param) == 1
        assert param[0].name == "levels"
        assert param[0].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        del sig, param

        new_log = list_log.filter_levels(ErrorLevels.ERROR)
        reveal_type(new_log)
        del new_log

        if _method_no_kwarg():
            new_log = list_log.filter_levels([ErrorLevels.ERROR, ErrorLevels.FATAL])
        else:
            new_log = list_log.filter_levels(
                levels=[ErrorLevels.ERROR, ErrorLevels.FATAL]
            )
        reveal_type(new_log)
        del new_log

        with pytest.raises(TypeError, match=r"argument .+ is not iterable"):
            _ = list_log.filter_levels(cast(Any, None))

    def test_filter_levels_shortcut(self, list_log: _ListErrorLog) -> None:
        sig = inspect.signature(list_log.filter_from_level)
        param = list(sig.parameters.values())
        assert len(param) == 1
        assert param[0].name == "level"
        assert param[0].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        del sig, param

        if _method_no_kwarg():
            new_log = list_log.filter_from_level(ErrorLevels.NONE)
        else:
            new_log = list_log.filter_from_level(level=ErrorLevels.NONE)
        reveal_type(new_log)
        del new_log

        assert inspect.signature(list_log.filter_from_errors) == inspect.Signature()
        reveal_type(list_log.filter_from_errors())

        assert inspect.signature(list_log.filter_from_fatals) == inspect.Signature()
        reveal_type(list_log.filter_from_fatals())

        assert inspect.signature(list_log.filter_from_warnings) == inspect.Signature()
        reveal_type(list_log.filter_from_warnings())

    # def test_filter_types(self, list_log: _ListErrorLog) -> None:
    # new_log = list_log.filter_types(ErrorTypes.???)

    def test_other_methods(self, list_log: _ListErrorLog) -> None:
        sig = inspect.signature(list_log.receive)
        param = list(sig.parameters.values())
        assert len(param) == 1
        assert param[0].name == "entry"
        assert param[0].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        del sig, param

        if _method_no_kwarg():
            ret = list_log.receive(list_log[0])
        else:
            ret = list_log.receive(entry=list_log[0])
        reveal_type(ret)
        del ret
        with pytest.raises(TypeError, match=r"expected .+\._LogEntry, got int"):
            list_log.receive(cast(Any, 1))

        # BEWARE: vanilla _ListErrorLog has no clear() method,
        # thus can't be inspected
        assert inspect.signature(list_log.copy) == inspect.Signature()
        err_copy = list_log.copy()
        reveal_type(err_copy)


class TestEmptyLog:
    # validate some methods and props works for empty log too
    def test_create_empty_log(self) -> None:
        data = "<doc><a>1</a></doc>"
        elem = fromstring(data)
        p = elem.getroottree().parser
        assert p is not None
        e = p.error_log
        reveal_type(len(e))
        reveal_type(e.last_error)
        with pytest.raises(IndexError, match="out of range"):
            _ = e[0]
        e_copy = e.copy()
        reveal_type(e_copy)


# TODO PyErrorLog, _RotatingErrorLog
# The unused _DomainErrorLog is ignored

# Not testing manual construction of _ErrorLog; technically
# feasible, but it does not make sense creating a collection
# of error entries out of context
