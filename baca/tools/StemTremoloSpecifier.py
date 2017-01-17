# -*- coding: utf-8 -*-
import abjad


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
            ...     ('vn', baca.select.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4 F4'),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.StemTremoloSpecifier(),
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
        '_patterns',
        '_selector',
        '_tremolo_flags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        patterns=None,
        selector=None,
        tremolo_flags=32,
        ):
        if patterns is not None:
            patterns = tuple(patterns)
            prototype = abjad.patterntools.Pattern
            assert all(isinstance(_, prototype) for _ in patterns)
        self._patterns = patterns
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
        selector = self._get_selector()
        selection = selector(argument)
        total_items = len(selection)
        for i, item in enumerate(selection):
            patterns = self._get_patterns()
            for pattern in patterns:
                if pattern.matches_index(i, total_items):
                    tremolo_flags = 32
                    stem_tremolo = abjad.indicatortools.StemTremolo(
                        tremolo_flags=self.tremolo_flags
                        )
                    abjad.attach(stem_tremolo, item)
                    break

    ### PRIVATE METHODS ###

    def _get_patterns(self):
        if self.patterns is None:
            return [abjad.patterntools.select_all()]
        return self.patterns

    def _get_selector(self):
        if self.selector is None:
            selector = abjad.selectortools.Selector()
            selector = selector.by_logical_tie(pitched=True, flatten=True)
            selector = selector.get_item(0, apply_to_each=True)
            return selector
        return self.selector

    ### PUBLIC PROPERTIES ###

    @property
    def patterns(self):
        r'''Gets patterns.

        ..  container:: example

            Selects first and last logical ties:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.select.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4 F4'),
                ...         baca.rhythm.make_even_run_rhythm_specifier(),
                ...         baca.tools.StemTremoloSpecifier(
                ...             patterns=[
                ...                 patterntools.select_first(),
                ...                 patterntools.select_last(),
                ...                 ],
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
                ...     ('vn', baca.select.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4 F4'),
                ...         baca.rhythm.make_even_run_rhythm_specifier(),
                ...         baca.tools.StemTremoloSpecifier(
                ...             patterns=[
                ...                 patterntools.select_every([1], period=2),
                ...                 ],
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

        Set to boolean patterns or none.
        '''
        return self._patterns

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
                ...     ('vn', baca.select.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4 F4'),
                ...         baca.rhythm.make_even_run_rhythm_specifier(),
                ...         baca.tools.StemTremoloSpecifier(),
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
                ...     ('vn', baca.select.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4 F4'),
                ...         baca.rhythm.make_even_run_rhythm_specifier(),
                ...         baca.tools.StemTremoloSpecifier(
                ...             selector=select().
                ...                 by_leaf(flatten=True).
                ...                 get_slice(start=-7, apply_to_each=False),
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
                ...     ('vn', baca.select.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4 F4'),
                ...         baca.rhythm.make_even_run_rhythm_specifier(),
                ...         baca.tools.StemTremoloSpecifier(),
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
                ...     ('vn', baca.select.stages(1)),
                ...     [
                ...         baca.pitch.pitches('E4 F4'),
                ...         baca.rhythm.make_even_run_rhythm_specifier(),
                ...         baca.tools.StemTremoloSpecifier(
                ...             tremolo_flags=16,
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
