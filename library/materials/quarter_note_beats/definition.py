# -*- encoding: utf-8 -*-
from abjad import *


quarter_note_beats = rhythmmakertools.DuratedBeatMaker(
    compound_beat_duration=Duration(3, 8),
    fuse_remainder=True,
    remainder_direction=Right,
    simple_beat_duration=Duration(1, 4),
    )