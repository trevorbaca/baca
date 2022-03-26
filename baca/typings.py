"""
Typings library.
"""
import typing

import abjad

IntegerList: typing.TypeAlias = list[int]

IndexedTweak: typing.TypeAlias = typing.Union[abjad.Tweak, tuple[abjad.Tweak, int]]

Indices: typing.TypeAlias = int | abjad.IntegerPair | IntegerList | None

Pair: typing.TypeAlias = tuple[typing.Any, typing.Any]

ScopeTyping: typing.TypeAlias = typing.Union[
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

SliceTyping: typing.TypeAlias = int | abjad.IntegerPair | None
