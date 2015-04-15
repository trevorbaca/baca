# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools


sixteenth_note_accelerandi = rhythmmakertools.AccelerandoRhythmMaker(
    beam_specifier=rhythmmakertools.BeamSpecifier(
        beam_each_division=True,
        beam_divisions_together=False,
        use_feather_beams=True,
        ),
    interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
        start_duration=durationtools.Duration(1, 16),
        stop_duration=durationtools.Duration(1, 32),
        written_duration=durationtools.Duration(1, 16),
        ),
    tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
        avoid_dots=False,
        flatten_trivial_tuplets=False,
        is_diminution=True,
        simplify_tuplets=False,
        use_note_duration_bracket=True,
        ),
    )