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
        stages: typing.Tuple[int, typing.Union[int, str]] = None,
        voice_name: str = None,
        ) -> None:
        assert isinstance(stages, tuple), repr(stages)
        assert len(stages) == 2, repr(stages)
        start, stop = stages
        assert isinstance(start, int), repr(start)
        assert isinstance(stop, int), repr(stop)
        self._stages = stages
        if voice_name is not None:
            assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name

    ### PUBLIC PROPERTIES ###

    @property
    def stages(self) -> typing.Tuple[int, typing.Union[int, str]]:
        r'''Gets stages.
        '''
        return self._stages

    @property
    def voice_name(self) -> str:
        r'''Gets voice name.
        '''
        return self._voice_name
