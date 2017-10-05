import abjad


class StageSliceSpecifier(abjad.AbjadValueObject):
    r'''Stage slice specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

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
