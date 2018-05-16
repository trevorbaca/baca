import abjad
import baca
import typing


class Scope(abjad.AbjadObject):
    r'''Scope.

    ..  container:: example

        >>> scope = baca.Scope(
        ...     stages=(1, 9),
        ...     voice_name='ViolinMusicVoice',
        ...     )

        >>> abjad.f(scope, strict=89)
        baca.Scope(
            stages=(1, 9),
            voice_name='ViolinMusicVoice',
            )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_stages',
        '_voice_name',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        stages: typing.Tuple[int, int] = None,
        voice_name: str = None,
        ) -> None:
        assert isinstance(stages, tuple), repr(stages)
        assert len(stages) == 2, repr(stages)
        start, stop = stages
        assert isinstance(start, int), repr(start)
        assert start != 0, repr(start)
        assert isinstance(stop, int), repr(stop)
        assert stop != 0, repr(stop)
        self._stages = stages
        if voice_name is not None:
            assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name

    ### PUBLIC PROPERTIES ###

    @property
    def stages(self) -> typing.Tuple[int, int]:
        r'''Gets stages.
        '''
        return self._stages

    @property
    def voice_name(self) -> typing.Optional[str]:
        r'''Gets voice name.
        '''
        return self._voice_name
