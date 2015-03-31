# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools


multimeasure_rests = rhythmmakertools.NoteRhythmMaker(
    output_masks=rhythmmakertools.BooleanPatternInventory(
        (
            rhythmmakertools.SilenceMask(
                indices=(0,),
                period=1,
                use_multimeasure_rests=True,
                ),
            )
        ),
    )