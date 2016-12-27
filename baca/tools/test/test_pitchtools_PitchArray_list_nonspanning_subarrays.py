# -*- coding: utf-8 -*-
import baca


def test_pitchtools_PitchArray_list_nonspanning_subarrays_01():

    array = baca.tools.PitchArray([
        [2, 2, 3, 1],
        [1, 2, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])

    '''
    [      ] [      ] [            ] []
    [] [      ] [] [] [      ] []
    [] [] [] [] [] [] [] []
    '''

    subarrays = array.list_nonspanning_subarrays()

    '''
    [      ] [      ]
    [] [      ] []
    [] [] [] []
    '''

    assert subarrays[0] == baca.tools.PitchArray(
        [[2, 2], [1, 2, 1], [1, 1, 1, 1]])

    '''
    [            ]
    [] [      ]
    [] [] []
    '''

    assert subarrays[1] == baca.tools.PitchArray([[3], [1, 2], [1, 1, 1]])

    '''
    []
    []
    []
    '''

    assert subarrays[2] == baca.tools.PitchArray([[1], [1], [1]])
