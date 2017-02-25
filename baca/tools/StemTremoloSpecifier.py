# -*- coding: utf-8 -*-
import abjad
import baca


class StemTremoloSpecifier(abjad.abctools.AbjadObject):
    r'''Stem tremolo specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Selects notes and chords by default:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select_stages(1)),
            ...     baca.pitches('E4 F4'),
            ...     baca.even_run_rhythm_specifier(),
            ...     baca.tools.StemTremoloSpecifier(),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
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

    __documentation_section__ = 'Specifiers'

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
            prototype = (abjad.Pattern, abjad.patterntools.CompoundPattern)
            assert isinstance(pattern, prototype), repr(pattern)
        self._pattern = pattern
        if selector is not None:
            assert isinstance(selector, abjad.selectortools.Selector)
        self._selector = selector
        assert abjad.mathtools.is_nonnegative_integer_power_of_two(
            tremolo_flags)
        self._tremolo_flags = tremolo_flags

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        selector = self.selector or baca.select_pitched_logical_tie_heads()
        selection = selector(argument)
        pattern = self.pattern or abjad.select_all()
        items = pattern.get_matching_items(selection)
        for item in items:
            stem_tremolo = abjad.StemTremolo(tremolo_flags=self.tremolo_flags)
            abjad.attach(stem_tremolo, item)

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            Selects first and last logical ties:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> pattern = abjad.select_first() | abjad.select_last()
                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.select_stages(1)),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_run_rhythm_specifier(),
                ...     baca.tools.StemTremoloSpecifier(
                ...         pattern=pattern,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
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

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.select_stages(1)),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_run_rhythm_specifier(),
                ...     baca.tools.StemTremoloSpecifier(
                ...         pattern=abjad.select_every([1], period=2),
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
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

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.select_stages(1)),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_run_rhythm_specifier(),
                ...     baca.tools.StemTremoloSpecifier(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
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

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.select_stages(1)),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_run_rhythm_specifier(),
                ...     baca.tools.StemTremoloSpecifier(
                ...         selector=abjad.select().
                ...             by_leaf(flatten=True).
                ...             get_slice(start=-7, apply_to_each=False),
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
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

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.select_stages(1)),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_run_rhythm_specifier(),
                ...     baca.tools.StemTremoloSpecifier(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
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

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.select_stages(1)),
                ...     baca.pitches('E4 F4'),
                ...     baca.even_run_rhythm_specifier(),
                ...     baca.tools.StemTremoloSpecifier(
                ...         tremolo_flags=16,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, segment_metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Score])
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
