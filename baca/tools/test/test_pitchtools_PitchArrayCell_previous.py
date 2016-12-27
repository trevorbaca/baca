# -*- coding: utf-8 -*-
import abjad
import baca
import pytest


def test_pitchtools_PitchArrayCell_previous_01():

    array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert array[0][1].previous is array[0][0]


def test_pitchtools_PitchArrayCell_previous_02():

    array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert pytest.raises(IndexError, 'array[0][0].previous')


def test_pitchtools_PitchArrayCell_previous_03():

    cell = baca.tools.PitchArrayCell([abjad.NamedPitch(1)])

    assert pytest.raises(IndexError, 'cell.previous')
