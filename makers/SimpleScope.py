# -*- encoding: utf-8 -*-
from abjad import *


class SimpleScope(abctools.AbjadObject):
    r'''SimpleScope.

    ..  container:: example

        ::

            >>> from baca import makers
            >>> scope = makers.SimpleScope(
            ...     context_name='Violin Music Voice',
            ...     stages=(1, 9),
            ...     )

        ::

            >>> print(format(scope, 'storage'))
            baca.makers.SimpleScope(
                context_name='Violin Music Voice',
                stages=(1, 9),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_name',
        '_stages',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        context_name=None,
        stages=None,
        ):
        if context_name is not None:
            assert isinstance(context_name, str), repr(context_name)
        self._context_name = context_name
        if isinstance(stages, int):
            stages = (stages, stages)
        if stages is not None:
            stages = tuple(stages)
            assert mathtools.all_are_positive_integers(stages), stages
        self._stages = stages

    ### PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        r'''Gets context name of scope.

        Set to string or none.
        '''
        return self._context_name

    @property
    def stages(self):
        r'''Gets stages of scope.

        Set to one or two positive integers or none.
        '''
        return self._stages