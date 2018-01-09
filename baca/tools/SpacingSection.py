import abjad


class SpacingSection(abjad.AbjadObject):
    r'''Spacing section.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(baca.SpacingSection((2, 24)), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \newSpacingSection
                \set Score.proportionalNotationDuration = #(ly:make-moment 2 24)
                c'4
                d'4
                e'4
                f'4
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

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

    def __eq__(self, argument):
        r'''Is true when `argument` is a spacing section with same duration as
        this spacing section.

        ..  container:: example

            >>> spacing_section_1 = baca.SpacingSection((2, 24))
            >>> spacing_section_2 = baca.SpacingSection((2, 24))
            >>> spacing_section_3 = baca.SpacingSection((3, 24))

            >>> spacing_section_1 == spacing_section_1
            True
            >>> spacing_section_1 == spacing_section_2
            True
            >>> spacing_section_1 == spacing_section_3
            False

            >>> spacing_section_2 == spacing_section_1
            True
            >>> spacing_section_2 == spacing_section_2
            True
            >>> spacing_section_2 == spacing_section_3
            False

            >>> spacing_section_3 == spacing_section_1
            False
            >>> spacing_section_3 == spacing_section_2
            False
            >>> spacing_section_3 == spacing_section_3
            True

        Returns string.
        '''
        if isinstance(argument, type(self)):
            return self.duration == argument.duration

    def __hash__(self):
        r'''Hashes spacing section.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(SpacingSection, self).__hash__()

    def __str__(self):
        r'''Gets string representation of spacing section.

        ..  container:: example

            >>> str(baca.SpacingSection((2, 24)))
            '2/24'

        Returns string.
        '''
        return str(self.duration)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf=None):
        bundle = abjad.LilyPondFormatBundle()
        moment = abjad.SchemeMoment(self.duration)
        strings = [r'\newSpacingSection']
        strings.append(rf'\set Score.proportionalNotationDuration = {moment}')
        bundle.before.commands.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

#    @property
#    def context(self):
#        r'''Gets class constant ``'Score'``.
#
#        ..  container:: example
#
#            >>> baca.SpacingSection((2, 24)).context
#            'Score'
#
#        Returns ``'Score'``.
#        '''
#        return self._context

    @property
    def duration(self):
        r'''Gets duration.

        ..  container:: example

            >>> baca.SpacingSection((2, 24)).duration
            NonreducedFraction(2, 24)

        Returns nonreduced fraction or none.
        '''
        return self._duration

#    @property
#    def persistent(self):
#        r'''Is class constant true.
#
#        ..  container:: example
#
#            >>> baca.SpacingSection((2, 24)).persistent
#            True
#
#        Returns true.
#        '''
#        return self._persistent

    ### PUBLIC METHODS ###

    @staticmethod
    def from_string(string):
        r'''Makes spacing section from fraction `string`.

        ..  container:: example

            >>> baca.SpacingSection.from_string('2/24')
            SpacingSection(duration=NonreducedFraction(2, 24))

        Returns new spacing section.
        '''
        duration = abjad.NonreducedFraction(string)
        return SpacingSection(duration=duration)
