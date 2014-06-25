# -*- encoding: utf-8 -*-
from abjad import *


test_talea_rythm_maker = rhythmmakertools.TaleaRhythmMaker(
    talea=rhythmmakertools.Talea(
        counts=(1, 2, 3, 4),
        denominator=16,
        ),
    )