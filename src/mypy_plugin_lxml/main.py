from __future__ import annotations

from collections.abc import (
    Callable,
)
from typing import cast

from mypy.checker import (
    TypeChecker,
)
from mypy.nodes import (
    TypeInfo,
)
from mypy.plugin import (
    MethodContext,
    Plugin,
)
from mypy.types import (
    Instance,
    Type,
    get_proper_type,
)


class MypyLxmlPlugin(Plugin):
    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        _, _, method_name = fullname.rpartition(".")
        if method_name in {"set_element_class_lookup", "setElementClassLookup"}:
            # Delegate class name checking to the hook, because we want to
            # support user custom subclasses
            return _set_class_lookup_method_hook
        else:
            return None


def _set_class_lookup_method_hook(ctx: MethodContext) -> Type:
    """Set subscript element type when changing class lookup for parsers"""

    def _get_typeinfo_from(fullname: str) -> TypeInfo:
        module_fullname, _, klass = fullname.rpartition(".")
        assert isinstance(ctx.api, TypeChecker)
        assert module_fullname in ctx.api.modules
        mod = ctx.api.modules[module_fullname]
        assert klass in mod.names
        node = mod.names[klass].node
        assert isinstance(node, TypeInfo)
        return node

    def _create_instance_from(fullname: str) -> Instance:
        return Instance(_get_typeinfo_from(fullname), [])

    def _fullname_or_base_is(name: str) -> Instance | None:
        lookup = get_proper_type(ctx.arg_types[0][0])
        assert isinstance(lookup, Instance)
        # Use stock class lookups -> check fullname
        # Custom subclassed lookups -> check bases
        if lookup.type.fullname == name:
            return lookup

        for base in lookup.type.bases:
            if base.type.fullname == name:
                return base
        else:
            return None

    if len(ctx.arg_types) == 0:  # Non-generic class like html.HTMLParser
        return ctx.default_return_type

    assert len(ctx.arg_types) == 1
    assert isinstance(ctx.type, Instance)

    if len(ctx.arg_types[0]) == 0:  # no arg = reset element lookup to default
        ctx.type.args = (_create_instance_from("lxml.etree._element._Element"),)
        return ctx.default_return_type

    assert len(ctx.arg_types[0]) == 1
    arg = None

    if lookup := _fullname_or_base_is("lxml.html._parse.HtmlElementClassLookup"):
        arg = _create_instance_from("lxml.html._element.HtmlElement")
    elif lookup := _fullname_or_base_is(
        "lxml.objectify._misc.ObjectifyElementClassLookup"
    ):
        arg = _create_instance_from("lxml.objectify._element.ObjectifiedElement")
    elif lookup := _fullname_or_base_is(
        "lxml.etree._classlookup.ElementDefaultClassLookup"
    ):
        arg = cast(Instance, lookup.args[0])
    if arg:
        ctx.type.args = (arg,)

    return ctx.default_return_type


def plugin(_: str) -> type[MypyLxmlPlugin]:
    return MypyLxmlPlugin
