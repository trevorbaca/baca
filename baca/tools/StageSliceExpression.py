# -*- coding: utf-8 -*-
import abjad


class StageSliceExpression(abjad.expressiontools.Expression):
    r'''Stage slice expression.
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
        r'''Gets start number of stage slice expression.

        Returns integer or none.
        '''
        return self._start_number

    @property
    def stop_number(self):
        r'''Gets stop number of stage slice expression.

        Returns integer or none.
        '''
        return self._stop_number