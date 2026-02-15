# Not much can be tested with resolvers, as they don't produce
# any apparent result. In places where the result matters, only
# content changes would happen, which are irrelevant to typing
# changes which we concern about. So we only check if lxml
# documentation examples wouldn't produce any error, and perform basic
# method checks.

from __future__ import annotations

import sys
import textwrap
from io import StringIO
from typing import (
    TYPE_CHECKING,
    Any,
)

import pytest
from hypothesis import given, settings
from lxml.etree import (
    XSLT,
    Resolver,
    XMLParser,
    XMLSyntaxError,
    XSLTParseError,
    parse,
)

from ._testutils import strategy as _st
from ._testutils.errors import (
    raise_unexpected_type,
)

if TYPE_CHECKING:
    from lxml.etree._docloader import (  # pyright: ignore[reportMissingModuleSource]
        _InputDocument,
    )

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class NullResolver(Resolver):
    def resolve(
        self,
        system_url: str | None,
        public_id: str | None,
        context: object,  # _ResolverContext
        /,
    ) -> None:
        print(f"Not resolving URL '{system_url}' and ID '{public_id}'")
        return None


class DTDResolver(Resolver):
    def resolve(
        self,
        url: str | None,
        id: str | None,
        context: object,
        /,
    ) -> _InputDocument:
        print(f"Resolving URL '{url}'")
        return self.resolve_string(
            f'<!ENTITY myentity "[resolved text: {url}]">',
            context,
        )


class EmptyDTDResolver(Resolver):
    def resolve(
        self,
        url: str | None,
        id: str | None,
        context: object,
        /,
    ) -> _InputDocument:
        print(f"Resolving URL '{url}' as empty document")
        return self.resolve_empty(context)


class PrefixResolver(Resolver):
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.result_xml = textwrap.dedent(f"""
            <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                <test xmlns="testNS">{prefix}-TEST</test>
            </xsl:stylesheet>""")

    def resolve(
        self,
        url: str | None,
        id: str | None,
        context: object,
        /,
    ) -> _InputDocument | None:
        if url and url.startswith(self.prefix):
            print(f"Resolved url '{url}' as prefix '{self.prefix}'")
            return self.resolve_string(self.result_xml, context)
        return None


unknown_entity_xml = '<!DOCTYPE doc SYSTEM "MissingDTD.dtd"><doc>&myentity;</doc>'


def test_null_resolver() -> None:
    resolver = NullResolver()
    reveal_type(resolver)
    parser = XMLParser(load_dtd=True)
    parser.resolvers.add(resolver)
    with pytest.raises(XMLSyntaxError, match="Entity 'myentity' not defined"):
        _ = parse(StringIO(unknown_entity_xml), parser)


class TestUseDtdResolver:
    def test_dtd_resolver(self) -> None:
        parser = XMLParser(load_dtd=True)
        with pytest.raises(XMLSyntaxError, match="Entity 'myentity' not defined"):
            _ = parse(StringIO(unknown_entity_xml), parser)

        resolver = DTDResolver()
        reveal_type(resolver)
        parser.resolvers.add(resolver)
        tree = parse(StringIO(unknown_entity_xml), parser)
        root = tree.getroot()
        print(root.text)

    def test_empty_dtd_resolver(self) -> None:
        resolver = EmptyDTDResolver()
        reveal_type(resolver)
        parser = XMLParser(load_dtd=True)
        parser.resolvers.add(resolver)
        with pytest.raises(XMLSyntaxError, match="Entity 'myentity' not defined"):
            _ = parse(StringIO(unknown_entity_xml), parser)


class TestPrefixResolver:
    def test_prefix_resolver(self) -> None:
        unresolved_xsl = textwrap.dedent("""
            <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                <xsl:include href="honk:test"/>
                <xsl:template match="/">
                    <test>
                        <xsl:value-of select="document('honk:test')/*/*/text()"/>
                    </test>
                </xsl:template>
            </xsl:stylesheet>""")

        bad_resolver = PrefixResolver("test")
        good_resolver = PrefixResolver("honk")
        reveal_type(bad_resolver)
        reveal_type(good_resolver)

        parser = XMLParser(load_dtd=True)
        tree = parse(StringIO(unresolved_xsl), parser)
        with pytest.raises(XSLTParseError, match="Cannot resolve URI honk:test"):
            _ = XSLT(tree)

        parser.resolvers.add(bad_resolver)
        tree = parse(StringIO(unresolved_xsl), parser)
        with pytest.raises(XSLTParseError, match="Cannot resolve URI honk:test"):
            _ = XSLT(tree)

        parser.resolvers.remove(bad_resolver)
        parser.resolvers.add(good_resolver)
        tree = parse(StringIO(unresolved_xsl), parser)
        transform = XSLT(tree)
        result = transform(tree)
        print(result)

#
# TODO Test for filename and file object resolvers
#

class TestRegistryMethods:
    # Positive method test already done in TestPrefixResolver
    @settings(max_examples=300)
    @given(thing=_st.all_instances_except_of_type())
    def test_registry_add_bad(self, thing: Any) -> None:
        parser = XMLParser(load_dtd=True)
        with raise_unexpected_type:
            parser.resolvers.add(thing)

    # Negative test for remove() actually implies the argument
    # can be anything as long as it's hashable. However, in
    # order to make it useful in stub, we limit the argument type only
    # to those processed by add() method, that is Resolver instances.
    @given(thing=_st.all_instances_except_of_type(set))
    def test_registry_remove_bad(self, thing: Any) -> None:
        parser = XMLParser(load_dtd=True)
        try:
            _ = hash(thing)
        except TypeError:
            with pytest.raises(TypeError, match=r"unhashable type: '.+?'"):
                parser.resolvers.remove(thing)
        else:
            # set.discard(nonexistent_element) never raises
            parser.resolvers.remove(thing)
