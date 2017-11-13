import abjad
import baca


class Scope(abjad.AbjadObject):
    r'''Scope.

    ..  container:: example

        >>> scope = baca.Scope(
        ...     voice_name='Violin Music Voice',
        ...     stages=(1, 9),
        ...     )

        >>> abjad.f(scope)
        baca.Scope(
            voice_name='Violin Music Voice',
            stages=(1, 9),
            )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(6) Utilities'

    __slots__ = (
        '_voice_name',
        '_stages',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        voice_name=None,
        stages=None,
        ):
        if voice_name is not None:
            assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name
        if isinstance(stages, int):
            stages = (stages, stages)
        elif isinstance(stages, tuple):
            assert len(stages) == 2, repr(stages)
        else:
            raise TypeError(stages)
        self._stages = stages

    ### PUBLIC PROPERTIES ###

    @property
    def stages(self):
        r'''Gets stages.

        Returns stage expression.
        '''
        return self._stages

    @property
    def voice_name(self):
        r'''Gets voice name.

        Returns string.
        '''
        return self._voice_name
