# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *


quarter_note_divisions = makertools.DivisionMaker(
    cyclic=True,
    pattern=[(1, 4)],
    pattern_rotation_index=0,
    remainder=Right,
    )