# -*- coding: utf-8 -*-
import abjad
import baca
import numbers


class Library(object):
    r'''Library.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def accents():
        r'''Accents every pitched head.

        ..  container:: example

            ::

                >>> figure_maker = baca.FigureMaker()
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.accents(),
                ...     baca.rests_around([2], [3]),
                ...     talea_counts=[1, 1, 5],
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8
                                c'16 -\accent [
                                d'16 -\accent ]
                                bf'4 -\accent ~
                                bf'16
                            }
                            {
                                fs''16 -\accent [
                                e''16 -\accent ]
                                ef''4 -\accent ~
                                ef''16 [
                                af''16 -\accent
                                g''16 -\accent ]
                            }
                            {
                                a'16 -\accent
                                r8.
                            }
                        }
                    }
                >>

        '''
        return baca.tools.ArticulationSpecifier(
            articulations=['>'],
            )

    @staticmethod
    def alternate_accented_bow_strokes():
        return baca.tools.ArticulationSpecifier(
            articulations=(['upbow', 'accent'], ['downbow', 'accent']),
            )

    @staticmethod
    def alternate_bow_strokes(downbow_first=True):
        if downbow_first:
            return baca.tools.ArticulationSpecifier(
                articulations=(['downbow'], ['upbow']),
                )
        else:
            return baca.tools.ArticulationSpecifier(
                articulations=(['upbow'], ['downbow']),
                )

    @staticmethod
    def anchor(remote_voice_name, remote_selector=None, local_selector=None):
        return baca.tools.AnchorSpecifier(
            local_selector=local_selector,
            remote_selector=remote_selector,
            remote_voice_name=remote_voice_name,
            )

    @staticmethod
    def anchor_after(
        remote_voice_name,
        remote_selector=None,
        local_selector=None,
        ):
        return baca.tools.AnchorSpecifier(
            local_selector=local_selector,
            remote_selector=remote_selector,
            remote_voice_name=remote_voice_name,
            use_remote_stop_offset=True,
            )

    @staticmethod
    def ancora_dynamic(dynamic_name, direction=Down):
        markup = abjad.Markup(dynamic_name).dynamic()
        markup += abjad.Markup('ancora').upright()
        markup = abjad.new(markup, direction=direction)
        return markup

    @staticmethod
    def arpeggiate_down(pattern=None):
        return baca.tools.ArpeggiationSpacingSpecifier(
            direction=Down,
            pattern=pattern,
            )

    @staticmethod
    def arpeggiate_up(pattern=None):
        return baca.tools.ArpeggiationSpacingSpecifier(
            direction=Up,
            pattern=pattern,
            )

    @staticmethod
    def arpeggios():
        return baca.tools.ArticulationSpecifier(articulations=['arpeggio'])

    @staticmethod
    def bass_to_octave(octave_number):
        return baca.tools.RegisterToOctaveSpecifier(
            anchor=Bottom,
            octave_number=octave_number,
            )

    @staticmethod
    def beam_divisions(beam_rests=False):
        return abjad.rhythmmakertools.BeamSpecifier(
            beam_each_division=True,
            beam_rests=beam_rests,
            )

    @staticmethod
    def beam_everything():
        return abjad.rhythmmakertools.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=True,
            )

    @staticmethod
    def beam_positions(n):
        assert isinstance(n, (int, float)), repr(n)
        return baca.tools.OverrideSpecifier(
            grob_name='beam',
            attribute_name='positions',
            attribute_value=str((n, n)),
            )

    @staticmethod
    def center_to_octave(octave_number):
        return baca.tools.RegisterToOctaveSpecifier(
            anchor=Center,
            octave_number=octave_number,
            )

    @staticmethod
    def chord_spacing_down(
        bass=None,
        pattern=None,
        semitones=None,
        soprano=None,
        ):
        return baca.tools.ChordalSpacingSpecifier(
            bass=bass,
            direction=Down,
            minimum_semitones=semitones,
            pattern=pattern,
            soprano=soprano,
            )

    @staticmethod
    def chord_spacing_up(
        bass=None,
        pattern=None,
        semitones=None,
        soprano=None,
        ):
        return baca.tools.ChordalSpacingSpecifier(
            bass=bass,
            direction=Up,
            minimum_semitones=semitones,
            pattern=pattern,
            soprano=soprano,
            )

    @staticmethod
    def clef(name):
        clef = abjad.Clef(name)
        return baca.wrap_leaves(clef)

    @staticmethod
    def clef_spanner(clef='percussion'):
        return abjad.ClefSpanner(clef=clef)

    @staticmethod
    def coat(argument):
        r'''Coats `argument`.
        '''
        return baca.tools.Coat(argument)

    @staticmethod
    def compound_quarter_divisions():
        expression = baca.tools.DivisionSequenceExpression()
        expression = expression.split_by_durations(
            compound_meter_multiplier=abjad.Multiplier((3, 2)),
            durations=[abjad.Duration(1, 4)],
            )
        expression = expression.flatten()
        return expression

    @staticmethod
    def constellate(cells, range, flatten=True):
        '''Constellates `cells` in `range`.

        ..  container:: example

            ::

                >>> pitches = [[0, 2, 10], [16, 19, 20]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.constellate(pitches, range_)
                >>> for segment in segments:
                ...     segment
                Sequence([0, 2, 4, 7, 8, 10])
                Sequence([0, 2, 10, 16, 19, 20])
                Sequence([0, 2, 10, 28, 31, 32])
                Sequence([4, 7, 8, 12, 14, 22])
                Sequence([12, 14, 16, 19, 20, 22])
                Sequence([12, 14, 22, 28, 31, 32])
                Sequence([4, 7, 8, 24, 26, 34])
                Sequence([16, 19, 20, 24, 26, 34])
                Sequence([24, 26, 28, 31, 32, 34])

        ..  container:: example

            ::

                >>> pitches = [[4, 8, 11], [7, 15, 17]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.constellate(pitches, range_)
                >>> for segment in segments:
                ...     segment
                Sequence([4, 7, 8, 11, 15, 17])
                Sequence([4, 8, 11, 19, 27, 29])
                Sequence([7, 15, 16, 17, 20, 23])
                Sequence([16, 19, 20, 23, 27, 29])
                Sequence([7, 15, 17, 28, 32, 35])
                Sequence([19, 27, 28, 29, 32, 35])

        Returns outer product of octave transpositions of `cells` in `range`.
        '''
        if not isinstance(range, abjad.PitchRange):
            message = 'must be pitch range: {!r}.'
            message = message.format(range)
            raise TypeError(message)
        transposition_list = []
        for cell in cells:
            transpositions = range.list_octave_transpositions(cell)
            transposition_list.append(transpositions)
        enumeration = abjad.sequencetools.Enumeration(transposition_list)
        result = enumeration.yield_outer_product()
        result = list(result)
        if flatten:
            for i, part in enumerate(result):
                result[i] = baca.Sequence(part).flatten()
        for i, cell in enumerate(result[:]):
            result[i] = cell.sort()
        return result

    @staticmethod
    def cross_note_heads():
        return baca.tools.OverrideSpecifier(
            grob_name='note_head',
            attribute_name='style',
            attribute_value="'cross'",
            )

    @staticmethod
    def cross_staff():
        return baca.tools.IndicatorSpecifier(
            indicators=[
                abjad.LilyPondCommand(r'\crossStaff'),
                ])

    @staticmethod
    def displacement(displacements):
        return baca.tools.OctaveDisplacementSpecifier(
            displacements=displacements,
            )

    @staticmethod
    def double_tonguing():
        return baca.tools.ArticulationSpecifier(articulations=['tongue #2'])

    @staticmethod
    def down_arpeggios():
        return baca.tools.IndicatorSpecifier(
            indicators=[
                abjad.Arpeggio(direction=Down),
                ])

    @staticmethod
    def down_bows():
        return baca.tools.ArticulationSpecifier(articulations=['downbow'])

    @staticmethod
    def dynamic_first_note(dynamic):
        dynamic = abjad.Dynamic(dynamic)
        return baca.tools.DynamicSpecifier(
            dynamic=dynamic,
            selector=baca.select_pitched_leaf(n=0),
            )

    @staticmethod
    def dynamic_line_spanner_staff_padding(n):
        return baca.tools.OverrideSpecifier(
            grob_name='dynamic_line_spanner',
            attribute_name='staff_padding',
            attribute_value=str(n),
            )

    @staticmethod
    def dynamic_line_spanner_up():
        return baca.tools.OverrideSpecifier(
            grob_name='dynamic_line_spanner',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def dynamics_down():
        return baca.tools.IndicatorSpecifier(
            indicators=[
                abjad.LilyPondCommand('dynamicDown'),
                ],
            selector=baca.select_leaf(0),
            )

    @staticmethod
    def dynamics_up():
        return baca.tools.IndicatorSpecifier(
            indicators=[
                abjad.LilyPondCommand('dynamicUp'),
                ],
            selector=baca.select_leaf(0),
            )

    @staticmethod
    def effort_dynamic(dynamic_name, direction=Down):
        # overriding font-name to false makes sure that
        # the LilyPond \dynamic command works correctly
        # in the case that TextScript.font-name is overridden score-globally
        left_quotes = abjad.Markup('“').italic().larger()
        dynamic_markup = abjad.Markup(dynamic_name)
        dynamic_markup = dynamic_markup.override(('font-name', False))
        dynamic_markup = dynamic_markup.dynamic()
        right_quotes = abjad.Markup('”').italic().larger()
        markup = left_quotes + dynamic_markup + right_quotes
        markup = abjad.new(markup, direction=direction)
        return markup

    @staticmethod
    def even_run_rhythm_specifier():
        return baca.tools.RhythmSpecifier(
            rhythm_maker=abjad.rhythmmakertools.EvenRunRhythmMaker()
            )

    @staticmethod
    def five_line_staff():
        return abjad.StaffLinesSpanner(lines=5)

    @staticmethod
    def fixed_pitches(source):
        return baca.tools.ScorePitchSpecifier(
            acyclic=True,
            source=source,
            )

    @staticmethod
    def flageolet():
        return abjad.LilyPondCommand(
            'flageolet',
            format_slot='right',
            )

    @staticmethod
    def flags():
        return abjad.rhythmmakertools.BeamSpecifier(
            beam_divisions_together=False,
            beam_each_division=False,
            )

    @staticmethod
    def fuse_compound_quarter_divisions(counts):
        expression = baca.tools.DivisionSequenceExpression()
        expression = expression.split_by_durations(
            compound_meter_multiplier=abjad.Multiplier((3, 2)),
            durations=[abjad.Duration(1, 4)],
            )
        expression = expression.flatten()
        expression = expression.partition_by_counts(
            counts=counts,
            cyclic=True,
            overhang=True,
            )
        expression = expression.map()
        expression = expression.sum()
        expression = expression.flatten()
        return expression

    @staticmethod
    def fused_tuplet_monad_rhythm_specifier(tuplet_ratio=None):
        if tuplet_ratio is None:
            tuplet_ratios = [(1,)]
        else:
            tuplet_ratios = [tuplet_ratio]
        return baca.tools.RhythmSpecifier(
            division_expression=abjad.sequence()
                .sum()
                .sequence()
                ,
            rhythm_maker=abjad.rhythmmakertools.TupletRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    use_messiaen_style_ties=True,
                    ),
                tuplet_ratios=tuplet_ratios,
                ),
            )

    @staticmethod
    def glissandi():
        return baca.tools.GlissandoSpecifier(
            pattern=abjad.select_last(1, inverted=True),
            )

    @staticmethod
    def grid_poss_to_flaut_poss():
        left_text = abjad.Markup('grid. possibile').italic().larger() + abjad.Markup.hspace(1)
        right_text = abjad.Markup.hspace(1) + abjad.Markup('flaut. possibile')
        right_text = right_text.italic().larger()
        grid_poss_to_flaut_poss = abjad.TextSpanner(
            overrides = {
                'text_spanner__bound_details__left__padding': -1,
                'text_spanner__bound_details__left__stencil_align_dir_y': 0,
                'text_spanner__bound_details__left__text': left_text,
                'text_spanner__bound_details__left_broken__text': None,
                'text_spanner__bound_details__right__arrow': True,
                'text_spanner__bound_details__right__padding': 1,
                'text_spanner__bound_details__right__stencil_align_dir_y': 0,
                'text_spanner__bound_details__right__text': right_text,
                'text_spanner__bound_details__right_broken__padding': 0,
                'text_spanner__bound_details__right_broken__text': None,
                'text_spanner__dash_fraction': 0.25,
                'text_spanner__dash_period': 1.5,
            }
        )

    @staticmethod
    def hairpins(
        hairpin_tokens, 
        enchain_hairpins=None,
        flare=None,
        include_following_rests=None,
        omit_lone_note_dynamic=None,
        span='contiguous notes and chords',
        ):
        hairpin_tokens_ = []
        for hairpin_token in hairpin_tokens:
            if isinstance(hairpin_token, str):
                hairpin_token = hairpin_token.split()
                hairpin_token = tuple(hairpin_token)
            hairpin_tokens_.append(hairpin_token)
        hairpin_tokens = hairpin_tokens_
        return baca.tools.HairpinSpecifier(
            enchain_hairpins=enchain_hairpins,
            flare=flare,
            hairpin_tokens=hairpin_tokens,
            include_following_rests=include_following_rests,
            omit_lone_note_dynamic=omit_lone_note_dynamic,
            span=span,
            )

    @staticmethod
    def helianthate(sequence, n=0, m=0):
        '''Helianthates `sequence` by outer index of rotation `n` and inner
        index of rotation `m`.

        ..  container:: example

            Helianthates list of lists:

            ::

                >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
                >>> sequence = baca.helianthate(sequence, n=-1, m=1)
                >>> for item in sequence:
                ...     item
                [1, 2, 3]
                [4, 5]
                [6, 7, 8]
                [5, 4]
                [8, 6, 7]
                [3, 1, 2]
                [7, 8, 6]
                [2, 3, 1]
                [4, 5]
                [1, 2, 3]
                [5, 4]
                [6, 7, 8]
                [4, 5]
                [8, 6, 7]
                [3, 1, 2]
                [7, 8, 6]
                [2, 3, 1]
                [5, 4]

        ..  container:: example

            Helianthates list of segments:

            ::

                >>> J = abjad.PitchClassSegment(items=[0, 2, 4])
                >>> K = abjad.PitchClassSegment(items=[5, 6])
                >>> L = abjad.PitchClassSegment(items=[7, 9, 11])
                >>> sequence = baca.helianthate([J, K, L], n=-1, m=1)
                >>> for item in sequence:
                ...     item
                ...
                PitchClassSegment([0, 2, 4])
                PitchClassSegment([5, 6])
                PitchClassSegment([7, 9, 11])
                PitchClassSegment([6, 5])
                PitchClassSegment([11, 7, 9])
                PitchClassSegment([4, 0, 2])
                PitchClassSegment([9, 11, 7])
                PitchClassSegment([2, 4, 0])
                PitchClassSegment([5, 6])
                PitchClassSegment([0, 2, 4])
                PitchClassSegment([6, 5])
                PitchClassSegment([7, 9, 11])
                PitchClassSegment([5, 6])
                PitchClassSegment([11, 7, 9])
                PitchClassSegment([4, 0, 2])
                PitchClassSegment([9, 11, 7])
                PitchClassSegment([2, 4, 0])
                PitchClassSegment([6, 5])

        ..  container:: example

            Trivial helianthation:

            ::

                >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
                >>> baca.helianthate(sequence)
                [[1, 2, 3], [4, 5], [6, 7, 8]]

        Returns new object with type equal to that of `sequence`.
        '''
        sequence_type = type(sequence)
        start = list(sequence[:])
        result = list(sequence[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m
        def _generalized_rotate(argument, n=0):
            if hasattr(argument, 'rotate'):
                return argument.rotate(n=n)
            argument_type = type(argument)
            argument = baca.Sequence(argument).rotate(n=n)
            return argument_type(argument)
        while True:
            inner = [_generalized_rotate(_, m) for _ in sequence]
            candidate = _generalized_rotate(inner, n)
            if candidate == start:
                break
            result.extend(candidate)
            n += original_n
            m += original_m
        result = sequence_type(result)
        return result

    @staticmethod
    def imbricate(
        voice_name,
        segment,
        *specifiers,
        allow_unused_pitches=None,
        extend_beam=None,
        hocket=None,
        selector=None,
        truncate_ties=None
        ):
        return baca.tools.ImbricationSpecifier(
            voice_name,
            segment,
            *specifiers,
            allow_unused_pitches=allow_unused_pitches,
            extend_beam=extend_beam,
            hocket=hocket,
            selector=selector,
            truncate_ties=truncate_ties,
            )

    @staticmethod
    def infinite_pitches(source, repetition_intervals):
        return baca.tools.ScorePitchSpecifier(
            repetition_intervals=repetition_intervals,
            source=source,
            )

    @staticmethod
    def invert(axis=None):
        return baca.tools.ScorePitchSpecifier(
            operators=[
                abjad.Inversion(axis=axis),
                ]
            )

    @staticmethod
    def invert_segments(axis=None):
        operator = baca.pitch_class_segment().invert(axis=axis)
        expression = baca.sequence().map(operator)
        return baca.tools.FigurePitchSpecifier(
            expressions=[expression],
            to_pitch_classes=True,
            )

    @staticmethod
    def laissez_vibrer():
        return baca.tools.ArticulationSpecifier(
            articulations=['laissezVibrer'],
            )

    @staticmethod
    def marcati():
        return baca.tools.ArticulationSpecifier(articulations=['marcato'])

    @staticmethod
    def messiaen_note_rhythm_specifier():
        return baca.tools.RhythmSpecifier(
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def messiaen_tie():
        tie = abjad.Tie(use_messiaen_style_ties=True)
        return baca.tools.SpannerSpecifier(spanner=tie)

    @staticmethod
    def messiaen_tied_note_rhythm_specifier():
        return baca.tools.RhythmSpecifier(
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    tie_across_divisions=True,
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def molto_flaut_to_molto_grid():
        left_text = abjad.Markup('molto flautando').italic().larger() + abjad.Markup.hspace(1)
        right_text = abjad.Markup.hspace(1) + abjad.Markup('molto gridato').italic().larger()
        molto_flaut_to_molto_grid = abjad.TextSpanner(
            overrides = {
                'text_spanner__bound_details__left__padding': -1,
                'text_spanner__bound_details__left__stencil_align_dir_y': 0,
                'text_spanner__bound_details__left__text': left_text,
                'text_spanner__bound_details__left_broken__text': None,
                'text_spanner__bound_details__right__arrow': True,
                'text_spanner__bound_details__right__padding': 1,
                'text_spanner__bound_details__right__stencil_align_dir_y': 0,
                'text_spanner__bound_details__right__text': right_text,
                'text_spanner__bound_details__right_broken__padding': 0,
                'text_spanner__bound_details__right_broken__text': None,
                'text_spanner__dash_fraction': 0.25,
                'text_spanner__dash_period': 1.5,
            }
        )

    @staticmethod
    def multimeasure_rest_rhythm_specifier():
        mask = abjad.rhythmmakertools.SilenceMask(
            pattern=abjad.patterntools.select_all(),
            use_multimeasure_rests=True,
            )
        return baca.tools.RhythmSpecifier(
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                division_masks=[mask],
                ),
            )

    @staticmethod
    def natural_harmonics():
        return baca.tools.OverrideSpecifier(
            grob_name='note_head',
            attribute_name='style',
            attribute_value="'harmonic'",
            )

    @staticmethod
    def nest(time_treatments=None):
        if not isinstance(time_treatments, list):
            time_treatments = [time_treatments]
        return baca.tools.NestingSpecifier(
            lmr_specifier=None,
            time_treatments=time_treatments,
            )

    @staticmethod
    def niente_swell_specifiers(dynamics):
        swell_specifiers = []
        for dynamic in dynamics:
            start_token = 'niente < {}'
            start_token = start_token.format(dynamic)
            stop_token = '{} > niente'
            stop_token = stop_token.format(dynamic)
            swell_specifier = baca.tools.SwellSpecifier(
                start_count=2,
                start_token=start_token,
                stop_count=2,
                stop_token=stop_token,
                )
            swell_specifiers.append(swell_specifier)
        return swell_specifiers

    @staticmethod
    def note_rhythm_specifier():
        return baca.tools.RhythmSpecifier(
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker()
            )

    @staticmethod
    def one_line_staff():
        return abjad.StaffLinesSpanner(lines=1)

    @staticmethod
    def ottava():
        return abjad.OctavationSpanner(start=1, stop=0)

    @staticmethod
    def ottava_bassa():
        return abjad.OctavationSpanner(start=-1, stop=0)

    @staticmethod
    def percussion_staff():
        return abjad.ClefSpanner(clef='percussion')

    @staticmethod
    def pervasive_trills():
        return baca.tools.TrillSpecifier(
            minimum_written_duration=None,
            )

    @staticmethod
    def pervasive_trills_at_interval(interval):
        return baca.tools.TrillSpecifier(
            interval=interval,
            minimum_written_duration=None,
            )

    @staticmethod
    def pervasive_trills_at_pitch(pitch, is_harmonic=None):
        return baca.tools.TrillSpecifier(
            is_harmonic=is_harmonic,
            minimum_written_duration=None,
            pitch=pitch,
            )

    @staticmethod
    def pitches(source, allow_repeat_pitches=True):
        return baca.tools.ScorePitchSpecifier(
            allow_repeat_pitches=True,
            source=source,
            )

    @staticmethod
    def possibile_dynamic(dynamic_name, direction=Down):
        markup = abjad.Markup(dynamic_name).dynamic()
        markup += abjad.Markup('possibile').upright()
        markup = abjad.new(markup, direction=direction)
        return markup

    @staticmethod
    def proportional_notation_duration(duration):
        assert isinstance(duration, tuple), repr(duration)
        assert len(duration) == 2, repr(duration)
        moment = abjad.schemetools.SchemeMoment(duration)
        return baca.tools.SettingSpecifier(
            context_name='score',
            setting_name='proportional_notation_duration',
            setting_value=moment,
            )

    @staticmethod
    def register(start_pitch, stop_pitch=None):
        if stop_pitch is None:
            return baca.tools.RegisterSpecifier(
                registration=abjad.Registration(
                    [('[A0, C8]', start_pitch)],
                    ),
                )
        return baca.tools.RegisterInterpolationSpecifier(
            start_pitch=start_pitch,
            stop_pitch=stop_pitch
            )

    @staticmethod
    def reiterated_dynamic(dynamic_name):
        return baca.tools.ArticulationSpecifier(
            articulations=[dynamic_name],
            )

    @staticmethod
    def remove_duplicate_pitch_classes():
        return baca.tools.FigurePitchSpecifier(
            remove_duplicate_pitch_classes=True,
            )

    @staticmethod
    def remove_duplicate_pitches():
        return baca.tools.FigurePitchSpecifier(
            remove_duplicate_pitches=True,
            )

    @staticmethod
    def repeat_ties_down():
        return baca.tools.OverrideSpecifier(
            grob_name='repeat_tie',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def repeat_ties_up():
        return baca.tools.OverrideSpecifier(
            grob_name='repeat_tie',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def repeated_duration_rhythm_specifier(durations):
        if isinstance(durations, abjad.Duration):
            durations = [durations]
        elif isinstance(durations, tuple):
            assert len(durations) == 2
            durations = [abjad.Duration(durations)]
        return baca.tools.RhythmSpecifier(
            division_expression=abjad.sequence()
                .sum()
                .sequence()
                .split(durations, cyclic=True, overhang=True)
                .flatten()
                ,
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def rest_position(n):
        return baca.tools.OverrideSpecifier(
            grob_name='rest',
            attribute_name='staff_position',
            attribute_value=n,
            )

    @staticmethod
    def rest_rhythm_specifier():
        mask = abjad.rhythmmakertools.SilenceMask(
            pattern=abjad.patterntools.select_all(),
            )
        return baca.tools.RhythmSpecifier(
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                division_masks=[mask],
                ),
            )

    @staticmethod
    def rests_after(counts):
        return baca.tools.RestAffixSpecifier(
            suffix=counts,
            )

    @staticmethod
    def rests_around(prefix, suffix):
        return baca.tools.RestAffixSpecifier(
            prefix=prefix,
            suffix=suffix,
            )

    @staticmethod
    def rests_before(counts):
        return baca.tools.RestAffixSpecifier(
            prefix=counts,
            )

    @staticmethod
    def rests_down():
        return baca.tools.OverrideSpecifier(
            grob_name='rest',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def rests_up():
        return baca.tools.OverrideSpecifier(
            grob_name='rest',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def resume_after(remote_voice_name):
        return baca.tools.AnchorSpecifier(
            remote_selector=baca.select_leaf(-1),
            remote_voice_name=remote_voice_name,
            use_remote_stop_offset=True,
            )

    @staticmethod
    def right_pedal(selector=None):
        return baca.tools.SpannerSpecifier(
            selector=selector,
            spanner=abjad.PianoPedalSpanner(
                style='bracket',
                ),
            )

    @staticmethod
    def scripts_down():
        return baca.tools.OverrideSpecifier(
            grob_name='script',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def scripts_up():
        return baca.tools.OverrideSpecifier(
            grob_name='script',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def select_chord(n=0):
        selector = abjad.select()
        selector = selector.by_class(flatten=True, prototype=abjad.Chord)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def select_leaf(n=0):
        selector = abjad.select()
        selector = selector.by_leaf(flatten=True)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def select_leaves(start=None, stop=None):
        selector = abjad.select()
        selector = selector.by_leaf(flatten=True)
        selector = selector.get_slice(
            start=start,
            stop=stop,
            apply_to_each=False,
            )
        return selector

    @staticmethod
    def select_logical_tie(n=0):
        selector = abjad.select()
        selector = selector.by_logical_tie(flatten=True)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def select_note(n=0):
        selector = abjad.select()
        selector = selector.by_class(flatten=True, prototype=abjad.Note)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def select_pitched_leaf(n=0):
        selector = abjad.select()
        selector = selector.by_leaf(
            flatten=True,
            pitched=True,
            )
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def select_pitched_leaves(start=None, stop=None):
        selector = abjad.select()
        selector = selector.by_leaf(flatten=True, pitched=True)
        selector = selector.get_slice(
            start=start,
            stop=stop,
            apply_to_each=False,
            )
        return selector

    @staticmethod
    def select_pitched_logical_tie(n=0):
        selector = abjad.select()
        selector = selector.by_logical_tie(flatten=True, pitched=True)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def select_pitched_logical_tie_heads():
        selector = abjad.Selector()
        selector = selector.by_logical_tie(pitched=True, flatten=True)
        selector = selector.get_item(0, apply_to_each=True)
        return selector

    @staticmethod
    def select_pitched_logical_ties(n=0):
        selector = abjad.select()
        selector = selector.by_logical_tie(flatten=True, pitched=True)
        if 0 <= n:
            selector = selector.get_slice(stop=n, apply_to_each=False)
        else:
            selector = selector.get_slice(start=n, apply_to_each=False)
        return selector

    @staticmethod
    def select_pitched_runs():
        selector = abjad.select()
        selector = selector.by_leaf()
        selector = selector.by_run(prototype=(abjad.Chord, abjad.Note))
        return selector

    @staticmethod
    def select_rest(n=0):
        selector = abjad.select()
        selector = selector.by_class(flatten=True, prototype=abjad.Rest)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def select_rests(n=0):
        selector = abjad.select()
        selector = selector.by_class(flatten=True, prototype=abjad.Rest)
        if 0 <= n:
            selector = selector.get_slice(stop=n, apply_to_each=False)
        else:
            selector = selector.get_slice(start=n, apply_to_each=False)
        return selector

    @staticmethod
    def select_stages(start, stop=None):
        if stop is None:
            stop = start
        return baca.tools.StageExpression(
            start=start, 
            stop=stop,
            )

    @staticmethod
    def select_tuplets():
        selector = abjad.select()
        selector = selector.by_class(abjad.Tuplet, flatten=True)
        selector = selector.get_slice(apply_to_each=True)
        return selector

    @staticmethod
    def single_attack_rhythm_specifier(duration):
        duration = abjad.Duration(duration)
        numerator, denominator = duration.pair
        rhythm_maker = abjad.rhythmmakertools.IncisedRhythmMaker(
            incise_specifier=abjad.rhythmmakertools.InciseSpecifier(
                fill_with_notes=False,
                outer_divisions_only=True,
                prefix_talea=[numerator],
                prefix_counts=[1],
                talea_denominator=denominator,
                ),
            )
        return baca.tools.RhythmSpecifier(
            rhythm_maker=rhythm_maker,
            )

    @staticmethod
    def single_taper_rhythm_specifier(
        denominator=16,
        start_talea=[4],
        stop_talea=[3, -1],
        ):
        return baca.tools.RhythmSpecifier(
            rhythm_maker=abjad.rhythmmakertools.IncisedRhythmMaker(
                incise_specifier = abjad.rhythmmakertools.InciseSpecifier(
                    outer_divisions_only=True,
                    prefix_talea=start_talea,
                    prefix_counts=[len(start_talea)],
                    suffix_talea=stop_talea,
                    suffix_counts=[len(stop_talea)],
                    talea_denominator=denominator,
                    ),
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    tie_consecutive_notes=True,
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def skips_after(counts):
        return baca.tools.RestAffixSpecifier(
            skips_instead_of_rests=True,
            suffix=counts,
            )

    @staticmethod
    def skips_around(prefix, suffix):
        return baca.tools.RestAffixSpecifier(
            prefix=prefix,
            skips_instead_of_rests=True,
            suffix=suffix,
            )

    @staticmethod
    def skips_before(counts):
        return baca.tools.RestAffixSpecifier(
            prefix=counts,
            skips_instead_of_rests=True,
            )
        
    @staticmethod
    def slur():
        return baca.tools.SpannerSpecifier(spanner=abjad.Slur())

    @staticmethod
    def slur_every_tuplet():
        return baca.tools.SpannerSpecifier(
            selector=abjad.select().
                by_class(abjad.Tuplet, flatten=True).
                get_slice(apply_to_each=True),
            spanner=abjad.Slur(),
            )

    @staticmethod
    def slur_pitched_runs():
        return baca.tools.SpannerSpecifier(
            selector=baca.select_pitched_runs(),
            spanner=abjad.Slur(),
            )

    @staticmethod
    def slurs_down():
        return baca.tools.OverrideSpecifier(
            grob_name='slur',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def slurs_up():
        return baca.tools.OverrideSpecifier(
            grob_name='slur',
            attribute_name='direction',
            attribute_value=Up,
            )
        
    @staticmethod
    def soprano_to_octave(octave_number):
        return baca.tools.RegisterToOctaveSpecifier(
            anchor=Top,
            octave_number=octave_number,
            )

    @staticmethod
    def split_by_durations(durations):
        durations = [abjad.Duration(_) for _ in durations]
        expression = abjad.sequence()
        expression = expression.flatten()
        expression = expression.sum()
        expression = expression.sequence()
        expression = expression.split(durations, cyclic=True, overhang=True)
        expression = expression.flatten()
        return expression

    @staticmethod
    def staccati():
        return baca.tools.ArticulationSpecifier(articulations=['staccato'])

    @staticmethod
    def staccatissimi():
        return baca.tools.ArticulationSpecifier(
            articulations=['staccatissimo'],
            )

    @staticmethod
    def stem_color(color, context_name=None):
        return baca.tools.OverrideSpecifier(
            context_name=context_name,
            grob_name='stem',
            attribute_name='color',
            attribute_value=repr(color),
            )

    @staticmethod
    def stem_tremolo():
        return baca.tools.StemTremoloSpecifier(tremolo_flags=32)

    @staticmethod
    def stems_down():
        return baca.tools.OverrideSpecifier(
            grob_name='stem',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def stems_up():
        return baca.tools.OverrideSpecifier(
            grob_name='stem',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def strict_note_spacing_off():
        return baca.tools.OverrideSpecifier(
            context_name='score',
            grob_name='spacing_spanner',
            attribute_name='strict_note_spacing',
            attribute_value=False,
            )

    @staticmethod
    def strict_quarter_divisions():
        expression = baca.tools.DivisionSequenceExpression()
        expression = expression.split_by_durations(
            durations=[abjad.Duration(1, 4)]
            )
        expression = expression.flatten()
        return expression

    @staticmethod
    def tenuti():
        return baca.tools.ArticulationSpecifier(articulations=['tenuto'])

    @staticmethod
    def text_script_color(color):
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='color',
            attribute_value=repr(color),
            )

    @staticmethod
    def text_script_padding(n):
        assert isinstance(n, numbers.Number), repr(n)
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='padding',
            attribute_value=n,
            )

    @staticmethod
    def text_script_staff_padding(n):
        assert isinstance(n, numbers.Number), repr(n)
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='staff_padding',
            attribute_value=n,
            )

    @staticmethod
    def text_scripts_down():
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def text_scripts_up():
        return baca.tools.OverrideSpecifier(
            grob_name='text_script',
            attribute_name='direction',
            attribute_value=Up,
            )

    @staticmethod
    def text_spanner_staff_padding(n):
        return baca.tools.OverrideSpecifier(
            grob_name='text_spanner',
            attribute_name='staff_padding',
            attribute_value=str(n),
            )

    @staticmethod
    def tie(messiaen=False):
        tie = abjad.Tie(use_messiaen_style_ties=messiaen)
        return baca.tools.SpannerSpecifier(spanner=tie)

    @staticmethod
    def tied_repeated_duration_rhythm_specifier(durations):
        specifier = make_repeated_duration_rhythm_specifier(durations)
        specifier = abjad.new(
            specifier,
            rewrite_meter=False,
            rhythm_maker__tie_specifier__tie_across_divisions=True,
            )
        return specifier

    @staticmethod
    def time_signature_extra_offset(extra_offset_pair):
        assert isinstance(extra_offset_pair, tuple), repr(extra_offset_pair)
        return baca.tools.OverrideSpecifier(
            context_name='score',
            grob_name='time_signature',
            attribute_name='extra_offset',
            attribute_value=extra_offset_pair,
            )

    @staticmethod
    def transition_spanner(start_markup=None, stop_markup=None):
        return baca.tools.TransitionSpecifier(
            start_markup=start_markup,
            stop_markup=stop_markup,
            )

    @staticmethod
    def transpose(n=0):
        return baca.tools.ScorePitchSpecifier(
            operators=[abjad.Transposition(n=n)],
            )

    @staticmethod
    def transpose_segments(n=0):
        operator = baca.pitch_class_segment().transpose(n=n)
        expression = baca.sequence().map(operator)
        return baca.tools.FigurePitchSpecifier(
            expressions=[expression],
            to_pitch_classes=True,
            )

    @staticmethod
    def tremolo_down(n, maximum_adjustment=-1.5):
        pair = (0, -n)
        return experimental.tools.baca.tools.OverrideSpecifier(
            grob_name='stem_tremolo',
            attribute_name='extra_offset',
            attribute_value=str(pair),
            maximum_written_duration=abjad.Duration(1),
            maximum_settings={
                'grob_name': 'stem_tremolo',
                'attribute_name': 'extra_offset',
                'attribute_value': str((0, maximum_adjustment)),
                },
            )

    @staticmethod
    def trill_quarter_notes():
        return baca.tools.TrillSpecifier(
            forbidden_annotations=['color fingering', 'color microtone'],
            minimum_written_duration=durationtools.Duration(1, 4),
            )

    @staticmethod
    def tuplet_bracket_extra_offset(pair):
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_bracket',
            attribute_name='extra_offset',
            attribute_value=pair,
            )

    @staticmethod
    def tuplet_bracket_staff_padding(n):
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_bracket',
            attribute_name='staff_padding',
            attribute_value=str(n),
            )

    @staticmethod
    def tuplet_brackets_down():
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_bracket',
            attribute_name='direction',
            attribute_value=Down,
            )

    @staticmethod
    def tuplet_brackets_up():
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_bracket',
            attribute_name='direction',
            attribute_value=Up,
            )
            
    @staticmethod
    def tuplet_number_extra_offset(pair):
        return baca.tools.OverrideSpecifier(
            grob_name='tuplet_number',
            attribute_name='extra_offset',
            attribute_value=pair,
            )

    @staticmethod
    def two_line_staff():
        return abjad.StaffLinesSpanner(lines=2)

    @staticmethod
    def up_arpeggios():
        return baca.tools.IndicatorSpecifier(
            indicators=[
                abjad.Arpeggio(direction=Up),
                ])

    @staticmethod
    def up_bows():
        return baca.tools.ArticulationSpecifier(articulations=['upbow'])

    @staticmethod
    def wrap_first_leaf(specifier):
        r'''Wraps specifier with first leaf selector.

        Returns specifier wrapper.
        '''
        return baca.wrap_leaf(specifier, n=0)

    @staticmethod
    def wrap_first_note(specifier):
        r'''Wraps specifier with first note or chord selector.

        Returns specifier wrapper.
        '''
        return baca.wrap_note(specifier, n=0)

    @staticmethod
    def wrap_leaf(specifier, n=0):
        r'''Wraps specifier with leaf selector.

        Returns specifier wrapper.
        '''
        prototype = abjad.Leaf
        if 0 < n:
            return baca.tools.SpecifierWrapper(
                prototype=prototype,
                specifier=specifier,
                start_index=n,
                stop_index=n+1,
                )
        elif n == 0:
            return baca.tools.SpecifierWrapper(
                prototype=prototype,
                specifier=specifier,
                stop_index=1
                )
        else:
            return baca.tools.SpecifierWrapper(
                prototype=prototype,
                specifier=specifier,
                start_index=n,
                stop_index=n+1
                )

    @staticmethod
    def wrap_leaves(
        specifier,
        start=None,
        stop=None,
        with_next_leaf=None,
        with_previous_leaf=None,
        ):
        r'''Wraps specifier with leaves selector.

        Returns specifier wrapper.
        '''
        return baca.tools.SpecifierWrapper(
            specifier=specifier,
            start_index=start,
            stop_index=stop,
            with_next_leaf=with_next_leaf,
            with_previous_leaf=with_previous_leaf,
            )

    @staticmethod
    def wrap_note(
        specifier,
        n=0,
        ):
        r'''Wraps specifier with note selector.

        Returns specifier wrapper.
        '''
        if 0 < n:
            return baca.tools.SpecifierWrapper(
                prototype=(abjad.Note, abjad.Chord),
                specifier=specifier,
                start_index=n,
                stop_index=n+1,
                )
        elif n == 0:
            return baca.tools.SpecifierWrapper(
                prototype=(abjad.Note, abjad.Chord),
                specifier=specifier,
                stop_index=1
                )
        else:
            return baca.tools.SpecifierWrapper(
                prototype=(abjad.Note, abjad.Chord),
                specifier=specifier,
                start_index=n,
                stop_index=n+1
                )

    @staticmethod
    def wrap_notes(
        specifier,
        start=None,
        stop=None,
        with_next_leaf=None,
        with_previous_leaf=None,
        ):
        r'''Wraps specifier with notes selector.

        Returns specifier wrapper.
        '''
        return baca.tools.SpecifierWrapper(
            prototype=abjad.Note,
            specifier=specifier,
            start_index=start,
            stop_index=stop,
            with_next_leaf=with_next_leaf,
            with_previous_leaf=with_previous_leaf,
            )
