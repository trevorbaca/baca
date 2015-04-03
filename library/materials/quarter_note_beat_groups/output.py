# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools
from experimental.tools import makertools


quarter_note_beat_groups = makertools.BeatGroupDivisionMaker(
    beat_grouper=rhythmmakertools.BeatGrouper(
        counts=[2],
        fuse_remainder=True,
        remainder_direction=Left,
        ),
    beat_maker=rhythmmakertools.DurationBeatMaker(
        compound_beat_duration=durationtools.Duration(3, 8),
        fuse_remainder=True,
        remainder_direction=Right,
        simple_beat_duration=durationtools.Duration(1, 4),
        ),
    )