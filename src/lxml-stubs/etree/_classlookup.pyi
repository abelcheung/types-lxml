#
# Types stub for lxml/classlookup.pxi
#

from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import Generic, Literal, TypeVar, final, overload
from typing_extensions import disjoint_base

from .._types import (
    _AttrMapping,
    _AttrName,
    _AttrVal,
    _DefEtreeParsers,
    _ET_co,
    _NSMapArg,
    _TagName,
    _TextArg,
)
from ._element import _Comment, _Element, _Entity, _ProcessingInstruction

#
# Public element classes
#
class ElementBase(_Element):
    """The public Element class. All custom Element classes must inherit
    from this one.

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ElementBase)
    """

    TAG: _TagName
    NAMESPACE: _TextArg
    HTML: bool
    PARSER: _DefEtreeParsers[_Element]

    @final
    def __init__(
        self,
        *children: object,
        attrib: _AttrMapping | None = None,
        nsmap: _NSMapArg | None = None,
        **_extra: _AttrVal,
    ) -> None: ...
    def _init(self) -> None: ...

class CommentBase(_Comment):
    """All custom Comment classes must inherit from this one

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.CommentBase)
    """

    @final
    def __init__(self, text: _TextArg | None) -> None: ...
    def _init(self) -> None: ...

class PIBase(_ProcessingInstruction):
    """All custom Processing Instruction classes must inherit from this one.

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.PIBase)
    """

    @final
    def __init__(
        self,
        target: _TextArg,
        text: _TextArg | None = None,
    ) -> None: ...
    def _init(self) -> None: ...

class EntityBase(_Entity):
    """All custom Entity classes must inherit from this one.

    To create an XML Entity instance, use the ``Entity()`` factory.

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.EntityBase)
    """

    @final
    def __init__(self, name: _TextArg) -> None: ...
    def _init(self) -> None: ...

#
# Class lookup mechanism described in
# https://lxml.de/element_classes.html#setting-up-a-class-lookup-scheme
#

@disjoint_base
class ElementClassLookup:
    """Superclass of Element class lookups

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ElementClassLookup)
    """

@disjoint_base
class FallbackElementClassLookup(ElementClassLookup):
    """Superclass of Element class lookups with additional fallback

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.FallbackElementClassLookup)
    """

    @property
    def fallback(self) -> ElementClassLookup | None: ...
    def __init__(self, fallback: ElementClassLookup | None = None) -> None: ...
    def set_fallback(self, lookup: ElementClassLookup) -> None:
        """Sets the fallback scheme for this lookup method

        See Also
        --------
        - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.FallbackElementClassLookup.set_fallback)
        """

_Public_ET_co = TypeVar("_Public_ET_co", bound=ElementBase, covariant=True)

@disjoint_base
class ElementDefaultClassLookup(ElementClassLookup, Generic[_ET_co]):
    """Element class lookup scheme that always returns the default Element
    class.

    Annotation
    ----------
    This is only a best-effort mimicry of runtime ElementDefaultClassLookup.
    In runtime, using ElementBase itself as element class will be rejected,
    while there is no equivalent mechanism in typing to express this.

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ElementDefaultClassLookup)
    """

    @property
    def element_class(self) -> type[_Element]: ...
    @property
    def comment_class(self) -> type[_Comment]: ...
    @property
    def pi_class(self) -> type[_ProcessingInstruction]: ...
    @property
    def entity_class(self) -> type[_Entity]: ...
    @overload
    def __new__(
        cls,
        element: type[_Public_ET_co],
        comment: type[CommentBase] | None = None,
        pi: type[PIBase] | None = None,
        entity: type[EntityBase] | None = None,
    ) -> ElementDefaultClassLookup[_Public_ET_co]: ...
    @overload
    def __new__(
        cls,
        element: None = None,
        comment: type[CommentBase] | None = None,
        pi: type[PIBase] | None = None,
        entity: type[EntityBase] | None = None,
    ) -> ElementDefaultClassLookup[_Element]: ...


@disjoint_base
class AttributeBasedElementClassLookup(FallbackElementClassLookup):
    """Checks an attribute of an Element and looks up the value in a
    class dictionary.

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.AttributeBasedElementClassLookup)
    """

    def __init__(
        self,
        attribute_name: _AttrName,
        class_mapping: (
            Mapping[str, type[_Element]] | Mapping[str | None, type[_Element]]
        ),
        fallback: ElementClassLookup | None = None,
    ) -> None: ...

class ParserBasedElementClassLookup(FallbackElementClassLookup):
    """Element class lookup based on the XML parser

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ParserBasedElementClassLookup)
    """

# Though Cython has no notion of abstract method, it is giving
# enough hints that all subclasses should implement lookup method
# making it de-facto abstract method
class CustomElementClassLookup(FallbackElementClassLookup, metaclass=ABCMeta):
    """Element class lookup based on a subclass method

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.CustomElementClassLookup)
    """

    @abstractmethod
    def lookup(
        self,
        type: Literal["element", "comment", "PI", "entity"],
        doc: object,  # Internal doc object
        namespace: str | None,
        name: str | None,
    ) -> type[_Element] | None: ...

class PythonElementClassLookup(FallbackElementClassLookup, metaclass=ABCMeta):
    """Element class lookup based on a subclass method

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.PythonElementClassLookup)
    """

    @abstractmethod
    def lookup(
        self,
        doc: object,
        element: _Element,  # quasi-Element with all attributes read-only
    ) -> type[_Element] | None: ...

def set_element_class_lookup(lookup: ElementClassLookup | None = None) -> None:
    """Set the global element class lookup method

    See Also
    --------
    - [API documentation](https://lxml.de/apidoc/lxml.etree.html#lxml.etree.set_element_class_lookup)
    """
