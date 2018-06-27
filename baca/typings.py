import abjad
import typing
from abjadext import rmakers
from .DivisionMaker import DivisionMaker
from .FlattenDivisionCallback import FlattenDivisionCallback
from .FuseByCountsDivisionCallback import FuseByCountsDivisionCallback
from .PartitionDivisionCallback import PartitionDivisionCallback
from .SplitByDurationsDivisionCallback import SplitByDurationsDivisionCallback
from .SplitByRoundedRatiosDivisionCallback import \
    SplitByRoundedRatiosDivisionCallback

division_maker_type = (
    DivisionMaker,
    FlattenDivisionCallback,
    FuseByCountsDivisionCallback,
    PartitionDivisionCallback,
    SplitByDurationsDivisionCallback,
    SplitByRoundedRatiosDivisionCallback,
    )

DivisionMakerTyping = typing.Union[
    DivisionMaker,
    FlattenDivisionCallback,
    FuseByCountsDivisionCallback,
    PartitionDivisionCallback,
    SplitByDurationsDivisionCallback,
    SplitByRoundedRatiosDivisionCallback,
    ]

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
