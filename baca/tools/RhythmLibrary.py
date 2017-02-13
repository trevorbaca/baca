# -*- coding: utf-8 -*-
import abjad
import baca


class RhythmLibrary(object):
    r'''Rhythm interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    ### PUBLIC METHODS ###

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
    def make_compound_quarter_divisions():
        expression = baca.tools.DivisionSequenceExpression()
        expression = expression.split_by_durations(
            compound_meter_multiplier=abjad.Multiplier((3, 2)),
            durations=[abjad.Duration(1, 4)],
            )
        expression = expression.flatten()
        return expression

    @staticmethod
    def make_fused_tuplet_monad_rhythm_specifier(tuplet_ratio=None):
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
    def make_even_run_rhythm_specifier():
        return baca.tools.RhythmSpecifier(
            rhythm_maker=abjad.rhythmmakertools.EvenRunRhythmMaker()
            )

    @staticmethod
    def make_messiaen_note_rhythm_specifier():
        return baca.tools.RhythmSpecifier(
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                tie_specifier=abjad.rhythmmakertools.TieSpecifier(
                    use_messiaen_style_ties=True,
                    ),
                ),
            )

    @staticmethod
    def make_messiaen_tied_note_rhythm_specifier():
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
    def make_multimeasure_rest_rhythm_specifier():
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
    def make_note_rhythm_specifier():
        return baca.tools.RhythmSpecifier(
            rewrite_meter=True,
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker()
            )

    @staticmethod
    def make_repeated_duration_rhythm_specifier(durations):
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
    def make_rest_rhythm_specifier():
        mask = abjad.rhythmmakertools.SilenceMask(
            pattern=abjad.patterntools.select_all(),
            )
        return baca.tools.RhythmSpecifier(
            rhythm_maker=abjad.rhythmmakertools.NoteRhythmMaker(
                division_masks=[mask],
                ),
            )

    @staticmethod
    def make_single_attack_rhythm_specifier(duration):
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
    def make_strict_quarter_divisions():
        expression = baca.tools.DivisionSequenceExpression()
        expression = expression.split_by_durations(
            durations=[abjad.Duration(1, 4)]
            )
        expression = expression.flatten()
        return expression

    @staticmethod
    def make_single_taper_rhythm_specifier(
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
    def make_tied_repeated_duration_rhythm_specifier(durations):
        specifier = make_repeated_duration_rhythm_specifier(durations)
        specifier = abjad.new(
            specifier,
            rewrite_meter=False,
            rhythm_maker__tie_specifier__tie_across_divisions=True,
            )
        return specifier

    @staticmethod
    def nest(time_treatments=None):
        if not isinstance(time_treatments, list):
            time_treatments = [time_treatments]
        return baca.tools.NestingSpecifier(
            lmr_specifier=None,
            time_treatments=time_treatments,
            )

    @staticmethod
    def rests_after(counts, denominator=16):
        return baca.tools.RestAffixSpecifier(
            denominator=denominator,
            suffix=counts,
            )

    @staticmethod
    def rests_around(prefix, suffix, denominator=16):
        return baca.tools.RestAffixSpecifier(
            denominator=denominator,
            prefix=prefix,
            suffix=suffix,
            )

    @staticmethod
    def rests_before(counts, denominator=16):
        return baca.tools.RestAffixSpecifier(
            denominator=denominator,
            prefix=counts,
            )

    @staticmethod
    def skips_after(counts, denominator=16):
        return baca.tools.RestAffixSpecifier(
            denominator=denominator,
            skips_instead_of_rests=True,
            suffix=counts,
            )

    @staticmethod
    def skips_around(prefix, suffix, denominator=16):
        return baca.tools.RestAffixSpecifier(
            denominator=denominator,
            prefix=prefix,
            skips_instead_of_rests=True,
            suffix=suffix,
            )

    @staticmethod
    def skips_before(counts, denominator=16):
        return baca.tools.RestAffixSpecifier(
            denominator=denominator,
            prefix=counts,
            skips_instead_of_rests=True,
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
