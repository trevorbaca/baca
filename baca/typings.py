"""
Typings library.
"""
import typing

import abjad

IntegerList = typing.List[int]

Indices = int | abjad.IntegerPair | IntegerList | None

Pair = typing.Tuple[typing.Any, typing.Any]

ScopeTyping = typing.Union[
    str,
    typing.List[str],
    typing.List[typing.Tuple[str, int]],
    typing.List[typing.Tuple[str, object]],
    typing.List[typing.Tuple[str, typing.List[int]]],
    typing.List[typing.Tuple[str, typing.List[object]]],
    typing.List[typing.Tuple[str, typing.List[typing.Tuple[int, int]]]],
    typing.List[typing.Tuple[str, typing.Tuple[int, int]]],
    typing.List[typing.Tuple[typing.Sequence[str], typing.Tuple[int, int]]],
    typing.List[typing.Tuple[typing.Sequence[str], object]],
    typing.Tuple[str, int],
    typing.Tuple[str, typing.List[int]],
    typing.Tuple[str, typing.List[object]],
    typing.Tuple[str, typing.List[typing.Tuple[int, int]]],
    typing.Tuple[str, typing.Tuple[int, int]],
    typing.Tuple[str, typing.Union[int, typing.Tuple[int, int]]],
    typing.Tuple[typing.List[str], int],
    typing.Tuple[typing.List[str], typing.List[int]],
    typing.Tuple[typing.List[str], typing.List[object]],
    typing.Tuple[typing.List[str], typing.List[typing.Tuple[int, int]]],
    typing.Tuple[typing.List[str], typing.Tuple[int, int]],
]

SliceTyping = int | abjad.IntegerPair | None
