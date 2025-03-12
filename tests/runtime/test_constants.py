from __future__ import annotations

import sys

import lxml.ElementInclude as _ei
import lxml.etree as _e
import lxml.html as _h
import lxml.isoschematron as _sch
import lxml.objectify as _o

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestEtreeConstants:
    def test_ver_const(self) -> None:
        reveal_type(_e.LIBXML_COMPILED_VERSION)
        reveal_type(_e.LIBXML_VERSION)
        reveal_type(_e.LIBXSLT_COMPILED_VERSION)
        reveal_type(_e.LIBXSLT_VERSION)
        reveal_type(_e.LXML_VERSION)
        reveal_type(_e.__version__)

        if _e.LXML_VERSION >= (5, 2, 2):
            reveal_type(_e.ICONV_COMPILED_VERSION)

        if _e.LXML_VERSION >= (6, 0):
            reveal_type(_e.LIBXML_COMPILED_FEATURES)
            reveal_type(_e.LIBXML_FEATURES)

        # no read-write test, they are actually writable

    def test_other_const(self) -> None:
        reveal_type(_e.DEBUG)
        _e.DEBUG = 1
        # Stop here, DEBUG can actually be set to anything


class TestSchematronConstants:
    def test_ns_const(self) -> None:
        reveal_type(_sch.RELAXNG_NS)
        reveal_type(_sch.SCHEMATRON_NS)
        reveal_type(_sch.SVRL_NS)
        reveal_type(_sch.XML_SCHEMA_NS)


class TestObjectifyConstants:
    def test_all_const(self) -> None:
        reveal_type(_o.__version__)
        reveal_type(_o.PYTYPE_ATTRIBUTE)


class TestHtmlConstants:
    def test_ns_const(self) -> None:
        reveal_type(_h.XHTML_NAMESPACE)


class TestElemIncludeConstants:
    def test_xinc_const(self) -> None:
        reveal_type(_ei.XINCLUDE)
        reveal_type(_ei.XINCLUDE_FALLBACK)
        reveal_type(_ei.XINCLUDE_INCLUDE)
        reveal_type(_ei.XINCLUDE_ITER_TAG)

    def test_other_const(self) -> None:
        reveal_type(_ei.DEFAULT_MAX_INCLUSION_DEPTH)
