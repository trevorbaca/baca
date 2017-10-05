import abjad


class MeasureSpecifier(abjad.AbjadValueObject):
    r'''Measure specifier.

    ..  container:: example

        Selects measures from indices 2 to 4:

        ::

            >>> specifier = baca.MeasureSpecifier(2, 4)

        ::

            >>> f(specifier)
            baca.MeasureSpecifier(
                start=2,
                stop=4,
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_start',
        '_stop',
        )

    _publish_storage_format = True

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
