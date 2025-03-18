from __future__ import annotations

import sys
from inspect import Parameter
from types import NoneType
from typing import Any

import pytest
from hypothesis import HealthCheck, given, settings
from lxml.etree import (
    Comment,
    Entity,
    ProcessingInstruction,
    _Comment as _Comment,
    _Entity as _Entity,
    _ProcessingInstruction as _ProcessingInstruction,
)

from .._testutils import signature_tester, strategy as _st
from .._testutils.errors import (
    raise_attr_not_writable,
    raise_invalid_utf8_type,
)

if sys.version_info >= (3, 11):
    from typing import reveal_type
else:
    from typing_extensions import reveal_type


class TestComment:
    @signature_tester(Comment, (
        ("text", Parameter.POSITIONAL_OR_KEYWORD, None),
    ))  # fmt: skip
    def test_init_ok(self) -> None:
        comm = Comment()
        reveal_type(comm)
        del comm

        for text in (None, "foo", b"foo", bytearray(b"foo")):
            comm = Comment(text)
            reveal_type(comm)
            del comm

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType, str, bytes, bytearray))
    @pytest.mark.slow
    def test_init_bad_1(self, thing: Any) -> None:
        with raise_invalid_utf8_type:
            _ = Comment(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_init_bad_2(self, iterable_of: Any) -> None:
        with raise_invalid_utf8_type:
            _ = Comment(iterable_of("foo"))

    def test_dummy_dunders(self) -> None:
        comm = Comment()
        assert len(comm) == 0
        assert comm[:] == []  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        get_exc_mesg = r"list index out of range"
        set_exc_mesg = r"this element does not have children or attributes"
        with pytest.raises(IndexError, match=get_exc_mesg):
            comm[0]  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            comm[0] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(IndexError, match=get_exc_mesg):
            comm["foo"]  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            comm["foo"] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            comm[:] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]

    # We only test methods explicitly banned in lxml source code.
    # For example, .append() is forbidden, yet one can use
    # .extend() to circumvent and mess it up.
    def test_dummy_methods(self) -> None:
        comm = Comment()
        assert len(comm.attrib) == 0
        set_exc_mesg = r"this element does not have children or attributes"
        with pytest.raises(TypeError, match=set_exc_mesg):
            comm.set("foo", "bar")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        assert comm.get("foo") is None
        with pytest.raises(TypeError, match=set_exc_mesg):
            comm.append(comm)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            comm.insert(0, comm)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]

    def test_tag_property(self) -> None:
        comm = Comment()
        # TODO: reveal_type on function object not supported yet
        assert comm.tag == Comment
        with raise_attr_not_writable:
            comm.tag = comm.tag  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with raise_attr_not_writable:
            del comm.tag  # pyright: ignore[reportAttributeAccessIssue]

    def test_text_property_ok(self) -> None:
        comm = Comment()
        reveal_type(comm.text)
        for text in (None, "foo", b"foo", bytearray(b"foo")):
            comm.text = text
            reveal_type(comm.text)
        with pytest.raises(NotImplementedError):
            del comm.text  # pyright: ignore[reportAttributeAccessIssue]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType, str, bytes, bytearray))
    @pytest.mark.slow
    def test_text_property_bad_1(self, thing: Any) -> None:
        comm = Comment()
        with raise_invalid_utf8_type:
            comm.text = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_text_property_bad_2(self, iterable_of: Any) -> None:
        comm = Comment()
        with raise_invalid_utf8_type:
            comm.text = iterable_of("foo")


