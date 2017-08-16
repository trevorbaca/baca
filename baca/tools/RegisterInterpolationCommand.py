import abjad


class RegisterInterpolationCommand(abjad.AbjadObject):
    r"""Register interpolation command.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With music-maker.

        All stages glued together:

        ::

            >>> music_maker = baca.MusicMaker()

        ::

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RegisterInterpolationCommand(
            ...         start_pitch=0,
            ...         stop_pitch=24,
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            fs'16 [
                            e'16
                            ef'16
                            f'16
                            a'16
                            bf'16
                            c''16
                            b'16
                            af'16
                            g''16
                            cs''16
                            d''16 ]
                        }
                        {
                            fs''16 [
                            e''16
                            ef''16
                            f''16
                            a''16
                            bf''16
                            c'''16
                            b''16
                            af''16
                            g'''16
                            cs'''16
                            d'''16 ]
                        }
                    }
                }
            >>

    ..  container:: example

        With chords:

        ::

            >>> music_maker = baca.MusicMaker()

        ::

            >>> collections = [
            ...     [6, 4], [3, 5], [9, 10], [0, 11], [8, 7], [1, 2],
            ...     ]
            >>> collections = [set(_) for _ in collections]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RegisterInterpolationCommand(
            ...         start_pitch=0,
            ...         stop_pitch=24,
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            <e' fs'>16
                        }
                        {
                            <f' ef''>16
                        }
                        {
                            <a' bf'>16
                        }
                        {
                            <c'' b''>16
                        }
                        {
                            <g'' af''>16
                        }
                        {
                            <cs''' d'''>16
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker.

        Holds register constant:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches(pitches),
            ...     baca.even_runs(),
            ...     baca.RegisterInterpolationCommand(
            ...         start_pitch=12,
            ...         stop_pitch=12,
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set Staff.instrumentName = \markup { Violin }
                                \set Staff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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
            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches(pitches),
            ...     baca.even_runs(),
            ...     baca.RegisterInterpolationCommand(
            ...         start_pitch=12,
            ...         stop_pitch=0,
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set Staff.instrumentName = \markup { Violin }
                                \set Staff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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
            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches(pitches),
            ...     baca.even_runs(),
            ...     baca.RegisterInterpolationCommand(
            ...         start_pitch=0,
            ...         stop_pitch=12,
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set Staff.instrumentName = \markup { Violin }
                                \set Staff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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
            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches(pitches),
            ...     baca.even_runs(),
            ...     baca.RegisterInterpolationCommand(
            ...         start_pitch=12,
            ...         stop_pitch=-12,
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set Staff.instrumentName = \markup { Violin }
                                \set Staff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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
            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        ::

            >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches(pitches),
            ...     baca.even_runs(),
            ...     baca.RegisterInterpolationCommand(
            ...         start_pitch=-12,
            ...         stop_pitch=12,
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set Staff.instrumentName = \markup { Violin }
                                \set Staff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_pattern',
        '_selector',
        '_start_pitch',
        '_stop_pitch',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        selector=None,
        start_pitch=None,
        stop_pitch=None,
        ):
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        start_pitch = abjad.NumberedPitch(start_pitch)
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector
        self._start_pitch = start_pitch
        stop_pitch = abjad.NumberedPitch(stop_pitch)
        self._stop_pitch = stop_pitch

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.pattern is None:
            selections = [argument]
        else:
            assert isinstance(argument, list), repr(argument)
            assert isinstance(argument[0], abjad.Selection), repr(argument)
            selections = argument
            selections = self.pattern.get_matching_items(selections)
        for selection in selections:
            logical_ties = abjad.iterate(selection).by_logical_tie(
                pitched=True,
                with_grace_notes=True,
                )
            logical_ties = list(logical_ties)
            length = len(logical_ties)
            for index, logical_tie in enumerate(logical_ties):
                registration = self._get_registration(index, length)
                for leaf in logical_tie:
                    if isinstance(leaf, abjad.Note):
                        written_pitches = registration([leaf.written_pitch])
                        leaf.written_pitch = written_pitches[0]
                    elif isinstance(leaf, abjad.Chord):
                        written_pitches = registration(leaf.written_pitches)
                        leaf.written_pitches = written_pitches
                    else:
                        raise TypeError(leaf)
                    abjad.detach('not yet registered', leaf)

    ### PRIVATE METHODS ###

    def _get_registration(self, logical_tie_index, logical_tie_count):
        start_pitch = self.start_pitch.number
        stop_pitch = self.stop_pitch.number
        compass = stop_pitch - start_pitch
        fraction = abjad.Fraction(logical_tie_index, logical_tie_count)
        addendum = fraction * compass
        current_pitch = start_pitch + addendum
        current_pitch = int(current_pitch)
        registration = abjad.Registration()
        registration.append(('[A0, C8]', current_pitch))
        return registration

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r"""Gets pattern.

        ..  container:: example

            Music-maker (first stage only):

            ::

                >>> music_maker = baca.MusicMaker()

            ::

                >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     collections,
                ...     baca.RegisterInterpolationCommand(
                ...         pattern=abjad.index_first(),
                ...         start_pitch=0,
                ...         stop_pitch=24,
                ...         ),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                fs'16 [
                                e'16
                                ef''16
                                f''16
                                a'16
                                bf'16
                                c''16
                                b''16
                                af''16
                                g''16
                                cs'''16
                                d'''16 ]
                            }
                            {
                                fs'16 [
                                e'16
                                ef'16
                                f'16
                                a'16
                                bf'16
                                c'16
                                b'16
                                af'16
                                g'16
                                cs'16
                                d'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Music-maker (last stage only):

            ::

                >>> music_maker = baca.MusicMaker()

            ::

                >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     collections,
                ...     baca.RegisterInterpolationCommand(
                ...         pattern=abjad.index_last(),
                ...         start_pitch=0,
                ...         stop_pitch=24,
                ...         ),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                fs'16 [
                                e'16
                                ef'16
                                f'16
                                a'16
                                bf'16
                                c'16
                                b'16
                                af'16
                                g'16
                                cs'16
                                d'16 ]
                            }
                            {
                                fs'16 [
                                e'16
                                ef''16
                                f''16
                                a'16
                                bf'16
                                c''16
                                b''16
                                af''16
                                g''16
                                cs'''16
                                d'''16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Music-maker (each stage registered separately):

            ::

                >>> music_maker = baca.MusicMaker()

            ::

                >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     collections,
                ...     baca.RegisterInterpolationCommand(
                ...         pattern=abjad.index_all(),
                ...         start_pitch=0,
                ...         stop_pitch=24,
                ...         ),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                fs'16 [
                                e'16
                                ef''16
                                f''16
                                a'16
                                bf'16
                                c''16
                                b''16
                                af''16
                                g''16
                                cs'''16
                                d'''16 ]
                            }
                            {
                                fs'16 [
                                e'16
                                ef''16
                                f''16
                                a'16
                                bf'16
                                c''16
                                b''16
                                af''16
                                g''16
                                cs'''16
                                d'''16 ]
                            }
                        }
                    }
                >>

        Set to pattern or none.

        Defaults to none.

        Returns pattern or none.
        """
        return self._pattern

    @property
    def selector(self):
        r'''Gets selector.

        Set to selector or none.
        '''
        return self._selector

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
