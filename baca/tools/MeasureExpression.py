import abjad


class MeasureExpression(abjad.Expression):
    r'''Measure expression.

    ::

        >>> import baca

    ..  container:: example

        Selects measures from indices 2 to 4:

        ::

            >>> expression = baca.MeasureExpression(2, 4)

        ::

            >>> f(expression)
            baca.MeasureExpression(
                start=2,
                stop=4,
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start=None,
        stop=None,
        ):
        self._start = start
        self._stop = stop

    ### PUBLIC PROPERTIES ###

    @property
    def start(self):
        r'''Gets start.

        Returns integer or none.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets stop.

        Returns integer or none.
        '''
        return self._stop
