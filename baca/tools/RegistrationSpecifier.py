# -*- coding: utf-8 -*-
from abjad.tools import abctools


class RegistrationSpecifier(abctools.AbjadObject):
    r"""Registration specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.**

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('G4 G4 G4 G4 Eb4 Eb4 Eb4'),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.RegistrationSpecifier(
            ...             registration=pitchtools.Registration(
            ...                 [('[A0, C4)', 15), ('[C4, C8)', 27)],
            ...                 ),
            ...             ),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                g'''8 [
                                g'''8
                                g'''8
                                g'''8 ]
                            }
                            {
                                ef'''8 [
                                ef'''8
                                ef'''8 ]
                            }
                            {
                                g'''8 [
                                g'''8
                                g'''8
                                g'''8 ]
                            }
                            {
                                ef'''8 [
                                ef'''8
                                ef'''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_registration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        registration=None,
        ):
        from abjad.tools import pitchtools
        prototype = (type(None), pitchtools.Registration)
        assert isinstance(registration, prototype), repr(registration)
        self._registration = registration

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls registration specifier.

        Returns none.
        '''
        for logical_tie in logical_ties:
            for note in logical_tie:
                written_pitch = self.registration([note.written_pitch])
                note.written_pitch = written_pitch

    ### PUBLIC PROPERTIES ###

    @property
    def registration(self):
        r'''Gets registration.

        ..  container:: example

            ::

                >>> specifier = baca.tools.RegistrationSpecifier(
                ...     registration=pitchtools.Registration(
                ...         [('[A0, C4)', 15), ('[C4, C8)', 27)],
                ...         ),
                ...     )

            ::

                >>> specifier.registration
                Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])

        Set to registration or none.

        Returns registration or none.
        '''
        return self._registration