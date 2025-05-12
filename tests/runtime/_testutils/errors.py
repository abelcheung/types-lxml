import pytest

#
# Shorthand for pytest.raises context manager
#

# apihelpers.pxi _utf8()
# TypeError(Argument must be bytes or unicode, got '{type(obj).__name__}')
raise_invalid_utf8_type = pytest.raises(
    TypeError, match=r"Argument must be bytes or unicode"
)

# apihelpers.pxi _encode_Filename() / _encode_FilenameUTF8()
# TypeError("Argument must be string or unicode.")
raise_invalid_filename_type = pytest.raises(
    TypeError, match=r"Argument must be string or unicode"
)

# apihelpers.pxi _documentOrRaise() / _rootNodeOrRaise()
# TypeError("Invalid input object: ...")
raise_invalid_lxml_type = pytest.raises(TypeError, match=r"Invalid input object: ")

# AttributeError("attribute '...' of '...' objects is not writable")
raise_attr_not_writable = pytest.raises(
    AttributeError, match=r"objects is not writable"
)

# AttributeError("'...' object has no attribute '...'")
# AttributeError("type object '...' has no attribute '...'")
raise_no_attribute = pytest.raises(
    AttributeError, match=r"('.+?' object|type object '.+?') has no attribute "
)

# TypeError("got an unexpected keyword argument '...'")
raise_unexpected_kwarg = pytest.raises(
    TypeError, match=r"got an unexpected keyword argument"
)

# TypeError("takes \d+ positional arguments? but \d+ was/were given")
# TypeError("takes (at most|exactly) \d+ positional argument \(\d+ given\)")
raise_wrong_pos_arg_count = pytest.raises(
    TypeError, match=r"takes (at least |at most |exactly )?\d+ positional argument"
)

raise_too_few_pos_arg = pytest.raises(
    TypeError, match=r"takes at least \d+ positional argument"
)

raise_too_many_pos_arg = pytest.raises(
    TypeError, match=r"takes at most \d+ positional argument"
)

raise_inexact_pos_arg = pytest.raises(
    TypeError, match=r"takes (exactly )?\d+ positional argument"
)

# TypeError("Argument '...' has incorrect type")
raise_wrong_arg_type = pytest.raises(
    TypeError, match=r"Argument '.+' has incorrect type"
)

# TypeError("'...' object is not iterable")
raise_non_iterable = pytest.raises(
    TypeError, match=r"(object|argument of type '.+?') is not iterable"
)

# TypeError("'...' object cannot be interpreted as an integer")
raise_non_integer = pytest.raises(
    TypeError, match="object cannot be interpreted as an integer"
)
