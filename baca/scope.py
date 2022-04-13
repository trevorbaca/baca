import dataclasses
import typing

from . import typings as _typings


@dataclasses.dataclass(slots=True)
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


@dataclasses.dataclass(slots=True)
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
