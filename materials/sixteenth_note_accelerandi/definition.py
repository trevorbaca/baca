# -*- encoding: utf-8 -*-
from abjad import *


sixteenth_note_accelerandi = rhythmmakertools.AccelerandoRhythmMaker(
    beam_specifier=rhythmmakertools.BeamSpecifier(
        use_feather_beams=True,
        ),
    interpolation_specifiers=rhythmmakertools.InterpolationSpecifier(
        start_duration=Duration(1, 16),
        stop_duration=Duration(1, 32),
        written_duration=Duration(1, 16),
        ),
    tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
        use_note_duration_bracket=True,
        ),
    )