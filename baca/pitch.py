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

def pitches(source):
    return baca.tools.PitchSpecifier(source=source)