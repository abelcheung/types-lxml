from __future__ import annotations

import sys
from inspect import Parameter
from types import NoneType
from typing import Any

import pytest
from hypothesis import HealthCheck, given, settings, strategies as st
from lxml.etree import (
    Comment,
    Entity,
    ProcessingInstruction,
    _Comment as _Comment,
    _Entity as _Entity,
    _ProcessingInstruction as _ProcessingInstruction,
)

from .._testutils import signature_tester, strategy as _st

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

    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    @given(text=_st.all_instances_except_of_type(NoneType, str, bytes, bytearray))
    @pytest.mark.slow
    def test_init_bad_1(self, text: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            _ = Comment(text)

    @given(text=st.iterables(
        _st.all_instances_except_of_type(), min_size=1, max_size=3,
    ))  # fmt: skip
    def test_init_bad_2(self, text: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            _ = Comment(text)

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
        mesg = r"objects is not writable"
        with pytest.raises(AttributeError, match=mesg):
            comm.tag = comm.tag  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with pytest.raises(AttributeError, match=mesg):
            del comm.tag  # pyright: ignore[reportAttributeAccessIssue]

    def test_text_property_ok(self) -> None:
        comm = Comment()
        reveal_type(comm.text)
        for text in (None, "foo", b"foo", bytearray(b"foo")):
            comm.text = text
            reveal_type(comm.text)
        with pytest.raises(NotImplementedError):
            del comm.text  # pyright: ignore[reportAttributeAccessIssue]

    @given(text=_st.all_instances_except_of_type(NoneType, str, bytes, bytearray))
    def test_text_property_bad_1(self, text: Any) -> None:
        comm = Comment()
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            comm.text = text

    @given(text=st.iterables(
        _st.all_instances_except_of_type(), min_size=1, max_size=3,
    ))  # fmt: skip
    def test_text_property_bad_2(self, text: Any) -> None:
        comm = Comment()
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            comm.text = text


class TestEntity:
    @signature_tester(Entity, (
        ("name", Parameter.POSITIONAL_OR_KEYWORD, Parameter.empty),
    ))  # fmt: skip
    def test_init_ok(self) -> None:
        for name in ("foo", b"foo", bytearray(b"foo")):
            ent = Entity(name)
            reveal_type(ent)
            del ent

    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    @given(name=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_init_bad_1(self, name: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            _ = Entity(name)

    @given(name=st.iterables(
        _st.all_instances_except_of_type(), min_size=1, max_size=3,
    ))  # fmt: skip
    def test_init_bad_2(self, name: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            _ = Entity(name)

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
        mesg = r"objects is not writable"
        # TODO: reveal_type on function object not supported yet
        assert ent.tag == Entity
        with pytest.raises(AttributeError, match=mesg):
            ent.tag = ent.tag  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with pytest.raises(AttributeError, match=mesg):
            del ent.tag  # pyright: ignore[reportAttributeAccessIssue]

    def test_text_property(self) -> None:
        ent = Entity("baz")
        reveal_type(ent.text)
        mesg = r"objects is not writable"
        with pytest.raises(AttributeError, match=mesg):
            ent.text = ent.text  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with pytest.raises(AttributeError, match=mesg):
            del ent.text  # pyright: ignore[reportAttributeAccessIssue]

    def test_name_property_ok(self) -> None:
        ent = Entity("baz")
        reveal_type(ent.name)
        for name in ("foo", b"foo", bytearray(b"foo")):
            ent.name = name
            reveal_type(ent.name)
        with pytest.raises(NotImplementedError):
            del ent.name  # pyright: ignore[reportAttributeAccessIssue]

    @given(name=_st.all_instances_except_of_type(str, bytes, bytearray))
    def test_name_property_bad_1(self, name: Any) -> None:
        ent = Entity("baz")
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            ent.name = name

    @given(name=st.iterables(
        _st.all_instances_except_of_type(), min_size=1, max_size=3,
    ))  # fmt: skip
    def test_name_property_bad_2(self, name: Any) -> None:
        ent = Entity("baz")
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            ent.name = name


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

    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    @given(target=_st.all_instances_except_of_type(str, bytes, bytearray))
    @pytest.mark.slow
    def test_target_arg_bad_1(self, target: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            _ = ProcessingInstruction(target)

    @given(target=st.iterables(
        _st.all_instances_except_of_type(), min_size=1, max_size=3,
    ))  # fmt: skip
    def test_target_arg_bad_2(self, target: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            _ = ProcessingInstruction(target)

    def test_text_arg_ok(self) -> None:
        for text in (None, "bar", b"bar", bytearray(b"bar")):
            pi = ProcessingInstruction("foo", text=text)
            reveal_type(pi)
            del pi

    @settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
    @given(text=_st.all_instances_except_of_type(NoneType, str, bytes, bytearray))
    @pytest.mark.slow
    def test_text_arg_bad_1(self, text: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            _ = ProcessingInstruction("foo", text)

    @given(text=st.iterables(
        _st.all_instances_except_of_type(), min_size=1, max_size=3,
    ))  # fmt: skip
    def test_text_arg_bad_2(self, text: Any) -> None:
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            _ = ProcessingInstruction("foo", text)

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
        set_exc_mesg = r"objects is not writable"
        with pytest.raises(AttributeError, match=set_exc_mesg):
            pi.attrib = {"foo": "bar"}  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with pytest.raises(AttributeError, match=set_exc_mesg):
            del pi.attrib  # pyright: ignore[reportAttributeAccessIssue]

    def test_tag_property(self) -> None:
        pi = ProcessingInstruction("baz")
        mesg = r"objects is not writable"
        # TODO: reveal_type on function object not supported yet
        assert pi.tag == ProcessingInstruction
        with pytest.raises(AttributeError, match=mesg):
            pi.tag = pi.tag  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]
        with pytest.raises(AttributeError, match=mesg):
            del pi.tag  # pyright: ignore[reportAttributeAccessIssue]

    def test_text_property_ok(self) -> None:
        pi = ProcessingInstruction("baz")
        reveal_type(pi.text)
        for text in (None, "foo", b"foo", bytearray(b"foo")):
            pi.text = text
            reveal_type(pi.text)
        with pytest.raises(NotImplementedError):
            del pi.text  # pyright: ignore[reportAttributeAccessIssue]

    @given(text=_st.all_instances_except_of_type(NoneType, str, bytes, bytearray))
    def test_text_property_bad_1(self, text: Any) -> None:
        pi = ProcessingInstruction("baz")
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            pi.text = text

    @given(text=st.iterables(
        _st.all_instances_except_of_type(), min_size=1, max_size=3,
    ))  # fmt: skip
    def test_text_property_bad_2(self, text: Any) -> None:
        pi = ProcessingInstruction("baz")
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            pi.text = text

    def test_target_property_ok(self) -> None:
        pi = ProcessingInstruction("baz")
        reveal_type(pi.target)
        for target in ("bar", b"bar", bytearray(b"bar")):
            pi.target = target
            reveal_type(pi.target)
        with pytest.raises(NotImplementedError):
            del pi.target  # pyright: ignore[reportAttributeAccessIssue]

    @given(target=_st.all_instances_except_of_type(str, bytes, bytearray))
    def test_target_property_bad_1(self, target: Any) -> None:
        pi = ProcessingInstruction("baz")
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            pi.target = target

    @given(target=st.iterables(
        _st.all_instances_except_of_type(), min_size=1, max_size=3,
    ))  # fmt: skip
    def test_target_property_bad_2(self, target: Any) -> None:
        pi = ProcessingInstruction("baz")
        with pytest.raises(TypeError, match="must be bytes or unicode"):
            pi.target = target
