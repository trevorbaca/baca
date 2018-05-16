import abjad
import collections
import typing
from .Typing import Number


class SystemSpecifier(abjad.AbjadObject):
    r"""System specifier.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_distances',
        '_measure',
        '_y_offset',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        distances: typing.Iterable[Number] = None,
        measure: int = None,
        y_offset: Number = None,
        ) -> None:
        distances_: typing.Optional[typing.List[Number]] = None
        if distances is not None:
            assert isinstance(distances, collections.Iterable), repr(distances)
            for distance in distances:
                assert isinstance(distance, (int, float)), repr(distance)
            distances_ = list(distances)
        else:
            distances_ = None
        self._distances = distances_
        if measure is not None:
            assert isinstance(measure, int), repr(measure)
        self._measure = measure
        if y_offset is not None:
            assert isinstance(y_offset, (int, float)), repr(y_offset)
        self._y_offset = y_offset

    ### PUBLIC PROPERTIES ###

    @property
    def distances(self) -> typing.Optional[typing.List[Number]]:
        r"""Gets distances.
        """
        return self._distances

    @property
    def measure(self) -> typing.Optional[int]:
        r"""Gets start measure.
        """
        return self._measure

    @property
    def y_offset(self) -> typing.Optional[Number]:
        r"""Gets Y-offset.
        """
        return self._y_offset
