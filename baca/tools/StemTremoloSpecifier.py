# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import indicatortools
from abjad.tools import patterntools
from abjad.tools.topleveltools import attach


class StemTremoloSpecifier(abctools.AbjadObject):
    r'''Stem tremolo specifier.

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
            ...         baca.pitch.pitches('E4 F4'),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.StemTremoloSpecifier(
            ...             patterns=[
            ...                 patterntools.select_every([1], period=2),
            ...                 patterntools.select_first(),
            ...                 ],
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
                                e'8 :32 [
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

    '''

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_patterns',
        )

    _selector_type = 'logical ties'

    ### INITIALIZER ###

    def __init__(
        self,
        patterns=None,
        ):
        from abjad.tools import pitchtools
        if patterns is not None:
            patterns = tuple(patterns)
            prototype = patterntools.Pattern
            assert all(isinstance(_, prototype) for _ in patterns)
        self._patterns = patterns

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls stem tremolo specifier.

        Returns none.
        '''
        total_logical_ties = len(logical_ties)
        for i, logical_tie in enumerate(logical_ties):
            for durations in self.patterns:
                if durations.matches_index(i, total_logical_ties):
                    hash_mark_count = 32
                    stem_tremolo = indicatortools.StemTremolo(hash_mark_count)
                    for leaf in logical_tie:
                        attach(stem_tremolo, leaf)
                    break

    ### PUBLIC PROPERTIES ###

    @property
    def patterns(self):
        r'''Gets patterns.

        ..  container:: example

            **Example 1.** Selects first and last logical ties:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
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

            **Example 2.** Selects every other logical tie:

            ::

                >>> segment_maker = baca.tools.SegmentMaker(
                ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.tools.stages(1)),
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