# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools


vanilla_accelerandi = rhythmmakertools.AccelerandoRhythmMaker(
    start_duration=durationtools.Duration(1, 4),
    stop_duration=durationtools.Duration(1, 16),
    written_duration=durationtools.Duration(1, 8),
    )