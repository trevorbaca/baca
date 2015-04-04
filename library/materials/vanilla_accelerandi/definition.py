# -*- encoding: utf-8 -*-
from abjad import *


vanilla_accelerandi = rhythmmakertools.AccelerandoRhythmMaker(
    start_duration=Duration(1, 4),
    stop_duration=Duration(1, 16),
    written_duration=Duration(1, 8),
    )