# -*- coding: utf-8 -*-
import abjad
import baca


class SimpleScope(abjad.abctools.AbjadObject):
    r'''SimpleScope.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> scope = baca.SimpleScope(
            ...     voice_name='Violin Music Voice',
            ...     stages=(1, 9),
            ...     )

        ::

            >>> f(scope)
            baca.tools.SimpleScope(
                voice_name='Violin Music Voice',
                stages=(1, 9),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

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
        if isinstance(stages, baca.StageExpression):
            #stages = (stages.start, stages.stop)
            pass
        elif isinstance(stages, int):
            stages = (stages, stages)
        self._stages = stages

    ### PUBLIC PROPERTIES ###

    @property
    def stages(self):
        r'''Gets stages of scope.

        Set to one or two positive integers or to stage expression none.
        '''
        return self._stages

    @property
    def voice_name(self):
        r'''Gets voice name of scope.

        Set to string or none.
        '''
        return self._voice_name
