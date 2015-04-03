# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools


quarter_note_beats = rhythmmakertools.DuratedBeatMaker(
    compound_beat_duration=durationtools.Duration(3, 8),
    fuse_remainder=True,
    remainder_direction=Right,
    simple_beat_duration=durationtools.Duration(1, 4),
    )