import abjad


class SpacingSection(abjad.AbjadObject):
    r'''Spacing section.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        )

    _context = 'Score'

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, duration=None):
        if duration is not None:
            duration = abjad.NonreducedFraction(duration)
        self._duration = duration

    ### SPECIAL METHODS ###

    def __call__(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets class constant ``'Score'``.

        ..  container:: example

            >>> baca.SpacingSection((2, 24)).context
            'Score'

        Returns ``'Score'``.
        '''
        return self._context

    @property
    def duration(self):
        r'''Gets duration.

        ..  container:: example

            >>> baca.SpacingSection((2, 24)).duration
            NonreducedFraction(2, 24)

        Returns nonreduced fraction or none.
        '''
        return self._duration

    @property
    def persistent(self):
        r'''Is class constant true.

        ..  container:: example

            >>> baca.SpacingSection((2, 24)).persistent
            True

        Returns true.
        '''
        return self._persistent
