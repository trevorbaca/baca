# -*- encoding: utf-8 -*-
from abjad import *
import baca


def test_utilities_repeat_subruns_to_length_01():

    notes = [Note(p, (1, 4)) for p in [0, 2, 4, 5, 7, 9, 11]]
    baca.utilities.repeat_subruns_to_length(notes, [(0, 4, 1), (2, 4, 1)])

    pitch_numbers = [note.written_pitch.pitch_number for note in notes]
    assert pitch_numbers == [0, 2, 4, 5, 0, 2, 4, 5, 7, 9, 4, 5, 7, 9, 11]
    assert len(notes) == len(set([id(note) for note in notes]))