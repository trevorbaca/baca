# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *


paired_quarter_note_beats = makertools.BeatGroupDivisionMaker(
    beat_grouper=rhythmmakertools.BeatGrouper(
        counts=[2],
        fuse_remainder=True,
        remainder_direction=Left,
        ),
    beat_maker=rhythmmakertools.DuratedBeatMaker(
        compound_beat_duration=Duration(3, 8),
        fuse_remainder=True,
        remainder_direction=Right,
        simple_beat_duration=Duration(1, 4),
        ),
    )