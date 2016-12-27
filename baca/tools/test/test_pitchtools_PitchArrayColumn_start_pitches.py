# -*- coding: utf-8 -*-
import abjad
import baca


def test_pitchtools_PitchArrayColumn_start_pitches_01():

    array = baca.tools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bf bqf     ]
    [g'      ] [fs'    ] []
    '''

    array.columns[0].start_pitches == (abjad.NamedPitch(7), )
    array.columns[1].start_pitches == (abjad.NamedPitch(2), )
    array.columns[2].start_pitches == (
        abjad.NamedPitch(-2), abjad.NamedPitch(-1.5), abjad.NamedPitch(6))
    array.columns[3].start_pitches == ()
