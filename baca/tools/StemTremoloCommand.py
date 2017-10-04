import abjad
import baca


class StemTremoloCommand(abjad.AbjadObject):
    r'''Stem tremolo command.

    ..  container:: example

        Selects notes and chords by default:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 F4'),
            ...     baca.even_runs(),
            ...     baca.StemTremoloCommand(),
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
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                e'8 :32 [
                                f'8 :32
                                e'8 :32
                                f'8 :32 ]
                            }
                            {
                                e'8 :32 [
                                f'8 :32
                                e'8 :32 ]
                            }
                            {
                                f'8 :32 [
                                e'8 :32
                                f'8 :32
                                e'8 :32 ]
                            }
                            {
                                f'8 :32 [
                                e'8 :32
                                f'8 :32 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_pattern',
        '_selector',
        '_tremolo_flags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        selector=None,
        tremolo_flags=32,
        ):
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        if selector is not None:
            assert isinstance(selector, abjad.Selector)
        self._selector = selector
        assert abjad.mathtools.is_nonnegative_integer_power_of_two(
            tremolo_flags)
        self._tremolo_flags = tremolo_flags

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        pattern = self.pattern
        if pattern is None:
            pattern = abjad.index_all()
        selector = self.selector or baca.select_plt_heads()
        selections = selector(argument)
        selections = baca.MusicMaker._normalize_selections(selections)
        for selection in selections:
            items = pattern.get_matching_items(selection)
            for item in items:
                stem_tremolo = abjad.StemTremolo(
                    tremolo_flags=self.tremolo_flags
                    )
                abjad.attach(stem_tremolo, item)

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            Selects first and last logical ties:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> pattern = abjad.index_first() | abjad.index_last()
                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.StemTremoloCommand(
                ...         pattern=pattern,
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
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    e'8 :32 [
                                    f'8
                                    e'8
                                    f'8 ]
                                }
                                {
                                    e'8 [
                                    f'8
                                    e'8 ]
                                }
                                {
                                    f'8 [
                                    e'8
                                    f'8
                                    e'8 ]
                                }
                                {
                                    f'8 [
                                    e'8
                                    f'8 :32 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Selects every other logical tie:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.StemTremoloCommand(
                ...         pattern=abjad.index_every([1], period=2),
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
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    e'8 [
                                    f'8 :32
                                    e'8
                                    f'8 :32 ]
                                }
                                {
                                    e'8 [
                                    f'8 :32
                                    e'8 ]
                                }
                                {
                                    f'8 :32 [
                                    e'8
                                    f'8 :32
                                    e'8 ]
                                }
                                {
                                    f'8 :32 [
                                    e'8
                                    f'8 :32 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects notes and chords by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.StemTremoloCommand(),
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
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    e'8 :32 [
                                    f'8 :32
                                    e'8 :32
                                    f'8 :32 ]
                                }
                                {
                                    e'8 :32 [
                                    f'8 :32
                                    e'8 :32 ]
                                }
                                {
                                    f'8 :32 [
                                    e'8 :32
                                    f'8 :32
                                    e'8 :32 ]
                                }
                                {
                                    f'8 :32 [
                                    e'8 :32
                                    f'8 :32 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Selects last seven notes and chords:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.StemTremoloCommand(
                ...         selector=abjad.select().
                ...             by_leaf(flatten=True).
                ...             get_slice(start=-7, apply_to_each=False),
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
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    e'8 [
                                    f'8
                                    e'8
                                    f'8 ]
                                }
                                {
                                    e'8 [
                                    f'8
                                    e'8 ]
                                }
                                {
                                    f'8 :32 [
                                    e'8 :32
                                    f'8 :32
                                    e'8 :32 ]
                                }
                                {
                                    f'8 :32 [
                                    e'8 :32
                                    f'8 :32 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Defaults to pitched logical ties.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector

    @property
    def tremolo_flags(self):
        r'''Gets tremolo flags.

        ..  container:: example

            Gets thirty-second-valued tremolo flags by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.StemTremoloCommand(),
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
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    e'8 :32 [
                                    f'8 :32
                                    e'8 :32
                                    f'8 :32 ]
                                }
                                {
                                    e'8 :32 [
                                    f'8 :32
                                    e'8 :32 ]
                                }
                                {
                                    f'8 :32 [
                                    e'8 :32
                                    f'8 :32
                                    e'8 :32 ]
                                }
                                {
                                    f'8 :32 [
                                    e'8 :32
                                    f'8 :32 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            With sixteenth-valued tremolo flags:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.StemTremoloCommand(
                ...         tremolo_flags=16,
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
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    e'8 :16 [
                                    f'8 :16
                                    e'8 :16
                                    f'8 :16 ]
                                }
                                {
                                    e'8 :16 [
                                    f'8 :16
                                    e'8 :16 ]
                                }
                                {
                                    f'8 :16 [
                                    e'8 :16
                                    f'8 :16
                                    e'8 :16 ]
                                }
                                {
                                    f'8 :16 [
                                    e'8 :16
                                    f'8 :16 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Defaults to 32.

        Set to nonnegative integer power of two or none.

        Returns nonnegative integer power of two or none.
        '''
        return self._tremolo_flags
