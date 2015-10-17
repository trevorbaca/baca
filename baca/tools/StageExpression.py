# -*- coding: utf-8 -*-
from abjad.tools.expressiontools.Expression import Expression


class StageExpression(Expression):
    r'''Stage expression.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = (
        '_component_start_index',
        '_component_stop_index',
        '_prototype',
        '_stage_start_number',
        '_stage_stop_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        component_start_index=None,
        component_stop_index=None,
        prototype=None,
        stage_start_number=None,
        stage_stop_number=None,
        ):
        self._component_start_index = component_start_index
        self._component_stop_index = component_stop_index
        self._prototype = prototype
        self._stage_start_number = stage_start_number
        self._stage_stop_number = stage_stop_number

    ### PUBLIC PROPERTIES ###

    @property
    def component_start_index(self):
        r'''Gets component start index of stage expression.

        Returns integer or none.
        '''
        return self._component_start_index

    @property
    def component_stop_index(self):
        r'''Gets component stop index of stage expression.

        Returns integer or none.
        '''
        return self._component_stop_index

    @property
    def prototype(self):
        r'''Gets prototype of stage expression.

        Defaults to none.

        Interprets none equal to logical ties.

        Returns class, tuple of classes or none.
        '''
        return self._prototype

    @property
    def stage_start_number(self):
        r'''Gets stage start number of stage expression.

        Returns integer or none.
        '''
        return self._stage_start_number

    @property
    def stage_stop_number(self):
        r'''Gets stage stop number of stage expression.

        Returns integer or none.
        '''
        return self._stage_stop_number