# -*- coding: utf-8 -*-
import baca


def test_pitchtools_PitchArrayRow_has_spanning_cell_over_index_01():

    array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(0)
    array[0].cells[1].append_pitch(2)
    array[1].cells[2].append_pitch(4)

    '''
    [c'] [d'     ] [  ]
    [         ] [] [e']
    '''

    assert not array[0].has_spanning_cell_over_index(0)
    assert not array[0].has_spanning_cell_over_index(1)
    assert array[0].has_spanning_cell_over_index(2)
    assert not array[0].has_spanning_cell_over_index(3)
    assert not array[0].has_spanning_cell_over_index(99)

    assert not array[1].has_spanning_cell_over_index(0)
    assert array[1].has_spanning_cell_over_index(1)
    assert not array[1].has_spanning_cell_over_index(2)
    assert not array[1].has_spanning_cell_over_index(3)
    assert not array[1].has_spanning_cell_over_index(99)
