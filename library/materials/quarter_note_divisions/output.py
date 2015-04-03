# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from experimental.tools import makertools


quarter_note_divisions = makertools.DivisionMaker(
    pattern=(
        durationtools.Division(1, 4),
        ),
    )