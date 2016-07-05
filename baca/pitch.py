# -*- coding: utf-8 -*-
import abjad
import baca


def displacement(displacements):
    return baca.tools.OctaveDisplacementSpecifier(
        displacements=displacements,
        )

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

def invert(axis=None):
    return baca.tools.PitchSpecifier(
        operators=[
            abjad.pitchtools.Inversion(axis=axis),
            ]
        )

def pitches(source, allow_repeated_pitches=True):
    return baca.tools.PitchSpecifier(
        allow_repeated_pitches=True,
        source=source,
        )

def register(start_pitch, stop_pitch=None):
    if stop_pitch is None:
        return baca.tools.RegisterSpecifier(
            registration=abjad.pitchtools.Registration(
                [('[A0, C8]', start_pitch)],
                ),
            )
    return baca.tools.RegisterInterpolationSpecifier(
        start_pitch=start_pitch,
        stop_pitch=stop_pitch
        )

def transpose(index=0):
    return baca.tools.PitchSpecifier(
        operators=[
            abjad.pitchtools.Transposition(index),
            ]
        )