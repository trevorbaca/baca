# -*- coding: utf-8 -*-


def stages(stage_start_number, stage_stop_number=None):
    import baca
    if stage_stop_number is None:
        stage_stop_number = stage_start_number
    return baca.tools.StageExpression(
        stage_start_number=stage_start_number, 
        stage_stop_number=stage_stop_number,
        )