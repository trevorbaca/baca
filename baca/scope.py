import dataclasses
import typing

import abjad

from . import typings as _typings


# TODO: frozen=True
@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Scope:
    """
    Scope.

    ..  container:: example

        >>> scope = baca.Scope(
        ...     measures=(1, 9),
        ...     voice_name="ViolinMusicVoice",
        ... )
        >>> scope
        Scope(measures=(1, 9), voice_name='ViolinMusicVoice')

    """

    # TODO: reverse order of parameters; make voice_name mandatory

    measures: _typings.Slice = (1, -1)
    voice_name: str | None = None

    def __post_init__(self):
        if isinstance(self.measures, int):
            self.measures = (self.measures, self.measures)
        assert isinstance(self.measures, list | tuple), repr(self.measures)
        assert len(self.measures) == 2, repr(self.measures)
        start, stop = self.measures
        assert isinstance(start, int), repr(start)
        assert start != 0, repr(start)
        assert isinstance(stop, int), repr(stop)
        assert stop != 0, repr(stop)
        assert isinstance(self.voice_name, str), repr(self.voice_name)


# TODO: frozen=True
@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class TimelineScope:
    """
    Timeline scope.

    ..  container:: example

        >>> scope = baca.timeline([
        ...     ("PianoMusicVoice", (5, 9)),
        ...     ("ClarinetMusicVoice", (7, 12)),
        ...     ("ViolinMusicVoice", (8, 12)),
        ...     ("OboeMusicVoice", (9, 12)),
        ... ])

        >>> for _ in scope.scopes: _
        Scope(measures=(5, 9), voice_name='PianoMusicVoice')
        Scope(measures=(7, 12), voice_name='ClarinetMusicVoice')
        Scope(measures=(8, 12), voice_name='ViolinMusicVoice')
        Scope(measures=(9, 12), voice_name='OboeMusicVoice')

    """

    scopes: typing.Any = None

    voice_name: typing.ClassVar[str] = "Timeline_Scope"

    def __post_init__(self):
        if self.scopes is not None:
            assert isinstance(self.scopes, tuple | list)
            scopes_ = []
            for scope in self.scopes:
                if not isinstance(scope, Scope):
                    scope = Scope(*scope)
                scopes_.append(scope)
            scopes = scopes_
            scopes = tuple(scopes)
            self.scopes = scopes


def _make_regions(measures, *, total=None):
    result = []
    for left, right in abjad.sequence.nwise(measures):
        result.append(left)
        if isinstance(left, int):
            stop = left
        else:
            assert isinstance(left, tuple)
            assert len(left) == 2
            stop = left[1]
        assert isinstance(stop, int)
        if isinstance(right, int):
            start = right
        else:
            assert isinstance(right, tuple)
            assert len(right) == 2
            start = right[0]
        assert isinstance(start, int)
        difference = start - stop
        assert 1 < difference, measures
        if difference == 2:
            result.append(stop + 1)
        else:
            pair = (stop + 1, start - 1)
            result.append(pair)
    result.append(right)
    if total is not None:
        assert isinstance(total, int), repr(total)
        if isinstance(right, int):
            stop = right
        else:
            stop = right[1]
        difference = total - stop
        if difference == 1:
            result.append(total)
        elif 1 < difference:
            pair = (stop + 1, total)
            result.append(pair)
    if isinstance(measures[0], int):
        start = measures[0]
    else:
        assert isinstance(measures[0], tuple)
        start = measures[0][0]
    if start == 1:
        begin_with_maker_2 = False
    elif start == 2:
        result.insert(0, 1)
        begin_with_maker_2 = True
    else:
        assert 2 < start
        pair = (1, start - 1)
        result.insert(0, pair)
        begin_with_maker_2 = True
    return result, begin_with_maker_2


def alternate_makers(
    accumulator, voice_name, measures, maker_1, maker_2, *, total=None
):
    regions, begin_with_maker_2 = _make_regions(measures, total=total)
    makers = [maker_1, maker_2]
    for i, region in enumerate(regions):
        if not begin_with_maker_2:
            maker = makers[i % 2]
        else:
            maker = makers[(i + 1) % 2]
        accumulator(
            (voice_name, region),
            maker,
        )


def timeline(scopes) -> TimelineScope:
    """
    Makes timeline scope.
    """
    scopes_ = []
    for scope in scopes:
        voice_name, measures = scope
        scope_ = Scope(measures=measures, voice_name=voice_name)
        scopes_.append(scope_)
    return TimelineScope(scopes=scopes_)
