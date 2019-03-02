"""
Typing library.
"""
import abjad
import typing
from abjadext import rmakers

IntegerList = typing.List[int]

IntegerPair = typing.Tuple[int, int]

Indices = typing.Union[int, IntegerPair, IntegerList]

Number = typing.Union[int, float]

NumberPair = typing.Tuple[Number, Number]

Pair = typing.Tuple[typing.Any, typing.Any]

RhythmMakerTyping = typing.Union[
    str,
    rmakers.RhythmMaker,
    abjad.Selection,
    typing.Iterable[
        typing.Tuple[
            typing.Union[
                rmakers.RhythmMaker,
                abjad.Selection,
                ],
            abjad.Pattern,
            ],
        ],
    ]

ScopeTyping = typing.Union[
    str,
    typing.List[str],
    typing.List[typing.Tuple[str, int]],
    typing.List[typing.Tuple[str, typing.List[object]]],
    typing.List[typing.Tuple[str, typing.List[typing.Tuple[int, int]]]],
    typing.List[typing.Tuple[str, typing.Tuple[int, int]]],
    typing.List[typing.Tuple[typing.Sequence[str], typing.Tuple[int, int]]],
    typing.List[typing.Tuple[typing.Sequence[str], object]],
    typing.Tuple[str, int],
    typing.Tuple[str, typing.List[int]],
    typing.Tuple[str, typing.List[typing.Tuple[int, int]]],
    typing.Tuple[str, typing.Tuple[int, int]],
    typing.Tuple[typing.List[str], int],
    typing.Tuple[typing.List[str], typing.List[typing.Tuple[int, int]]],
    typing.Tuple[typing.List[str], typing.Tuple[int, int]],
    ]

Selector = typing.Union[str, abjad.Expression]

Slice = typing.Union[int, IntegerPair]

Strings = typing.Union[str, typing.Sequence[str]]
