# -*- coding: utf-8 -*-
import baca


def test_pitchtools_PitchArrayCell_indices_01():

    array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert array[0].cells[0].indices == (0, (0,))
    assert array[0].cells[1].indices == (0, (1, 2))
    assert array[0].cells[2].indices == (0, (3,))

    assert array[1].cells[0].indices == (1, (0, 1))
    assert array[1].cells[1].indices == (1, (2,))
    assert array[1].cells[2].indices == (1, (3,))
