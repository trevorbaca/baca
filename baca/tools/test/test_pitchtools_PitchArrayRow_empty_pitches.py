# -*- coding: utf-8 -*-
import baca


def test_pitchtools_PitchArrayRow_empty_pitches_01():

    array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(0)
    array[0].cells[1].append_pitch(2)
    array[1].cells[2].append_pitch(4)

    '''
    [c'] [d'     ] [  ]
    [         ] [] [e']
    '''

    array[0].empty_pitches()

    '''
    [] [      ] [  ]
    [      ] [] [e']
    '''

    assert array[0].dimensions == (1, 4)
    assert array[0].cell_widths == (1, 2, 1)
    assert array[0].pitches == ()
