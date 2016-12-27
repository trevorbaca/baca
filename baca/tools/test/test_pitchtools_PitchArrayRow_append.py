# -*- coding: utf-8 -*-
import abjad
import baca


def test_pitchtools_PitchArrayRow_append_01():
    r'''Append cell by positive integer width.
    '''

    array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(abjad.NamedPitch(0))
    array[0].cells[1].append_pitch(abjad.NamedPitch(2))
    array[0].cells[1].append_pitch(abjad.NamedPitch(4))

    '''
    [c'] [d' e'    ] [ ]
    [          ] [ ] [ ]
    '''

    cell = baca.tools.PitchArrayCell(width=1)
    array[0].append(cell)
    cell = baca.tools.PitchArrayCell(width=1)
    array[1].append(cell)

    '''
    [c'] [d' e'    ] [ ] [ ]
    [          ] [ ] [ ] [ ]
    '''

    assert str(array) == "[c'] [d' e'    ] [ ] [ ]\n[          ] [ ] [ ] [ ]"


def test_pitchtools_PitchArrayRow_append_02():

    array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(abjad.NamedPitch(0))
    array[0].cells[1].append_pitch(abjad.NamedPitch(2))
    array[0].cells[1].append_pitch(abjad.NamedPitch(4))

    '''
    [c'] [d' e'     ] [ ]
    [           ] [ ] [ ]
    '''

    cell = baca.tools.PitchArrayCell(pitches=[0])
    array[0].append(cell)
    cell = baca.tools.PitchArrayCell(pitches=[2])
    array[1].append(cell)

    '''
    [c'] [d' e'    ] [ ] [c']
    [          ] [ ] [ ] [d']
    '''

    assert str(array) == "[c'] [d' e'    ] [ ] [c']\n[          ] [ ] [ ] [d']"
