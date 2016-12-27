# -*- coding: utf-8 -*-
import abjad


class RegisterSpecifier(abjad.abctools.AbjadObject):
    r"""Register specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Transposes to the octave of Eb5:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4'),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.RegisterSpecifier(
            ...             registration=pitchtools.Registration(
            ...                 [('[A0, C8]', 15)],
            ...                 ),
            ...             ),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
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
                                g''8 [
                                gqs''8
                                gs''8
                                gtqs''8 ]
                            }
                            {
                                aqf''8 [
                                af''8
                                atqf''8 ]
                            }
                            {
                                g''8 [
                                gqs''8
                                gs''8
                                gtqs''8 ]
                            }
                            {
                                aqf''8 [
                                af''8
                                atqf''8 ]
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
        prototype = (type(None), abjad.pitchtools.Registration)
        assert isinstance(registration, prototype), repr(registration)
        self._registration = registration

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls registration specifier on `expr`.

        Returns none.
        '''
        for logical_tie in abjad.iterate(expr).by_logical_tie(
            pitched=True,
            with_grace_notes=True,
            ):
            for note in logical_tie:
                written_pitch = self.registration([note.written_pitch])
                self._set_pitch(note, written_pitch)

    ### PRIVATE METHODS ###

    @staticmethod
    def _set_pitch(note, written_pitch):
        note.written_pitch = written_pitch
        abjad.detach('not yet registered', note)

    ### PUBLIC PROPERTIES ###

    @property
    def registration(self):
        r'''Gets registration.

        ..  container:: example

            ::

                >>> specifier = baca.tools.RegisterSpecifier(
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
