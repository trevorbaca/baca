# -*- coding: utf-8 -*-
import baca


def test_pitchtools_PitchArrayColumn_has_voice_crossing_01():

    array = baca.tools.PitchArray([
        [1, (2, 1), (-1.5, 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bqf     ]
    [g'      ] [fs'] []
    '''

    assert not array.columns[0].has_voice_crossing
    assert array.columns[1].has_voice_crossing
    assert array.columns[2].has_voice_crossing
    assert not array.columns[3].has_voice_crossing
