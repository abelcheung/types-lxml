from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

# ElementTree API is notable of canonicalizing byte / unicode input data.
# Not to be confused with typing.AnyStr which is TypeVar.
_AnyStr = Union[str, bytes]

_ListAnyStr = Union[List[str], List[bytes]]
_DictAnyStr = Union[Dict[str, str], Dict[bytes, bytes]]
_Dict_Tuple2AnyStr_Any = Union[Dict[Tuple[str, str], Any], Tuple[bytes, bytes], Any]
_NSMap = Union[Dict[Union[bytes, None], bytes], Dict[Union[str, None], str]]
_OptionalNamespace = Optional[Mapping[str, Any]]
