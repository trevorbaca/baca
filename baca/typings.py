import abjad
import typing
from abjadext import rmakers

IntegerPair = typing.Tuple[int, int]

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
