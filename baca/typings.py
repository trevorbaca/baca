"""
Typings library.
"""
import typing

import abjad

IntegerList = list[int]

Indices = int | abjad.IntegerPair | IntegerList | None

Pair = tuple[typing.Any, typing.Any]

ScopeTyping = typing.Union[
    str,
    list[str],
    list[tuple[str, int]],
    list[tuple[str, object]],
    list[tuple[str, typing.List[int]]],
    list[tuple[str, typing.List[object]]],
    list[tuple[str, typing.List[typing.Tuple[int, int]]]],
    list[tuple[str, typing.Tuple[int, int]]],
    list[tuple[typing.Sequence[str], typing.Tuple[int, int]]],
    list[tuple[typing.Sequence[str], object]],
    tuple[str, int],
    tuple[str, list[int]],
    tuple[str, list[object]],
    tuple[str, list[typing.Tuple[int, int]]],
    tuple[str, typing.Tuple[int, int]],
    tuple[str, typing.Union[int, typing.Tuple[int, int]]],
    tuple[list[str], int],
    tuple[list[str], typing.List[int]],
    tuple[list[str], typing.List[object]],
    tuple[list[str], typing.List[typing.Tuple[int, int]]],
    tuple[list[str], typing.Tuple[int, int]],
]

SliceTyping = int | abjad.IntegerPair | None
