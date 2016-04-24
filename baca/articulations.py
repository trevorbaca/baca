# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools


def accents(pattern=None):
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['>'],
        pattern=pattern,
        )

def alternate_accented_bow_strokes():
    import baca
    return baca.tools.PatternedArticulationsHandler(
        articulation_lists=(['upbow', 'accent'], ['downbow', 'accent']),
        )

def alternate_bow_strokes(downbow_first=True):
    import baca
    if downbow_first:
        return baca.tools.PatternedArticulationsHandler(
            articulation_lists=(['downbow'], ['upbow']),
            )
    else:
        return baca.tools.PatternedArticulationsHandler(
            articulation_lists=(['upbow'], ['downbow']),
            )

def down_bows():
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['downbow'],
        )

def double_tonguing():
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['tongue #2'],
        )

def flageolet():
    return indicatortools.LilyPondCommand('flageolet', format_slot='right')

def laissez_vibrer(pattern=None):
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['laissezVibrer'],
        pattern=pattern,
        )

def marcati():
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['marcato'],
        skip_ties=True,
        )

def staccati():
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['staccato'],
        maximum_duration=durationtools.Duration(1, 2),
        skip_ties=True,
        )

def staccatissimi():
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['staccatissimo'],
        skip_ties=True,
        )

def tenuti():
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['tenuto'],
        )

def stem_tremolo(pattern=None):
    import baca
    return baca.tools.StemTremoloHandler(
        hash_mark_counts=[32],
        pattern=pattern,
        )

def tremolo_down(n, maximum_adjustment=-1.5):
    import baca
    pair = (0, -n)
    return experimental.tools.baca.tools.OverrideHandler(
        grob_name='stem_tremolo',
        attribute_name='extra_offset',
        attribute_value=str(pair),
        maximum_written_duration=durationtools.Duration(1),
        maximum_settings={
            'grob_name': 'stem_tremolo',
            'attribute_name': 'extra_offset',
            'attribute_value': str((0, maximum_adjustment)),
            },
        )

def up_bows():
    import baca
    return baca.tools.ReiteratedArticulationHandler(
        articulation_list=['upbow'],
        )