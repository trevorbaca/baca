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

Selector = typing.Union[str, abjad.Expression]

Slice = typing.Union[int, IntegerPair, None]
