# -*- coding: utf-8 -*-
import abjad


class MeasureExpression(abjad.expressiontools.Expression):
    r'''Measure expression.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Selects measures from indices 2 to 4:

        ::

            >>> expression = baca.tools.MeasureExpression(2, 4)
        
        ::

            >>> f(expression)
            baca.tools.MeasureExpression(
                start_number=2,
                stop_number=4,
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_start_number',
        '_stop_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_number=None,
        stop_number=None,
        ):
        self._start_number = start_number
        self._stop_number = stop_number

    ### PUBLIC PROPERTIES ###

    @property
    def start_number(self):
        r'''Gets start index of measure expression.

        Returns integer or none.
        '''
        return self._start_number

    @property
    def stop_number(self):
        r'''Gets stop index of measure expression.

        Returns integer or none.
        '''
        return self._stop_number
