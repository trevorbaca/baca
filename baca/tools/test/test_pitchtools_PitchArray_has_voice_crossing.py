# -*- coding: utf-8 -*-
import baca


def test_pitchtools_PitchArray_has_voice_crossing_01():

    array = baca.tools.PitchArray([
        [1, (2, 1), (-1.5, 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bqf     ]
    [g'      ] [fs'] []
    '''

    assert array.has_voice_crossing
