from __future__ import annotations

from collections.abc import (
    Callable,
)

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
)


class MypyLxmlPlugin(Plugin):
    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        _, _, method_name = fullname.rpartition(".")
        match method_name:
            # Delegate class name checking to the hook, because we want to
            # support user custom subclasses
            case ('set_element_class_lookup' | 'setElementClassLookup'):
                return _set_class_lookup_method_hook
            case _:
                return None


def _set_class_lookup_method_hook(ctx: MethodContext) -> Type:
    """Set subscript element type when changing class lookup for parsers
    """
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


    if len(ctx.arg_types) == 0: # Non-generic class like html.HTMLParser
        return ctx.default_return_type

    assert len(ctx.arg_types) == 1
    assert isinstance(ctx.type, Instance)

    # Don't need any check on class names (ctx.type.type), since only
    # etree.XMLParser, etree.HTMLParser, iterparse and their subclasses
    # can possibly have set_element_class_lookup method

    if len(ctx.arg_types[0]) == 0:  # no arg = reset element lookup to default
        ctx.type.args = (_create_instance_from('lxml.etree._element._Element'),)
        return ctx.default_return_type

    assert len(ctx.arg_types[0]) == 1
    lookup = ctx.arg_types[0][0]
    assert isinstance(lookup, Instance)

    # FIXME Not handling custom ElementClassLookup subclass yet
    match lookup.type.fullname:
        case 'lxml.html._parse.HtmlElementClassLookup':
            ctx.type.args = (_create_instance_from('lxml.html._element.HtmlElement'),)
            return ctx.default_return_type
        case 'lxml.objectify._misc.ObjectifyElementClassLookup':
            ctx.type.args = (_create_instance_from('lxml.objectify._element.ObjectifiedElement'),)
            return ctx.default_return_type
        case _:  # output vanilla _Element for other lookups
            return ctx.default_return_type

def plugin(_: str) -> type[MypyLxmlPlugin]:
    return MypyLxmlPlugin
