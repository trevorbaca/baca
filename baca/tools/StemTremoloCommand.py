import abjad
import baca
from .Command import Command


class StemTremoloCommand(Command):
    r'''Stem tremolo command.

    ..  container:: example

        Selects notes and chords by default:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.pitches('E4 F4'),
            ...     baca.even_runs(),
            ...     baca.stem_tremolo(),
            ...     )

        ::

            >>> result = segment_maker.run(is_doc_example=True)
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

    __slots__ = (
        '_tremolo_flags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        selector='baca.select().pls()',
        tremolo_flags=32,
        ):
        Command.__init__(self, selector=selector)
        assert abjad.mathtools.is_nonnegative_integer_power_of_two(
            tremolo_flags)
        self._tremolo_flags = tremolo_flags

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls command on `music`.

        Returns none.
        '''
        selections = self._select(music)
        for selection in selections:
            pls = baca.select().pls()(selection)
            for pl in pls:
                stem_tremolo = abjad.StemTremolo(
                    tremolo_flags=self.tremolo_flags
                    )
                abjad.attach(stem_tremolo, pl)

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        ..  container:: example

            Selects pitched leaves:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> segment_maker(
                ...     baca.scope('Violin Music Voice', 1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.stem_tremolo(),
                ...     )

            ::

                >>> result = segment_maker.run(is_doc_example=True)
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

            Selects last seven pitched leaves:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> segment_maker(
                ...     baca.scope('Violin Music Voice', 1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.stem_tremolo(baca.select().pls()[-7:]),
                ...     )

            ::

                >>> result = segment_maker.run(is_doc_example=True)
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

                >>> segment_maker(
                ...     baca.scope('Violin Music Voice', 1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.stem_tremolo(),
                ...     )

            ::

                >>> result = segment_maker.run(is_doc_example=True)
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

                >>> segment_maker(
                ...     baca.scope('Violin Music Voice', 1),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_runs(),
                ...     baca.StemTremoloCommand(tremolo_flags=16),
                ...     )

            ::

                >>> result = segment_maker.run(is_doc_example=True)
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
