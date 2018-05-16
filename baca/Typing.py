import abjad
import typing

Number = typing.Union[int, float]

NumberPair = typing.Tuple[Number, Number]

Selector = typing.Union[str, abjad.Expression]

Tweak = typing.Tuple[str, typing.Any]
