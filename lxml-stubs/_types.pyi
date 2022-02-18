from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

# ElementTree API is notable of canonicalizing byte / unicode input data.
# Not to be confused with typing.AnyStr which is TypeVar.
_AnyStr = Union[str, bytes]

_ListAnyStr = Union[List[str], List[bytes]]
_DictAnyStr = Union[Dict[str, str], Dict[bytes, bytes]]
_Dict_Tuple2AnyStr_Any = Union[Dict[Tuple[str, str], Any], Tuple[bytes, bytes], Any]

# See https://github.com/python/typing/pull/273
# Due to Mapping having invariant key types, Mapping[Union[A, B], ...]
# would fail to validate against either Mapping[A, ...] or Mapping[B, ...]
# Try to settle for simpler solution, assuming users would not use byte
# string as namespace prefix.
NSMapArg = Optional[
    Union[
        Mapping[None, _AnyStr],
        Mapping[str, _AnyStr],
        Mapping[Optional[str], _AnyStr],
    ]
]
NonDefaultNSMapArg = Optional[Mapping[str, _AnyStr]]
