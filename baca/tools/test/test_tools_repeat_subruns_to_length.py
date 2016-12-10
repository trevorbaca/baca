# -*- coding: utf-8 -*-
import abjad
import baca


def test_tools_repeat_subruns_to_length_01():

    pitches = [0, 2, 4, 5, 7, 9, 11]
    notes = list(abjad.scoretools.make_notes(pitches, [abjad.Duration(1, 4)]))
    baca.tools.repeat_subruns_to_length(notes, [(0, 4, 1), (2, 4, 1)])

    pitch_numbers = [note.written_pitch.pitch_number for note in notes]
    assert pitch_numbers == [0, 2, 4, 5, 0, 2, 4, 5, 7, 9, 4, 5, 7, 9, 11]
    assert len(notes) == len(set([id(note) for note in notes]))
