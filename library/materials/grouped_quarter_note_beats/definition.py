# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *


grouped_quarter_note_beats = makertools.BeatGroupDivisionMaker(
    beat_grouper=rhythmmakertools.BeatGrouper(
        counts=[2],
        fuse_remainder=True,
        remainder_direction=Right,
        ),
    beat_maker=rhythmmakertools.DurationBeatMaker(
        compound_beat_duration=Duration(3, 8),
        simple_beat_duration=Duration(1, 4),
        ),
    decrease_durations_monotonically=False,
    )