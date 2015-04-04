# -*- encoding: utf-8 -*-
from abjad import *


sixteenth_note_accelerandi = rhythmmakertools.AccelerandoRhythmMaker(
    start_duration=Duration(1, 16),
    stop_duration=Duration(1, 32),
    written_duration=Duration(1, 16),
    )