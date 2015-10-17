# -*- coding: utf-8 -*-
import baca
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import patterntools
from abjad.tools import rhythmmakertools
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import sequence


def fuse_compound_quarter_divisions(counts):
    expression = baca.tools.DivisionSequenceExpression()
    expression = expression.split_by_durations(
        compound_meter_multiplier=durationtools.Multiplier((3, 2)),
        durations=[durationtools.Duration(1, 4)],
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

def make_compound_quarter_divisions():
    expression = baca.tools.DivisionSequenceExpression()
    expression = expression.split_by_durations(
        compound_meter_multiplier=durationtools.Multiplier((3, 2)),
        durations=[durationtools.Duration(1, 4)],
        )
    expression = expression.flatten()
    return expression

def make_fused_tuplet_monad_rhythm_specifier(tuplet_ratio=None):
    if tuplet_ratio is None:
        tuplet_ratios = [(1,)]
    else:
        tuplet_ratios = [tuplet_ratio]
    return baca.tools.RhythmSpecifier(
        division_expression=sequence()
            .sum()
            .sequence()
            ,
        rhythm_maker=rhythmmakertools.TupletRhythmMaker(
            tie_specifier=rhythmmakertools.TieSpecifier(
                use_messiaen_style_ties=True,
                ),
            tuplet_ratios=tuplet_ratios,
            ),
        )

def make_messiaen_note_rhythm_specifier():
    return baca.tools.RhythmSpecifier(
        rewrite_meter=True,
        rhythm_maker=rhythmmakertools.NoteRhythmMaker(
            tie_specifier=rhythmmakertools.TieSpecifier(
                use_messiaen_style_ties=True,
                ),
            ),
        )

def make_messiaen_tied_note_rhythm_specifier():
    return baca.tools.RhythmSpecifier(
        rewrite_meter=True,
        rhythm_maker=rhythmmakertools.NoteRhythmMaker(
            tie_specifier=rhythmmakertools.TieSpecifier(
                tie_across_divisions=True,
                use_messiaen_style_ties=True,
                ),
            ),
        )

def make_multimeasure_rest_rhythm_specifier():
    mask = rhythmmakertools.SilenceMask(
        pattern=patterntools.select_all(),
        use_multimeasure_rests=True,
        )
    return baca.tools.RhythmSpecifier(
        rhythm_maker=rhythmmakertools.NoteRhythmMaker(
            division_masks=[mask],
            ),
        )

def make_note_rhythm_specifier():
    return baca.tools.RhythmSpecifier(
        rewrite_meter=True,
        rhythm_maker=rhythmmakertools.NoteRhythmMaker()
        )

def make_repeated_duration_rhythm_specifier(durations):
    if isinstance(durations, durationtools.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [durationtools.Duration(durations)]
    return baca.tools.RhythmSpecifier(
        division_expression=sequence()
            .sum()
            .sequence()
            .split(durations, cyclic=True, overhang=True)
            .flatten()
            ,
        rewrite_meter=True,
        rhythm_maker=rhythmmakertools.NoteRhythmMaker(
            tie_specifier=rhythmmakertools.TieSpecifier(
                use_messiaen_style_ties=True,
                ),
            ),
        )

def make_rest_rhythm_specifier():
    mask = rhythmmakertools.SilenceMask(
        pattern=patterntools.select_all(),
        )
    return baca.tools.RhythmSpecifier(
        rhythm_maker=rhythmmakertools.NoteRhythmMaker(
            division_masks=[mask],
            ),
        )

def make_single_attack_rhythm_specifier(duration):
    duration = durationtools.Duration(duration)
    numerator, denominator = duration.pair
    rhythm_maker = rhythmmakertools.IncisedRhythmMaker(
        incise_specifier=rhythmmakertools.InciseSpecifier(
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

def make_strict_quarter_divisions():
    expression = baca.tools.DivisionSequenceExpression()
    expression = expression.split_by_durations(
        durations=[durationtools.Duration(1, 4)]
        )
    expression = expression.flatten()
    return expression

def make_single_taper_rhythm_specifier(
    denominator=16,
    start_talea=[4],
    stop_talea=[3, -1],
    ):
    return baca.tools.RhythmSpecifier(
        rhythm_maker=rhythmmakertools.IncisedRhythmMaker(
            incise_specifier = rhythmmakertools.InciseSpecifier(
                outer_divisions_only=True,
                prefix_talea=start_talea,
                prefix_counts=[len(start_talea)],
                suffix_talea=stop_talea,
                suffix_counts=[len(stop_talea)],
                talea_denominator=denominator,
                ),
            tie_specifier=rhythmmakertools.TieSpecifier(
                tie_consecutive_notes=True,
                use_messiaen_style_ties=True,
                ),
            ),
        )

def make_tied_repeated_duration_rhythm_specifier(durations):
    specifier = make_repeated_duration_rhythm_specifier(durations)
    specifier = new(
        specifier,
        rewrite_meter=False,
        rhythm_maker__tie_specifier__tie_across_divisions=True,
        )
    return specifier

def split_by_durations(durations):
    durations = [durationtools.Duration(_) for _ in durations]
    expression = sequence()
    expression = expression.flatten()
    expression = expression.sum()
    expression = expression.sequence()
    expression = expression.split(durations, cyclic=True, overhang=True)
    expression = expression.flatten()
    return expression