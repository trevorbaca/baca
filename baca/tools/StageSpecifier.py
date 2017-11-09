import abjad


class StageSpecifier(abjad.AbjadValueObject):
    r'''Stage specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(3) Specifiers'

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
        r'''Gets stage start number.

        Returns integer or none.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets stage stop number.

        Returns integer or none.
        '''
        return self._stop
