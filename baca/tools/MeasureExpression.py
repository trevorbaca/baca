# -*- coding: utf-8 -*-
from abjad.tools.expressiontools.Expression import Expression


class MeasureExpression(Expression):
    r'''Measure expression.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Selects measures from indices 2 to 4:

        ::

            >>> expression = baca.tools.MeasureExpression(2, 4)
        
        ::

            >>> print(format(expression))
            baca.tools.MeasureExpression(
                start_number=2,
                stop_number=4,
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-maker components'

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