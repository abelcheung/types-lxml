from __future__ import annotations

import operator
from typing import Any, Literal, cast

import hypothesis.strategies as st
from hypothesis import note
from lxml.etree import QName


def all_types_except(
    *excluded: type[Any], exact: bool = False
) -> st.SearchStrategy[type]:
    if Any in excluded or object in excluded:  # type: ignore[comparison-overlap]
        raise ValueError("Cannot exclude everything")
    strategy: st.SearchStrategy[type] = st.from_type(type)
    if len(excluded) == 0:
        return strategy
    elif exact:
        return strategy.filter(lambda x: x not in excluded)
    else:
        return strategy.filter(lambda x: not issubclass(x, excluded))


def all_instances_except_of_type(*excluded: type[Any]) -> st.SearchStrategy[Any]:
    return cast(  # type: ignore[redundant-cast]
        st.SearchStrategy[Any], all_types_except(*excluded).flatmap(st.from_type)
    )


# Although stringified XML names use colon (:) character,
# lxml uses Clark notation ({namespace}name) for accessing
# namespaced tags and attributes. Therefore we don't generate
# names with colon.
# https://www.w3.org/TR/xml-names/#Conformance
# https://www.w3.org/TR/xml/#NT-NameStartChar
# https://www.w3.org/TR/xml/#NT-NameChar
def _xml_name_unicode_char(*, start: bool) -> st.SearchStrategy[str]:
    return st.one_of(  # prefers earlier strategies
        st.characters(
            min_codepoint=ord("A"),
            max_codepoint=0x2FF,
            categories={"L"},
            include_characters="_" if start else "_-.0123456789\xb7",
            exclude_characters="\xaa\xb5\xba",
        ),
        st.characters(
            min_codepoint=0x370 if start else 0x300,
            max_codepoint=0x1FFF,
            blacklist_characters="\u037e",
        ),
        st.characters(
            min_codepoint=0x2070,
            max_codepoint=0x218F,
            include_characters="\u200c\u200d" if start else "\u200c\u200d\u203f\u2040",
        ),
        st.characters(
            min_codepoint=0x2C00,
            max_codepoint=0xEFFFF,
            exclude_categories={"Cs", "Co", "Cn"},
            exclude_characters="".join(chr(c) for c in range(0x2FF0, 0x3001)),
        ),
    )


# Lxml expects 7-bit ASCII for names if supplied as bytes
def _xml_name_ascii_char(*, start: bool) -> st.SearchStrategy[str]:
    return st.characters(
        codec="ascii",
        min_codepoint=ord("A"),
        max_codepoint=ord("z"),
        categories={"Lu", "Ll"},
        include_characters="_" if start else "_-.0123456789",
    )


def xml_name_nons(
    variant: Literal["unicode", "ascii"] = "unicode",
) -> st.SearchStrategy[str]:
    char_strategy = (
        _xml_name_unicode_char if variant == "unicode" else _xml_name_ascii_char
    )
    first_char = char_strategy(start=True)
    rest_char = st.text(max_size=4, alphabet=char_strategy(start=False))
    return st.builds(operator.add, first_char, rest_char)


def xml_name(
    variant: Literal["unicode", "ascii"] = "unicode",
) -> st.SearchStrategy[str]:
    def add_ns(ns: str, n: str) -> str:
        note(f"ns: {ns}, n: {n}")
        return "{" + ns + "}" + n

    name_strat = xml_name_nons(variant)
    return st.one_of(
        st.builds(
            add_ns,
            st.text(
                max_size=5,
                # Exclude characters used in Clark notation
                alphabet=xml_legal_char(variant).filter(lambda c: c not in "{}"),
            ),
            name_strat,
        ),
        name_strat,
        name_strat.map(lambda x: "{}" + x),
    )


# FIXME: For future test, QName("", "foo") raise exception
def xml_name_arg() -> st.SearchStrategy[str | bytes | bytearray | QName]:
    s = xml_name()
    qn = s.map(QName)
    b = xml_name("ascii").map(lambda x: x.encode("ascii"))
    ba = b.map(bytearray)
    return st.one_of(s, b, ba, qn)


# https://www.w3.org/TR/xml/#NT-Char
def xml_legal_char(
    variant: Literal["unicode", "ascii"] = "unicode",
) -> st.SearchStrategy[str]:
    codec = "utf-8" if variant == "unicode" else "ascii"
    # TODO consider excluding following ranges too
    # [#x7F-#x84], [#x86-#x9F], [#xFDD0-#xFDEF]
    return st.characters(
        codec=codec,
        min_codepoint=ord(" "),
        include_characters="\t\n\r",
        exclude_categories={"Cc", "Cs", "Co", "Cn"},
    )


# https://www.w3.org/TR/xml/#NT-CharRef
def xml_char_decimal_ref(
    char_strategy: st.SearchStrategy[str] = xml_legal_char(),
) -> st.SearchStrategy[str]:
    return char_strategy.map(lambda i: "&#{};".format(ord(i)))


def xml_char_hex_ref(
    char_strategy: st.SearchStrategy[str] = xml_legal_char(),
) -> st.SearchStrategy[str]:
    return char_strategy.map(lambda i: "&#x{:x};".format(ord(i)))


# https://www.w3.org/TR/xml/#NT-EntityRef
def xml_entity_ref(
    variant: Literal["unicode", "ascii"] = "unicode",
) -> st.SearchStrategy[str]:
    return xml_name_nons(variant).map(lambda x: f"&{x};")


# https://www.w3.org/TR/xml/#NT-AttValue
def xml_attr_value(
    variant: Literal["unicode", "ascii"] = "unicode",
) -> st.SearchStrategy[str]:
    refined_char = xml_legal_char(variant).filter(lambda x: x not in "&<")
    return st.lists(
        st.one_of(
            refined_char,
            xml_char_decimal_ref(refined_char),
            xml_char_hex_ref(refined_char),
            xml_entity_ref(variant),
        ),
        max_size=5,
    ).map(lambda x: "".join(x))


def xml_attr_value_arg() -> st.SearchStrategy[str | bytes | bytearray | QName]:
    s = xml_attr_value()
    # Note that QName only accepts characters usable in XML name
    # Practically QName is not used for attribute values, but
    # we concern about annotation only
    qn = xml_name().map(QName)
    b = xml_attr_value("ascii").map(lambda x: x.encode("ascii"))
    ba = b.map(bytearray)
    return st.one_of(s, b, ba, qn)