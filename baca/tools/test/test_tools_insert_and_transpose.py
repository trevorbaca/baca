# -*- coding: utf-8 -*-
import abjad
import baca


def test_tools_insert_and_transpose_01():
    '''Inserts are shown in brackets.
    '''

    items = [abjad.Note(_, (1, 4)) for _ in [0, 2, 7, 9, 5, 11, 4]]
    subrun_tokens = [(0, [2, 4]), (4, [3, 1])]
    baca.tools.insert_and_transpose(items, subrun_tokens)

    pitch_classes = []
    for item in items:
        if isinstance(item, abjad.Note):
            pitch_classes.append(item.written_pitch.pitch_class_number)
        else:
            assert isinstance(item, list), repr(item)
            pitch_classes_ = [
                note.written_pitch.pitch_class_number for note in item
                ]
            pitch_classes.append(pitch_classes_)

    assert pitch_classes == [
        0, [5, 7], 2, [4, 0, 6, 11], 7, 9, 5, [10, 6, 8], 11, [7], 4]
