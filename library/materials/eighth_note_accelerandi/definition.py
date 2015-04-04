# -*- encoding: utf-8 -*-
from abjad import *


eighth_note_accelerandi = rhythmmakertools.AccelerandoRhythmMaker(
    start_duration=Duration(1, 8),
    stop_duration=Duration(1, 16),
    written_duration=Duration(1, 8),
    )