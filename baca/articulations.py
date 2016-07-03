# -*- coding: utf-8 -*-
import abjad


def accents():
    import baca
    return baca.tools.ArticulationSpecifier(articulations=['>'])

def alternate_accented_bow_strokes():
    import baca
    return baca.tools.ArticulationSpecifier(
        articulations=(['upbow', 'accent'], ['downbow', 'accent']),
        )

def alternate_bow_strokes(downbow_first=True):
    import baca
    if downbow_first:
        return baca.tools.ArticulationSpecifier(
            articulations=(['downbow'], ['upbow']),
            )
    else:
        return baca.tools.ArticulationSpecifier(
            articulations=(['upbow'], ['downbow']),
            )

def down_bows():
    import baca
    return baca.tools.ArticulationSpecifier(articulations=['downbow'])

def double_tonguing():
    import baca
    return baca.tools.ArticulationSpecifier(articulations=['tongue #2'])

def flageolet():
    return abjad.indicatortools.LilyPondCommand(
        'flageolet',
        format_slot='right',
        )

def laissez_vibrer():
    import baca
    return baca.tools.ArticulationSpecifier(articulations=['laissezVibrer'])

def marcati():
    import baca
    # TODO: avoid nontrivial logical ties
    return baca.tools.ArticulationSpecifier(articulations=['marcato'])

def staccati():
    import baca
    # TODO: avoid nontrivial logical ties
    return baca.tools.ArticulationSpecifier(articulations=['staccato'])

def staccatissimi():
    import baca
    # TODO: avoid nontrivial logical ties
    return baca.tools.ArticulationSpecifier(articulations=['staccatissimo'])

def tenuti():
    import baca
    return baca.tools.ArticulationSpecifier(articulations=['tenuto'])

def stem_tremolo():
    import baca
    return baca.tools.StemTremoloSpecifier(tremolo_flags=32)

def tremolo_down(n, maximum_adjustment=-1.5):
    import baca
    pair = (0, -n)
    return experimental.tools.baca.tools.OverrideSpecifier(
        grob_name='stem_tremolo',
        attribute_name='extra_offset',
        attribute_value=str(pair),
        maximum_written_duration=abjad.Duration(1),
        maximum_settings={
            'grob_name': 'stem_tremolo',
            'attribute_name': 'extra_offset',
            'attribute_value': str((0, maximum_adjustment)),
            },
        )

def up_bows():
    import baca
    return baca.tools.ArticulationSpecifier(articulations=['upbow'])