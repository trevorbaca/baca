# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import set_


class SpacingSpecifier(AbjadObject):
    r'''Spacing specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** No spacing specifier:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4 F4'),
            ...         baca.tools.RhythmSpecifier(
            ...             rhythm_maker=rhythmmakertools.EvenRunRhythmMaker(),
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
                            \time 8/16
                            R1 * 1/2
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 2/4
                            R1 * 1/2
                        }
                        {
                            \time 1/2
                            R1 * 1/2
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 8/16
                            s1 * 1/2
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 2/4
                            s1 * 1/2
                        }
                        {
                            \time 1/2
                            s1 * 1/2
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                e'16 [
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16 ]
                            }
                            {
                                e'8 [
                                f'8
                                e'8
                                f'8 ]
                            }
                            {
                                e'4
                                f'4
                            }
                            {
                                e'2
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        **Example 2.** Null spacing specifier:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.tools.SpacingSpecifier(),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4 F4'),
            ...         baca.tools.RhythmSpecifier(
            ...             rhythm_maker=rhythmmakertools.EvenRunRhythmMaker(),
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
                            \time 8/16
                            R1 * 1/2
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 2/4
                            R1 * 1/2
                        }
                        {
                            \time 1/2
                            R1 * 1/2
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 8/16
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 4/8
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 8)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 2/4
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 4)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 1/2
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 2)
                            \newSpacingSection
                            s1 * 1/2
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                e'16 [
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16 ]
                            }
                            {
                                e'8 [
                                f'8
                                e'8
                                f'8 ]
                            }
                            {
                                e'4
                                f'4
                            }
                            {
                                e'2
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        **Example 3.** Measurewise proportional spacing based on minimum
        duration per measure:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.tools.SpacingSpecifier(
            ...         multiplier=Multiplier(1),
            ...         ),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4 F4'),
            ...         baca.tools.RhythmSpecifier(
            ...             rhythm_maker=rhythmmakertools.EvenRunRhythmMaker(),
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
                            \time 8/16
                            R1 * 1/2
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 2/4
                            R1 * 1/2
                        }
                        {
                            \time 1/2
                            R1 * 1/2
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 8/16
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 4/8
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 8)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 2/4
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 4)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 1/2
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 2)
                            \newSpacingSection
                            s1 * 1/2
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                e'16 [
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16 ]
                            }
                            {
                                e'8 [
                                f'8
                                e'8
                                f'8 ]
                            }
                            {
                                e'4
                                f'4
                            }
                            {
                                e'2
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        **Example 4.** Measurewise proportional spacing based on twice the
        minimum duration per measure:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.tools.SpacingSpecifier(
            ...         multiplier=Multiplier(2),
            ...         ),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4 F4'),
            ...         baca.tools.RhythmSpecifier(
            ...             rhythm_maker=rhythmmakertools.EvenRunRhythmMaker(),
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
                            \time 8/16
                            R1 * 1/2
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 2/4
                            R1 * 1/2
                        }
                        {
                            \time 1/2
                            R1 * 1/2
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 8/16
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 32)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 4/8
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 2/4
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 8)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 1/2
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 4)
                            \newSpacingSection
                            s1 * 1/2
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                e'16 [
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16 ]
                            }
                            {
                                e'8 [
                                f'8
                                e'8
                                f'8 ]
                            }
                            {
                                e'4
                                f'4
                            }
                            {
                                e'2
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        **Example 5.** Measurewise proportional spacing based on twice the
        minimum duration per measure with minimum width equal to an eighth
        note:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.tools.SpacingSpecifier(
            ...         multiplier=Multiplier(2),
            ...         minimum_width=Duration(1, 8),
            ...         ),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4 F4'),
            ...         baca.tools.RhythmSpecifier(
            ...             rhythm_maker=rhythmmakertools.EvenRunRhythmMaker(),
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
                            \time 8/16
                            R1 * 1/2
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 2/4
                            R1 * 1/2
                        }
                        {
                            \time 1/2
                            R1 * 1/2
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 8/16
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 32)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 4/8
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 2/4
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 1/2
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
                            \newSpacingSection
                            s1 * 1/2
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                e'16 [
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16
                                e'16
                                f'16 ]
                            }
                            {
                                e'8 [
                                f'8
                                e'8
                                f'8 ]
                            }
                            {
                                e'4
                                f'4
                            }
                            {
                                e'2
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
        '_fermata_measure_width',
        '_minimum_width',
        '_multiplier',
        '_overrides',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        fermata_measure_width=None,
        minimum_width=None,
        multiplier=None,
        overrides=None,
        ):
        if fermata_measure_width is not None:
            fermata_measure_width = durationtools.Duration(
                fermata_measure_width)
        self._fermata_measure_width = fermata_measure_width
        if minimum_width is not None:
            minimum_width = durationtools.Duration(minimum_width)
        self._minimum_width = minimum_width    
        if multiplier is not None:
            multiplier = durationtools.Multiplier(multiplier)
        self._multiplier = multiplier
        if overrides is not None:
            overrides = tuple(overrides)
        self._overrides = overrides

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker):
        r'''Calls spacing specifier.

        Returns none.
        '''
        score = segment_maker._score
        skip_context = score['Time Signature Context Skips']
        leaves = iterate(score).by_leaf()
        minimum_leaf_durations_by_measure = \
            self._get_minimum_leaf_durations_by_measure(skip_context, leaves)
        fermata_start_offsets = segment_maker._fermata_start_offsets
        skips = iterate(skip_context).by_leaf(scoretools.Skip)
        for measure_index, skip in enumerate(skips):
            measure_timespan = inspect_(skip).get_timespan()
            if (self.fermata_measure_width is not None and
                measure_timespan.start_offset in fermata_start_offsets):
                duration = self.fermata_measure_width
            else:
                duration = minimum_leaf_durations_by_measure[measure_index]
                if self.minimum_width is not None:
                    if self.minimum_width < duration:
                        duration = self.minimum_width
                if self.multiplier is not None:
                    duration = duration / self.multiplier
            command = indicatortools.LilyPondCommand('newSpacingSection')
            attach(command, skip)
            moment = schemetools.SchemeMoment(duration)
            set_(skip).score.proportional_notation_duration = moment

    ### PRIVATE METHODS ###

    def _get_minimum_leaf_durations_by_measure(self, skip_context, leaves):
        measure_timespans = []
        leaf_durations_by_measure = []
        for skip in skip_context:
            measure_timespan = inspect_(skip).get_timespan()
            measure_timespans.append(measure_timespan)
            leaf_durations_by_measure.append([])
        leaf_timespans = set()
        leaf_count = 0
        for leaf in leaves:
            leaf_timespan = inspect_(leaf).get_timespan()
            leaf_timespans.add(leaf_timespan)
            leaf_count += 1
        measure_index = 0
        measure_timespan = measure_timespans[measure_index]
        leaf_timespans = list(leaf_timespans)
        leaf_timespans.sort(key=lambda _: _.start_offset)
        start_offset = 0
        for leaf_timespan in leaf_timespans:
            leaf_duration = leaf_timespan.duration
            assert start_offset <= leaf_timespan.start_offset
            start_offset = leaf_timespan.start_offset
            if leaf_timespan.starts_during_timespan(measure_timespan):
                leaf_durations_by_measure[measure_index].append(leaf_duration)
            else:
                measure_index += 1
                measure_timespan = measure_timespans[measure_index]
                assert leaf_timespan.starts_during_timespan(measure_timespan)
                leaf_durations_by_measure[measure_index].append(leaf_duration)
        minimum_leaf_durations_by_measure = [
            min(_) for _ in leaf_durations_by_measure
            ]
        return minimum_leaf_durations_by_measure

    ### PUBLIC PROPERTIES ###

    @property
    def fermata_measure_width(self):
        r'''Gets fermata measure width.

        Sets fermata measures to exactly this width when set; ignores minimum
        width and multiplier.

        Defaults to none.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._fermata_measure_width

    @property
    def minimum_width(self):
        r'''Gets minimum width.

        Defaults to none and interprets none equal to ``1/8``.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._minimum_width

    @property
    def multiplier(self):
        r'''Gets multiplier.

        Defaults to none.

        Set to multiplier or none.

        Returns multiplier or none.
        '''
        return self._multiplier

    @property
    def overrides(self):
        r'''Gets overrides.

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._overrides