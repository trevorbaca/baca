# -*- coding: utf-8 -*-
from abjad.tools import scoretools
import baca


def stages(stage_start_number, stage_stop_number=None):
    if stage_stop_number is None:
        stage_stop_number = stage_start_number
    return baca.tools.StageExpression(
        stage_start_number=stage_start_number, 
        stage_stop_number=stage_stop_number,
        )

def stage_leaves(stage_number, leaf_start_index=None, leaf_stop_index=None):
    if isinstance(stage_number, int):
        stage_start_number = stage_number
        stage_stop_number = stage_number
    elif isinstance(stage_number, tuple):
        stage_start_number, stage_stop_number = stage_number
    return baca.tools.StageExpression(
        component_start_index=leaf_start_index,
        component_stop_index=leaf_stop_index,
        prototype=scoretools.Leaf,
        stage_start_number=stage_start_number, 
        stage_stop_number=stage_stop_number,
        )