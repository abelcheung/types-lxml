from types import TracebackType
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    ContextManager,
    Iterable,
    overload,
)

from _typeshed import SupportsWrite

from .._types import (
    SupportsLaxedItems,
    _AnyStr,
    _FileReadSource,
    _FileWriteSource,
    _NSMapArg,
    _OutputMethodArg,
    _TagName,
)
from . import LxmlError, _Element, _ElementOrAnyTree

class SerialisationError(LxmlError): ...

# Interface quite similar to a ParserTarget, but canonicalized output
# is written during various stages before calling .close()
class C14NWriterTarget:
    def __init__(
        self,
        write: Callable[[str], Any],
        *,
        with_comments: bool = ...,
        strip_text: bool = ...,
        rewrite_prefixes: bool = ...,
        qname_aware_tags: Iterable[str] | None = ...,
        qname_aware_attrs: Iterable[str] | None = ...,
        exclude_attrs: Iterable[str] | None = ...,
        exclude_tags: Iterable[str] | None = ...,
    ) -> None: ...
    def data(self, data: str) -> None: ...
    def start_ns(self, prefix: str, uri: str) -> None: ...
    def start(self, tag: str, attrs: SupportsLaxedItems | None) -> None: ...
    def end(self, tag: str) -> None: ...
    def comment(self, text: str) -> None: ...
    def pi(self, target: str, data: str | None) -> None: ...
    def close(self) -> None: ...

# canonicalize() overload matrix:
# 2x input (via xml_data, via from_file)
# 2x output (None, .write())
# options keyword arguments come from C14NWriterTarget.__init__
@overload
def canonicalize(
    xml_data: _AnyStr | _ElementOrAnyTree,
    *,
    out: SupportsWrite,
    from_file: Any = ...,
    with_comments: bool = ...,
    strip_text: bool = ...,
    rewrite_prefixes: bool = ...,
    qname_aware_tags: Iterable[str] | None = ...,
    qname_aware_attrs: Iterable[str] | None = ...,
    exclude_attrs: Iterable[str] | None = ...,
    exclude_tags: Iterable[str] | None = ...,
) -> None: ...
@overload
def canonicalize(
    xml_data: None = ...,
    *,
    out: SupportsWrite,
    from_file: _FileReadSource,
    with_comments: bool = ...,
    strip_text: bool = ...,
    rewrite_prefixes: bool = ...,
    qname_aware_tags: Iterable[str] | None = ...,
    qname_aware_attrs: Iterable[str] | None = ...,
    exclude_attrs: Iterable[str] | None = ...,
    exclude_tags: Iterable[str] | None = ...,
) -> None: ...
@overload
def canonicalize(
    xml_data: _AnyStr | _ElementOrAnyTree,
    *,
    out: None = ...,
    from_file: Any = ...,
    with_comments: bool = ...,
    strip_text: bool = ...,
    rewrite_prefixes: bool = ...,
    qname_aware_tags: Iterable[str] | None = ...,
    qname_aware_attrs: Iterable[str] | None = ...,
    exclude_attrs: Iterable[str] | None = ...,
    exclude_tags: Iterable[str] | None = ...,
) -> str: ...
@overload
def canonicalize(
    xml_data: None = ...,
    *,
    out: None = ...,
    from_file: _FileReadSource,
    with_comments: bool = ...,
    strip_text: bool = ...,
    rewrite_prefixes: bool = ...,
    qname_aware_tags: Iterable[str] | None = ...,
    qname_aware_attrs: Iterable[str] | None = ...,
    exclude_attrs: Iterable[str] | None = ...,
    exclude_tags: Iterable[str] | None = ...,
) -> str: ...

#
# Incremental serializers
# https://lxml.de/api.html#incremental-xml-generation
#
# Special notes:
# 1. .method() argument can accept 'text', but it just behaves like 'xml'
# 2. Both sync/async version of .method() return the same context
#    manager objects. For coherence, we distinguish their return type
#    differently.
#
class _IncrementalFileWriter:
    def write_declaration(
        self,
        version: _AnyStr | None = ...,
        standalone: bool | None = ...,
        doctype: _AnyStr | None = ...,
    ) -> None: ...
    def write_doctype(self, doctype: _AnyStr | None) -> None: ...
    def write(
        self,
        *args: _AnyStr | _Element,
        with_tail: bool = ...,
        pretty_print: bool = ...,
        method: _OutputMethodArg | None = ...,
    ) -> None: ...
    def flush(self) -> None: ...
    def method(self, method: _OutputMethodArg | None) -> ContextManager[None]: ...
    def element(
        self,
        tag: _TagName,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        method: _OutputMethodArg | None = ...,
        **_extra: _AnyStr,
    ) -> ContextManager[None]: ...

class _AsyncIncrementalFileWriter:
    async def write_declaration(
        self,
        version: _AnyStr | None = ...,
        standalone: bool | None = ...,
        doctype: _AnyStr | None = ...,
    ): ...
    async def write_doctype(self, doctype: _AnyStr | None) -> None: ...
    async def write(
        self,
        *args: _AnyStr | _Element | None,
        with_tail: bool = ...,
        pretty_print: bool = ...,
        method: _OutputMethodArg | None = ...,
    ) -> None: ...
    async def flush(self) -> None: ...
    def method(self, method: _OutputMethodArg | None) -> AsyncContextManager[None]: ...
    def element(
        self,
        tag: _TagName,
        attrib: SupportsLaxedItems[str, _AnyStr] | None = ...,
        nsmap: _NSMapArg | None = ...,
        method: _OutputMethodArg | None = ...,
        **_extra: _AnyStr,
    ) -> AsyncContextManager[None]: ...

class xmlfile(
    AsyncContextManager[_AsyncIncrementalFileWriter],
    ContextManager[_IncrementalFileWriter],
):
    def __init__(
        self,
        output_file: _FileWriteSource,
        encoding: _AnyStr | None = ...,
        compression: int | None = ...,
        close: bool = ...,
        buffered: bool = ...,
    ) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

class htmlfile(xmlfile): ...
