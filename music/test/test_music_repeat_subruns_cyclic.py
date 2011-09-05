from abjad import *
from baca import music


def test_music_repeat_subruns_cyclic_01():

    notes = [Note(p, (1, 4)) for p in [0, 2, 4, 5, 7, 9, 11]]
    music.repeat_subruns_cyclic(notes, [(0, 4, 1), (2, 4, 1)])

    assert [abs(note.written_pitch) for note in notes] == [0, 2, 4, 5, 0, 2, 4, 5, 7, 9, 4, 5, 7, 9, 11]
    assert len(notes) == len(set([id(note) for note in notes]))
