# 2026.01.01

## Breaking or important changes

- Supports facebook's `pyrefly` type checker ([#106](https://github.com/abelcheung/types-lxml/issues/106), [#107](https://github.com/abelcheung/types-lxml/issues/107))
- Initial mypy plugin that mimics `XMLParser.set_element_class_lookup()` behavior

## Bug fixes

- Setting `HtmlElement.label` to `None` is disallowed
- Basic stub works with Python 3.9 again; `TypeAlias` usage caused requirement of Python 3.10

## Test related

- Migrate `HtmlMixin` properties and `.set()` method tests to runtime

## Other changes

- `types-lxml[dev]` extras is installable again
- It is possible to verify all release files indeed originate from GitHub and not altered elsewhere using GitHub CLI

# 2025.11.25

## Breaking and Important changes
- Declare Python 3.14 support
- [PEP 800](https://peps.python.org/pep-0800/) support (`@disjoint_base`)
  - As a result, remove Python 3.8 support and require newest type checkers / `typing_extensions`

## Features
- Additional `libxml2` error constants from `lxml` 6.0.1+
- Use `io.Reader` and `io.Writer` from Python 3.14, replacing `SupportsRead` and `SupportsWrite` from `typeshed`.

## Bug fix
- ([#100](https://github.com/abelcheung/types-lxml/issues/100), thanks to @BeatButton) Replace `__init__()` with `__new__()` for all `XMLParser` subclasses, overriding `XMLParser.__new__()`. Due to `CustomTargetParser` change in [fdf2a8117562c1b07309239554bb36d021f0b207](https://github.com/abelcheung/types-lxml/commit/fdf2a8117562c1b07309239554bb36d021f0b207), `XMLParser` uses `__new__()` instead of `__init__()`. That commit brought in undesirable effect: `pyright` treats all `XMLParser` / `HTMLParser` subclasses instances as base class instances.
- Add `@type_check_only` to some protocols and generics

## Refactor
- Drop deprecated collection-related typing aliases
- Replace some `LiteralString` with `Literal` constants when value is fixed
- Drop unused type ignore comments because we are not supporting wide range of type checker versions now

## Minor changes
- No more globally ignore mypy `assignment` error code in tests
- Add `HTMLParser.__init__()` and `XMLParser.__init__()` to allowlist, due to [#100](https://github.com/abelcheung/types-lxml/issues/100)


# 2025.08.25

## Breaking or important changes

- Brings in full `lxml` 6.0.x support. Additional exported constants were already present in earlier `types-lxml` release, here are the remaining features:
  - `xmlfile.write()` supports writing `CDATA` object directly
  - ([#94](https://github.com/abelcheung/types-lxml/issues/94), thanks to @udifuchs) `Element()` and `ElementTree()` used to be factory functions to generate `_Element` and `_ElementTree` correspondingly, but now become virtual superclasses themselves
- No more tested against lxml 4.9.x. Doesn't mean it will break immediately, but will not have any guarantee that `types-lxml` completely matches 4.9.x API over time.

## Features

- Also test against lxml 5.4 and newest 5.3.x
- ([#92](https://github.com/abelcheung/types-lxml/issues/92), thanks to @macro1) Apply [`mypy.stubtest`](https://mypy.readthedocs.io/en/stable/stubtest.html) check to help guarantee stub implementation doesn't deviate too much from runtime signatures and types, except intentional ones. Helps finding many of the bug fixes below.
- Compatible with `mypy` 1.16+ and `pyright` 1.1.399+
- ([#86](https://github.com/abelcheung/types-lxml/issues/86)) Revive [custom target parser](https://github.com/abelcheung/types-lxml/wiki/Custom-target-parser) support (stub-only `ParserTarget` as target object, and `CustomTargetParser` as stub-only variant of `XMLParser`)
  - Functions involved: `fromstring()`, `parse()`, `_ElementTree.parse()`, `ElementTree()`, `fromstringlist()`, `HTML()`, `XML()`
  - Params of all target object methods are positional
  - attribute is a dict in target object `.start()` method
  - Leave the capability of creating custom target parser to only `XMLParser` and `HTMLParser`, and drop `target=` param from all parser subclasses (such as `lxml.html` ones)
  - `C14NWriterTarget` inherits from `ParserTarget`

## Bug Fixes

- Sync or add `__all__` in various submodules

### Fixes for `lxml.etree`
- ([#85](https://github.com/abelcheung/types-lxml/issues/85), thanks to @BrandonStudio) `cleanup_namespaces()` shouldn't warn without `keep_ns_prefixes` arg
- Allow specifying default value of `output_parent` arg for `XSLTExtension.apply_template()` and `.process_children()`
- Mark `_Attrib` as final
- Add missing `XMLSyntaxAssertionError.__init__()`
- `set_default_parser()` arg missing default value
- `strip_elements()` `with_tail` arg should be keyword-only
- Use original param name in tag cleanup functions
- Strip unnecessary arguments in `XSLTExtension` overloads
- Give users a rough idea about `XSLTExtension` method arguments, such as using `_Element` to approximately represent `_ReadOnlyElementProxy`. Avoids creating even more stub-only classes and requiring user to poke into them

### Fixes for `lxml.html`
- `FormElement._name` is a method, not property

### Fixes for `lxml.isoschematron`
- some Schematron variables are Literal constants

### Fixes for `lxml.objectify`
- `enable_recursive_str()` arg missing default value
- `parse()` file parameter name was wrong

## Minor changes

- Trim down `canonicalize()`, `etree.tostring()` and `Extension()` overloads to avoid confusion
- Implement `objectify.NumberElement` after all, in rare case where somebody wants to implement new type of number related to `DataElement`
- Move `NumberElement._setValueParser()` to subclasses
- ([#71](https://github.com/abelcheung/types-lxml/issues/71)) Remove last traces of `_AnyStr`
- Reorder `_ElementTree.write()` overloads, with the most generic overload presented first for UX
- Fix `XMLParser` and `HTMLParser` API doc links
- Better docstring and warning for `C14NWriterTarget`
- Drop unused `_HtmlElemParser` alias


# 2025.03.30

## Features

- ([#82](https://github.com/abelcheung/types-lxml/issues/82)) Add buffer type support for upcoming lxml 6.0.
- `HtmlElement.text_content()` result will become plain `str` since lxml 6.0. This change shouldn't break much compatibility for users of previous lxml versions.
- Warn user about `str` input and `guess_charset` combo bug in `html.html5parser` functions
- Warn user about incorrect usage of specifying single element as `.extend()` argument
- lxml 6.0 exports `LIBXML_COMPILED_FEATURES` constant

## Bug fixes

- ([#84](https://github.com/abelcheung/types-lxml/issues/84)) Tag selector supports iterator but not `bytearray`
- A few combinations of `QName` construction argument were actually disallowed; second argument can't be `QName` or `_Element` if first argument is non-empty
- Multiple issues for `Resolver` class
    - Don't annotate opaque internal context object
    - Drop `_ResolverRegistry.resolve()` which can't possibly appear in user land code
    - Missing default value for `Resolver.resolve_file()` keyword arguments
    - `Resolver.resolve()` arguments can be `None`
- Drop unused keyword arguments from `iterparse()` html mode overload
- `namespaces` arg of `.xpath()` method accepts tuple form. Change for `XPath` classes already done earlier.
- Confine the type of public element (subclass of `ElementBase`) class attributes
- `_Element.findtext()` didn't allow default argument in certain overload form
- `RelaxNG.from_rnc_string()` `base_url` argument accepts `bytes`
- `html.html5parser` `guess_charset` bug revisited
    - `parse()` is not affected as it always open files/URL in binary mode
    - For other functions, even `guess_charset=False` triggers the bug
- Some `html5parser.HTMLParser` initialisation arguments should be keyword only
- Corrected import of `typing.Never` in `html` module and `html.html5parser` submodule
- `.extend()` and `__setitem__()` of `_Element` and `HtmlElement` support iterator as value
- `_Element.index()` had wrong parameter name
- Continued verification of properties and arguments supporting `bytearray`:
    - `_Element` `.text` and `.tail` properties
    - Content-only elements
    - `XPath` input expression
    - `_IDDict` mixin arguments
    - `xmlfile.write*()` methods and `encoding` argument

## Minor changes

- Drop `_ElemClsLookupArg` alias, which is almost unused
- Rename `_StrictNSMap` to more aptly named `_StrOnlyNSMap`
- Don't include superclass attributes in `ParseError` definition
- Continue getting rid of `_AnyStr` in most places
- Mark constants as `Final`

## Tests

- Migrate following tests to property based runtime testing:
  - All basic validators: `DTD`, `RelaxNG`, `ISO Schematron` (`XMLSchema` done in earlier release)
  - All existing `_Element` method / property tests and content-only elements
  - `html.html5parser` submodule
  - `XMLID()` and friends
  - `QName`
- For all negative tests on properties or arguments bombarded with random objects, also add iterables of correct objects to the list, to make sure iterables of correct argument or value would become incorrect arguments.

## Documentation

- Fill in docstring for all `_Element` properties and methods


# 2025.03.04

## Features and breaking changes

- Depends on `beautifulsoup4` itself because version 4.13 has bundled inline annotation. Dropping `types-beautifulsoup4` dependency as result.
- Multi subclass patch includes change in `CSSSelector` result
- Implement `ErrorTypes` constants as enum

## Bug fixes

- Additional `type: ignore`s that improve compatibility with older versions of `mypy` and `pyright`
- For `soupparser` submodule input arguments, copy definition from `beautifulsoup4` code directly
- `html.fragment_fromstring` `create_parent` argument can be string ([#83](https://github.com/abelcheung/types-lxml/issues/83), thanks to @sciyoshi)
- `XPath` `namespaces` argument can accept namespace tuples
- Fixes compatibility with mypy 1.14+
- `bytes` not allowed as `html.diff.htmldiff()` argument
- Parser `encoding` arguments do support `bytearray`
- `_ListErrorLog.filter_from_level()` supports real numbers

## Minor changes and tests

- Migrate `beautifulsoup` and `ErrorLog` tests to property based
- Migrate `cssselect` and `XMLSchema` tests to runtime ones
- Add mocked HTTP response to file input fixture; introduces `urllib3` and `pook` as test dependency


# 2025.02.24

## Features and breaking changes

- Add [`basedpyright`](https://github.com/DetachHead/basedpyright) type checker support

- Incorporate changes from `lxml` 5.3.1 and (pending) 6.0
    - More `html.builder` shorthands
    - `libxml` feature constants
    - `etree.DTD(external_id=...)` support `str` now
    - Deprecate some `Memdebug` methods

## Bug fixes

- `html.submit_form()` always return `HTTPResponse` for default handler

- Instance attributes are converted to properties because they are not deletable:
    - `html.SelectElement.multiple`
    - `html.InputElement.type`

- More function arguments supports `bytearray`:
    - `register_namespace()`
    - `inclusive_ns_prefixes` parameter of `etree.tostring()`

## Minor changes

- Add docstring for some `etree` module function `overload`s
- Drop `_AnyStr` from `etree` module level functions

# 2024.12.13

## Breaking changes and features
- `bytearray` accepted as tag names, attribute names and attribute values
  - Related change: create `_TextArg` type alias to slowly replace existing `_AnyStr` ([#71](https://github.com/abelcheung/types-lxml/issues/71))
- Warn IDE users via `warnings.deprecated` about exception upon certain argument combinations in HTML link functions

## Bug fixes
- Property deleter missing for HTML elements ([#73](https://github.com/abelcheung/types-lxml/issues/73))
- `etree.strip_attributes()` support `bytes` and `QName` as input
- Completion of [#64](https://github.com/abelcheung/types-lxml/issues/64) for remaining known cases
- Corrected link replacement function return type in `html.rewrite_links()`
- `etree.canonicalize()` shouldn't accept `bytes` as input

## Tests related
- Use [`hypothesis`](https://hypothesis.readthedocs.io/) for extensive tests on function arguments, currently used in `_Attrib` and HTML link function tests ([#75](https://github.com/abelcheung/types-lxml/issues/75))
- `reveal_type()` injector has been split into [its own project](https://github.com/abelcheung/pytest-revealtype-injector) and pulled via dependency

## Internal changes
- Folder structure changes for the whole repository ([#70](https://github.com/abelcheung/types-lxml/issues/70))
- Remove `_HANDLE_FAILURES` type alias and show values directly to users
- Rename type-only protocol `SupportsLaxedItems` to `SupportsLaxItems`


# 2024.11.08

## Breaking and important changes

![image showing deprecation warning](https://github.com/user-attachments/assets/6ab30a54-60e7-4e34-932a-2ac2e253c669)

- `pyright` users (and IDE that can make use of `pyright`) will see warning if a single string is supplied where collection of string is expected (`tuple`, `set`, `list` etc). In terms of typing, a single `str` itself is valid as a `Sequence`, so type checkers normally would not raise alarm when using `str` in such function parameters, but can induce unexpected runtime behavior. ([#64](https://github.com/abelcheung/types-lxml/issues/64))
  - `_ElementTree.write()`, `etree.fromstringlist()`, `etree.tostring()`, `html.soupparser.fromstring()`, `html.soupparser.parse()`
- It is possible to verify release files indeed come from GitHub and not maliciously altered. See [Release file attestation](README.md#release-file-attestation) for detail.
- Runtime tests support comparing with `mypy` results, therefore officially making static stub tests obsolete


## Bug fixes

- Element tag names, attribute names and attribute values support `bytearray`. This is discovered via `hypothesis` testing, which is intended to be utilized in next release
- Compatibility with `pyright ⩾ 1.1.378`, which imposes additional overload warning for `etree.iterparse()`
- Use relative import in `lxml.ElementInclude`, otherwise `mypy` triggers `--install-type` behavior.
- `ObjectifiedElement` `__getitem()__` and `__setitem()__` should accept `str` as key, which behaves mostly like `__getattr__()` and `__setattr__()`. That means, `elem["foo"]` is equivalent to `elem.foo` for non-repeating subelements.

### fixes for etree submodule

- `_Element.tag` property is not just a `str`. It is `str` after initial document or string parsing, but can be set manually to any type supported by tag name and returns the same object.
- When `QName` is initialized with first argument set to `None`, `_Element` can be used as second argument (which is promoted to first argument in implementation)
- Relax single argument usage in `_Element.iter*()` method family, doesn't need `tag=` keyword when argument is `None`
- `FunctionNamespace()` should generate an `_XPathFunctionNamespaceRegistry` object, not its superclass
- For [decorator usage](https://lxml.de/element_classes.html#implementing-namespaces-1) of `_XPathFunctionNamespaceRegistry` and `_ClassNamespaceRegistry`, decorator signature included an extraneous argument, though it doesn't affect any existing correct usage.
- `indent()` first parameter has wrong name

### fixes for html submodule

- `soupparser.parse()` should accept `pathlib.Path` object as input
- `.value` property of `SelectElement` can't be set to `bytes`
- `.action` property of `FormElement` can have a value of `None`, and can be set to `None`. They have different meanings though.

## Small and internal changes

- Declare python 3.13 support and perform CI tests.
- Separation of `pyright` and `mypy` ignore comments: in previous releases `# type: ignore[code]` was enabled in `pyright` settings. Now it only uses `# pyright: ignore[code]` so `mypy` comment won't affect `pyright` behavior.
- Add `._name` property to `html.FormElement` for form name
- Eliminate `typing.TypeAlias` usage ([declared obsolete](https://docs.python.org/3/library/typing.html#deprecation-timeline-of-major-features), and we can do without it)

## Test related changes

- Stub tests migration to runtime:
    - Most of remaining `etree._Element` methods, now only `.makeelement()` and `.xpath()` left in stub test
- Runtime test additions:
  - `ElementNamespaceClassLookup()`
- `tox` config migrated to `pyproject.toml`, thus requiring `tox ⩾ 4.22`
- Runtime tests are now executed within `test-rt` folder due to [python/mypy#8400](https://github.com/python/mypy/issues/8400)
- Some tests need to be performed conditionally when multi-subclass patch is applied
- Some tests or syntaxes need to be turned off to cope with `mypy` deficiencies
- Usage of [Rust-based `uv`](https://docs.astral.sh/uv/) as well as [related `tox` plugin](https://github.com/tox-dev/tox-uv) to speed up test environment recreation
- Don't force users installing [`tox-gh-actions`](https://github.com/ymyzk/tox-gh-actions) when checkout out repository, it is only useful for GitHub workflows

## Docstring additions

- `etree` submodule: `parse()`, `fromstringlist()`, `tostring()`, `indent()`, `iselement()`, `adopt_external_document()`, `DocInfo` properties, `QName`, `CData`, some exception classes
- `html.soupparser` submodule: `fromstring()`, `parse()`, `convert_tree()`


# 2024.09.16

## Bug fix

- Namespace argument in Elementpath methods should allow `None` ([#60](https://github.com/abelcheung/types-lxml/issues/60) thanks to @cukiernick)

## Internal changes

- Perform runtime tests against `lxml 5.3`

# 2024.08.07

## Breaking changes

- Multiple builds available, with the alternative build enhancing multiple XML subclassing scenario. See [relevant README section](https://github.com/abelcheung/types-lxml#choosing-the-build) for detail. Thanks to @scanny for the driving force behind [#51](https://github.com/abelcheung/types-lxml/issues/51).
- `Mypy` 1.11 required, which introduced backward incompatible `@typing.overload` changes.
- `lxml.html.clean` stub depreated, `lxml 5.2.0` completely removes the submodule due to multiple security issues. Corresponding code and type definitions are split into a [new independent repo](https://github.com/fedora-python/lxml_html_clean).

## Features

- ([#56](https://github.com/abelcheung/types-lxml/issues/56)) Replace `typing.TypeGuard` with `typing.TypeIs`
- Use [callback protocol](https://github.com/python/typing/discussions/1432) for more precise element and `ElementMaker` factory function typing
- `lxml.etree.ICONV_COMPILED_VERSION` exported since `5.2.2`
- Special handling for `ObjectifiedElement` and `HTMLElement` in `lxml.cssselect.CSSSelector` and various `cssselect()` methods
- `html.builder` shorthands return more precise element type for certain HTML elements. For example, `html.builder.LABEL()`, corresponding to `<LABEL>` tag, yields `LabelElement`.
- More precise `etree.Extension()` annotation depending on supplied namespace
- Stricter namespace argument type in `_Element` ElementPath methods
- For `lxml.builder.ElementMaker` class:
  - Provide better hint in `__call__()` argument
  - Accepts namespace tuple in `nsmap` argument
  - Export private properties
- For `lxml.sax` module:
  - Export private properties in various classes
  - Explicitly list all inherited methods in `ElementTreeContentHandler` class, as method arguments names are different from superclass ones
- Alert `etree.HTMLParser` users to remove deprecated `strip_cdata` argument

## Bug fix and small changes

- Some `_Element` related input arguments fixed to use `typing.Sequence` instead of `Interable`, as `_Element` is already an `Iterable` itself. Supplying `_Element` where a proper `Iterable` is expected would cause problem.
- Similar situation arises for `str` or `byte` in tag selector argument; use `typing.Collection` to alert user more clearly.
- `None` can't be used as `etree.strip_*()` argument
- Some `etree.DocInfo` read-only properties can't be `None`
- Fix `etree.Resolver` method return types
- Avoid exception raising arg combinations in `html.html5parser.HTMLParser`

## Internal changes

- The usual static stub to runtime test migration:
  - Part of basic `_Element` tests and its `find*()` methods
  - More extensive `_Attrib` tests
- Use [`ruff`](https://docs.astral.sh/ruff/) to replace [`black`](https://black.readthedocs.io/en/stable/) and [`isort`](https://pycqa.github.io/isort/) as code formatter
- Migrate stub tests to support `pytest-mypy-plugins ⩾ 2.0`
- Use [`pdm-backend`](https://backend.pdm-project.org/) as build backend due to its more versatile versioning support

# 2024.04.14

## Breaking changes

- `Mypy` 1.9 is required, dropping 1.5 support. 1.6 - 1.8 was never supported.
- `lxml.ElementInclude` completely reworked

## Features

- [PEP 696](https://peps.python.org/pep-0696/) support, simplifying usage of some subscripted types ([#42](https://github.com/abelcheung/types-lxml/issues/42))
  - As a convenient side effect, `lxml.html` parser constructor signatures can be removed
- All annotations do provide default values in their signatures now instead of `...`

## Bug fix and small changes

- Type of `_Comment.text` property (and those of similar elements) is always `str` ([#46](https://github.com/abelcheung/types-lxml/issues/46), thanks to @eemeli)
- Tag selector argument in element iterator methods should support keyword with a single tag ([#45](https://github.com/abelcheung/types-lxml/issues/45), thanks to @eemeli)
- `html.fragments_fromstring()` should receive same fix as `html.html5parser.fragments_fromstring()` do ([#43](https://github.com/abelcheung/types-lxml/issues/43), thanks to @Wuestengecko)
- `@overload` for `etree.SubElement()` on handling of `HtmlElement` and `ObjectifiedElement`
- Some exported constants were missing from `lxml.ElementInclude` stub
- `html.soupparser` module functions return type depends on `makeelement` argument
- Keyword arguments in `html.soupparser` module functions are explicitly listed now (instead of generic `**kwargs` before)
- The 2 arguments in `html.diff.html_annotate()` should align their annotation types
- `html.submit_form()` return type depends on the result of `open_http` function argument
- Add missing exported variable for `lxml.isoschematron`
- Uppercase variants of output method arguments ("HTML", "TEXT", "XML") were dropped

## Internal changes

- Usual runtime test additions: `lxml.html.soupparser`, `lxml.ElementInclude`, various exported constants
- Runtime tests also do test against lxml 5.2

# 2024.03.27

## Breaking change

- Requires `cssselect ⩾ 1.2` for annotation in `lxml.cssselect`, since `cssselect` is now inline annotated.

## Bug fix and small changes

- Compatibility with `pyright ⩾ 1.1.353`
- In `etree.clean_*` functions, first argument (the Element or ElementTree to be processed) must be strictly positional
- `etree._LogEntry.filename` property is never empty, as it uses the value `<string>` as fallback
- `etree._BaseErrorLog.receive()` argument name was wrong
- Self brewed `SupportsReadClose` protocol dropped, replacing with more standardized `SupportsRead`
- `html.html5parser.parse()` should support data stream as input
- `html.html5parser.fragments_fromstring()` return type is dependent on `no_leading_text` argument
- `encoding` arguments in various methods / functions used to only support ASCII and UTF-8 as byte encodings, now the restriction is lifted
- Place some `typing` usage under python version check (`if sys.version_info >= (3, x)`)
- `etree.PyErrorLog` constructor shouldn't accept 2 logger arguments simultaneously
- `etree.PyErrorLog.level_map` property reverted to vanilla type (`int`) instead of our fake `enum`

## Internal changes

- Some runtime tests are lxml version dependent ([#34](https://github.com/abelcheung/types-lxml/issues/34), thanks to @fabaff)
- Adds stub check for `_Element`, `_Comment` and `_ElementTree` ([#33](https://github.com/abelcheung/types-lxml/issues/33), thanks to @udifuchs)
- Following stub tests migrated to runtime: `_Attrib`, `_ErrorLog` and friends, `html5lib`

# 2024.02.09

## Bug fix and small changes

- Add back `HtmlProcessingInstruction` element ([#28](https://github.com/abelcheung/types-lxml/issues/28), thanks to @eliotwrobson)
- Silence `pyright` ⩾ 1.1.345 warning on overriding read-write property with read-only one (`ObjectifyElement.text`)

## Documentation

- `mypy` ⩾ 1.6 does not support PEP702, thus shouldn't be used with `types-lxml`

## Internal changes

- Stub test suite uses `mypy` 1.5.x now

# 2023.10.21

## Bug Fix

- Types for emitted events and values in `iterparse()` were not optimal (issue [#19](https://github.com/abelcheung/types-lxml/issues/19), thanks to @Daverball)
- Most `html` link and clean functions should be unable to process `ElementTree`, except `Cleaner.clean_html()`

## Feature

- Completed following modules, thus _really_ having `lxml` fully covered (sans a few submodules that will never be implemented):
	- `lxml.html.diff`
	- `lxml.ElementInclude`
- Declares support for Python 3.12
- Update for upcoming `lxml` 5.0
	- `Schematron` constructor arguments
	- Some obsolete functions removed

## Internal change

- Start implementing runtime type checks and compare with static type checker results, utilizing [`typeguard`](https://github.com/agronholm/typeguard) and [`pyright`](https://github.com/microsoft/pyright)
- Use [`setuptools_scm`](https://github.com/pypa/setuptools_scm) in place of [`pdm-backend`](https://github.com/pdm-project/pdm-backend) as package build backend

# 2023.3.28

The list of changes [since last release](https://github.com/abelcheung/types-lxml/compare/2023.02.11...2023.3.28) is huge, be it visible by users or not.

## Breaking changes

- Class inheritance of `html.HtmlComment` and friends have changed to deviate from source code. Now they are 'thought' to inherit from `html.HtmlElement` within stubs, like the XML `etree._Element` counterpart. [Refer to wiki document](https://github.com/abelcheung/types-lxml/wiki/Element-inheritance-change) on how and why this change is done.
- Shelved custom parser target support (custom parser target is used when initiating XML / HTML parsers with `target=` argument), as current python typing system is deemed insufficient to get it working without plugins.
- Stub package only depends on other stub packages, following behavior of typeshed distributed stubs. This means `lxml` is no longer pulled in when installing `types-lxml`.
- `etree.SmartStr` reverted back to [its original class name](https://github.com/abelcheung/types-lxml/wiki/Smart-string-usage)
- `etree._ErrorLog` is now made a function that generates `etree._ListErrorLog` (despite the fact that it is a class in source code), according to actual created instance type

## Significant changes / completion

- Completed following submodules and parts, thus removing [the partial status](https://peps.python.org/pep-0561/#partial-stub-packages) of `types-lxml` package:
  - `lxml.etree` proper:
    - [x] XSLT related classes / functions
    - [x] XML:ID support
    - [x] External [document and URI resolving](https://lxml.de/resolvers.html)
    - [x] XInclude support
    - [x] XPath and XSLT [extension function registry](https://lxml.de/extensions.html)
    - [x] Error log and reporting, along with numerous bug fixes
    - [x] `etree.iterparse` and `etree.iterwalk`
    - [x] Various `ElementClassLookup` types
  - [x] `lxml.objectify`
    - [x] Includes all `DataElement` subtypes and type annotation support
  - [x] `lxml.isoschematron`
- When subclassing XML elements, now most of its methods can be inherited without overriding output element type.

## Smaller changes

- More extensive usage of Python 3.9-3.11 typing features, this is possible since `types-lxml` is external stub package and doesn't affect source code. Such as:
  - Marking string constants as `LiteralString` ([PEP 675](https://peps.python.org/pep-0675/))
  - Make type aliases more explicit ([PEP 613](https://peps.python.org/pep-0613/))
  - Convenient `Self` when declaring methods ([PEP 673](https://peps.python.org/pep-0673/))
- Both `mypy` and `pyright` type checkers have strict mode turned on when verifying stub source
- `_Element.sourceline` property becomes read-only
- Re-added most deprecated methods in various places, with help from provisional [PEP 702](https://peps.python.org/pep-0702/) support (`@deprecated`) in `pyright`
- Incorporate more docstring from official `lxml` classes, in case IDEs can display them in user interface.
- Force `_XPathEvaluatorBase` subclasses to make `__call__` available, by explicitly declaring it as abstract method within `_XPathEvaluatorBase`
- Removal of `http.open_http_urllib`, which is only intended as a fallback callback function for `html.submit_form()` without user intervention
- `libxml2` error constants become integer `enum` in stub
- Warn userland usage of dummy `etree.PyErrorLog.copy()`, because it is only intended for smoother internal `lxml` error handling.

## Bug fixes

- File reading source (used in `file=` argument in `parse()` and friends) requirement relaxed
- `html.(X)HtmlParser` `__init__` was missing some arguments
- Convert `iter*` methods of Elements and some tag cleanup functions into `@overload`, to better reflect its original intended arguments usage
- `etree.ElementBase` and similar public base element classes lacked `__init__`
- Setting of `etree.DocInfo` text properties now accepts `bytes`
- `name=` argument of `html.HtmlElementClassLookup()` doesn't accept `None`
- Concerning `_Comment`, `_Entity`, `_ProcessingInstruction`, and their subclasses
  - `.tag` attribute now returns correct value (the basic etree element factory function)
  - Users will be warned if they use these elements like normal XML `_Element` do, such as treating them as parent elements and insert children element into them

# 2023.02.11

## Feature

- Add types for [XML canonicalization function/class](https://lxml.de/api.html#serialisation) and [incremental generation context managers](https://lxml.de/api.html#incremental-xml-generation)

# 2022.11.8

## Fixes

- ([#5](https://github.com/abelcheung/types-lxml/issues/5), thanks to @f-ohler) Add `etree.indent()`
- ([#6](https://github.com/abelcheung/types-lxml/issues/6), thanks to @wRAR) Fix signature of `_Attrib.pop()`
- ([#7](https://github.com/abelcheung/types-lxml/issues/7), thanks to @wRAR) Fix signature of `etree.fromstring()`
- Fix signature of `objectify.fromstring()`

# 2022.4.10

This is the second release of `types-lxml`. Followings are enhancements on top of `lxml-stubs` 0.4.0:

- All previous contributions reviewed and made coherent (contributions came from so many people)
- Implemented stub for following submodules:
  - `lxml.builder`
  - `lxml.sax`
  - `lxml.html.builder`
  - `lxml.html.clean`
  - `lxml.html.soupparser` (adapter for [BeautifulSoup 4](https://beautiful-soup-4.readthedocs.io/en/latest/))
  - `lxml.html.html5parser` (adapter for [html5lib](https://github.com/html5lib/html5lib-python))
- Annotations for lots of classes and methods implemented too, please browse [commit log](https://github.com/abelcheung/types-lxml/commits/main) for detail, or [project page] for future plans and progress
  - In particular, annotations for `lxml.etree.DTD` and `lxml.etree.RelaxNG` classes are complete in this release
- `Pyright` support (guarantees error-free under basic checking mode)
- Extensively expanded test cases

There are still [some missing puzzle pieces](https://github.com/abelcheung/types-lxml/projects/1) before whole annotation package can be deemed complete and escape its `partial` status.

# 2022.4.1

First release to stand in its own right. There are still [some missing puzzle pieces](https://github.com/abelcheung/types-lxml/projects/1) before whole annotation package can be deemed complete and escape its `partial` status. Followings are enhancements done so far:

- All previous contributions reviewed and made coherent (contributions came from so many people)
- Pyright support (not the test cases though, which are mypy checkable only)
- Extensively expanded test cases
- Implemented stub for following submodules:
  - `lxml.builder`
  - `lxml.sax`
  - `lxml.html.builder`
  - `lxml.html.clean`
  - `lxml.html.soupparser` (adapter for BeautifulSoup)
