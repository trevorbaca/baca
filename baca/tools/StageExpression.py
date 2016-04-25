# -*- coding: utf-8 -*-
from abjad.tools.expressiontools.Expression import Expression


class StageExpression(Expression):
    r'''Stage expression.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_stage_start_number',
        '_stage_stop_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        stage_start_number=None,
        stage_stop_number=None,
        ):
        self._stage_start_number = stage_start_number
        self._stage_stop_number = stage_stop_number

    ### PUBLIC PROPERTIES ###

    @property
    def stage_start_number(self):
        r'''Gets stage start number.

        Returns integer or none.
        '''
        return self._stage_start_number

    @property
    def stage_stop_number(self):
        r'''Gets stage stop number.

        Returns integer or none.
        '''
        return self._stage_stop_number