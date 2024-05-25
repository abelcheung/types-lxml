from __future__ import annotations

import logging
from inspect import Parameter
from typing import Any, cast

import _testutils
import pytest
from lxml.etree import (
    LXML_VERSION,
    ErrorDomains,
    ErrorLevels,
    ErrorTypes as ErrorTypes,
    PyErrorLog,
    XMLSyntaxError,
    _ListErrorLog,
    _LogEntry as _LogEntry,
    clear_error_log,
    fromstring,
    use_global_python_log,
)

reveal_type = getattr(_testutils, "reveal_type_wrapper")


### NOTES
#
# - Not testing manual construction of _ErrorLog; technically
# feasible, but it does not make sense creating a collection
# of error entries out of context
#
# - Not testing _DomainErrorLog as it is completely unused
#
# - Not testing _RotatingErrorLog, which is only used in
# global lxml logging, and doesn't expose any attributes
# other than those already present in _ListErrorLog


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


class TestListLogMethods:
    @_testutils.signature_tester(_ListErrorLog.filter_domains, (
        ("domains", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_filter_domains(self, list_log: _ListErrorLog) -> None:
        filtered = list_log.filter_domains([ErrorDomains.XINCLUDE, ErrorDomains.DTD])
        reveal_type(filtered)
        del filtered

        filtered = list_log.filter_domains(ErrorDomains.PARSER)
        reveal_type(filtered)
        del filtered

        with pytest.raises(TypeError, match=r"argument .+ is not iterable"):
            _ = list_log.filter_domains(cast(Any, None))

    @_testutils.signature_tester(_ListErrorLog.filter_levels, (
        ("levels", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))
    def test_filter_levels(self, list_log: _ListErrorLog) -> None:
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

    @_testutils.empty_signature_tester(
        _ListErrorLog.filter_from_errors,
        _ListErrorLog.filter_from_fatals,
        _ListErrorLog.filter_from_warnings,
    )
    @_testutils.signature_tester(_ListErrorLog.filter_from_level, (
        ("level", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))
    def test_filter_from_level(self, list_log: _ListErrorLog) -> None:
        if _method_no_kwarg():
            new_log = list_log.filter_from_level(ErrorLevels.NONE)
        else:
            new_log = list_log.filter_from_level(level=ErrorLevels.NONE)
        reveal_type(new_log)
        del new_log

        reveal_type(list_log.filter_from_errors())
        reveal_type(list_log.filter_from_fatals())
        reveal_type(list_log.filter_from_warnings())

    # TODO implement filter_types test when enums are completed in stub
    # def test_filter_types(self, list_log: _ListErrorLog) -> None:
    # new_log = list_log.filter_types(ErrorTypes.???)

    @_testutils.signature_tester(_ListErrorLog.receive, (
        ("entry", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))
    def test_receive(self, list_log: _ListErrorLog) -> None:
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

    @_testutils.empty_signature_tester(_ListErrorLog.copy)
    def test_copy(self, list_log: _ListErrorLog) -> None:
        reveal_type(list_log.copy())


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


class TestModuleFunc:
    @_testutils.empty_signature_tester(clear_error_log)
    @_testutils.signature_tester(use_global_python_log, (
        ("log", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_sig(self) -> None:
        pass

    def test_global_log_usage(self) -> None:
        with pytest.raises(
            TypeError, match=r"expected lxml\.etree\.PyErrorLog, got int"
        ):
            use_global_python_log(cast(Any, 1))

        # exception if used after use_global_python_log
        clear_error_log()

        pylog = PyErrorLog()
        use_global_python_log(pylog)


class TestPyErrorLog:
    def test_construct(self) -> None:
        pylog = PyErrorLog()
        use_global_python_log(pylog)
        del pylog

        pylog = PyErrorLog("foobar")
        use_global_python_log(pylog)
        del pylog

        with pytest.raises(TypeError, match="logger name must be a string"):
            _ = PyErrorLog(cast(Any, 1))

        pylog = PyErrorLog(logger_name="foobar")
        use_global_python_log(pylog)
        del pylog

        logger = logging.Logger("foobar")
        pylog = PyErrorLog(logger=logger)
        use_global_python_log(pylog)
        del pylog

        with pytest.raises(AttributeError, match="has no attribute 'log'"):
            _ = PyErrorLog(logger=cast(Any, "foobar"))

    def test_properties(self) -> None:
        pylog = PyErrorLog()
        use_global_python_log(pylog)

        reveal_type(pylog.last_error)  # None initially
        for mapping in pylog.level_map.items():
            reveal_type(mapping[0])
            reveal_type(mapping[1])

        broken_xml = "<doc><a><b></a>&bar;</doc>"
        with pytest.raises(XMLSyntaxError):
            _ = fromstring(broken_xml)

        assert pylog.last_error is not None
        reveal_type(pylog.last_error)
        pylog.receive(pylog.last_error)
