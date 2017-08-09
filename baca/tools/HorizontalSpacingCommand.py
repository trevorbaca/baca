# -*- coding: utf-8 -*-
import abjad


class HorizontalSpacingCommand(abjad.AbjadObject):
    r'''Horizontal spacing command.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        No spacing command:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 F4'),
            ...     baca.RhythmSpecifier(
            ...         rhythm_maker=abjad.rhythmmakertools.EvenRunRhythmMaker(),
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
                    \context GlobalSkips = "Global Skips" {
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

        Null spacing command:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingCommand(),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 F4'),
            ...     baca.RhythmSpecifier(
            ...         rhythm_maker=abjad.rhythmmakertools.EvenRunRhythmMaker(),
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
                    \context GlobalSkips = "Global Skips" {
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

        Measurewise proportional spacing based on minimum duration per measure:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingCommand(
            ...         multiplier=abjad.Multiplier(1),
            ...         ),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 F4'),
            ...     baca.RhythmSpecifier(
            ...         rhythm_maker=abjad.rhythmmakertools.EvenRunRhythmMaker(),
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
                    \context GlobalSkips = "Global Skips" {
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

        Measurewise proportional spacing based on twice the minimum duration
        per measure:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingCommand(
            ...         multiplier=abjad.Multiplier(2),
            ...         ),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 F4'),
            ...     baca.RhythmSpecifier(
            ...         rhythm_maker=abjad.rhythmmakertools.EvenRunRhythmMaker(),
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
                    \context GlobalSkips = "Global Skips" {
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

        Measurewise proportional spacing based on twice the minimum duration
        per measure with minimum width equal to an eighth note:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingCommand(
            ...         multiplier=abjad.Multiplier(2),
            ...         minimum_width=abjad.Duration(1, 8),
            ...         ),
            ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 F4'),
            ...     baca.RhythmSpecifier(
            ...         rhythm_maker=abjad.rhythmmakertools.EvenRunRhythmMaker(),
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
                    \context GlobalSkips = "Global Skips" {
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

        Works with accelerando and ritardando figures:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingCommand(
            ...         minimum_width=abjad.Duration(1, 8),
            ...         ),
            ...     time_signatures=[(4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 F4'),
            ...     baca.RhythmSpecifier(
            ...         rhythm_maker=abjad.rhythmmakertools.AccelerandoRhythmMaker(
            ...             beam_specifier=abjad.rhythmmakertools.BeamSpecifier(
            ...             use_feather_beams=True,
            ...                 ),
            ...             interpolation_specifiers=abjad.rhythmmakertools.InterpolationSpecifier(
            ...                 start_duration=abjad.Duration(1, 8),
            ...                 stop_duration=abjad.Duration(1, 20),
            ...                 written_duration=abjad.Duration(1, 16),
            ...                 ),
            ...             tuplet_spelling_specifier=abjad.rhythmmakertools.TupletSpellingSpecifier(
            ...                 use_note_duration_bracket=True,
            ...                 ),
            ...             ),
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
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
                            \newSpacingSection
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)
                            \newSpacingSection
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            \override TupletNumber.text = \markup {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score \with {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            } <<
                                                \new RhythmicStaff \with {
                                                    \remove Time_signature_engraver
                                                    \remove Staff_symbol_engraver
                                                    \override Stem.direction = #up
                                                    \override Stem.length = #5
                                                    \override TupletBracket.bracket-visibility = ##t
                                                    \override TupletBracket.direction = #up
                                                    \override TupletBracket.padding = #1.25
                                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                    tupletFullLength = ##t
                                                } {
                                                    c'2
                                                }
                                            >>
                                            \layout {
                                                indent = #0
                                                ragged-right = ##t
                                            }
                                        }
                                }
                            \times 1/1 {
                                \once \override Beam.grow-direction = #right
                                e'16 * 63/32 [
                                f'16 * 115/64
                                e'16 * 91/64
                                f'16 * 35/32
                                e'16 * 29/32
                                f'16 * 13/16 ]
                            }
                            \revert TupletNumber.text
                            \override TupletNumber.text = \markup {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score \with {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            } <<
                                                \new RhythmicStaff \with {
                                                    \remove Time_signature_engraver
                                                    \remove Staff_symbol_engraver
                                                    \override Stem.direction = #up
                                                    \override Stem.length = #5
                                                    \override TupletBracket.bracket-visibility = ##t
                                                    \override TupletBracket.direction = #up
                                                    \override TupletBracket.padding = #1.25
                                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                    tupletFullLength = ##t
                                                } {
                                                    c'4.
                                                }
                                            >>
                                            \layout {
                                                indent = #0
                                                ragged-right = ##t
                                            }
                                        }
                                }
                            \times 1/1 {
                                \once \override Beam.grow-direction = #right
                                e'16 * 117/64 [
                                f'16 * 99/64
                                e'16 * 69/64
                                f'16 * 13/16
                                e'16 * 47/64 ]
                                \bar "|"
                            }
                            \revert TupletNumber.text
                        }
                    }
                >>
            >>

        Minimum duration in each measure is taken from the **nonmultiplied**
        duration of each note.

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

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
            fermata_measure_width = abjad.Duration(fermata_measure_width)
        self._fermata_measure_width = fermata_measure_width
        if minimum_width is not None:
            minimum_width = abjad.Duration(minimum_width)
        self._minimum_width = minimum_width    
        if multiplier is not None:
            multiplier = abjad.Multiplier(multiplier)
        self._multiplier = multiplier
        if overrides is not None:
            overrides = tuple(overrides)
        self._overrides = overrides

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker=None):
        r'''Calls command on `segment_maker`.

        Returns none.
        '''
        score = segment_maker._score
        skip_context = score['Global Skips']
        leaves = abjad.iterate(score).by_leaf()
        minimum_durations_by_measure = self._get_minimum_durations_by_measure(
            skip_context,
            leaves,
            )
        fermata_start_offsets = getattr(
            segment_maker,
            '_fermata_start_offsets',
            [],
            )
        skips = abjad.iterate(skip_context).by_leaf(abjad.Skip)
        for measure_index, skip in enumerate(skips):
            measure_timespan = abjad.inspect(skip).get_timespan()
            if (self.fermata_measure_width is not None and
                measure_timespan.start_offset in fermata_start_offsets):
                duration = self.fermata_measure_width
            else:
                duration = minimum_durations_by_measure[measure_index]
                if self.minimum_width is not None:
                    if self.minimum_width < duration:
                        duration = self.minimum_width
                if self.multiplier is not None:
                    duration = duration / self.multiplier
            command = abjad.LilyPondCommand('newSpacingSection')
            abjad.attach(command, skip)
            moment = abjad.SchemeMoment(duration)
            abjad.setting(skip).score.proportional_notation_duration = moment

    ### PRIVATE METHODS ###

    def _get_minimum_durations_by_measure(self, skip_context, leaves):
        measure_timespans = []
        durations_by_measure = []
        for skip in skip_context:
            measure_timespan = abjad.inspect(skip).get_timespan()
            measure_timespans.append(measure_timespan)
            durations_by_measure.append([])
        leaf_timespans = set()
        leaf_count = 0
        for leaf in leaves:
            leaf_timespan = abjad.inspect(leaf).get_timespan()
            leaf_duration = leaf_timespan.duration
            prototype = (abjad.Multiplier, abjad.NonreducedFraction)
            multiplier = abjad.inspect(leaf).get_indicator(prototype)
            if multiplier is not None:
                leaf_duration = leaf_duration / multiplier
            pair = (leaf_timespan, leaf_duration)
            leaf_timespans.add(pair)
            leaf_count += 1
        measure_index = 0
        measure_timespan = measure_timespans[measure_index]
        leaf_timespans = list(leaf_timespans)
        leaf_timespans.sort(key=lambda _: _[0].start_offset)
        start_offset = 0
        for pair in leaf_timespans:
            leaf_timespan, leaf_duration = pair
            assert start_offset <= leaf_timespan.start_offset
            start_offset = leaf_timespan.start_offset
            if leaf_timespan.starts_during_timespan(measure_timespan):
                durations_by_measure[measure_index].append(leaf_duration)
            else:
                measure_index += 1
                if len(measure_timespans) <= measure_index:
                    continue
                measure_timespan = measure_timespans[measure_index]
                assert leaf_timespan.starts_during_timespan(measure_timespan)
                durations_by_measure[measure_index].append(leaf_duration)
        minimum_durations_by_measure = [min(_) for _ in durations_by_measure]
        return minimum_durations_by_measure

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
