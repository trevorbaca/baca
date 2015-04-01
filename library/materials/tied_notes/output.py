# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools


tied_notes = rhythmmakertools.NoteRhythmMaker(
    tie_specifier=rhythmmakertools.TieSpecifier(
        tie_across_divisions=True,
        use_messiaen_style=True,
        ),
    )