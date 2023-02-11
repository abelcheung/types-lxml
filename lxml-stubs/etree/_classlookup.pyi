#
# Types stub for lxml/classlookup.pxi
#

from abc import ABCMeta, abstractmethod

from .._types import _ElemClsLookupArg
from . import _Comment, _Element, _Entity, _ProcessingInstruction

#
# Public element classes
#
# Special note from docstring:
# Subclasses *must not* override __init__ or
# __new__ as it is absolutely undefined when these objects will be
# created or destroyed.  All persistent state of Elements must be
# stored in the underlying XML.  If you really need to initialize
# the object after creation, you can implement an ``_init(self)``
# method that will be called directly after object creation.
#
class ElementBase(_Element):
    def _init(self) -> None: ...

class CommentBase(_Comment):
    def _init(self) -> None: ...

class PIBase(_ProcessingInstruction):
    def _init(self) -> None: ...

class EntityBase(_Entity):
    def _init(self) -> None: ...

#
# Class lookup mechanism described in
# https://lxml.de/element_classes.html#setting-up-a-class-lookup-scheme
#

class ElementClassLookup: ...

class FallbackElementClassLookup(ElementClassLookup):
    @property
    def fallback(self) -> ElementClassLookup | None: ...
    def __init__(self, fallback: ElementClassLookup | None = ...) -> None: ...
    def set_fallback(self, lookup: ElementClassLookup) -> None: ...

# Though Cython has no notion of abstract method, it is giving
# enough hints that all subclasses should implement lookup method
# making it de-facto abstract method
class CustomElementClassLookup(FallbackElementClassLookup, metaclass=ABCMeta):
    @abstractmethod
    def lookup(
        self,
        type: _ElemClsLookupArg,
        doc: str,
        namespace: str | None,
        name: str | None,
    ) -> type[_Element] | None: ...

## TODO?
# ElementDefaultClassLookup
# AttributeBasedElementClassLookup
# ParserBasedElementClassLookup
# PythonElementClassLookup
# def set_element_class_lookup()
