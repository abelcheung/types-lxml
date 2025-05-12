from __future__ import annotations

import logging
import sys
from collections.abc import Iterable
from decimal import Decimal
from inspect import Parameter
from numbers import Real
from types import NoneType
from typing import Any, cast

import pytest
from hypothesis import HealthCheck, assume, given, settings
from lxml.etree import (
    LXML_VERSION,
    ErrorDomains,
    ErrorLevels,
    ErrorTypes,
    PyErrorLog,
    QName,
    XMLSyntaxError,
    _ListErrorLog,
    _LogEntry as _LogEntry,
    clear_error_log,
    fromstring,
    use_global_python_log,
)

from ._testutils import empty_signature_tester, signature_tester, strategy as _st
from ._testutils.errors import (
    raise_attr_not_writable,
    raise_no_attribute,
    raise_non_iterable,
    raise_wrong_arg_type,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


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

        for attr in (
            "domain_name",
            "type_name",
            "level_name",
            "line",
            "column",
            "message",
            "filename",
            "path",
        ):
            with raise_attr_not_writable:
                setattr(e0, attr, getattr(e0, attr))

        reveal_type(list_log.last_error)

        # types-lxml is lying below for following properties:
        # they are only present as int in runtime, but we want to
        # encourage symbolic comparisons, not whether they are int
        assert e0.domain == ErrorDomains.PARSER
        assert e0.level == ErrorLevels.FATAL
        assert e0.type == ErrorTypes.ERR_TAG_NAME_MISMATCH

    def test_container_behavior(self, list_log: _ListErrorLog) -> None:
        e0 = list_log[0]
        reveal_type(len(list_log))
        reveal_type(e0)
        reveal_type(e0 in list_log)
        for e in list_log:
            reveal_type(e)


class TestListLogMethods:
    @signature_tester(_ListErrorLog.filter_domains, (
        ("domains", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_filter_domains_arg_ok(self, list_log: _ListErrorLog) -> None:
        new_log = list_log.filter_domains(ErrorDomains.PARSER)
        reveal_type(new_log)
        assert len(new_log) > 0
        del new_log

        domains = iter([ErrorDomains.PARSER, ErrorDomains.BUFFER])
        new_log = list_log.filter_domains(domains)
        reveal_type(new_log)
        assert len(new_log) > 0

    # FIXME: negative test only proves arg is of type
    # int | Iterable[Any], and we want int | Iterable[int].
    #
    # Whole slew of types and classes don't cause any exception if placed
    # insider iterable, like NotImplementedType, enumerate, map, lambda etc.
    #
    # Issues apply to filter_levels below as well
    @settings(suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.function_scoped_fixture,
    ])  # fmt: skip
    @given(domains=_st.all_instances_except_of_type(int, Iterable))
    @pytest.mark.slow
    def test_filter_domains_arg_bad(
        self, list_log: _ListErrorLog, domains: Any
    ) -> None:
        with raise_non_iterable:
            _ = list_log.filter_domains(cast(Any, None))

    @signature_tester(
        _ListErrorLog.filter_types,
        (("types", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_filter_types_arg_ok(self, list_log: _ListErrorLog) -> None:
        new_log = list_log.filter_types(ErrorTypes.ERR_TAG_NAME_MISMATCH)
        reveal_type(new_log)
        assert len(new_log) > 0
        del new_log

        types = iter([
            ErrorTypes.ERR_TAG_NAME_MISMATCH,
            ErrorTypes.ERR_UNKNOWN_ENCODING,
        ])
        new_log = list_log.filter_types(types)
        reveal_type(new_log)
        assert len(new_log) > 0

    @settings(suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.function_scoped_fixture,
    ])  # fmt: skip
    @given(types=_st.all_instances_except_of_type(int, Iterable))
    @pytest.mark.slow
    def test_filter_types_arg_bad(self, list_log: _ListErrorLog, types: Any) -> None:
        with raise_non_iterable:
            _ = list_log.filter_types(types)

    @signature_tester(
        _ListErrorLog.filter_levels,
        (("levels", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_filter_levels_arg_ok(self, list_log: _ListErrorLog) -> None:
        new_log = list_log.filter_levels(ErrorLevels.FATAL)
        reveal_type(new_log)
        assert len(new_log) > 0
        del new_log

        levels = iter([ErrorLevels.ERROR, ErrorLevels.FATAL])
        if _method_no_kwarg():
            new_log = list_log.filter_levels(levels)
        else:
            new_log = list_log.filter_levels(levels=levels)
        reveal_type(new_log)
        assert len(new_log) > 0

    @settings(suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.function_scoped_fixture,
    ])  # fmt: skip
    @given(levels=_st.all_instances_except_of_type(int, Iterable))
    @pytest.mark.slow
    def test_filter_levels_arg_bad(self, list_log: _ListErrorLog, levels: Any) -> None:
        with raise_non_iterable:
            _ = list_log.filter_levels(levels)

    @signature_tester(
        _ListErrorLog.filter_from_level,
        (("level", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_filter_from_level_arg_ok(self, list_log: _ListErrorLog) -> None:
        if _method_no_kwarg():
            new_log = list_log.filter_from_level(ErrorLevels.NONE)
        else:
            new_log = list_log.filter_from_level(level=ErrorLevels.NONE)
        reveal_type(new_log)
        assert len(new_log) > 0

    @settings(suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.function_scoped_fixture,
    ])  # fmt: skip
    @given(level=_st.all_instances_except_of_type(int, float, Real, Decimal, QName))
    @pytest.mark.slow
    def test_filter_from_level_arg_bad(
        self, list_log: _ListErrorLog, level: Any
    ) -> None:
        with pytest.raises(TypeError, match=r"'>=' not supported between instances"):
            _ = list_log.filter_from_level(level)

    @empty_signature_tester(
        _ListErrorLog.filter_from_errors,
        _ListErrorLog.filter_from_fatals,
        _ListErrorLog.filter_from_warnings,
    )
    def test_filter_from_level_deriv(self, list_log: _ListErrorLog) -> None:
        reveal_type(list_log.filter_from_errors())
        reveal_type(list_log.filter_from_fatals())
        reveal_type(list_log.filter_from_warnings())

    @signature_tester(
        _ListErrorLog.receive,
        (("entry", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_receive(self, list_log: _ListErrorLog) -> None:
        if _method_no_kwarg():
            assert list_log.receive(list_log[0]) is None
        else:
            assert list_log.receive(entry=list_log[0]) is None
        with pytest.raises(TypeError, match=r"expected .+\._LogEntry, got int"):
            list_log.receive(cast(Any, 1))

    # BEWARE: vanilla _ListErrorLog has no clear() method,
    # thus can't be inspected

    @empty_signature_tester(_ListErrorLog.copy)
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
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type())
    @pytest.mark.slow
    def test_global_log_arg_bad_1(self, thing: Any) -> None:
        with pytest.raises(TypeError, match=r"expected .+\.PyErrorLog, got .+"):
            use_global_python_log(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_global_log_arg_bad_2(self, iterable_of: Any) -> None:
        pylog = PyErrorLog()
        with pytest.raises(TypeError, match=r"expected .+\.PyErrorLog, got .+"):
            use_global_python_log(iterable_of(pylog))

    @empty_signature_tester(clear_error_log)
    @signature_tester(
        use_global_python_log,
        (("log", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_global_log_arg_ok(self) -> None:
        # exception if used after use_global_python_log
        clear_error_log()

        pylog = PyErrorLog()
        use_global_python_log(pylog)


class TestPyErrorLog:
    # Generic Cython function signature
    def test_init_and_prop(self) -> None:
        pylog = PyErrorLog()
        use_global_python_log(pylog)

        reveal_type(pylog.last_error)  # None initially
        reveal_type(pylog.level_map)

        for attr_ in ("last_error", "level_map"):
            with raise_attr_not_writable:
                delattr(pylog, attr_)
            with raise_attr_not_writable:
                setattr(pylog, attr_, getattr(pylog, attr_))

        broken_xml = "<doc><a><b></a>&bar;</doc>"
        with pytest.raises(XMLSyntaxError):
            _ = fromstring(broken_xml)

        assert pylog.last_error is not None
        reveal_type(pylog.last_error)
        pylog.receive(pylog.last_error)

    def test_init_name_arg_ok(self) -> None:
        pylog = PyErrorLog("foobar")
        use_global_python_log(pylog)

        pylog = PyErrorLog(logger_name="foobar")
        use_global_python_log(pylog)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str))
    @pytest.mark.slow
    def test_init_name_arg_bad_1(self, thing: Any) -> None:
        assume(thing is NotImplemented or bool(thing))
        with pytest.raises(TypeError, match="logger name must be a string"):
            _ = PyErrorLog(logger_name=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_init_name_arg_bad_2(self, iterable_of: Any) -> None:
        with pytest.raises(TypeError, match="logger name must be a string"):
            _ = PyErrorLog(logger_name=iterable_of("foobar"))

    def test_init_logger_arg_ok(self) -> None:
        logger = logging.Logger("foobar")
        pylog = PyErrorLog(logger=logger)
        use_global_python_log(pylog)

        new_logger = logging.LoggerAdapter(logger, {})
        pylog = PyErrorLog(logger=new_logger)
        use_global_python_log(pylog)

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType))
    @pytest.mark.slow
    def test_init_logger_arg_bad_1(self, thing: Any) -> None:
        with raise_no_attribute:
            _ = PyErrorLog(logger=thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_init_logger_arg_bad_2(self, iterable_of: Any) -> None:
        logger = logging.Logger("foobar")
        with raise_no_attribute:
            _ = PyErrorLog(logger=iterable_of(logger))


class TestPyErrorLogMethods:
    @signature_tester(PyErrorLog.log, (
        ("log_entry", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("message"  , Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("args"     , Parameter.VAR_POSITIONAL       , Parameter.empty),
    ))  # fmt: skip
    def test_log_method_sig(self) -> None:
        pass

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type())
    @pytest.mark.slow
    def test_log_arg1_bad(self, pylog: PyErrorLog, thing: Any) -> None:
        with raise_no_attribute:
            pylog.log(log_entry=thing, message="dummy message")

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_log_arg1_bad_2(self, pylog: PyErrorLog, iterable_of: Any) -> None:
        with raise_no_attribute:
            pylog.log(log_entry=iterable_of(pylog.last_error), message="dummy message")

    def test_log_arg1_ok(self, pylog: PyErrorLog) -> None:
        assert pylog.last_error is not None
        pylog.log(pylog.last_error, "dummy message")

    # Don't perform any tests on .log() second argument.
    # logging module stringify the message so that any type
    # is acceptable, i.e. the method never fails.
    # Similarly, no varargs tests are performed, as they
    # are just passed to logging module as-is without any
    # effect by default.

    @signature_tester(
        PyErrorLog.receive,
        (("log_entry", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),),
    )
    def test_receive_sig(self) -> None:
        pass

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type())
    @pytest.mark.slow
    def test_receive_arg_bad_1(self, pylog: PyErrorLog, thing: Any) -> None:
        raise_cm = raise_no_attribute if thing is None else raise_wrong_arg_type
        with raise_cm:  # type: ignore[attr-defined]
            pylog.receive(thing)

    @given(iterable_of=_st.fixed_item_iterables())
    def test_receive_arg_bad_2(self, pylog: PyErrorLog, iterable_of: Any) -> None:
        with raise_wrong_arg_type:
            pylog.receive(iterable_of(pylog.last_error))

    def test_receive_arg_ok(self, pylog: PyErrorLog) -> None:
        assert pylog.last_error is not None
        pylog.receive(pylog.last_error)
