# -*- coding: utf-8 -*-
import baca


def fixed_pitches(source):
    return baca.tools.PitchSpecifier(
        acyclic=True,
        source=source,
        )

def infinite_pitches(source, repetition_intervals):
    return baca.tools.PitchSpecifier(
        repetition_intervals=repetition_intervals,
        source=source,
        )

# TODO: implement baca.tools.CompoundSpecifier
r'''
def natural_harmonics(source):
    return baca.tools.CompoundSpecifier([
        baca.tools.PitchSpecifier(source=source),
        handlertools.OverrideHandler(
            grob_name='note_head',
            attribute_name='style',
            attribute_value="'harmonic'",
            ),
        ])
'''

def pitches(source):
    return baca.tools.PitchSpecifier(source=source)