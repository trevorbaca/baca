# -*- coding: utf-8 -*-
import abjad


class RegisterInterpolationSpecifier(abjad.abctools.AbjadObject):
    r'''Register interpolation specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Holds register constant:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches(pitches),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.RegisterInterpolationSpecifier(
            ...             start_pitch=12,
            ...             stop_pitch=12,
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
                                fs''8 [
                                e''8
                                ef''8
                                f''8 ]
                            }
                            {
                                a''8 [
                                bf''8
                                c''8 ]
                            }
                            {
                                b''8 [
                                af''8
                                g''8
                                cs''8 ]
                            }
                            {
                                d''8 [
                                fs''8
                                e''8 ]
                            }
                            {
                                ef''8 [
                                f''8
                                a''8
                                bf''8 ]
                            }
                            {
                                c''8 [
                                b''8
                                af''8 ]
                            }
                            {
                                g''8 [
                                cs''8
                                d''8
                                fs''8 ]
                            }
                            {
                                e''8 [
                                ef''8
                                f''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Register interpolates from the octave of C5 to the octave of C4:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches(pitches),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.RegisterInterpolationSpecifier(
            ...             start_pitch=12,
            ...             stop_pitch=0,
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
                                fs''8 [
                                e''8
                                ef''8
                                f''8 ]
                            }
                            {
                                a''8 [
                                bf'8
                                c''8 ]
                            }
                            {
                                b'8 [
                                af'8
                                g''8
                                cs''8 ]
                            }
                            {
                                d''8 [
                                fs'8
                                e''8 ]
                            }
                            {
                                ef''8 [
                                f'8
                                a'8
                                bf'8 ]
                            }
                            {
                                c''8 [
                                b'8
                                af'8 ]
                            }
                            {
                                g'8 [
                                cs''8
                                d'8
                                fs'8 ]
                            }
                            {
                                e'8 [
                                ef'8
                                f'8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Register interpolates from the octave of C4 to the octave of C5:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches(pitches),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.RegisterInterpolationSpecifier(
            ...             start_pitch=0,
            ...             stop_pitch=12,
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
                                fs'8 [
                                e'8
                                ef'8
                                f'8 ]
                            }
                            {
                                a'8 [
                                bf'8
                                c''8 ]
                            }
                            {
                                b'8 [
                                af'8
                                g'8
                                cs''8 ]
                            }
                            {
                                d''8 [
                                fs'8
                                e''8 ]
                            }
                            {
                                ef''8 [
                                f''8
                                a'8
                                bf'8 ]
                            }
                            {
                                c''8 [
                                b'8
                                af'8 ]
                            }
                            {
                                g''8 [
                                cs''8
                                d''8
                                fs''8 ]
                            }
                            {
                                e''8 [
                                ef''8
                                f''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Register interpolates from the octave of C5 to the octave of C3:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches(pitches),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.RegisterInterpolationSpecifier(
            ...             start_pitch=12,
            ...             stop_pitch=-12,
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
                                fs''8 [
                                e''8
                                ef''8
                                f''8 ]
                            }
                            {
                                a'8 [
                                bf'8
                                c''8 ]
                            }
                            {
                                b'8 [
                                af'8
                                g'8
                                cs''8 ]
                            }
                            {
                                d'8 [
                                fs'8
                                e'8 ]
                            }
                            {
                                ef'8 [
                                f'8
                                a'8
                                bf8 ]
                            }
                            {
                                c'8 [
                                b8
                                af8 ]
                            }
                            {
                                g8 [
                                cs'8
                                d'8
                                fs8 ]
                            }
                            {
                                e8 [
                                ef8
                                f8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Register interpolates from the octave of C3 to the octave of C5:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches(pitches),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.RegisterInterpolationSpecifier(
            ...             start_pitch=-12,
            ...             stop_pitch=12,
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
                                fs8 [
                                e8
                                ef8
                                f8 ]
                            }
                            {
                                a8 [
                                bf8
                                c'8 ]
                            }
                            {
                                b8 [
                                af8
                                g'8
                                cs'8 ]
                            }
                            {
                                d'8 [
                                fs'8
                                e'8 ]
                            }
                            {
                                ef'8 [
                                f'8
                                a'8
                                bf'8 ]
                            }
                            {
                                c''8 [
                                b'8
                                af'8 ]
                            }
                            {
                                g'8 [
                                cs''8
                                d''8
                                fs''8 ]
                            }
                            {
                                e''8 [
                                ef''8
                                f''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_start_pitch',
        '_stop_pitch',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_pitch=None,
        stop_pitch=None,
        ):
        start_pitch = abjad.pitchtools.NumberedPitch(start_pitch)
        self._start_pitch = start_pitch
        stop_pitch = abjad.pitchtools.NumberedPitch(stop_pitch)
        self._stop_pitch = stop_pitch

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls register interpolation specifier on `expr`.

        Returns none.
        '''
        logical_ties = abjad.iterate(expr).by_logical_tie(
            pitched=True,
            with_grace_notes=True,
            )
        logical_ties = list(logical_ties)
        total = len(logical_ties)
        for index, logical_tie in enumerate(logical_ties):
            registration = self._get_registration(index, total)
            for note in logical_tie:
                written_pitch = registration([note.written_pitch])
                self._set_pitch(note, written_pitch)

    ### PRIVATE METHODS ###

    def _get_registration(self, logical_tie_index, logical_tie_count):
        start_pitch = self.start_pitch.pitch_number
        stop_pitch = self.stop_pitch.pitch_number
        compass = stop_pitch - start_pitch
        fraction = abjad.Fraction(logical_tie_index, logical_tie_count)
        addendum = fraction * compass
        current_pitch = start_pitch + addendum
        current_pitch = int(current_pitch)
        registration = abjad.pitchtools.Registration()
        registration.append(('[A0, C8]', current_pitch))
        return registration
    
    @staticmethod
    def _set_pitch(note, written_pitch):
        note.written_pitch = written_pitch
        abjad.detach('not yet registered', note)

    ### PUBLIC PROPERTIES ###

    @property
    def start_pitch(self):
        r'''Gets start pitch.

        Set to pitch.

        Returns pitch.
        '''
        return self._start_pitch

    @property
    def stop_pitch(self):
        r'''Gets stop pitch.

        Set to pitch.

        Returns pitch.
        '''
        return self._stop_pitch