class TestEntity:
    @signature_tester(Entity, (
        ("name", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_init_ok(self) -> None:
        for name in ("foo", b"foo", bytearray(b"foo")):
            ent = Entity(name)
            reveal_type(ent)
            del ent

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_init_bad_1(self, thing: Any) -> None:
        with raise_invalid_utf8_type:
            _ = Entity(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_init_bad_2(self, iterable_of: Any) -> None:
        with raise_invalid_utf8_type:
            _ = Entity(iterable_of("foo"))

    def test_dummy_dunders(self) -> None:
        ent = Entity("baz")
        assert len(ent) == 0
        assert ent[:] == []  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        get_exc_mesg = r"list index out of range"
        set_exc_mesg = r"this element does not have children or attributes"
        with pytest.raises(IndexError, match=get_exc_mesg):
            ent[0]  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            ent[0] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(IndexError, match=get_exc_mesg):
            ent["foo"]  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            ent["foo"] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            ent[:] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]

    # We only test methods explicitly banned in lxml source code.
    # For example, .append() is forbidden, yet one can use
    # .extend() to circumvent and mess it up.
    def test_dummy_methods(self) -> None:
        ent = Entity("baz")
        assert len(ent.attrib) == 0
        set_exc_mesg = r"this element does not have children or attributes"
        with pytest.raises(TypeError, match=set_exc_mesg):
            ent.set("foo", "bar")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        assert ent.get("foo") is None
        with pytest.raises(TypeError, match=set_exc_mesg):
            ent.append(ent)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            ent.insert(0, ent)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]

    def test_tag_property(self) -> None:
        ent = Entity("baz")
        # TODO: reveal_type on function object not supported yet
        assert ent.tag == Entity
        with raise_attr_not_writable:
            ent.tag = ent.tag  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with raise_attr_not_writable:
            del ent.tag  # pyright: ignore[reportAttributeAccessIssue]

    def test_text_property(self) -> None:
        ent = Entity("baz")
        reveal_type(ent.text)
        with raise_attr_not_writable:
            ent.text = ent.text  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with raise_attr_not_writable:
            del ent.text  # pyright: ignore[reportAttributeAccessIssue]

    def test_name_property_ok(self) -> None:
        ent = Entity("baz")
        reveal_type(ent.name)
        for name in ("foo", b"foo", bytearray(b"foo")):
            ent.name = name
            reveal_type(ent.name)
        with pytest.raises(NotImplementedError):
            del ent.name  # pyright: ignore[reportAttributeAccessIssue]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_name_property_bad_1(self, thing: Any) -> None:
        ent = Entity("baz")
        with raise_invalid_utf8_type:
            ent.name = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_name_property_bad_2(self, iterable_of: Any) -> None:
        ent = Entity("baz")
        with raise_invalid_utf8_type:
            ent.name = iterable_of("foo")


class TestPI:
    @signature_tester(ProcessingInstruction, (
        ("target", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
        ("text"  , Parameter.POSITIONAL_OR_KEYWORD, None           ),
    ))  # fmt: skip
    def test_signature(self) -> None:
        pass

    def test_target_arg_ok(self) -> None:
        for target in ("foo", b"foo", bytearray(b"foo")):
            pi = ProcessingInstruction(target=target)
            reveal_type(pi)
            del pi

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_target_arg_bad_1(self, thing: Any) -> None:
        with raise_invalid_utf8_type:
            _ = ProcessingInstruction(thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_target_arg_bad_2(self, iterable_of: Any) -> None:
        with raise_invalid_utf8_type:
            _ = ProcessingInstruction(iterable_of("foo"))

    def test_text_arg_ok(self) -> None:
        for text in (None, "bar", b"bar", bytearray(b"bar")):
            pi = ProcessingInstruction("foo", text=text)
            reveal_type(pi)
            del pi

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType, str, bytes, bytearray))
    @pytest.mark.slow
    def test_text_arg_bad_1(self, thing: Any) -> None:
        with raise_invalid_utf8_type:
            _ = ProcessingInstruction("foo", thing)

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_text_arg_bad_2(self, iterable_of: Any) -> None:
        with raise_invalid_utf8_type:
            _ = ProcessingInstruction("foo", iterable_of("bar"))

    def test_dummy_dunders(self) -> None:
        pi = ProcessingInstruction("baz")
        assert len(pi) == 0
        assert pi[:] == []  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        get_exc_mesg = r"list index out of range"
        set_exc_mesg = r"this element does not have children or attributes"
        with pytest.raises(IndexError, match=get_exc_mesg):
            pi[0]  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            pi[0] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(IndexError, match=get_exc_mesg):
            pi["foo"]  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            pi["foo"] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            pi[:] = "bar"  # type: ignore[index]  # pyright: ignore[reportArgumentType]

    # We only test methods explicitly banned in lxml source code.
    # For example, .append() is forbidden, yet one can use
    # .extend() to circumvent and mess it up.
    def test_dummy_methods(self) -> None:
        pi = ProcessingInstruction("baz")
        set_exc_mesg = r"this element does not have children or attributes"
        with pytest.raises(TypeError, match=set_exc_mesg):
            pi.set("foo", "bar")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        assert pi.get("foo") is None
        with pytest.raises(TypeError, match=set_exc_mesg):
            pi.append(pi)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError, match=set_exc_mesg):
            pi.insert(0, pi)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]

    def test_attrib_property(self) -> None:
        pi = ProcessingInstruction("xml-stylesheet", "type='text/xsl' href='style.xsl'")
        assert len(pi.attrib) == 2
        reveal_type(pi.attrib.get("type"))
        reveal_type(pi.attrib["href"])
        with raise_attr_not_writable:
            pi.attrib = {"foo": "bar"}  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with raise_attr_not_writable:
            del pi.attrib  # pyright: ignore[reportAttributeAccessIssue]

    def test_tag_property(self) -> None:
        pi = ProcessingInstruction("baz")
        # TODO: reveal_type on function object not supported yet
        assert pi.tag == ProcessingInstruction
        with raise_attr_not_writable:
            pi.tag = pi.tag  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with raise_attr_not_writable:
            del pi.tag  # pyright: ignore[reportAttributeAccessIssue]

    def test_text_property_ok(self) -> None:
        pi = ProcessingInstruction("baz")
        reveal_type(pi.text)
        for text in (None, "foo", b"foo", bytearray(b"foo")):
            pi.text = text
            reveal_type(pi.text)
        with pytest.raises(NotImplementedError):
            del pi.text  # pyright: ignore[reportAttributeAccessIssue]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(NoneType, str, bytes, bytearray))
    @pytest.mark.slow
    def test_text_property_bad_1(self, thing: Any) -> None:
        pi = ProcessingInstruction("baz")
        with raise_invalid_utf8_type:
            pi.text = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_text_property_bad_2(self, iterable_of: Any) -> None:
        pi = ProcessingInstruction("baz")
        with raise_invalid_utf8_type:
            pi.text = iterable_of("foo")

    def test_target_property_ok(self) -> None:
        pi = ProcessingInstruction("baz")
        reveal_type(pi.target)
        for target in ("bar", b"bar", bytearray(b"bar")):
            pi.target = target
            reveal_type(pi.target)
        with pytest.raises(NotImplementedError):
            del pi.target  # pyright: ignore[reportAttributeAccessIssue]

    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=300)
    @given(thing=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_target_property_bad_1(self, thing: Any) -> None:
        pi = ProcessingInstruction("baz")
        with raise_invalid_utf8_type:
            pi.target = thing

    @settings(max_examples=5)
    @given(iterable_of=_st.fixed_item_iterables())
    def test_target_property_bad_2(self, iterable_of: Any) -> None:
        pi = ProcessingInstruction("baz")
        with raise_invalid_utf8_type:
            pi.target = iterable_of("foo")
