# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from experimental.tools import makertools


full_measure_divisions = makertools.SplitByDurationsDivisionCallback(
    compound_meter_multiplier=durationtools.Multiplier(1, 1),
    )